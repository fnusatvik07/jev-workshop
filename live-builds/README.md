# Live Builds: 5 resume-ready projects on Jev

Five small, complete, original projects built on Jev (TypeSafe AI's System One
model). Each is one file you can read on a projector in a few minutes, each
teaches a distinct pattern, and each maps to a distinct, in-demand job area. All
five were run against the live API while building; the outputs in this README are
real.

```bash
uv sync
export TYPESAFE_API_KEY="your-typesafe-key"     # console.typesafe.ai/keys
export OPENAI_API_KEY="your-openai-key"         # only project 1 needs this
uv run python live-builds/model_router.py
```

| # | File | Pattern it teaches | Job area | Resume line |
| - | - | - | - | - |
| 1 | `model_router.py` | cheap judge picks the model, then the model runs | LLMOps / cost | routes to the cheapest capable LLM, cut inference cost ~75% |
| 2 | `tool_firewall.py` | AI as a runtime guardrail, confidence-gated | AI safety / agents | screens every agent tool call before it executes |
| 3 | `content_blocker.py` | filter by meaning, not blocklists | product / full-stack | semantic content blocker with toggleable categories |
| 4 | `shapeshift.py` | typed classification drives the UI | AI UX / frontend | adaptive UI that builds the right controls from NL |
| 5 | `jev_evals.py` | System One as the LLM judge | AI evals / quality | grade 100% of LLM traffic for pennies, catch hallucinations |
| 6 | `rag_reranker.py` | re-score retrieved passages by relevance | RAG / search | lift retrieval precision, drop junk context before the LLM |

The through-line: **Jev makes the decision, your code owns the action.** The model
never generates the output you ship; it returns typed, calibrated numbers you
branch on. That is what makes every one of these cheap enough to run on every
request and safe enough to put in production.

---

## 1. Model Router  (`model_router.py`)

Jev classifies each request (difficulty, kind, stakes) in ~100ms, then code picks
the cheapest OpenAI model that can handle it and actually calls it. The judge is
100x cheaper than the thing it is saving you from, which is the whole point.

```
What's the capital of Australia?      -> gpt-5.4-nano   (difficulty 0.00)
Prove sqrt(2) is irrational.          -> gpt-5.4        (difficulty 2.43)
model bill, always-frontier: $7.50   with router: $1.90   (-75%)
```

The nice emergent moments: a dangerous request escalates on the `high_stakes`
signal alone, and the router itself cost $0.0001 to route everything.

## 2. Agent Tool-Call Firewall  (`tool_firewall.py`)

A judge between an agent's intent and the real side effect. Every tool call is
screened against the agent's stated goal for destruction, secret exfiltration,
off-task drift, and injection signatures, then ALLOW / REVIEW / BLOCK is decided
in code. Only genuine danger blocks; off-task routes to a human.

```
[ALLOW ] read_file(README.md)
[REVIEW] run_shell(npm install)          off_task 0.93
[BLOCK ] read_file(.env)                 exfiltrates_secrets 0.83
[BLOCK ] run_shell(rm -rf / ...)         destructive 0.98
```

## 3. Semantic Content Blocker  (`content_blocker.py`)

An ad/distraction blocker that works on meaning, not domain lists. Toggle the
categories you want gone (ads, ragebait, crypto shilling, spoilers, AI slop); for
each item one Jev call answers one yes/no per enabled category and code decides
HIDE / BLUR / DIM / SHOW. The decision function is the core of a browser
extension; the extension is just DOM plumbing.

```
[ HIDE ] ███████...   flagged as ad 0.98
[ BLUR ] In tonight's finale, the detective...   flagged as spoiler 0.98
[ show ] Our team just shipped incremental static regeneration...
7 of 10 items removed or blurred, each judged in ~100ms.
```

## 4. Shapeshift: a UI that builds itself  (`shapeshift.py`)

One text box. The user types intent; the right input control materializes. One
Jev request picks a control type (date picker, slider, color picker, rating,
toggle, file upload) plus feature flags, and code renders it. Low confidence
falls back to a plain text field instead of guessing wrong.

```
"remind me to call the dentist next tuesday at 3pm"  -> [date picker][time]  (1.00)
"set the thermostat to a comfortable temperature"    -> [slider]             (0.99)
"how would you rate your support experience today?"  -> [star rating]        (1.00)
```

## 5. Jev Evals  (`jev_evals.py`)

LLM-as-judge, but the judge is a System One model, so grading is cheap enough to
run on 100% of traffic instead of a 1% sample. Each answer is graded on
faithfulness, relevance, and completeness; the verdict is computed in code; and
low-confidence grades are flagged for human review (an eval of the eval).

```
A: "...designed by Thomas Edison in 1901."  -> FAIL · hallucination  (faithful 0.02)
A: "In 1889."  (to 'when AND why')          -> REVISE · incomplete
2 pass  1 revise  3 fail   ·   ~$0.021 per 1,000 answers graded
```

## 6. RAG Reranker  (`rag_reranker.py`)

Retrieval's weakest link: the keyword/embedding retriever puts three keyword-match
distractors on top and buries the real answer at rank 6. Jev re-scores every
candidate for relevance in one request, so the right passage rises to rank 1 and
everything below the relevance bar is dropped before it reaches the LLM.

```
query: What should I do if my sourdough starter isn't rising?
BEFORE: real answer at rank 6, behind "sun rising", "interest rates rising", "starter kit"
AFTER:  real answer at rank 1 (score 2.99); 7 of 8 distractors dropped
```

---

Each file is self-contained and heavily commented for a live walkthrough. Start
anywhere; `_jev.py` holds the shared key-loading and pretty-printing helpers so
the project files stay short.
