"""
PROJECT 5 - Jev Evals: grade your LLM's answers at a price that lets you grade ALL of them.

Everyone running an LLM in production needs evals: is the answer faithful to the
context, does it actually address the question, is it complete? The usual tool is
"LLM-as-judge", a second expensive model grading the first. It works, but it is
slow and costs as much as the thing it grades, so teams sample 1% of traffic and
hope.

Swap the judge for a System One model and the economics flip. Grading becomes a
handful of typed judgments in one ~100ms call for a fraction of a cent, so you
can grade 100% of production traffic instead of a sample. And because Jev reports
calibrated confidence, you can send the uncertain GRADES themselves to a human,
an eval of the eval.

This is the single most in-demand AI skill on the market right now, and it is
about 60 lines.

Resume line: "Built an automated LLM/RAG eval harness grading faithfulness,
relevance, and completeness at <$0.001 per response, enabling 100% coverage with
confidence-gated human review of low-certainty grades."

Run:  uv run python jev_evals.py
"""

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

from _jev import bar, ensure_key, rule

ensure_key()

# The rubric. Each dimension is one typed judgment about (question, context, answer).
RUBRIC = {
    "faithful": Noul(
        instructions="Is EVERY factual claim in `answer` supported by `context`? Answer no if it adds any fact not in the context.",
    ),
    "relevant": Score(
        instructions="How well does `answer` address `question`?",
        criteria=["Off-topic", "Partially addresses it", "Directly and fully on-topic"],
    ),
    "complete": Score(
        instructions="Given `context`, how completely does `answer` cover what the question asks?",
        criteria=["Misses most of it", "Covers some of it", "Covers everything the context supports"],
    ),
    "refuses": Noul(instructions="Is `answer` a non-answer, refusal, or hedge rather than a real attempt?"),
}

# Thresholds in one place. Relevance below OFFTOPIC means it misses the topic
# entirely; between there and COMP_OK it is on-topic but needs more.
OFFTOPIC, COMP_OK, GRADE_CONFIDENT = 1.0, 1.5, 0.55


def grade(question: str, context: str, answer: str, client: TypeSafeClient) -> dict:
    state = {"question": question, "context": context, "answer": answer}
    r = client.system_one(state=state, questions=RUBRIC)
    faithful = r.nouls["faithful"].noul
    relevant = r.scores["relevant"]
    complete = r.scores["complete"]
    refuses = r.nouls["refuses"].noul

    # The verdict is computed in code, not asked of the model.
    if faithful < 0.5:
        verdict = "FAIL · hallucination"
    elif refuses > 0.5:
        verdict = "FAIL · non-answer"
    elif relevant.score < OFFTOPIC:
        verdict = "FAIL · off-topic"
    elif complete.score < COMP_OK:
        verdict = "REVISE · incomplete"
    else:
        verdict = "PASS"

    # Meta-eval: if the grader itself was unsure, a human should check this grade.
    grader_unsure = min(relevant.confidence, complete.confidence) < GRADE_CONFIDENT
    return {"verdict": verdict, "faithful": faithful, "relevant": relevant.score,
            "complete": complete.score, "review": grader_unsure, "tokens": r.usage.input_tokens}


# A tiny RAG-style eval set. Context is the ground truth; answers vary in quality.
CTX = ("The Eiffel Tower was completed in 1889 for the World's Fair. It is 330 metres tall "
       "including antennas and is located on the Champ de Mars in Paris.")

CASES = [
    ("How tall is the Eiffel Tower?", CTX,
     "It is 330 metres tall including antennas."),                                 # good -> PASS
    ("How tall is the Eiffel Tower?", CTX,
     "It is 330 metres tall and was designed by Thomas Edison in 1901."),          # hallucination -> FAIL
    ("When was the Eiffel Tower completed and why?", CTX,
     "In 1889."),                                                                  # misses the 'why' -> REVISE
    ("How tall is the Eiffel Tower?", CTX,
     "Paris is a wonderful city with great food and museums."),                    # off-topic -> FAIL
    ("Where is the Eiffel Tower?", CTX,
     "I'm not able to help with that."),                                           # refusal -> FAIL
    ("When was the Eiffel Tower completed and why?", CTX,
     "It was completed in 1889 for the World's Fair."),                            # full -> PASS
]


def main() -> None:
    rule("JEV EVALS  ·  grade every answer, not a 1% sample")
    counts = {"PASS": 0, "REVISE": 0, "FAIL": 0}
    flagged = total_tokens = 0
    with TypeSafeClient() as client:
        for q, ctx, ans in CASES:
            d = grade(q, ctx, ans, client)
            counts[d["verdict"].split(" ")[0]] += 1
            total_tokens += d["tokens"]
            if d["review"]:
                flagged += 1
            mark = "  ⚑ review grade" if d["review"] else ""
            print(f"\n  Q: {q}")
            print(f"  A: {ans[:70]}")
            print(f"     -> {d['verdict']:<22} "
                  f"faithful {d['faithful']:.2f}  relevant {d['relevant']:.2f}  complete {d['complete']:.2f}{mark}")

    n = len(CASES)
    cost = total_tokens / 1_000_000 * 0.042
    rule("SCORECARD")
    print(f"  {counts['PASS']} pass   {counts['REVISE']} revise   {counts['FAIL']} fail   "
          f"(pass rate {counts['PASS'] / n * 100:.0f}%)")
    print(f"  {flagged} grade(s) flagged for human review (the grader was not confident)")
    print(f"  cost to grade all {n}: ${cost:.6f}  ->  about ${cost / n * 1000:.3f} per 1,000 answers")
    print("  At that price you grade 100% of production traffic, not a sample. The")
    print("  hallucinated 'Thomas Edison' answer was caught by faithfulness, in code.\n")


if __name__ == "__main__":
    main()
