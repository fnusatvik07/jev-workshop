<p align="center">
  <img src="docs/images/banner.png" alt="Jev Workshop: teach the first System One model" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-1F1E1D?style=flat-square&labelColor=F0EEE6&color=5E6B7A" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/install-uv%20sync-D97757?style=flat-square&labelColor=F0EEE6" alt="uv">
  <img src="https://img.shields.io/badge/notebooks-5%2C%20all%20executed%20live-7D8B6A?style=flat-square&labelColor=F0EEE6" alt="notebooks">
  <img src="https://img.shields.io/badge/walkthroughs-24%20projects%20%2B%20use%20cases-1F7A3D?style=flat-square&labelColor=F0EEE6" alt="walkthroughs">
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

### Research: what people built (`reference/`)

- **[TOP-25-USE-CASES.md](reference/TOP-25-USE-CASES.md)** — a skimmable, grouped top-25 with the article link for each (and which ones are built in this repo). Start here.
- **[JEV-USE-CASES-WILD.md](reference/JEV-USE-CASES-WILD.md)** — the full catalog: 82 verified real-world builds (Ender Dragon under $1, a Postgres plain-English WHERE clause, an "LLM" made of 521 Jev units, a NAND-gate CPU, live crypto trading, drone control), a live-build shortlist with 30-45 minute plans, and a sources section. Every link fetched and checked.

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

### 24 walkthrough notebooks with live UIs (`apps/`)

**24 self-contained, presentable walkthroughs.** All the code sits in visible cells and is explained step by step: the problem, why Jev, the questions, the raw Jev response, the decision logic in plain Python, a run on examples, an HTML/ipywidgets UI you type into, and a recap with exercises. Nothing is hidden behind imports.

<p align="center">
  <img src="docs/images/apps-preview.png" alt="The project UIs rendered in Jupyter" width="80%">
</p>

```bash
uv run jupyter lab apps/     # or open in VS Code with the .venv kernel; Run All, then "Try it yourself"
```

**The original nine:** `01` emoji picker, `02` mood to color, `03` shapeshift UI, `04` content blocker, `05` tool firewall, `06` model router, `07` evals, `08` RAG reranker, `09` semantic Ctrl-F.

**The 18 practical use cases.** Every use case from [*18 practical Jev use cases for AI agents*](https://huggingface.co/blog/karmen-beatapi/18-practical-jev-use-cases-for-ai-agents) is built as a working notebook. Each follows the article's guidance: exact rules first, Jev for the ambiguous part, thresholds in code, and always a "none" or human-review path.

| # | Use case | Notebook | What it shows |
| --- | --- | --- | --- |
| 1 | Verify that an agent actually finished | [`10`](apps/10_agent_completion_check.ipynb) | goal + evidence → CLOSE / REVIEW / KEEP OPEN; self-report and stale evidence caught |
| 2 | Select a tool, then authorize it | [`11`](apps/11_tool_selection.ipynb) | Choice over tools incl. `none`, then permission + required-arg checks in code |
| 3 | Route to a model, code path or person | [`06`](apps/06_model_router_app.ipynb) | difficulty/kind/stakes → cheapest capable OpenAI model |
| 4 | Pick a skill or sub-agent | [`12`](apps/12_skill_router.ipynb) | top-1 vs top-2 margin → load one, ask, or plan multi-step |
| 5 | Confidence gate in a workflow | [`13`](apps/13_confidence_gate.ipynb) | AUTO / CONFIRM / FALLBACK bands with live threshold sliders |
| 6 | Filter RAG passages before generation | [`14`](apps/14_rag_passage_filter.ipynb) | keep/drop per passage, precision and recall measured against labels |
| 7 | Rerank a short candidate set | [`08`](apps/08_rag_reranker_app.ipynb) | the right passage jumps from rank 6 to rank 1 |
| 8 | Check a citation against a claim | [`15`](apps/15_citation_check.ipynb) | supports / contradicts / not addressed, plus an exact quote-in-source check |
| 9 | Align two entity records | [`16`](apps/16_entity_matching.ipynb) | deterministic blocking first, Jev for the gray zone, false merges counted |
| 10 | Screen LLM input and output | [`17`](apps/17_llm_io_guard.ipynb) | regex hard rules + one Noul per hazard → PASS / REVIEW / BLOCK |
| 11 | Apply a fixed evaluation rubric | [`07`](apps/07_jev_evals_app.ipynb) | faithfulness, relevance, completeness; verdict computed in code |
| 12 | Flag semantic issues in code changes | [`18`](apps/18_code_review_rules.ipynb) | plain-English team rules → review comments, with noise tracking |
| 13 | Check a document against a checklist | [`19`](apps/19_document_checklist.ipynb) | MET / UNCERTAIN / MISSING plus an audit record |
| 14 | Triage a support inbox | [`20`](apps/20_support_triage.ipynb) | queue + urgency + escalation in one call, PII redacted first |
| 15 | Classify within a large taxonomy | [`21`](apps/21_taxonomy_classifier.ipynb) | level-by-level Choice with a beam and a `none_of_these` exit |
| 16 | Select among extracted candidates | [`22`](apps/22_span_selection.ipynb) | regex finds spans, Jev picks one, value copied verbatim (can't invent) |
| 17 | Combine several scored dimensions | [`23`](apps/23_multi_score_prioritizer.ipynb) | four rubrics, weights in code, live weight sliders |
| 18 | Semantic features for a classic ML model | [`24`](apps/24_semantic_features.ipynb) | Jev outputs as features in a NumPy logistic regression, evaluated on held-out data |

Several notebooks include a **Workshop note** describing a wording change that fixed a wrong answer during development. That is part of the lesson: the question text is everything the model sees. See [`apps/README.md`](apps/README.md). Outputs are pre-run so they show on GitHub; the "Try it yourself" boxes need a live kernel. `06` and `09` also need `OPENAI_API_KEY`.

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
├── apps/                 24 walkthrough notebooks with live UIs (9 projects + 18 use cases)
├── live-builds/          the projects as single-file terminal scripts
├── gallery/              quick visual demos (emoji, color, semantic find)
├── deck/
│   ├── Jev-Workshop.pptx the 48-slide presentation
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
