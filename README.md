<p align="center">
  <img src="docs/images/banner.png" alt="Jev Workshop: teach the first System One model" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-1F1E1D?style=flat-square&labelColor=F0EEE6&color=5E6B7A" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/install-uv%20sync-D97757?style=flat-square&labelColor=F0EEE6" alt="uv">
  <img src="https://img.shields.io/badge/notebooks-5%2C%20all%20executed%20live-7D8B6A?style=flat-square&labelColor=F0EEE6" alt="notebooks">
  <img src="https://img.shields.io/badge/deck-48%20slides%20%2B%20speaker%20notes-BD5D3A?style=flat-square&labelColor=F0EEE6" alt="deck">
  <img src="https://img.shields.io/badge/license-MIT-8A8780?style=flat-square&labelColor=F0EEE6" alt="MIT">
</p>

# Jev Workshop

**A complete, battle-tested workshop for [Jev](https://typesafe.ai), TypeSafe AI's System One model: the model that returns *decisions* instead of text.**

LLMs write prose for people. Your code needs a category, a score, a probability it can branch on. Jev takes a *state* (any text or JSON) plus typed *questions* and returns typed answers with **calibrated probabilities**, in ~100 ms, at **$0.042 per million input tokens** (output is free). No prompt-engineering for output format. No JSON parsing. No retries on malformed replies.

This repo is everything you need to **learn it or teach it**: five Jupyter notebooks that run against the live API, a 48-slide presentation with speaker notes on every slide, and a 15,000-word cited reference distilled from the entire official documentation. **Every number in all three was verified against the real API** while building this.

---

## The 60-second tour

We drew a porch, sent it to Jev with four questions, and drew its answer back onto the image. One request, 1,229 input tokens, about $0.00005:

<p align="center">
  <img src="deck/assets/porch_annotated.png" alt="Jev finds the parcel: bounding box drawn from the live answer" width="55%">
</p>

| Question | Type | Jev's answer | What the code does |
| --- | --- | --- | --- |
| Is there a person in `porch`? | Noul | **0.05** | no 3 am ping |
| Is there a delivered package? | Noul | **0.97** | notify "package delivered" |
| Door open or closed? | Choice | **closed** (0.99) | nothing to flag |
| "the parcel on the mat" | Box | the green box, confidence 0.85 | crop the thumbnail |

That green rectangle was not drawn by a human. It is the model's answer, as four fractional edges, rendered by three lines of PIL. Notebook 02 reproduces this end to end.

---

## Quickstart

You need [uv](https://docs.astral.sh/uv/) and a free API key from the [TypeSafe console](https://console.typesafe.ai/keys).

```bash
git clone https://github.com/fnusatvik07/jev-workshop.git
cd jev-workshop
uv sync                                  # installs everything, pinned
export TYPESAFE_API_KEY="your-key"       # or: cp .env.example .env and edit
uv run jupyter lab notebooks/
```

That is the whole setup. The notebooks find the key from the environment or any `.env` file up the tree. A full top-to-bottom run of all five notebooks costs **under one cent**.

> No key yet? Every notebook ships **with its outputs saved**, so you can read the entire workshop, real API responses included, right on GitHub.

---

## What's inside

### The notebooks (`notebooks/`)

| # | Notebook | What you build and learn |
| --- | --- | --- |
| 01 | [Hello, Jev](notebooks/01_hello_jev.ipynb) | The mental model, your first call, typed answers, the latency and cost math |
| 02 | [The Primitives](notebooks/02_primitives.ipynb) | Choice, Score, Noul, Box in depth, with live anti-examples that show *why* the rules exist |
| 03 | [Probability vs Confidence](notebooks/03_confidence.ipynb) | The three numbers untangled (100-experts analogy), the exact formulas verified against the API, routing on uncertainty |
| 04 | [Architectural Patterns](notebooks/04_patterns.ipynb) | Speculative fan-out, confidence-gated routing, composite scoring, intent routing, plus a measured batching experiment |
| 05 | [Real-World Builds](notebooks/05_real_world.ipynb) | An LLM guardrail layer, semantic line search, the 9 documented failure modes with live demos, the properties reference |

### The deck (`deck/Jev-Workshop.pptx`)

48 slides, fully editable, speaker notes on every slide with facilitation tips (where to poll the room, which wrong answers to expect). Built as a story: a support ticket arrives at 9:04 am, and by the closing slide the room can triage 500 of them for a cent.

<p align="center">
  <img src="docs/images/slides-preview.png" alt="Six slides from the deck" width="100%">
</p>

It assumes zero background: what a model actually is (knobs and gradient descent), how RLHF really works step by step, why RLVR makes reasoning models, and how RLCD (Jev's recipe) rewards honest probabilities instead. Two audience quiz slides are built in. Rebuild or restyle it with `uv run python build_deck.py` from `deck/build/`.

### The wild-side catalog (`reference/JEV-USE-CASES-WILD.md`)

82 verified things people have actually built with Jev in its first month: beating Minecraft's Ender Dragon for under $1, a PostgreSQL extension with plain-English WHERE clauses, an LLM reconstructed out of 521 Jev models, a NAND gate made of API calls, live crypto trading, drone control, and more. Every link was fetched and checked before inclusion, and it ends with a ranked top-5 shortlist for building live in front of a class, each with a 30-45 minute step plan.

### Five resume-ready projects (`live-builds/`)

Five small, original, end-to-end projects, each one file you can read on a projector, each a distinct pattern and a distinct job area. All verified against the live API.

| # | Project | Pattern | Job area |
| --- | --- | --- | --- |
| 1 | [`model_router.py`](live-builds/model_router.py) | Jev picks the cheapest capable model, then OpenAI runs it (cut cost ~75%) | LLMOps / cost |
| 2 | [`tool_firewall.py`](live-builds/tool_firewall.py) | screen every agent tool call before it executes (ALLOW/REVIEW/BLOCK) | AI safety / agents |
| 3 | [`content_blocker.py`](live-builds/content_blocker.py) | block web content by meaning, not blocklists; toggleable categories | product / full-stack |
| 4 | [`shapeshift.py`](live-builds/shapeshift.py) | a UI that builds the right input control from natural language | AI UX / frontend |
| 5 | [`jev_evals.py`](live-builds/jev_evals.py) | LLM-as-judge cheap enough to grade 100% of traffic and catch hallucinations | AI evals / quality |
| 6 | [`rag_reranker.py`](live-builds/rag_reranker.py) | re-score retrieved passages so the right one reaches rank 1 | RAG / search |

The through-line: Jev makes the decision, your code owns the action. See [`live-builds/README.md`](live-builds/README.md) for real output and resume lines. Projects 1 (router) needs `OPENAI_API_KEY`.

### A gallery of fun, visual demos (`gallery/`)

Run-in-30-seconds use cases that a room can *see*:

| File | What it does |
| --- | --- |
| [`emoji_picker.py`](gallery/emoji_picker.py) | type a word, the matching emoji group floats to the top |
| [`color_mood.py`](gallery/color_mood.py) | type a feeling, a blended color materializes in your terminal |
| [`semantic_find.py`](gallery/semantic_find.py) | semantic Ctrl-F: find a page passage by meaning, answer through chat |

See [`gallery/README.md`](gallery/README.md) for real output. `semantic_find.py` also needs `OPENAI_API_KEY`.

### The reference (`reference/JEV-REFERENCE.md`)

A 15,000-word distillation of the complete official docs: every primitive field, every limit, pricing, context windows, the full Python SDK surface, all 20 cookbooks, and 54 numbered best practices. Every fact carries an inline source citation, and the whole thing was adversarially fact-checked against the raw documentation (about 120 spot-checked claims).

---

## Numbers we measured ourselves

Not vendor claims. These came out of the notebooks in this repo, run against the live API:

| Measurement | Result |
| --- | --- |
| Text call latency (incl. network) | ~280 ms |
| 8 questions batched vs 8 separate calls | **6.8x faster, 6.1x fewer tokens**, answers identical |
| 5-question ticket triage | ~500 tokens = **$0.000021 per ticket** |
| Confidence formulas (Choice and Score) | reimplemented by hand, match the API to 2 decimals |
| Box on a synthetic scene (Jev 1.14) | parcel edges within 0.03 of ground truth, confidence 0.85 |

And one honest failure we kept in on purpose: ask Jev which month `11/05/2026` falls in and it splits its probability between May and November, because the date is genuinely ambiguous. The confidence gate catches it. That is the whole product philosophy in one demo: **honest uncertainty you can route on** (notebook 05).

---

## What is Jev, in 20 lines

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

ticket = "Our API returns 500 errors on every request. We can't process orders!"

with TypeSafeClient() as client:            # reads TYPESAFE_API_KEY
    r = client.system_one(
        state=ticket,
        questions={
            "team":    Choice(instructions="Which team should handle this?",
                              criteria={"billing": None, "technical": None, "sales": None}),
            "anger":   Score(instructions="How frustrated is the customer?",
                             criteria=["calm", "frustrated", "furious"]),
            "urgent":  Noul(instructions="The message conveys urgency"),
        },
    )

r.choices["team"].choice          # "technical"
r.choices["team"].probabilities   # {"technical": 1.0, "billing": 0.0, "sales": 0.0}
r.scores["anger"].score           # 0.67  (a position on YOUR rubric)
r.nouls["urgent"].noul            # 0.99  (probability of yes)
```

Every question is evaluated **in parallel, independently**, in one request. Adding a question barely moves latency and costs only its own tokens, which is why the idiomatic pattern is to ask everything you might need and let code ignore the rest.

---

## Repo map

```
jev-workshop/
├── notebooks/            5 executed notebooks (outputs included)
├── deck/
│   ├── Jev-Workshop.pptx the 42-slide presentation
│   ├── assets/           charts + diagrams used by the deck and this README
│   └── build/            python-pptx build scripts (rebuild/restyle the deck)
├── reference/
│   └── JEV-REFERENCE.md  the cited, fact-checked distillation of the docs
├── WORKSHOP_GUIDE.md     2-hour teaching agenda and setup notes
├── .env.example          put your TYPESAFE_API_KEY here
└── pyproject.toml        uv sync and you are done
```

## FAQ

**Do I need to pay to run this?** A key from the [console](https://console.typesafe.ai/keys) and about one cent of usage runs everything here.

**Can I read it without running anything?** Yes. All notebooks are committed with their live outputs, and the deck renders in the GitHub preview.

**Why do image cells take ~10 seconds?** Image requests are a preview feature and run seconds, not milliseconds. The notebooks raise the SDK timeout for those cells; if you write your own code, do the same or the default 10 s timeout plus retries will stack into minutes.

**Is this affiliated with TypeSafe AI?** No. Independent teaching material. Five diagrams in the deck come from the [official docs](https://docs.typesafe.ai) and are credited on-slide; the jaggedness and criticism slides are included deliberately, because honest material teaches better.

## Credits

Built in October 2026 against `typesafe-sdk` 0.7.5, Jev 1.13 and 1.14. Sources: [docs.typesafe.ai](https://docs.typesafe.ai), the installed SDK source, and cited press coverage (The Register, InfoQ, Bloomberg). All original content is MIT licensed; TypeSafe's diagrams and documentation excerpts remain theirs.

---

<p align="center">
  <b>Code owns the workflow. Jev answers the judgment calls.</b><br>
  <sub>If this repo helped you teach or learn, a star helps others find it.</sub>
</p>
