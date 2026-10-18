"""
PROJECT 1 - Model Router: a cheap judge in front of expensive LLMs.

Every team with an LLM bill eventually wants this: stop sending "what's 2+2" to
your most expensive reasoning model. Classify the request first, route cheap
requests to cheap models, and only pay for the big model when the task needs it.

The catch is that the router itself must be cheaper and faster than the thing it
is saving you from. An LLM-based router defeats the purpose. Jev is a System One
model, so the routing decision is ~100ms and a fraction of a cent, which is the
whole reason this works. Jev DECIDES; OpenAI RUNS.

Resume line: "Built a System One model router that classifies request difficulty
in ~100ms and cuts LLM inference cost ~60% by selecting the cheapest capable model."

Run:  uv run python model_router.py
"""

import time

from openai import OpenAI
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

from _jev import bar, ensure_key, rule

ensure_key()

# --- The ladder of real OpenAI models we route between --------------------
TIERS = {
    "small":    {"model": "gpt-5.4-nano", "price": 0.05, "desc": "fast, cheap"},
    "mid":      {"model": "gpt-5.4-mini", "price": 0.25, "desc": "balanced"},
    "frontier": {"model": "gpt-5.4",      "price": 1.25, "desc": "deep reasoning"},
}
BASELINE = TIERS["frontier"]["price"]  # what you'd pay if every call went to the top

# --- One Jev request, four typed judgments, evaluated in parallel ---------
ROUTER_QUESTIONS = {
    "difficulty": Score(
        instructions="How much reasoning does answering this request well require?",
        criteria=[
            "Trivial: a lookup, a greeting, or a one-line fact",
            "Moderate: a short explanation or a small, well-scoped task",
            "Hard: multi-step work, careful code, or nuanced judgment",
            "Expert: deep multi-step reasoning, proofs, or tricky debugging",
        ],
    ),
    "kind": Choice(
        instructions="What kind of request is this?",
        criteria={
            "factual_lookup": "Asking for a known fact or definition",
            "simple_rewrite": "Rephrase, summarize, or reformat supplied text",
            "code": "Write, fix, or explain code",
            "reasoning_math": "Logic, math, or multi-step problem solving",
            "creative": "Open-ended writing or brainstorming",
        },
    ),
    "high_stakes": Noul(
        instructions="Would a wrong answer here be costly, unsafe, or hard to undo?",
    ),
}
CONFIDENT = 0.55  # below this on difficulty, do not trust the cheapest route


def choose_tier(prompt: str, jev: TypeSafeClient) -> dict:
    """The routing decision: all policy is plain code reading Jev's numbers."""
    r = jev.system_one(state=prompt, questions=ROUTER_QUESTIONS)
    diff = r.scores["difficulty"]
    kind = r.choices["kind"]
    stakes = r.nouls["high_stakes"].noul

    if diff.score < 1.0:
        tier = "small"
    elif diff.score < 2.2:
        tier = "mid"
    else:
        tier = "frontier"

    reasons = [f"difficulty {diff.score:.2f}"]
    if diff.confidence < CONFIDENT and tier == "small":
        tier, _ = "mid", reasons.append(f"unsure ({diff.confidence:.2f}), no cheap route")
    if kind.choice == "reasoning_math" and tier == "small":
        tier, _ = "mid", reasons.append("reasoning task, floor at mid")
    if stakes > 0.7 and tier != "frontier":
        tier, _ = "frontier", reasons.append(f"high stakes {stakes:.2f}")

    return {"tier": tier, "difficulty": diff.score, "kind": kind.choice,
            "reasons": reasons, "jev_tokens": r.usage.input_tokens}


def run(prompt: str, jev: TypeSafeClient, oai: OpenAI) -> dict:
    """Route, then actually call the chosen OpenAI model."""
    d = choose_tier(prompt, jev)
    model = TIERS[d["tier"]]["model"]
    t0 = time.perf_counter()
    resp = oai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=2000,
    )
    d["latency_ms"] = (time.perf_counter() - t0) * 1000
    d["answer"] = (resp.choices[0].message.content or "").strip().replace("\n", " ")
    d["model"] = model
    d["price"] = TIERS[d["tier"]]["price"]
    return d


PROMPTS = [
    "What's the capital of Australia?",
    "Reformat 'john smith, jane doe' to Title Case.",
    "Prove that the square root of 2 is irrational.",
    "Write a haiku about a tired Monday.",
    "A payment webhook fires twice per event intermittently. What are the top 3 causes?",
    "hi there",
]


def main() -> None:
    rule("MODEL ROUTER  ·  Jev decides, OpenAI runs")
    routed = baseline = 0.0
    jev_tokens = 0
    with TypeSafeClient() as jev:
        oai = OpenAI()
        for p in PROMPTS:
            d = run(p, jev, oai)
            routed += d["price"]
            baseline += BASELINE
            jev_tokens += d["jev_tokens"]
            tag = {"small": " small ", "mid": "  MID  ", "frontier": "FRONTIER"}[d["tier"]]
            print(f"\n  {p}")
            print(f"    [{tag}] {d['model']:<13} {d['latency_ms']:>6.0f}ms  "
                  f"difficulty {bar(d['difficulty'] / 3)} {d['difficulty']:.2f} ({d['kind']})")
            print(f"       why: {'; '.join(d['reasons'])}")
            print(f"       answer: {d['answer'][:88]}")

    jev_cost = jev_tokens / 1_000_000 * 0.042
    rule("SCOREBOARD")
    print(f"  routing all of it on Jev cost ${jev_cost:.6f} ({jev_tokens} tokens)")
    print(f"  model bill, always-frontier: ${baseline:.2f}   with router: ${routed:.2f}   "
          f"(-{(1 - routed / baseline) * 100:.0f}%)")
    print("  The routing decision was made by a 100ms sub-cent classifier, not by the")
    print("  expensive model you were trying to avoid calling.\n")


if __name__ == "__main__":
    main()
