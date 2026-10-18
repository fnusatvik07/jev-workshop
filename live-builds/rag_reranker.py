"""
PROJECT 6 - RAG Reranker: fix the weakest link in retrieval.

Every RAG system has the same failure: the retriever (BM25, or embeddings) pulls
the top-k passages by surface similarity, and the genuinely relevant passage sits
at rank 6 while three keyword-matching distractors sit on top. Feed that to the
LLM and it answers from the wrong context.

The standard fix is a reranker: a second, smarter pass that re-scores each
candidate against the query. Cross-encoder rerankers are accurate but add latency
and a model to host. Jev reranks with one request: a relevance Score per
candidate, all in parallel, ~100ms, a fraction of a cent, and it returns
calibrated scores you can threshold (drop everything below "partially relevant"
so the LLM never even sees the junk). TypeSafe's own CLERC cookbook took top-1
retrieval accuracy from 5% to 18% this way.

Resume line: "Built a RAG reranker that lifts retrieval precision by re-scoring
candidate passages with a calibrated relevance model, dropping irrelevant context
before it reaches the LLM."

Run:  uv run python rag_reranker.py
"""

from typesafe_sdk import Score, TypeSafeClient

from _jev import bar, ensure_key, rule

ensure_key()

QUERY = "What should I do if my sourdough starter isn't rising?"

# Pretend output of a keyword/embedding retriever: ranked by surface similarity.
# Notice the keyword traps near the top ("rising", "starter") that are off-topic,
# and the actually-useful passage sitting down at rank 6.
CANDIDATES = [
    "The sun was rising over the bakery as the queue formed outside.",            # 'rising' trap
    "Our starter kit for new bakers includes three loaf tins and a scraper.",     # 'starter' trap
    "Bread has been a staple food across human civilizations for millennia.",     # on-topic-ish, useless
    "Rising interest rates have pushed up the cost of commercial ovens.",          # 'rising' trap
    "A sourdough starter is a fermented culture of flour and water.",              # relevant background
    "If your starter is sluggish, feed it more often and keep it around 24-26C; "
    "discard half before each feeding to concentrate the yeast.",                  # THE answer, at rank 6
    "Starter homes in the area now average four hundred thousand dollars.",        # 'starter' trap
    "Preheat a Dutch oven to 230C before baking for the best crust.",             # baking, not the question
]

LEVELS = [
    "Irrelevant: does not address the query at all",
    "Tangential: same topic area but does not help answer it",
    "Partially relevant: touches the answer but incomplete",
    "Directly relevant: actually answers the query",
]
KEEP = 1.5  # drop anything the reranker scores below "partially relevant"


def rerank(query: str, candidates: list[str], client: TypeSafeClient):
    # One request: a relevance Score for every candidate, in parallel.
    questions = {
        f"c{i}": Score(instructions=f"How well does `passages[{i}]` answer `query`?", criteria=LEVELS)
        for i in range(len(candidates))
    }
    r = client.system_one(state={"query": query, "passages": candidates}, questions=questions)
    scored = [(i, r.scores[f"c{i}"].score) for i in range(len(candidates))]
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored, r.usage


def main() -> None:
    rule("RAG RERANKER  ·  the right passage was at rank 6")
    print(f"  query: {QUERY}\n")
    print("  BEFORE  (retriever order, by keyword similarity):")
    for i, c in enumerate(CANDIDATES):
        print(f"    {i + 1}. {c[:66]}")

    with TypeSafeClient() as client:
        scored, usage = rerank(QUERY, CANDIDATES, client)

    print("\n  AFTER  (Jev relevance rerank):")
    for rank, (i, s) in enumerate(scored, 1):
        kept = "keep " if s >= KEEP else "drop "
        print(f"    {rank}. [{kept}] {bar(s / 3, 16)} {s:.2f}  {CANDIDATES[i][:52]}")

    gold = 5  # index of the real answer
    before = CANDIDATES.index(CANDIDATES[gold]) + 1
    after = [r for r, (i, _) in enumerate(scored, 1) if i == gold][0]
    kept = sum(1 for _, s in scored if s >= KEEP)
    cost = usage.input_tokens / 1_000_000 * 0.042
    rule("RESULT")
    print(f"  the passage that actually answers the question moved from rank {before} to rank {after}.")
    print(f"  {kept} of {len(CANDIDATES)} passages cleared the relevance bar; the LLM now sees only those.")
    print(f"  reranked all {len(CANDIDATES)} candidates in one request for ${cost:.6f}.")
    print("  Better context in, better answer out, and the junk never reaches the expensive model.\n")


if __name__ == "__main__":
    main()
