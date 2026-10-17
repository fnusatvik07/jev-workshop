# JEV-REFERENCE.md

Single source of truth for the Jev workshop. Every fact below is attributed to its source page as an inline citation like (source: primitives/choice). Sources are the official docs (docs.typesafe.ai paths), the installed Python SDK docs/source (sdk/python/... paths), and the public web (full URLs or named outlets). Where sources conflict, SDK source wins over docs, and docs win over web; conflicts are flagged where they occur.

---

## 1. What Jev is

### The one-line pitch

Jev is TypeSafe AI's "System One" classification model: it never generates text. It takes unstructured state plus typed questions and returns typed probabilistic decisions with calibrated confidence, all evaluated in parallel (source: https://typesafe.ai; https://typesafe.ai/blog/introducing-system-one-models-and-jev).

### System One vs System Two framing

The name is borrowed from Kahneman's fast System 1 thinking: TypeSafe defines System One models as "a new class of frontier models built to make fast, structured decisions that software can use directly" (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev). Where an LLM (System Two, in this framing) deliberates and writes prose, Jev makes snap judgments: "unstructured state in, typed probabilistic decisions out" (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev). The founding framing quote from CEO Diogo Almeida: "Models have been superhuman at chat for years, so where is all the automation?" (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev).

Both the SDK method `system_one` and the endpoint `https://api.typesafe.ai/v1/systemone` are named after the category (source: primitives).

The docs' own concept pages carry the canonical positioning. Most queries complete in about 100 ms, fast enough for real-time request paths and user interfaces, and TypeSafe's stated target is a greater-than-100x intelligence-to-speed-and-cost ratio, on the bet that cheaper intelligence creates much more demand (source: concepts/how-to-build-with-system-one). Six properties make System One composable: structured (type-safe by construction, no value recovered from prose), parallel (questions evaluated independently; one result never becomes hidden context for another), comparable (sortable outputs that drive thresholds and smart if statements), fast, calibrated confidence (via RLCD, instead of tending toward overconfidence), and self-consistent (designed to return stable answers across repeated evaluations) (source: concepts/how-to-build-with-system-one). The same page frames three software architectures: traditional software (reliable primitives composed into decision trees), LLM agents (the model chooses its own next step; every loop is another opportunity to go off the rails), and AI-powered software, TypeSafe's design target, where code handles deterministic work and owns the control flow, and the model appears only where the system needs programmable common sense or must interpret unstructured data, each AI task kept atomic and constrained (source: concepts/how-to-build-with-system-one; concepts/system-one).

### Company background

- TypeSafe AI is a San Francisco AI lab founded in 2024 by CEO Diogo Almeida (ex-OpenAI/Google Brain, reported co-inventor of RLHF), COO Sasha Sheng, and CTO Erik Gafni (source: https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/; https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/). Team includes alumni of OpenAI, Google Brain, Meta FAIR, Stripe, Airbnb, Plaid, and Docker (source: hpcwire.com, same article).
- Jev launched September 15, 2026 in waitlisted early access; the company exited stealth September 16, 2026 with a $40M seed led by DCVC, with an approximately $200M post-money valuation reported by Sacra/Dealroom (an estimate, not company-confirmed) (source: hpcwire.com; https://typesafe.ai/blog/introducing-system-one-models-and-jev).
- On October 9, 2026, Bloomberg (via Investing.com) reported an $870M Series A at a $7.5B valuation led by Andreessen Horowitz (Martin Casado joining the board), with Sequoia Capital and DCVC participating (source: https://www.investing.com/news/stock-market-news/typesafe-ai-raises-870-million-led-by-andreessen-horowitz--bloomberg-93CH-4941303). That is roughly a 37x valuation step-up in about three weeks post-launch (source: same article, timeline synthesis).
- Company-reported metrics in that coverage: 1M+ users within days of launch and roughly one-third of Fortune 500 companies using the product. Both are company-reported and unverified (source: investing.com, same article).
- Training method: "Reinforcement Learning for Calibrated Decisions" (RLCD), positioned as a successor/alternative to RLHF; optimizes for calibrated decision probabilities rather than human-preferred text (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev). The docs' AI primer sets RLCD against the two prior post-training approaches: RLHF (turned pretrained models into chatbots; used for InstructGPT and ChatGPT and co-invented by TypeSafe cofounder Diogo Almeida) and RLVR (reinforcement learning with verifiable rewards, which created reasoning models that are strong at tasks such as mathematics but slower and more expensive). The primer names RLHF's failure modes: it can reward sycophancy and confident-sounding hallucinations, and preference optimization causes mode dropping, a milder version of the GAN failure mode called mode collapse. The framing thesis is "Machine Native Intelligence" (AI with software-like properties: structure, reliability, observability, testability, speed, consistency, low cost) and the expectation that large-scale AI automation will be closer to 99% machine-to-machine interactions and 1% human interaction (source: https://docs.typesafe.ai/introduction/machine-learning-primer).
- Signature launch demo: Jev playing Doom from structured game state, covered by The Register (September 16, 2026), with the headline comparison 0.114s for Jev vs 8.566s for GPT-5.6 Terra (source: https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711).
- Adoption signals: nearly 13% of Vercel paid teams within 24 hours (2x GPT-5.6-family adoption); users report safety-classifier speedups of 5-18x vs the LLM they replaced; an OpenChamber analysis of 12,759 tweets found a median 7x speedup, 30x cost savings, 76ms median latency (upper quartile 270ms) (source: https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/).
- Access is closed, hosted, and waitlisted: no open weights, no self-hosted option. Third-party availability exists via Cloudflare AI (listed as typesafe/jev) and OpenRouter (listed as typesafe/jev-1.14) (source: https://developers.cloudflare.com/ai/models/typesafe/jev/).
- Known criticism: Armin Ronacher (Earendil CTO) praised it but cautioned it "delegates the hallucination problem... to the user"; a Hacker News critic noted it "can still emit a completely wrong valid value" (source: infoq.com, same article). HiddenLayer (October 16, 2026, via InfoWorld) claims Jev is more susceptible than LLMs to adversarial text, prompt injection, and TokenBreak (source: https://www.itsecuritynews.info/typesafes-jev-even-more-susceptible-to-attack-than-llms-says-security-vendor/). See section 9.

---

## 2. How it works

### The mental model

You send one request containing:

1. `state`: the content to evaluate. A string or JSON object (and, with images enabled, image references). Every question in the request sees the same state (source: primitives).
2. `model`: e.g. `jev-latest` or `jev-preview` (source: primitives/choice).
3. `questions`: a map from question IDs you choose to typed question objects (source: primitives/choice).

You get back typed answers keyed by your question IDs, plus `model` (the concrete version that answered, e.g. `jev-1.13.0`) and `usage` with `input_tokens` and `output_tokens` (source: primitives/choice).

Calls go to the `system_one` SDK method or the `https://api.typesafe.ai/v1/systemone` HTTP endpoint (source: primitives/choice; https://docs.typesafe.ai/introduction/quickstart.md).

### Core mechanics

- Every question has a user-chosen ID, a `type` (`choice`, `score`, `noul`, or `box`), `instructions`, and, except for Box, `criteria` (source: primitives; primitives/box).
- Question IDs are for your code only; they are never sent to the model. Write the complete question in `instructions` even when the ID looks self-explanatory (source: primitives).
- Every answer is constrained to the options you supplied: the model returns a probability distribution over your options or levels, never a value outside them (source: primitives).
- Every answer is independent: one question's answer is never hidden context for another; you can add or remove questions without changing the other answers. If a later judgment depends on an earlier answer, make a second request in code (source: primitives).
- Questions in one request are evaluated in parallel; adding questions barely changes response time and costs only the tokens for the extra questions (source: primitives).
- There is no limit on the number of questions in a request; what limits a request is its size, which must fit the model's per-request context and per-question context (source: primitives).
- Reference specific state fields in `instructions` with a dot-and-index path to the key in backticks, e.g. "Does `ticket.messages[0].text` request a refund?" (source: primitives).

### The batching economics

Batching N questions into one call sends the state once instead of N times. The primitives page cites the Parallel questions cookbook figure of batching 13 questions into one call being 11.5x cheaper and 9.6x faster than 13 separate calls with no change in answers (source: primitives). The cookbook page itself reports the measured run as 12.2x cheaper and 10.0x faster: one call with all 13 questions cost $0.000497 and took 0.27s vs $0.006090 and 2.71s for 13 single-question calls (source: cookbooks/parallel_questions). Both figures are docs-published; the cookbook page is the measured run.

### How it differs from LLM prompting / structured output

- No text generation: Jev is "not trained to generate text" (source: https://docs.typesafe.ai/model-jaggedness/jev-1.13.md). The response is pure typed JSON: no prose, no parsing step, no retry-on-malformed-JSON logic (source: https://docs.typesafe.ai/introduction/quickstart.md).
- Calibrated probabilities, not samples: instead of a single sampled token sequence, every answer is a full probability distribution over the options you defined, plus a confidence statistic. Code thresholds on these numbers (source: confidence; primitives).
- Constrained by construction: structured output on an LLM constrains the format; Jev constrains the answer space itself. The model cannot return a value outside your options (source: primitives). Caveat: this does not make answers correct; it "can still emit a completely wrong valid value" (source: infoq.com).
- The SDE cascade cookbook deliberately avoids LLM structured outputs, tool calls, and JSON mode for its extraction rungs: a schema-following mistake is not the mistake expected from an LLM, and "if an LLM fails to follow the schema it's almost always very confused," so constrained decoding does not fix the underlying issue (source: cookbooks/sde_cascade).
- Decomposition as design principle: "Decomposition maximizes the intelligence of every prompt, and makes the algorithm tunable and interpretable" (source: cookbooks/sde_cascade docs principle, "the TypeSafe Way").
- Speed and price class: 70-500ms claimed latency and $0.042 per 1M input tokens with free output, vs generative-model latency and pricing (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev). Launch demo: 0.114s vs 8.566s for GPT-5.6 Terra (source: theregister.com).

### Minimal HTTP shape

```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "state": "Our API integration started returning 500 errors...",
  "model": "jev-latest",
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle this",
      "criteria": {
        "billing": "Payment or subscription issues",
        "technical": "Bugs or integration problems",
        "sales": "Pricing or account questions"
      }
    }
  }
}
```

Response:

```
{
  "model": "jev-1.13.0",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "technical",
      "confidence": 1.0,
      "probabilities": { "technical": 1.0, "billing": 0.0, "sales": 0.0 }
    }
  },
  "usage": { "input_tokens": 428, "output_tokens": 73 }
}
```

(source: https://docs.typesafe.ai/introduction/quickstart.md)

### The agent skill and coding agents

Jev is explicitly NOT a drop-in replacement for the LLM behind Claude Code, Cursor, opencode, Copilot, or similar tools: it does not generate text, write code, call tools, or hold a conversation, so there is no `model: "jev-latest"` setting that turns a coding agent into a Jev-powered agent; the two systems solve different problems (source: https://docs.typesafe.ai/introduction/coding-agents). The fastest integration path the docs recommend is installing the TypeSafe agent skill BEFORE letting a coding agent write the integration; it gives Claude Code, Codex, and other agents full context on the API, primitives, and patterns. Install with `claude plugin marketplace add typesafe-ai/skills` then `claude plugin install typesafe@typesafe-ai` (Claude Code), or `npx skills add typesafe-ai/skills --skill typesafe-ai` for other agents; the quickstart lists this "Vibe it" path alongside the SDK, the raw API, and the Playground, and nearly every primitive page points to it (source: https://docs.typesafe.ai/introduction/quickstart.md; https://docs.typesafe.ai/introduction/coding-agents).

---

## 3. The four primitives in depth

The three text question types and their answer fields, at a glance: Choice returns `choice`, `probabilities`, `confidence`; Score returns `score`, `legend`, `probabilities`, `confidence`; Noul returns `noul` (0 to 1) with no separate confidence (source: primitives). Box is the fourth, image-only, preview-grade type (source: primitives/box).

`instructions` and all criteria values are EntryType: string, object, array, or null (source: primitives/advanced). A string is enough for most questions (source: primitives).

### 3.1 Choice

Pick one option from a defined set.

Question fields (source: primitives/choice):
- `type`: always "choice".
- `instructions`: the question.
- `criteria`: a map where each key is an option name and each value is a description. Option names AND descriptions are both sent to the model. Descriptions can be `null` when the option names are clear on their own, e.g. `{"calm": None, "frustrated": None, "angry": None}`.

SDK note (SDK wins where it differs from the docs phrasing): in the Python SDK, Choice's `criteria` is a required "nonempty mapping of labels to text, asset, object, or array descriptions, or None for undescribed labels" and `instructions` is optional; the JSON schema marks `criteria` as required (source: sdk/python/api/types/questions).

Answer fields (source: primitives/choice):
- `choice`: the option with the highest probability.
- `probabilities`: the full distribution across every option; values sum to 1 (SDK phrasing: "values sum to approximately 1", source: sdk/python/api/types/responses).
- `confidence`: 0 to 1, computed from how `probabilities` is spread: flat = low, single peak = high.

Limits and guidance (source: primitives/choice):
- A Choice question accepts up to 255 options; adding options costs a few tokens each.
- Add an `other` or `none of the above` option when the list might not cover every input.
- In structured criteria objects, field names like `question`, `focus`, `what`, `not_for`, `examples` are not part of the API and none are reserved; you choose them and the model sees the names along with the values.

Worked example (ambiguous shoe-store ticket): department `returns` 0.61 / `billing` 0.35 / `shipping` 0.04 at confidence 0.42; requested_resolution `refund` 0.40 at confidence 0.20; tone `frustrated` 0.84 at confidence 0.76 (source: primitives/choice).

### 3.2 Score

Rate the state along ordered descriptive levels.

Question fields (source: primitives/score):
- `type`: always "score".
- `instructions`.
- `criteria`: an ordered array of level descriptions from the low end to the high end. Should have at least two levels; the API accepts up to 10. A level's number is its position in the array starting at 0; the order of the array is the numbering. The model gets the descriptions and nothing else, and each level is judged on its own against the state.

SDK note: Score's `criteria` is a required "nonempty, ordered list of text, asset, object, or array descriptions, one per score from zero" (JSON schema minItems: 1); `instructions` is optional (source: sdk/python/api/types/questions). In SDK v0.6.0 (2026-09-15, breaking) criteria changed from a dictionary keyed by integers to an ordered sequence (source: sdk/python/changelog).

Answer fields (source: primitives/score):
- `score`: position on the level number line from 0 to the top level number. It is the probability-weighted mean: each level number multiplied by its probability, added up, e.g. 0x0.0 + 1x0.57 + 2x0.43 = 1.43. It can fall between two levels.
- `legend`: level number mapped back to its description.
- `probabilities`: keyed by level number, sum 1.
- `confidence`: 0 to 1 from the spread.

Key representation detail: over HTTP, `probabilities` and `legend` are keyed by level number AS STRINGS ("0", "1", "2"); the Python SDK's `ScoreAnswer` keys both by integer level (source: primitives/score; sdk/python/api/types/responses). Teaching code must not mix the two.

Guidance (source: primitives/score):
- Different distributions can produce the same score: 1.0 can mean all probability on level 1, or half each on levels 0 and 2. Read `probabilities` and `confidence` alongside the score.
- Numbers-only levels fail: criteria `["0", "1", "2"]` on a cosmetic bug scored 0.55 at confidence 0.33; the same report with descriptive levels scored 0.0 at confidence 1.0. The model does not see a level's number or its neighbours.
- To combine Scores of different scale lengths, normalize: divide each score by its top level number, `len(criteria) - 1`, putting every score on 0 to 1 before applying weights.
- Structured level descriptions with a matching example changed the Safari ticket result from 1.43 / confidence 0.35 (plain strings) to 1.03 / 0.96; an unrelated example returned the same 1.43 / 0.35 as plain strings. Higher confidence does not establish which answer is correct.
- Give a rare extreme case its own level: a sentiment scale that ends at "very angry" can add "abusive or threatening"; without that level, both kinds of message may score near the top and the score alone may not distinguish them.
- Keep each Score question to one dimension: a description like "punctual and smart and experienced" is measuring three things, so an input high on one and low on another cannot be placed; confidence drops and the score means less. Split into one Score per thing and combine in code.
- If there is no in-between at all and the answer is one of a few discrete categories, use a Choice instead, or split the question into several Nouls.
- Use as many levels as you can describe distinctly, up to 10; three is fine. Test levels against your own data: two wordings of the same scale can behave differently on your data.

### 3.3 Noul

A yes/no question whose answer is a single probability.

Question fields (source: primitives/noul):
- `type`: always "noul".
- `instructions`: the yes/no question, or a statement to judge (a statement works as well as a question).
- `criteria`: optional, an object with `true` and `false` descriptions of what yes and no mean (Python SDK: `NoulCriteria(true=..., false=...)`, a TypedDict with `true` and `false` keys, each an optional Content description) (source: primitives/noul; sdk/python/api/types/questions).

SDK note (SDK wins): in the Python SDK, Noul's `instructions` is "optional when `criteria` describes an outcome" and `criteria` is "required when `instructions` is `None`"; the two fields backstop each other (source: sdk/python/api/types/questions).

Answer (source: primitives/noul):
- `noul`: a single number, the probability that the answer is yes. 0 means no, 1 means yes, near 0.5 means the model gives yes and no similar probability.
- There is NO separate `confidence` value: the distribution has only two outcomes, so the single `noul` value describes it completely (source: primitives/noul). If you want a confidence-style number, compute |2p - 1| (source: confidence).

Semantics and guidance (source: primitives/noul):
- A Noul value of 0.5 means equal yes/no probability; it does NOT mean a medium level of the thing asked about. Use Score with defined levels to measure a position on a spectrum.
- Ask one yes/no question per Noul: a two-condition question like "Is the customer angry and asking for a refund?" makes the value mean less.
- Phrase so a high value means yes (inverted phrasing silently flips what downstream code reads).
- Threshold guidance: use 0.5 when yes and no are equally easy to act on; raise it when acting on a false yes is expensive (paging someone, issuing a refund); lower it when missing a true yes is expensive (failing to flag a safety issue); middle values can go to a person.

Worked calibration example, jev-1.13.0 answers to "Is the customer asking for a human agent?" (source: primitives/noul):

| Message | noul |
|---|---|
| "Thanks, that fixed it!" | 0.02 |
| "How do I reset my password?" | 0.07 |
| "I need this sorted today, whatever it takes." | 0.26 |
| "Are you a bot?" | 0.40 |
| "Is there any way to speak to someone about my invoice?" | 0.84 |
| "I have asked three times now. Can I please just talk to a real person?" | 0.99 |

Noul vs Score on degree (candidates, "strong in Python?" Noul vs 4-level Score): 0.03 vs 0.0; 0.14 vs 1.0; 0.81 vs 2.05; 0.92 vs 2.89. The Noul value is the probability of one proposition, not a scale of experience (source: primitives/noul).

### 3.4 Box

Locate something in an image. Dreamer-ready preview, not production-ready: the request format, answers, and limits can change between releases, and accuracy will change as models update (source: primitives/box).

Requirements (source: primitives/box):
- The `TypeSafe-Danger-Zone-Images: true` header on each request.
- Jev 1.14: send `jev-preview` or `jev-1.14.0` as the `model`.
- An image in the request.

Question fields (source: primitives/box):
- `type`: always "box".
- `instructions`: what to find and in which image; does not have to be a question. Box takes NO `criteria`.

Answer (source: primitives/box):
- `box`: four edges `top`, `bottom`, `left`, `right`, each 0 to 1 as fractions of image size measured from the top-left corner (`left`/`right` are fractions of width, `top`/`bottom` of height); `left` < `right` and `top` < `bottom`.
- `confidence`: 0 to 1 per the docs; the SDK types it as `float | None`, "or None when the model does not provide it" (SDK wins: treat it as nullable) (source: primitives/box; sdk/python/api/types/responses).

Behavior and guidance (source: primitives/box):
- A Box answer is ALWAYS a box: there is no "not found" answer, so a question about something absent still returns four edges. Pair it with a Noul in the same request asking whether the target is in the image, and ignore the box when the Noul is low.
- One box per question: Box finds one target. For several things, ask one Box question each in the same request; when duplicates cannot be told apart in words, add a Choice with options `none`, `one`, `several` and split the image into regions when `several`.
- There is no recommended Box confidence threshold yet; tune on your own images. Below-threshold options: ask again on a better image/crop, pad the box before cropping, or check the box with edge questions.
- Edge-question benchmark: on 36 test crops of paintings with a known part of the target cut off, four per-edge Noul questions caught 30 of the cuts; a single "Is all of the mug inside `crop`?" question caught 26; drawing the box as an outline on the full image and asking about it caught 20.

Worked example response: `{"type": "box", "box": {"top": 0.25, "bottom": 0.82, "left": 0.44, "right": 0.84}, "confidence": 0.92}` under model jev-1.14.0 (source: primitives/box).

### 3.5 Structure in instructions and criteria

Structure is allowed, all of type EntryType (string, object, array, or null), in: `instructions` (Choice, Score, Noul), Choice `criteria` values, Score `criteria` entries, and Noul `criteria.true`/`criteria.false` (source: primitives/advanced). Structure a question when it helps clarity (labeled keys for multi-part questions) or when the question needs supporting data that is already JSON (schema, taxonomy, database row) (source: primitives/advanced).

Taxonomy walking: ask one Choice per level; options are the children of the current node and each option's value is the child's subtree, so the model sees what lives under a branch before committing. If a branch is too large, trim the value to its direct children and a sample of leaves (source: primitives/advanced).

---

## 4. Confidence vs probability

### What "calibrated" means

The AI primer defines calibration operationally: across many predictions from a well-calibrated model, outcomes assigned a probability of 0.2 should occur about 20% of the time, outcomes assigned 0.8 about 80% of the time, and outcomes assigned 1.0 should occur 100% of the time. These rates describe groups of predictions, never a guarantee about any single answer (source: https://docs.typesafe.ai/introduction/machine-learning-primer).

### Exact semantics

- `probabilities` is the model's full distribution across your options or levels; values sum to 1 and are constrained to what you supplied (source: confidence; primitives).
- `confidence` is a statistic computed from the answer's own `probabilities` distribution: 1 when all probability is on one outcome, 0 when spread evenly. It is returned on every Choice and Score answer; Noul answers do not carry one (source: confidence).
- Confidence "describes the model's answer, not a guarantee that the answer is correct" (source: primitives gotcha, confidence framing). TypeSafe's `confidence` is "one reasonable way to summarize a distribution, not the only one"; the formulas are exact and every answer includes full `probabilities`, so you can compute your own measure instead (source: confidence).

### Exact formulas (source: confidence)

- Choice: confidence = (p_max - 1/n) / (1 - 1/n) for n options, measuring how far the top probability sits above an even split. Only the top probability counts: (0.6, 0.3, 0.1) and (0.6, 0.2, 0.2) both have confidence 0.4.
- Score: confidence = max(0, 1 - (sum_i p_i * |i - m|) / MAD_unif), where m is the most likely level and MAD_unif = (1/n) * sum_i |i - (n-1)/2|. Probability on a neighboring level lowers confidence less than probability further away: with three levels, (0, 0.5, 0.5) has confidence 0.25 while (0.5, 0, 0.5) has confidence 0; the Choice formula would give both 0.25.
- Worked Score example: probabilities (0, 0.57, 0.43), most likely level 1, spread 0.43, MAD_unif for three levels 2/3, confidence = 1 - 0.43/(2/3), approximately 0.35.
- Noul equivalent (not returned by the API): confidence = |2p - 1|, giving 0 at p=0.5 and 1 at p=0 or p=1; it equals the Choice formula applied to a yes-or-no Choice.

Reference reimplementation (source: confidence):

```python
def choice_confidence(probabilities: list[float]) -> float:
    n = len(probabilities)
    return (max(probabilities) - 1 / n) / (1 - 1 / n)

def score_confidence(probabilities: list[float]) -> float:
    n = len(probabilities)
    m = probabilities.index(max(probabilities))
    spread = sum(p * abs(i - m) for i, p in enumerate(probabilities))
    even_spread = sum(abs(i - (n - 1) / 2) for i in range(n)) / n
    return max(0.0, 1 - spread / even_spread)
```

For Score, sort the level keys first: `levels = sorted(answer.probabilities)` then `score_confidence([answer.probabilities[level] for level in levels])` (source: confidence).

### Alternative measures worth trying (source: confidence)

- Top probability p_max: meaning depends on option count (0.5 is weak among 2 options, strong among 10), so threshold per question.
- Top-to-second ratio p_max / p_second: how clearly the winner beats the runner-up; useful because the official formula ignores everything but the top probability.

### Thresholding guidance

Three-band pattern (source: confidence):
- High confidence: act automatically.
- Medium: proceed with caution (confirm, flag for review, gather more info).
- Low: do not act (route to a human, request clarification, or fall back).

Where you draw the boundaries depends on the stakes; different actions in one system should be gated at different levels (destructive operations higher than read-only ones). "Start with conservative thresholds, test with your own data, and adjust as you observe results" (source: confidence).

Risk-scaled example from the docs: a single 0.5 floor for "genuinely unsure" routes to a human; `check_balance` (low stakes) proceeds at any confidence above the floor; `approve_transfer` (high stakes) executes with confirmation only above 0.9 and otherwise asks the user to verify (source: confidence).

Noul banding example: YES = 0.8, NO = 0.2; values between go to a reviewer; narrow the gap if reviewers see too much, widen it if wrong routes get through (source: primitives/noul).

---

## 5. Properties: models, pricing, tokens, latency, limits, jaggedness

### Models and aliases

- Request `model` values seen in docs: `jev-latest`, `jev-preview`, `jev-1.12`, `jev-1.13.0`, `jev-1.14.0`. Responses report the concrete version (e.g. `jev-1.13.0` for text examples, `jev-1.14.0` for Box) (source: primitives; primitives/box).
- Official models page: jev-1.14.0 (released October 14, 2026) and jev-1.13.0, both $42/BTok input with free output; aliases jev-latest -> jev-1.13.0 (stable, SDK default) and jev-preview -> jev-1.14.0; all served via POST /v1/systemone (source: https://docs.typesafe.ai/models.md).
- jev-latest is scheduled to move to 1.14.0 around October 21, 2026; deprecation promises are 60 days notice for 1.13.0 and 30 days for 1.14.0 (source: https://systemonemodels.org/guides/jev-1-14/; https://docs.typesafe.ai/models.md).
- Jev 1.14 was announced October 14, 2026 at 1:14pm PT as jev-preview, adding experimental image input (images themselves also work on 1.13) and the Box question type, which is the only 1.14-only feature. Long context is NOT a 1.14 addition: the official models page says long context is off by default and works on both Jev 1.14 and Jev 1.13 via the `TypeSafe-Danger-Zone-Long-Context: true` header (docs over web: systemonemodels.org folds 262k long context into its 1.14 write-up, but the models page wins under this file's conflict rule). The core 1.14 change is described as "small, subtle improvements to everything," with the biggest expected gain multilingual; no changelog or benchmark numbers were published (source: https://docs.typesafe.ai/models.md#long-context; https://systemonemodels.org/guides/jev-1-14/; images: /images).
- The first public release is jev-1.13.0; no public 1.0-1.12 versions exist and TypeSafe has not explained the numbering (note: the cookbooks pin `jev-1.12` as a model string, which the public web notes do not reconcile; treat the docs cookbook model IDs as authoritative for those cookbooks) (source: https://typesafe.ai launch coverage; cookbooks/parallel_questions).
- SDK model discovery: `client.models.list()` returns each model's name, description, and release date (YYYY-MM-DD). The underlying `GET /v1/models` currently lists ONLY the aliases; versioned IDs such as `jev-1.14.0` are accepted by the `model` field whether or not they appear in the list (source: sdk/python/api/clients/sync; sdk/python/api/types/responses; https://docs.typesafe.ai/models.md#listing-models).
- Alias movement: an alias moves when a new release ships, so its answers can change without any change to your code; each response's `model` field logs the versioned ID that answered. If you have tuned confidence thresholds against one version, send that version's ID instead of the alias and switch to the new version deliberately when ready (source: https://docs.typesafe.ai/models.md#aliases).
- Customizing Jev: there is no fine-tuning or LoRA adaptation with customer data; the same weights serve every account. You shape behavior only through the request: proprietary content and records in `state`, domain rules and boundary cases in each question's `instructions` and `criteria`, and decomposition into atomic questions combined in code (the AutoResearch cookbook shows training a downstream classical model on Jev's probabilities) (source: https://docs.typesafe.ai/models.md#customizing-jev).
- Data handling: Jev is not trained on customer requests or responses; zero data retention (ZDR) is available for enterprise customers (see the Legal page for the DPA and privacy policy) (source: https://docs.typesafe.ai/models.md#data-handling).
- Input modality is text only: strings, JSON objects, and arrays of text. No audio or video; convert those into text or structured fields before sending them as `state` (source: https://docs.typesafe.ai/models.md; concepts/state).
- English is the primary training language and where accuracy is currently best; other languages, including CJK scripts, are "handled but not equally well," so test on your own content before relying on Jev for a non-English workload and pay close attention to confidence when routing non-English input (source: https://docs.typesafe.ai/models.md#language-support; cookbooks/twitch_chat_filter).

### Pricing

- $0.042 per 1M input tokens ($42/BTok); output tokens free; cached input free (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev; https://docs.typesafe.ai/models.md; https://developers.cloudflare.com/ai/models/typesafe/jev/).
- The cookbooks use the constant PRICE = (0.042, 0.00) dollars per 1M tokens (input, output) for jev-1.12, checked 2026-08/2026-09 (source: cookbooks/parallel_questions; cookbooks/rerank_typesafe).
- Images have no separate charge: each image counts as input tokens billed at the same per-token input price as text (source: images).
- Marketing comparisons: homepage claims 238x lower input price than Claude Fable 5.1 and shows a $0.000081 per-call demo cost; The Register compared against GPT-5.6 Terra's $2.00/$12 per MTok. These are vendor comparisons of a non-generative classifier against generative LLMs and were flagged as not apples-to-apples by The Register and Hacker News (source: https://typesafe.ai; theregister.com; infoq.com).

### Token accounting / Usage

- Response `usage` has `input_tokens` and `output_tokens` (source: primitives/choice).
- Output tokens are metered in `usage` but billed at $0 (source: https://docs.typesafe.ai/introduction/quickstart.md; models.md pricing).
- SDK: `Usage` fields are `input_tokens: int | None` and `output_tokens: int | None`, each None when the API did not report it; guard before arithmetic (source: sdk/python/api/types/responses).
- Image tokens are included in `usage.input_tokens` and count toward context length; guidance on estimating image token usage is "coming soon" (source: images).
- Example magnitudes: the five-question triage request used 589 input / 212 output tokens (source: primitives/choice); the quickstart single-Choice request used 428 input / 73 output (source: https://docs.typesafe.ai/introduction/quickstart.md); the 1,200-call re-rank used 1,536,002 input + 25,200 output tokens for $0.0645 total (source: cookbooks/rerank_typesafe).

### Latency

- Claimed envelope: 70ms-500ms, claimed 40x-200x faster than frontier LLMs; workflow evals claim roughly 194x speed and roughly 445x cost reduction (vendor claims) (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev).
- Company demo: 0.114s vs 8.566s for GPT-5.6 Terra (source: theregister.com).
- Independent aggregate: 76ms median latency, upper quartile 270ms, across 12,759 tweets analyzed by OpenChamber (source: infoq.com).
- Cookbook observations: one 13-question batched call over a 53,777-character document took 0.27s (source: cookbooks/parallel_questions); Twitch chat classification requests took a median of about 0.4 seconds (source: cookbooks/twitch_chat_filter); skill-suggestion demo timings were 0.09-0.31s per request (source: cookbooks/skill_suggestion).

### Context and rate limits

- Context: 64k tokens per request / 32k per question; 262k for both limits with the `TypeSafe-Danger-Zone-Long-Context: true` header, off by default, working on both Jev 1.14 and Jev 1.13, at the same pricing, but slower and less accurate per TypeSafe itself (source: https://docs.typesafe.ai/models.md#long-context). Conflict note: Cloudflare's third-party listing says a 32,000-token context window; prefer the official 64k-per-request / 32k-per-question split (docs over web) (source: https://developers.cloudflare.com/ai/models/typesafe/jev/).
- Rate limits are tokens/sec and requests/sec per organization. The numbers are not printed in the docs, but each organization's current limits ARE visible in the developer console at console.typesafe.ai/rate-limits. A request over either limit returns 429 Too Many Requests; the SDKs retry these by default, waiting longer between attempts and following the `retry-after` header when present. Higher limits are available on custom and enterprise plans via sales@typesafe.ai (source: https://docs.typesafe.ai/models.md#rate-limits).
- Choice: max 255 options (source: primitives/choice). Score: 2 to 10 levels (source: primitives/score). No limit on question count per request, only size (source: primitives).

### HTTP request rules, compression, and error codes (source: https://docs.typesafe.ai/api)

- Request rules, applied to every request: body at most 32 MiB (413 above it; headers do not count); UTF-8 JSON without a byte order mark (BOM); at most 64 nested levels of objects and arrays in each of `state`, `instructions`, and `criteria` (flatten deeper content); finite numbers only, so `NaN`, `Infinity`, and numbers too large to represent such as `1e400` are rejected, and identifiers and exact large quantities must be sent as strings. Violations other than body size return 400. The finite-numbers rule is the server-side reason SDK v0.7.4 began serializing non-finite numbers as strings (see section 6 changelog).
- Compression contract: `Content-Encoding: gzip` (or `x-gzip`) or `zstd` is accepted; use exactly one compression layer and keep zstd's window at most 8 MiB. The 32 MiB limit applies to BOTH the compressed and the decompressed body. An unsupported `Content-Encoding` or more than one layer returns 415 Unsupported Media Type; a malformed compressed body returns 400. (The SDKs compress bodies of 1 KiB or more with zstd when the runtime supports it; see section 6.)
- Full HTTP error table: 400 Bad Request (a request-rule break, a malformed compressed body, or `max_tokens_exceeded` when the request is longer than the model's context length), 401 Unauthorized (missing or invalid API key), 413 Payload Too Large (body over 32 MiB), 415 Unsupported Media Type (bad `Content-Encoding` or multiple compression layers), 422 Unprocessable Entity (the request body failed validation, for example a missing required field or a malformed question; the response details the offending field), 429 Too Many Requests, and 529 Overloaded (TypeSafe temporarily overloaded). Retry 429 and 529 with exponential backoff instead of immediately; the SDKs handle both automatically under their default retry policy.

### Image limits (all inclusive; violations reject the image, never resize it; if any image is rejected the whole request fails with no partial answers) (source: images)

- Format: PNG or JPEG still images only; animated PNGs rejected.
- File size: 16 MiB per image (after decoding for base64).
- Dimensions: width and height 280 to 1568 pixels each; total pixels 78,400 to 2,458,624 (280x280 to 1568x1568 square area).
- Request body: 32 MiB including JSON, base64 text, and multipart framing (headers do not count; compression does not raise it).
- All images in the request: 32 MiB shared after API processing (re-encoding can enlarge images).
- Expanded request: 32 MiB after every reference is replaced by its image (a 10 MiB processed image referenced four times is over the limit).
- References: each max 1,024 bytes of UTF-8; all references together max 65,536 bytes; a reference cannot be empty or only whitespace.
- Multipart rules in detail: the first part must be named `request` and hold the JSON body (the name `request` is reserved for it); part names must be unique and non-empty; each image part's content type must be `image/png`, `image/jpeg`, `image/jpg`, `application/octet-stream`, or absent, and any other content type returns 400; each file part must belong to exactly one asset, so a part no asset names, two assets naming the same part, and an asset whose part is missing each return 400 (source: images).
- Error mapping: 400 for missing danger-zone header, rejected image/asset, unreferenced asset, invalid base64/format, empty reference, multipart rule breaks, or `max_tokens_exceeded`; 413 when over a size limit. A multi-problem request reports only one error (source: images).

### Known jaggedness (TypeSafe's own jev-1.13 limitations page, 9 failure modes)

The page's own "failure modes in detail" table lists exactly nine: 1 Literal reading ("answers the question you wrote, not the one you meant"), 2 Math and Numbers (not a calculator; with three sub-sections: Counting, Numeric representations such as hex/RGB comparison, and Math using score), 3 Date and time comparison (dates read as text, not ordered quantities), 4 Indirection (double negatives and multi-hop reasoning), 5 Large state full of irrelevant detail, 6 Adversarial content ("does not treat [data] as hostile by default", injection-prone), 7 Contradictory instructions and criteria, 8 Choice option order (leans toward the first option), 9 Generation ("not trained to generate text"). Counting the three Math sub-sections separately gives eleven; page last reviewed 2026-10-02 (source: https://docs.typesafe.ai/model-jaggedness/jev-1.13.md, "The failure modes in detail" table).

The page's "do this instead" column is as teachable as the failure modes (source: https://docs.typesafe.ai/model-jaggedness/jev-1.13.md):

- Literal reading: state the exact condition in `instructions`, put boundary cases in the criteria; when you catch yourself explaining what you really meant, that explanation is the missing half of the instruction; split unavoidable interpretation into two literal questions combined in code.
- Counting: count in code. To count items matching a criterion, iterate one Noul per item and sum the thresholded answers yourself; the page's worked snippet builds `item_{i}` Nouls over a list ("Is `items[{i}]` the name of a fruit?") and computes `count = sum(result.nouls[f"item_{i}"].noul > YES ...)`.
- Numeric representations: do the conversion in code and pass either the computed number or a named bucket; keep the model for the part that is genuinely a judgment, such as whether a color reads as a warning.
- Math using score: never reconstruct an exact magnitude by interpolating between the two nearest levels; score levels are weak in numerical calibration, so use the expectation only to check whether it passes a threshold.
- Dates: split the work; extraction is a judgment, arithmetic is not. Every date part is a small closed set (twelve months, thirty-one possible days, a bounded range of years), so extract parts as Choices over enumerated options with an explicit "not stated" option so a missing part is reported rather than guessed, then do the calendar math in code; the date_extraction cookbook is the worked version.
- Large state: retrieve and filter in code first and send only the fields the question needs; when you cannot filter in state, use a Noul to filter for relevance (the classifying_rag_passages cookbook is the worked example).
- Adversarial content: be explicit in the criteria and test edge cases before deploying to many users.
- Contradictions: treat the criteria as an extension of the instruction and align the two (a Noul where `true` maps to no and `false` maps to yes performs worse).
- Option order: reorder the options and check the answer stays consistent.
- The page closes with a context-rot warning box: avoid asking the model something code can compute exactly, hiding several judgments inside one question, System Two multi-hop tasks, and giving `state` more context than the question needs, since Jev suffers from context rot and unrelated material costs accuracy.

Security research: HiddenLayer (published October 16, 2026) claims Jev is "even more vulnerable to attacks" than LLMs, citing adversarial text attacks, prompt injection, and TokenBreak; Kasimir Schulz: "TokenBreak, for example, normally does not work with larger LLMs, but Jev is vulnerable to it out of the box." TypeSafe did not respond to requests for comment (source: https://www.itsecuritynews.info/typesafes-jev-even-more-susceptible-to-attack-than-llms-says-security-vendor/).

---

## 6. Python SDK surface

Package: `typesafe-sdk` (docs cover 0.5.7 through 0.7.5; workshop target is 0.7.5). Install with `uv add typesafe-sdk` or `pip install typesafe-sdk`. Extras: `http2` (HTTP/2), `pil` (send Pillow images via `Image.from_pil`), `zstd` (compress request bodies on Python 3.13 and earlier). Source: github.com/typesafe-ai/typesafe-sdk-python; API keys at console.typesafe.ai (source: sdk/python). A JavaScript/TypeScript SDK also exists (`npm install @typesafe-ai/sdk`), and the HTTP API can be called from any language; SDKs "provide typed questions and answers for the TypeSafe API and handle retries automatically with their default retry policy" (source: sdk).

### Clients

- `TypeSafeClient` (sync) and `AsyncTypeSafeClient` (async) mirror each other. Async differences: `transport` is `httpx2.AsyncBaseTransport`, `http_client` is `httpx2.AsyncClient`, cleanup is `await client.aclose()`; `system_one` and `models.list` are async; `attach_assets` still uses a plain `with` block (source: sdk/python/api/clients/async).
- Constructor parameters (all default None): `api_key`, `model`, `retry` (RetryPolicy; `RetryPolicy(max_retries=0)` disables retries), `timeout` (float or httpx2.Timeout; inherits http_client.timeout when supplied, otherwise the SDK default), `headers`, `transport`, `http_client` (mutually exclusive with transport; closed when the SDK client closes), `base_url`, `compression` (Literal['zstd', False] or None; defaults to zstd when available). Raises TypeSafeError (missing/invalid API key, invalid timeout, zstd unavailable) or ValueError (both transport and http_client supplied). Explicit options take precedence over environment variables; empty or whitespace-only env values are ignored (source: sdk/python/api/clients/sync).
- `system_one(state, questions, model=None, assets=None, retry=None, timeout=None, extra_headers=None, extra_body=None, response_model=None)`. `state` is Content and cannot be None (values inside an object may be None); `questions` is a nonempty mapping of names to question objects or raw dicts with a `type` key ("noul"/"choice"/"score"/"box"), freely mixed. `extra_body` is shallow-merged over the body after state/model/questions/assets are set (last-write-wins; object values replaced, not deep-merged). Returns SystemOneResponse or your response_model type. Raises TypeSafeError (invalid before sending, e.g. empty questions or unreadable asset), TypeSafeAPIError (unsuccessful HTTP response after retries), TypeSafeAPIConnectionError (cannot connect or times out after retries), TypeSafeAPIResponseValidationError (body does not match the response model) (source: sdk/python/api/clients/sync; sdk/python/api/types/questions).
- `client.models` is a cached property; `models.list()` returns ListModelsResponse with `models: tuple[ModelMetadata, ...]` (name, description, release_date YYYY-MM-DD) plus request_id and raw_http_response. In extra_headers overrides, "authentication, SDK identification, and `Accept` remain protected" (source: sdk/python/api/clients/sync; sdk/python/api/types/responses).
- Select a model at construction: `TypeSafeClient(model="jev")`; `jev-latest` is the default (DEFAULT_MODEL constant) (source: sdk/python/usage/basic; sdk/python/api/constants).

### Question objects

- `Noul(instructions=..., criteria=NoulCriteria(true=..., false=...))`: instructions optional when criteria describes an outcome; criteria required when instructions is None (source: sdk/python/api/types/questions).
- `Choice(instructions=..., criteria={...})`: criteria required, nonempty mapping of labels to descriptions or None (source: sdk/python/api/types/questions).
- `Score(instructions=..., criteria=[...])`: criteria required, nonempty ordered sequence, one description per score from zero (source: sdk/python/api/types/questions).
- `Box(instructions=...)`: "A question that locates what its instructions describe in the request's image"; only field is instructions. Docs example pins `model="jev-preview"` (source: sdk/python/api/types/questions).
- TypedDict forms: NoulModel, ChoiceModel, ScoreModel, BoxModel; `Question` = a question object or question dictionary; `Questions` = question inputs keyed by the names used to identify their answers. Raw dicts can carry unknown forward-compat fields such as `"weight": 2` (source: sdk/python/api/types/questions; sdk/python/usage/advanced).

### Responses

- `SystemOneResponse`: `model` (str), `usage` (Usage), `answers` (dict[str, Answer] keyed by question name); cached per-type accessors `nouls`, `choices`, `scores`, `boxes`; `request_id` (the `x-typesafe-request-id` header); `raw_http_response` (the underlying `httpx2.Response`). model_config = ConfigDict(extra="ignore", frozen=True, strict=True) (source: sdk/python/api/types/responses).
- Answer types: `NoulAnswer.noul` (float 0-1, schema example 0.98); `ChoiceAnswer.choice` / `.confidence` / `.probabilities` (example {"angry": 0.8, "calm": 0.1, "excited": 0.1}, confidence example 0.9); `ScoreAnswer.score` (example 1.7) / `.confidence` / `.legend` (dict[int, ...]) / `.probabilities` (dict[int, float]); `BoxAnswer.box` (BoxCoordinates top/bottom/left/right, schema examples 0.2/0.66/0.19/0.68) / `.confidence` (float | None). `Answer` is a discriminated union on the `type` key (source: sdk/python/api/types/responses).
- `response_model=` (added v0.7.0): pass a subclass of SystemOneResponse with typed answer attributes (e.g. `billing: NoulAnswer`, which equals `result.nouls["billing"]`), or a fully custom pydantic BaseModel mirroring the JSON body. Mismatch raises TypeSafeAPIResponseValidationError with a dotted `field_path` like `answers.tone.confidence` (source: sdk/python/usage/basic; sdk/python/api/exceptions).
- Unknown answer kinds are logged as a warning and skipped from typed accessors (recover via `result.raw_http_response.json()["answers"]`); unknown extra fields on recognized responses are ignored (source: sdk/python/usage/advanced).

### Assets and images

- `Asset`: "An asset referenced from request content; currently only images are supported," "with more modalities coming in the future." The API detects each image's format from its bytes. Image support is "only dreamer-ready" as of November 14, 2026 and requires `headers={"TypeSafe-Danger-Zone-Images": "true"}` on the client (source: sdk/python/api/types/assets; sdk/python/usage/basic).
- `Image` is a dataclass over image file bytes or a path; accepts Buffer objects (bytearray, memoryview, mmap, NumPy arrays); loaded once on first use and reused by every request sending the same Image object; non-bytes buffers are copied into memory once so the original can change or be closed afterwards. `Image.from_base64(data)` (whitespace in wrapped base64 ignored; raises TypeSafeError on invalid base64). `Image.from_pil(image, format="jpeg")` needs the `pil` extra; Pillow default encoder settings except JPEG quality 95; JPEG cannot store transparency or palettes, so pass format="png" for RGBA or P mode (source: sdk/python/api/types/assets).
- Three ways to reference assets (source: sdk/python/usage/basic; sdk/python/api/clients/sync):
  1. Direct placement in content (state/instructions/criteria): each asset gets a unique uuid-like automatic reference.
  2. `attach_assets(assets)` context manager: inside the `with` block, calls send each attached asset whose reference `str(asset)` appears in the request, enabling f-string embedding. Warning: the SDK only recognizes references to assets that are attached, passed in `assets`, or placed directly in content; any other reference is sent as plain text without the asset.
  3. Named references via the `assets` argument keyed by your chosen reference (e.g. `"<product>"`); use distinct delimiters to avoid matching ordinary text. Both styles may be mixed; an asset passed through `assets` and also placed directly is sent once, under its name.
- Requests with assets are sent as multipart/form-data, with each asset's raw bytes in its own part (source: sdk/python/usage/basic).

### Retries

`RetryPolicy` (dataclass) attributes: `max_retries` (0 disables), `backoff_initial` (first delay, doubled each attempt up to `backoff_max`; zero disables backoff), `backoff_max` (zero disables backoff), `backoff_jitter` (fraction of each delay randomly subtracted, 0 to 1), `http_statuses` (status codes retried), `respect_retry_after` (honor Retry-After and retry-after-ms headers), `api_connection_error` / `api_timeout_error` (retry those exception classes), `exceptions` (extra exception types), `predicate` (called with the raised exception; True triggers a retry), `timeout` (total retry budget in seconds per SDK call, including the initial attempt and delays; None disables; "stops before a retry whose delay would reach or exceed the budget, re-raising the last error") (source: sdk/python/api/retries). RetryPolicy can be set on the client or per call (docs example: `RetryPolicy(max_retries=3, timeout=10.0, http_statuses={429, 500, 502, 503, 504})`) (source: sdk/python/api/retries).

### Errors

Hierarchy (source: sdk/python/api/exceptions):
- `TypeSafeError` (Exception): base for SDK failures. Invalid API keys raise it at client creation, before any request (source: sdk/python/usage/basic).
- `TypeSafeAPIError` (TypeSafeError): carries `status`, `body` (JSON error body, plain text, or None), `headers`, `endpoint` (method and URL without credentials/query/fragment), and `request_id` property.
  - Status subclasses: TypeSafeBadRequestError (400), TypeSafeAuthenticationError (401), TypeSafePermissionDeniedError (403), TypeSafeNotFoundError (404), TypeSafeUnprocessableEntityError (422), TypeSafeRateLimitError (429, with `retry_after_ms` or None), TypeSafeInternalServerError (5xx).
  - `TypeSafeAPIResponseValidationError`: a successful HTTP response whose body was missing or structurally invalid required data; `field_path` dotted path; args = (status, body, headers, field_path, endpoint).
- `TypeSafeAPIConnectionError` (TypeSafeError + builtin ConnectionError): request failed without an HTTP response. `TypeSafeAPITimeoutError` subclasses it and builtin TimeoutError, with a `timeout` attribute. Generic `except ConnectionError` / `except TimeoutError` handlers will catch them.

API key handling: keys from `api_key` or TYPESAFE_API_KEY have leading/trailing whitespace stripped (including newlines from key files); empty keys, internal whitespace, control characters, and non-ASCII characters are rejected before sending. An explicitly empty key does not fall back to the environment (source: sdk/python/usage/basic).

### Env vars and constants

`typesafe_sdk.constants`: API_KEY_ENV = 'TYPESAFE_API_KEY' (required, no default), BASE_URL_ENV = 'TYPESAFE_BASE_URL' (default https://api.typesafe.ai), DEFAULT_MODEL_ENV = 'TYPESAFE_DEFAULT_MODEL' (default jev-latest), LOG_LEVEL_ENV = 'TYPESAFE_LOG_LEVEL' (applied once at import; default unset), DEFAULT_BASE_URL = 'https://api.typesafe.ai', DEFAULT_MODEL = 'jev-latest', DEFAULT_TIMEOUT = 10.0 seconds per HTTP operation (source: sdk/python/api/constants; sdk/python/usage/basic).

### Performance defaults and tuning (source: sdk/python/usage/advanced)

- Built on `httpx2` (not httpx): custom transports, clients, timeouts, limits, and raw responses are httpx2 types.
- Defaults: HTTP/1.1; at most 100 connections, all kept alive 30 seconds while idle; zstd compression of request bodies >= 1 KiB (on by default since v0.7.5; ensure the zstd extra on Python earlier than 3.14; disable with `compression=False`, and note the changelog caveat that "non-official APIs may not support this immediately").
- Reuse client instances (new clients cost connections + TLS handshakes). Share across threads is allowed but the pool bottlenecks under heavy load; use one client per thread (threading.local pattern).
- HTTP/2 multiplexes all requests over one connection (one handshake, one socket) but that connection caps throughput; keep HTTP/1.1 for high request rates, HTTP/2 for low-to-moderate concurrency. Enable via `typesafe-sdk[http2]` + `http_client=httpx2.Client(http2=True)`.
- High-rate async: `AsyncTypeSafeClient(http_client=Httpx2AiohttpClient())` from `httpx-aiohttp[httpx2]`.
- Logging: logger name `typesafe_sdk`; `info` = one summary line per request; `debug` also logs request and response headers and bodies. Secret headers (authorization, API keys, cookies, any header name containing `token` or `secret`) are redacted; bodies are NOT redacted.

### Gateways (alternative base_url; must follow the TypeSafe OpenAPI spec) (source: sdk/python/usage/basic)

| Gateway | base_url | model | key env |
|---|---|---|---|
| OpenRouter | https://openrouter.ai/api | ~typesafe/jev-latest | OPENROUTER_API_KEY |
| Vercel AI Gateway | https://ai-gateway.vercel.sh/typesafe | typesafe-ai/jev | AI_GATEWAY_API_KEY |
| Pydantic AI Gateway | https://gateway-us.pydantic.dev/proxy/typesafe | jev-latest | PYDANTIC_AI_GATEWAY_API_KEY |

### Changelog highlights (source: sdk/python/changelog)

- v0.7.5 (2026-10-14): zstd-by-default; Image assets from raw bytes, paths, base64, PIL; Box questions and answers; attach_assets; docs restructure. Box and Image support do not exist in earlier 0.7.x.
- v0.7.4 (2026-10-09): serialize non-finite numbers as strings instead of invalid JSON tokens.
- v0.7.3 (2026-10-09): fix async crashes during concurrent TLS with truststore<=0.10.4; more request validation; 30-second keepalive default; Performance docs.
- v0.7.2 (2026-09-26): http2 extra. v0.7.1 (2026-09-21): early API key validation, key excluded from logged exceptions; gateway examples.
- v0.7.0 (2026-09-18) BREAKING: msgspec -> pydantic ser/de; str subclasses now serialized as strings, not lists of characters; `response_model` added.
- v0.6.0 (2026-09-15) BREAKING: Score.criteria became an ordered sequence instead of an int-keyed dict; abstract input types; richer error messages; picklable exceptions/responses. v0.5.7 (2026-09-14): initial public release.

### Canonical quickstart

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        state={"document": "I was charged twice. Please fix this ASAP."},
        questions={
            "billing": Noul(instructions="Is this ticket about billing?"),
            "tone": Choice(
                instructions="What is the customer's tone?",
                criteria={"calm": None, "frustrated": None, "angry": None},
            ),
            "urgency": Score(
                instructions="How urgent is this ticket?",
                criteria=["can wait", "this week", "today"],
            ),
        },
    )

print(response.nouls["billing"].noul)
print(response.choices["tone"].choice)
print(response.scores["urgency"].score)
```

(source: sdk/python)

---

## 7. Architectural patterns

The docs ship four dedicated pattern pages under /patterns, each with its own worked example: Speculative Fan-Out (cost, speed), Confidence-Gated Routing (reliability, safety), Composite Scoring (cost, reliability, speed), and Intent Routing (cost, speed) (source: https://docs.typesafe.ai/patterns).

### 7.1 Speculative fan-out (/patterns/fan-out)

Ask every question the code MIGHT need in one request against the same state, including "speculative" questions asked before knowing they are relevant (e.g. "What action should be taken on the lights?"), and let code ignore unused answers. Questions are evaluated in parallel so extra questions are close to free (source: patterns/fan-out; primitives; demos/smart-home). The pattern page's own worked example is support-ticket triage: one request carrying a category Choice, a bug-severity Score, a reproducible-steps Noul, a refund-requested Noul, and a frustration Score; code branches on `category.choice` (bug_report escalates when severity > 1.5 and repro > 0.6; billing flags a likely refund above 0.7; frustration > 1.5 flags priority regardless of category) and simply ignores the speculative answers that turned out irrelevant (source: patterns/fan-out). The wrong way is sequential calls (category first, then domain/device, then action): it "optimizes for a minimum number of questions, but it ends up being much slower and more expensive than batching all of the questions in to one upfront API call" (source: demos/smart-home). Economics: 13 questions in one call was 11.5x cheaper and 9.6x faster than 13 calls per the primitives page, 12.2x/10.0x per the cookbook's measured run (source: primitives; cookbooks/parallel_questions).

### 7.2 Confidence-gated routing (/patterns/confidence-routing)

Act automatically above a threshold, escalate (to a human or an LLM) below it; different actions gated at different levels within one system (destructive higher than read-only). The dedicated pattern page lives at /patterns/confidence-routing (not /confidence, which is the concept page for thresholds and formulas): "Use confidence as a second axis. The answer tells you what; confidence tells you whether to act" (source: patterns/confidence-routing; confidence). The pattern page's worked example is voice banking commands with a 0.6 floor: "Below 0.6 confidence on any action, route to a human"; `check_balance` is low stakes, so 0.6 confidence is sufficient; `approve_transfer` executes automatically only above 0.85 and otherwise asks the user to confirm, because each action type gets its own threshold based on the consequences of acting on a wrong classification (source: patterns/confidence-routing). Variants: Choice confidence floors plus secondary-probability copies (notify a second team whose probability share > 0.25) (source: primitives/choice); Noul three-band YES/NO gates with the middle going to review (source: primitives/noul).

### 7.3 Composite scoring (/patterns/composite-scoring)

Split a complex judgment into one Score question per factor, normalize each score by its top level number (`len(criteria) - 1`) so scales of different lengths are comparable on 0-1, then combine with weights that live in your code: e.g. priority = 0.6 x severity + 0.3 x frustration + 0.1 x report_quality = 0.664 in the worked example. Change the weights in code when the ranking disagrees with the team (source: primitives/score). The dedicated pattern page's worked example is resume screening: four Scores (Python depth, team leadership, system design, generalist) each normalized by dividing by 4, then combined under role-specific weight sets, Senior IC = 0.40 py + 0.10 lead + 0.40 arch + 0.10 general vs Engineering Manager = 0.15 py + 0.40 lead + 0.20 arch + 0.25 general, so one request ranks a candidate for both roles and the weights stay visible and adjustable (source: patterns/composite-scoring).

### 7.4 Intent routing (/patterns/intent-routing)

Route a request to a handler with a Choice: deterministic logic, a specialist LLM, or a human. The dedicated pattern page's worked example is customer-service routing: an intent Choice plus a complexity Score in one request; intent confidence below 0.5 routes straight to a human; `order_status` goes to deterministic order-lookup code with no LLM involved; `product_question` and `return_exchange` go to different specialist LLMs, each loaded with different context; `complaint` escalates to a human when complexity.score > 1 or the complexity answer's own confidence is below 0.5, otherwise a complaint-resolution LLM handles it. Expensive resources only get invoked for the requests that actually need them (source: patterns/intent-routing). Threshold-picking guidance lives on /confidence and the confidence-routing pattern page at /patterns/confidence-routing. The ranking-plus-gate refinement: a Choice's probabilities always sum to 1, so something always ranks first even when nothing fits; pair the relative Choice with independent absolute Nouls (an "exists" check, gate questions, or per-candidate "fits" checks) to detect the no-answer case. "The Choice settles which skill, and the nouls settle whether to say anything at all" (source: cookbooks/semantic_find; cookbooks/skill_suggestion).

### 7.5 TypeSafe + LLM pairing

Use Jev for the fast typed decisions and an LLM at the seams: a Noul detects compound requests ("more than one distinct action"), an LLM splits them into atomic commands which Jev evaluates individually; conversational or general-information requests fall back to the LLM for freeform response. "The initial TypeSafe response is so fast compared to the LLM response that it adds negligible latency to the overall system" (source: demos/smart-home). The SDE cascade is the heavyweight version: cheap LLM extracts, Jev verifies per field, expensive LLM re-does only flagged items (source: cookbooks/sde_cascade).

### 7.6 Two-stage narrowing (wide rank then rerank)

When the option set exceeds what one Choice handles well (or the 255 cap): rank wide with cheap descriptions, shortlist, then rerank the shortlist with full detail plus independent fits Nouls. Used for 182-skill selection (one Choice holds 182 comfortably; "a few times larger and you would split it into chunks and rank each one, then run this same shortlist step over the winners") and for documents past 255 lines (pick a window of lines first, then rank lines inside it) (source: cookbooks/skill_suggestion; cookbooks/semantic_find).

### 7.7 Answers describe, code decides

Keep model answers as descriptions of the input and put all policy in code: the Twitch filter's `decide()` maps cached answers to show/highlight/dim/hide/blur, so changing a rule replays cached answers with zero new requests ("14 messages changed, 0 new requests"); the guardrails `route()` holds named threshold policies so strict vs permissive is a product decision, not a model one (source: cookbooks/twitch_chat_filter; cookbooks/llm_guardrails).

### 7.8 Concurrency for independent items

When items (not questions) are independent, fan out requests with a thread pool: ThreadPoolExecutor with 8 workers in the cookbooks ("enough to keep a live run to minutes, gentle on rate limits"), 12 for the re-rank; `pool.map` preserves input order; on rate limits, lower max_workers and rerun since completed answers are cached (source: cookbooks/skill_suggestion; cookbooks/twitch_chat_filter; cookbooks/rerank_typesafe).

---

## 8. Use cases and cookbook catalog

The official Cookbooks index lists exactly 20 cookbooks across 5 categories: 6 LLMs-and-agents (function calling, skill suggestion, LLM guardrails, citation check, classifying RAG passages, basic memory), 3 Classification (hierarchical classification, classification using confidence, Twitch chat filter), 4 Extraction (SDE cascade, date extraction, pre-parsed value extraction, structure recovery), 3 Search-and-matching (re-ranking, line-by-line search, entity alignment), and 4 Techniques (self-consistency with Choices, self-consistency with Nouls, parallel questions, AutoResearch feature discovery) (source: https://docs.typesafe.ai/cookbooks). Sections 8.1 through 8.8 cover eight of them in depth; section 8.12 summarizes the other twelve.

Shared cookbook infrastructure: `pip install 'cooksafe>=0.2.0,<0.3.0'`; `JsonCache("json_cache.json")` caches every API call keyed on its inputs so reruns replay published numbers without a key or spend (keyless kernels use api_key="cache-only"; delete the file to run live); `make_playground_link(state, questions, models=[...])` builds a console.typesafe.ai/playground#share/... URL that re-runs the request in the browser (source: cookbooks/llm_guardrails; cookbooks/parallel_questions; cookbooks/semantic_find).

### 8.1 LLM guardrails (cookbooks/llm_guardrails)

- Problem: screen every message into and out of an LLM app. System-prompt rules are exactly where a jailbreak talks its way past, and a second guard LLM costs a call's latency and money per turn and can be talked past too.
- Approach: one system_one request per message carrying a battery of Noul hazard questions plus one 4-level severity Score (0-3: No harm / Mild / Serious / Severe). INPUT_BATTERY: jailbreak, harmful_request, medical_advice, self_harm + severity. OUTPUT_BATTERY: broke_policy, harmful_request, medical_advice, self_harm + severity. Application-owned `route()` maps hazards to actions (jailbreak/broke_policy/harmful_request -> block, medical_advice -> review, self_harm -> support; PRECEDENCE = support, block, review, pass) under named policies: strict {review 0.35, action 0.70, severity_block 2.0} and permissive {review 0.35, action 0.85, severity_block 2.0}. Severity at/above its threshold upgrades reviews to blocks. Run on BOTH inputs and outputs.
- Standout numbers: "Ignore your instructions" scores as a jailbreak instead of working as one; dan jailbreak 0.98 -> block; neurosemantical jailbreak 0.74 / severity 0.51 -> block under strict, review under permissive (same probabilities, different decisions); dosage_request medical_advice 0.95 with severity 2.02 crossing the 2.0 line turns review into block; self_harm 0.96 -> support; good_refusal passes at broke_policy 0.07; jailbreaks taken verbatim from TrustAIRLab's in-the-wild collection; model jev-1.12, numbers from 2026-08-15.

### 8.2 Parallel questions (cookbooks/parallel_questions)

- Problem: a 13-question regulatory briefing (8 Noul + 2 Choice + 3 Score) over the GDPR Wikipedia article (revision 1363040264, 53,777 characters); N single-question calls pay for the document N times.
- Approach: send all 13 in one request; run both strategies 5 times; compare mean (bias) and std dev (noise) per question.
- Standout numbers: one call $0.000497 / 0.27s vs 13 calls $0.006090 / 2.71s = 12.2x cheaper, 10.0x faster; choices, scores, and 6 of 8 nouls identical across all repeats (std dev exactly 0.0 under both strategies); breach_72h batched mean 0.804 vs single 0.814 with std 0.0055 both ways; criminal_penalties mean 0.108 both, stds 0.0045 vs 0.0084. Noise is a property of the question, not the batching. The speed figure sums sequential single-call latencies; concurrent firing shrinks the latency gap but the 13x token cost stays.

### 8.3 Pre-parsed value extraction (cookbooks/pre_parsed_value_extraction_cookbook)

- Problem: generative extractors can invent values or transpose digits.
- Approach: (1) regex over-finds candidate spans (emails, phones, amounts); (2) a Choice whose options ARE the candidate spans picks the one that plays the requested role, with a NONE = "none" escape hatch, and companion Choice/Noul questions read attributes code needs (currency, country, credit-vs-charge); (3) code copies the picked value verbatim and normalizes it. The model chooses, code owns the string.
- Standout numbers: receipt email dana.personal@gmail.com at confidence 0.98 (the Reply-To the body asks for, not the From line); mobile "(415) 555-0177" at 1.00 + country US at 0.90 combined by the phonenumbers library into E.164 +14155550177; $1,315.50 charge at P(credit)=0.01 vs $50.00 credit at P(credit)=0.99. Limits: the 255-option Choice cap (narrow in two stages beyond it) and candidate-finding is the hard part (names need a roster, an NER, or an LLM proposer).

### 8.4 Re-ranking (cookbooks/rerank_typesafe)

- Problem: on the CLERC legal dataset (3,565 court-opinion passages pooled from 170 rows; 40 query rows; TOP_K=30), BM25 gets the gold passage into its 30-candidate shortlist for 100% of queries but ranks it first only 5% of the time. Fast search narrows; it cannot decide.
- Approach: one Noul per query-candidate pair ("Is this candidate the cited case?" with explicit true/false criteria), 40 x 30 = 1,200 calls via ThreadPoolExecutor(max_workers=12), sort each shortlist by noul descending. The noul is the sort score directly; no invented scoring scale, unlike repeated LLM-judge calls which can produce different scores for the same pair. Re-ranking can only reorder the shortlist; it cannot add passages fast search missed.
- Standout numbers: Top-1 5% -> 18%; Top-5 15% -> 35%; Top-10 38% -> 62%; 1,200 calls = 1,536,002 input + 25,200 output tokens = $0.0645 total at $0.042/1M input (jev-1.12, 2026-08). A real app would ask several questions per pair in one call (parallel-questions / fan-out pattern).

### 8.5 SDE cascade (cookbooks/sde_cascade)

- Problem: structured data extraction where schema validation catches structural errors but never semantic ones. Worked case: scrapegraphai/scrapegraphai-100k row [516], an NYU events page lacking both requested fields; gpt-5.4-mini returns a schema-valid record whose description is fabricated (possibly parroting the schema's own example), and jsonschema Draft202012Validator prints True.
- Approach: (1) extract with cheap gpt-5.4-mini ($0.75/$4.50 per 1M, text mode, deliberately NOT structured outputs/tool calls/JSON mode); (2) verify with a jev-1.12 Noul battery in one call: 7 heads per non-empty field (name_desc_mismatch, type_mismatch, unreasonable, hallucinated, off_target, incomplete, format_violation; type_mismatch skipped when the field type is "unknown"), one absence_wrong head per empty field, plus a displayed-only holistic __overall__::judge; all framed so bad = TRUE; (3) escalate to gpt-5.5 reasoning ($5.00/$30.00, roughly 7x the mini, reasoning_effort="high") only when ANY per-field P(wrong) exceeds FIRE_T=0.7 (a max-style any_flag gate, never a mean, so one confident red flag is not averaged into silence).
- Standout numbers: description::hallucinated 0.95 and off_target 0.85 fire while the holistic judge reads only 0.56; registration_open_date::absence_wrong 0.14 (correctly empty field stays low); gpt-5.5 re-extracts and returns description "" (honest empty field); over 100 prompts, gpt-5.5-reasoning alone sits at about 0.81 quality for about $0.10/extraction while the cascade's pareto frontier sits up-and-left of every single model (chart is a historical snapshot, costs not recalculated at the current Jev rate); verifier jev-1.12 at $0.042/$0.00, prices checked September 15, 2026. If json.loads on the extractor reply fails, the record is treated as fully empty, which the verifier flags and the gate escalates (the safe direction).

### 8.6 Semantic line-by-line search (cookbooks/semantic_find)

- Problem: given GitHub's Terms of Service (218 lines, 43,980 characters) and a plain-language question, return the exact quotable lines, and detect when the document has no answer, which raw ranking cannot do because Choice probabilities always sum to 1.
- Approach: tag each line with an ID via `line_id(i) = f"L{i:03d}"` and join into one state; in a single request ask a "where" Choice over all 218 line IDs (criteria None; the document carries the text) plus an "exists" Noul with explicit true/false criteria. Thresholds FOUND=0.7 / ABSENT=0.35 ("present answers typically read >=0.9, absent <=0.05") map exists to answered / partially addressed / not in this document; tune against your own documents before production. jev-1.12, TypeSafeClient(timeout=120.0).
- Standout numbers: "who owns the code I upload?" exists 0.98, L052 at 0.95; "can GitHub kick me off without warning?" exists 0.97, L168 at 0.97; the arbitration trap: closest line scores 0.86 yet exists 0.14 so the verdict is "not in this document"; minors question exists 0.46 = partially addressed, L029 at 0.90. Past 255 lines, search in two passes (window then lines).

### 8.7 Skill suggestion (cookbooks/skill_suggestion)

- Problem: an agent picking from Nous Research's 182-skill Hermes catalog sees index descriptions truncated to 60 characters (average 54), confuses lookalikes, and loads skills when nothing fits. Baseline claude-haiku-4-5-20251001: 16.8% wrong loads on covered requests, 9.8% needless loads on uncovered ones. Of 36 wrong first picks, 10 came from the right skill's own category: "the hard part is telling a few lookalikes apart."
- Approach: two TypeSafe requests per turn. Request 1 (rank_wide): Choice over all 182 names with index descriptions as criteria, plus three gate Nouls about whether an ACTION is wanted (acts_on_user_system, would_follow_documented_procedure, and inverted prose_suffices); oriented mean < GATE_THRESHOLD 0.30 means suggest nothing; keep top 12. Request 2 (rerank): Choice over the top-3 shortlist with description_full + 700-char SKILL.md excerpts as criteria, plus one independent fits::{name} Noul per candidate; best fits < FITS_THRESHOLD 0.30 drops everything. The single winner goes into a <skill_relevance> system-prompt block appended AFTER the prompt-cache breakpoint, worded so it can be ignored; an empty result still sends "No skill in the roster appears relevant to this request." to oppose the roster's "err on the side of loading" instruction. jev-1.12; WORKERS=8; rendered 2026-07-31.
- Standout numbers over 488 requests (315 covered across 171 distinct skills, 173 uncovered and written to punish guessing): wrong loads 16.8% -> 7.3% (2.3x fewer), needless loads 9.8% -> 4.0% (2.4x fewer), vs an oracle floor of 2.5% / 1.2%; fixed 37 requests and broke 7 the agent had right alone ("a confident wrong suggestion is more persuasive than no suggestion at all"); pitch-deck request flips powerpoint (0.700 on 60-char descriptions) to pptx-author on full-text rerank, while fits Nouls disagree (powerpoint 0.73, pptx-author 0.38); known failure: the Mastodon request survives both checks (gate 0.78, xurl fits 0.56) and suggests the X skill, since the second pass can only reject what the wide ranking hands it; rank_wide 0.16-0.31s, rerank 0.09-0.12s; roster prompt 16,089 characters.

### 8.8 Twitch chat filter (cookbooks/twitch_chat_filter)

- Problem: chat moves faster than a viewer can read; keyword lists cannot catch backseating ("go left, there's a treasure box behind the tree") or spoilers, neither of which contains bad words.
- Approach: one request per message with the stream title and game in the state (spoiler/backseat status depends on the game) and three questions: a category Choice over five fenced labels (question / hype / conversation / backseat / spam, with each criteria string carrying what the label IS and is NOT: "repetition alone does not make cheering spam", "A link alone is not spam"), a toxic Noul with true/false criteria, and a spoiler Noul. Pure-code `decide()` precedence: toxic >= 0.7 hide; category rule hide; spoiler >= 0.7 blur; else category rule. 29 messages fan out 8 at a time; pool.map preserves chat order. jev-1.13.0 (numbers 2026-09-25), timeout=60.0, `pip install 'typesafe-sdk>=0.7.1,<0.8.0'`.
- Standout numbers: 29 messages -> show 14, highlight 6, hide 7 (3 backseat + 2 spam + 2 toxic), blur 2; backseat advice scored 1.00; the Ranni plot-twist message favored conversation 0.57 over backseat 0.42 but spoiler 0.94 caught it; "you're so bad at this boss lmao, love you tho" stayed at toxic 0.21 thanks to the "light banter" false criteria; on the samples every toxic is >= 0.97 or <= 0.24 and every spoiler >= 0.94 or <= 0.20 (real traffic lands in between); median latency about 0.4s; rule change QUIET = hide hype + dim conversation: "14 messages changed, 0 new requests". Live caveats: hide lines until classified or accept brief exposure; mainly-English training; the spoiler check has no record of the streamer's progress.

### 8.9 Smart Home Assistant demo (demos; demos/smart-home)

- Problem: a voice-style assistant must handle varied requests fast; sequential questioning is slower and more expensive.
- Approach: speculative fan-out of one long question list per request (category, room/domain, device, action, including speculative ones), code filters irrelevant answers; TypeSafe + LLM pairing for compound-request splitting and conversational fallback. "Turn off all of the lights in the house" needs only four answers: category = smarthome command, domain = whole house, device = lights, action = turn off. Built as a Vite/React SPA; source on GitHub at release. The only demo listed on the demos index.

### 8.10 Cross-cutting worked examples from the primitives pages

- Five-Choice ticket triage: one request, five Choice questions (two speculative), thresholds in code, second-team copies above 0.25 probability share, unused answers ignored; usage 589/212 tokens (source: primitives/choice).
- Entity dedup: one Noul per candidate record with object instructions ({"potential_duplicate": {...}, "question": SAME_PERSON}) and the DB id baked into the question key; answers 0.74 / 0.09 / 0.08; keep noul > 0.7 (source: primitives/noul).
- Box + edge questions: crop to the box, ask one Noul per edge whether the target continues past it, move out yes edges and re-ask; 30/36 known cuts caught vs 26 and 20 for the alternatives (source: primitives/box).

### 8.11 Third-party-reported production use

Early adopters swapped LLM safety classifiers and intent routers for Jev questions: safety classifiers 5-18x faster than the LLM replaced; Gemini described as 10-20x more expensive for comparable tasks; roughly 13% of Vercel paid teams within 24 hours (source: infoq.com).

### 8.12 The other twelve cookbooks

- Function calling (cookbooks/function_calling): turns natural-language trading requests into calls to ten ordinary typed functions whose arguments are already `Literal` enums; function names and closed-set arguments map to confidence-aware TypeSafe questions, e.g. "plot rolling correlation between nvda and spy for the past month" becomes rolling_correlation(symbol='NVDA', benchmark='SPY', window='1mo') at confidence 0.91 and "what tickers do you have" becomes list_symbols() at 1.00.
- Hierarchical classification (cookbooks/hierarchical_classification): classifies documents through four deep hierarchies (CPC patents, Shopify retail products, MeSH biomedical, the cooksafe repository tree) with parallel beam search over Choice probabilities: every node is a Choice whose full distribution is its edges, the best K paths are kept by length-normalized geometric-mean edge probability `product(edge_probabilities) ** (1 / decisions)`, and deeper evidence can repair an ambiguous early decision that greedy search cannot. Alongside two-stage narrowing, this level-by-level Choice chaining is the docs' answer to option sets past the 255-option Choice cap (source: cookbooks/hierarchical_classification; primitives/choice).
- Classification using confidence (cookbooks/classification_using_confidence): one Choice over 75 SEC SIC industry groups per 10-K business description; when the answer's own confidence is below 0.9, report the broader division the group rolls up into, with no second call since the broad label follows from the narrow one. Across 60 filings the confident half is right 90% of the time; the unconfident half goes from 40% right at group level to 70% reported one level up.
- Date extraction (cookbooks/date_extraction_cookbook): `extract_date(document, role)` asks Choices in one call for the date's kind and which month, day, year, or weekday the text names, each a small closed set with an explicit not-stated option; code resolves relative dates ("tomorrow", "next Thursday") from today, validates that the parts assemble into a real date, and confidence-gates review. The model reads what the text says and never does the calendar math.
- Structure recovery (cookbooks/autoformat): reconstructs Markdown from formatting-stripped text in two sequential requests: pass 1 asks one Noul per adjacent pair of lines (did the break split a sentence?) and merges continuing lines into blocks; pass 2 asks one Choice per merged block (heading / paragraph / list item / quote / code / callout) plus companion questions (heading level, step order, callout kind) read only when relevant. Direct evidence like blank lines and explicit markers stays in code, and every character of the output comes from the input.
- Double-checking citations (cookbooks/citation_check): an ordinary string match first marks quotes missing from the source document as fabricated; one Choice then reads each surviving quote's context and decides whether it supports, contradicts, or says nothing about the claim (verified / contradicted / unsupported), and verdicts below 0.8 confidence go to a human to confirm.
- Classifying RAG passages (cookbooks/classifying_rag_passages): between retrieval and generation, one request per query-passage pair carries four Nouls (is it relevant, does it state something usable in an answer, does it contradict something the query takes for granted, is it trying to instruct the model); `route()` thresholds label each passage as evidence, conflicting information, or dropped, and evidence and conflicts reach the answering LLM in separate blocks. The test run flags a planted prompt injection and two false-premise questions. This is the docs' prescribed fix for the large-state jaggedness mode (source: cookbooks/classifying_rag_passages; https://docs.typesafe.ai/model-jaggedness/jev-1.13.md).
- Simple memory system (cookbooks/basic_memory): after each call, a gate Noul sees the request and its answer together and asks whether the request states an important fact about the customer worth remembering; at P(yes) >= 0.5 the ticket and answer are saved per customer in a plain dict, and an `ask_with_memory()` wrapper (a basic agent harness) adds the saved memories to the state of later calls. Routing the example tickets alone gets 2 of 6 right; with memory, all 6.
- Knowledge graph entity alignment (cookbooks/entity_alignment): decides which of 450 candidate pairs from two beer catalogues describe the same product with one 3-level Score (different product / related, but possibly not the same, hand to a curator / same product) plus three companion Nouls that surface which fields disagree; the score is rounded to the nearest level to pick the outcome. A Score fits because each outcome gets its own semantic label, including the middle one; a wrong merge is the expensive mistake, which is why the curator level exists.
- Self-consistency, Choices (cookbooks/consistency_choice_cookbook): repeat sampling to measure answer stability: one borderline moderation post, an 8-Choice rubric, 15 repeats per condition against LLM baselines. TypeSafe repeats its plurality labels 90.8% of the time (LLM conditions 87.5% to 100%) and still flips on 2 of the 8 questions; requiring a top probability of at least 0.60 (otherwise `uncertain`, to human review) raises agreement to 99.2% with automatic labels on 74.2% of answers.
- Self-consistency, Nouls (cookbooks/consistency_noul_cookbook): the Noul twin: one auto-insurance claim, a 14-Noul rubric, 15 repeats per condition. TypeSafe's mean per-question probability standard deviation is 0.0102, below every LLM probability condition tested, yet its `covered` answers span 0.43 to 0.53 across a 0.5 threshold; probabilities from 0.30 through 0.70 become an explicit `uncertain` outcome for human review while the underlying noul values stay visible.
- AutoResearch feature discovery (cookbooks/autoresearch_feature_discovery): an autoresearch loop where an LLM proposes TypeSafe questions, Jev answers them for every row (29 Score questions x 2 columns plus 9 Nouls x 1 = 67 numeric features per wine tasting note), and a supervised CatBoost regressor trains on the answers (2,000 reviews, held-out RMSE 1.77 points on an 80-100 critic scale); each round the proposal call reads which questions the model used and which rows it still gets wrong. The models page's "Customizing Jev" section points here as the way to adapt Jev's outputs to a domain without fine-tuning (source: cookbooks/autoresearch_feature_discovery; https://docs.typesafe.ai/models.md#customizing-jev).

---

## 9. Gotchas and best practices

### Question design

1. Question IDs carry zero signal to the model; put the complete question in `instructions` (source: primitives).
2. Noul 0.5 means equal yes/no probability, not "medium"; inventing 0-1 bands in code means nothing was judged against them. Use Score for position on a spectrum (source: primitives/noul).
3. One yes/no condition per Noul; compound conditions make the value mean less. Phrase so high means yes; inverted phrasing ("Is the message free of personal data?") flips the meaning silently (source: primitives/noul).
4. Score levels must describe situations, not degrees or numbers: the model never sees level numbers or neighbours, so "worse than the previous level" means nothing and numbers-only criteria produced 0.55 @ 0.33 where descriptive levels gave 0.0 @ 1.0 (source: primitives/score).
5. Use the same structured field names on every Score level so the model compares like with like; structured field names are model-visible and user-chosen, none reserved; keep labels short (source: primitives/choice; primitives/advanced).
6. Level examples steer only when they match real inputs; an unrelated example changes nothing, and higher confidence alone does not show a description is better. Validate on examples with known expected levels (source: primitives/score).
7. Criteria strings that say what a label is NOT prevent bleed between lookalike labels (Twitch's "not gameplay instructions phrased as a question"); the "light banter" false-criteria is why borderline insults scored toxic 0.21 (source: cookbooks/twitch_chat_filter).
8. Gate questions must probe whether an action is wanted, not subject matter: a topical question cannot separate "explain what a monad is" from a request that needs a software skill (source: cookbooks/skill_suggestion).
9. Frame verifier Nouls so bad = TRUE with explicit criteria; vague questions ("is this extraction good?") give mushy, uncalibrated scores (source: cookbooks/sde_cascade).

### Reading answers

10. Confidence describes the model's answer, not correctness; confidence 1.0 is not a guarantee (source: primitives; confidence).
11. Different distributions can produce the same score; always read `probabilities` and `confidence` alongside it (source: primitives/score).
12. Normalize Scores by `len(criteria) - 1` before comparing or weighting across scales (source: primitives/score).
13. HTTP keys Score `probabilities`/`legend` by strings; the Python SDK keys them by integers. Do not mix (source: primitives/score; sdk/python/api/types/responses).
14. The Choice confidence formula counts only the top probability; use top-to-second ratio when the runner-up matters, and remember raw p_max thresholds shift meaning with option count (source: confidence).
15. Noul answers have no `confidence` field; compute |2p - 1| if you want to share gating code (source: primitives/noul; confidence).
16. A Choice always ranks something first (probabilities sum to 1); pair relative Choices with independent Nouls (exists / gate / fits) to detect the no-answer case, and include an `other`/`none` option when the list might not cover every input (source: cookbooks/semantic_find; primitives/choice).
17. The relative Choice and absolute Nouls can legitimately disagree; they are not redundant checks (source: cookbooks/skill_suggestion).

### Requests and architecture

18. Questions in one request are independent; only make a second request when code literally cannot proceed without the first answer. Otherwise ask everything at once and ignore extras (source: primitives).
19. Thresholds are domain-dependent and example-calibrated, not universal: cookbook sample data separates cleanly (toxic >= 0.97 or <= 0.24); real traffic lands in between. Start conservative, test with your own data, adjust; gate destructive actions higher than read-only ones (source: confidence; cookbooks/twitch_chat_filter).
20. A confident wrong suggestion is more persuasive than none (fixed 37, broke 7); word model-driven suggestions as ignorable, and when suggesting nothing still say so explicitly (source: cookbooks/skill_suggestion).
21. Keep large shared text byte-identical across turns and append per-turn additions after the prompt-cache breakpoint, or you lose prefix caching (source: cookbooks/skill_suggestion).
22. Two-stage narrowing cannot fix nearest-neighbor failures: the rerank can only reject what the wide ranking hands it (the Mastodon/xurl case), and the oracle floor is not zero (2.5%/1.2%) (source: cookbooks/skill_suggestion).
23. Re-ranking cannot add passages fast search missed; its ceiling is the shortlist's recall (source: cookbooks/rerank_typesafe).
24. Schema-valid is not correct; gate escalation on per-field heads aggregated with max (any_flag), never a mean, and exclude holistic judges from the gate (0.56 vs 0.95 on the same record) (source: cookbooks/sde_cascade).
25. Guardrails must run on both inputs and outputs; the batteries differ (broke_policy replaces jailbreak on the output side) (source: cookbooks/llm_guardrails).
26. Latency reality for streams: a median of about 0.4s per classification means hiding each new line until classified or accepting brief exposure; one request at a time cannot keep up, so run several concurrently (source: cookbooks/twitch_chat_filter).
27. Money parsing: to_decimal-style code assumes US comma/dot conventions; ask a Noul which convention the document uses and branch in code for cases like the European 1.315,50 (source: cookbooks/pre_parsed_value_extraction_cookbook).

### Images and Box

28. Box and Images are Dreamer-ready, not production-ready; format, answers, and limits can change between releases. Both need the `TypeSafe-Danger-Zone-Images: true` header on every such request (400 without it); Box additionally needs Jev 1.14, while plain images work on 1.13 and 1.14 (source: primitives/box; images).
29. A Box answer is always a box (no "not found"); pair with a Noul existence check (source: primitives/box).
30. There is no recommended Box confidence threshold; PAD=0.05 and MIN_CONFIDENCE=0.6 in the docs are explicitly examples to tune (source: primitives/box).
31. Image references are matched as plain text (whole value first, then left-to-right, no overlapping matches): a short reference like `cat` can match inside `category`; use per-request UUIDs. Object keys (Choice option names, question IDs) are never replaced, so an image-defined option must put the reference in the description, not the key (source: images).
32. Every use of a reference adds the image again toward the 32 MiB expanded-request limit; put a shared image in `state` once rather than in several questions' `instructions` (which also sends it to the model once per question) (source: images).
33. The API strips all image metadata and does NOT apply EXIF orientation: rotate the pixels upright (ImageOps.exif_transpose) before sending; resize so the longest side is at most 1568 px; convert GIF/WebP/HEIC; prefer baseline over progressive JPEG; re-export rejected files (source: images).
34. Base64 inflates each image by about a third against the 32 MiB body limit; multipart is recommended. data_base64 must use the standard alphabet with = padding, no whitespace, no `data:` prefix. If an asset has both `part` and `data_base64`, the API uses `part` (source: images).
35. An unreferenced asset is a 400 for the whole request; images outside limits are rejected, never resized; one rejected image fails the entire request with no partial answers; a multi-problem request reports one error (source: images).

### SDK-specific

36. Forgetting `with client.attach_assets(...)` sends str(asset) references as plain text WITHOUT the asset (source: sdk/python/api/clients/sync).
37. `debug` logging writes bodies unredacted; only secret headers are redacted. TYPESAFE_LOG_LEVEL is applied once at import (source: sdk/python/usage/advanced).
38. `extra_body` silently overrides colliding top-level fields (shallow merge, last-write-wins) (source: sdk/python/api/clients/sync).
39. Invalid API keys fail at client creation; an explicitly empty api_key does not fall back to the env var (source: sdk/python/usage/basic).
40. Two distinct timeout knobs: client/call `timeout` (per HTTP operation, default 10.0s) vs `RetryPolicy.timeout` (total per-call retry budget including the initial attempt and delays) (source: sdk/python/api/constants; sdk/python/api/retries).
41. The SDK is built on `httpx2`, not httpx; supplying both `transport` and `http_client` raises ValueError; a supplied http_client is closed with the SDK client (source: sdk/python/usage/advanced; sdk/python/api/clients/sync).
42. Keep HTTP/1.1 for high request rates; one client per thread under heavy threaded load; reuse clients (source: sdk/python/usage/advanced).
43. zstd-by-default (v0.7.5) may break non-official gateways; disable with `compression=False` (source: sdk/python/changelog).
44. Unknown answer kinds are warned and skipped; recover via `raw_http_response.json()["answers"]` (source: sdk/python/usage/advanced).
45. Usage token fields are nullable; guard before arithmetic (source: sdk/python/api/types/responses).
46. Breaking changes to remember when reading old samples: v0.6.0 Score criteria dict -> sequence; v0.7.0 msgspec -> pydantic; Box/Image/attach_assets only exist from v0.7.5 (source: sdk/python/changelog).

### Cookbook tooling

47. JsonCache keys on state + questions as JSON, NOT the model: changing the model replays stale answers unless you move json_cache.json aside; editing one word of a question silently invalidates the cache and triggers live spend (source: cookbooks/twitch_chat_filter; cookbooks/skill_suggestion).
48. pool.map preserves input order, which is what lets results re-zip by position; live integrations should carry the platform message ID instead (source: cookbooks/twitch_chat_filter).

### Model-level cautions

49. Jev's own jaggedness page: literal reading, unreliable counting/arithmetic, dates compared as text, double negatives, multi-hop indirection, accuracy loss with large irrelevant state, option-order bias in Choice lists, contradictory instruction/criteria degradation, and no hostile-by-default treatment of data (source: https://docs.typesafe.ai/model-jaggedness/jev-1.13.md).
50. Security: treat untrusted state as injection surface; HiddenLayer reports adversarial text, prompt injection, and TokenBreak working "out of the box" (source: itsecuritynews.info).
51. No hallucinated prose does not mean no wrong answers: Jev "can still emit a completely wrong valid value" (source: infoq.com).
52. TypeSafe publishes no benchmark numbers; 1.14 shipped with "internal intelligence measurements" only; the strongest adoption claims (1M users in days, one-third of Fortune 500) are company-reported and unverified (source: systemonemodels.org; investing.com).
53. Mainly-English training at publication: expect more misses on non-English input; 1.14's biggest expected gain is multilingual (source: cookbooks/twitch_chat_filter; systemonemodels.org).
54. Unresolved/unconfirmed items from web research, flagged as such: why versioning starts at 1.13; exact founding month in 2024; the ~$200M seed post-money (estimate); the homepage marker "TS.AI.0S1 (Version 0.01)"; publicly printed rate-limit figures (per-org values are visible in the developer console at console.typesafe.ai/rate-limits, but no numbers are printed in the docs) (source: public-web research notes, gotchas; https://docs.typesafe.ai/models.md#rate-limits).

---

## 10. Glossary

- **System One**: TypeSafe's coined category (after Kahneman's fast System 1 thinking) for models built to make fast, structured decisions software can use directly; also the name of the SDK method (`system_one`) and endpoint (`/v1/systemone`) (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev; primitives).
- **Jev**: TypeSafe AI's flagship and first System One model, launched September 15, 2026. $0.042/MTok input, output free, 70-500ms claimed latency (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev).
- **RLCD (Reinforcement Learning for Calibrated Decisions)**: TypeSafe's training method, optimizing calibrated decision probabilities rather than human-preferred text; positioned as the successor/alternative to RLHF (source: https://typesafe.ai/blog/introducing-system-one-models-and-jev).
- **Primitive (question/answer pair)**: the small typed building blocks of TypeSafe: a question defines one judgment for the model to make about a state, and its answer is the typed value that comes back, composed in code (source: primitives).
- **State**: the content being evaluated, sent in the top-level `state` field; string or JSON (and image references with images on). Every question in a request sees the same state. Cannot be None in the SDK, though values inside an object may be (source: primitives; sdk/python/api/types/questions).
- **Choice**: question type selecting one option from a defined set (max 255). Answer: `choice`, `probabilities` (sum 1), `confidence` (source: primitives/choice).
- **Score**: question type rating the state along 2 to 10 ordered descriptive levels numbered from 0 by array position. Answer: `score`, `legend`, `probabilities`, `confidence` (source: primitives/score).
- **Noul**: question type evaluating a yes/no question; returns `noul`, a single 0-1 probability of yes; optional {true, false} criteria; no separate confidence. (TypeSafe neologism; etymology not explained anywhere found) (source: primitives/noul; infoq-era web notes).
- **Box**: Dreamer-ready question type (Jev 1.14 only) locating what its instructions describe in an image; takes only `instructions`; answer is `box` {top, bottom, left, right} as 0-1 fractions from the top-left, plus confidence (nullable per the SDK) (source: primitives/box; sdk/python/api/types/responses).
- **criteria**: the possible answers of a question: option map for Choice, ordered level list for Score, optional {true, false} for Noul; Box takes none. Values accept string, object, array, or null (source: primitives).
- **instructions**: the question being asked about the state; where the evaluation logic goes. String, object, or array (source: primitives).
- **EntryType**: the accepted shape of `instructions` and all criteria values: string, object, array, or null (source: primitives/advanced).
- **score (value)**: the probability-weighted mean of level numbers, from 0 to the top level number; can be fractional; a position usable for ranking or rounding (source: primitives/score).
- **noul (value)**: the probability that the answer is yes: near 1 strong yes, near 0 strong no, near 0.5 uncertain. The answer and the certainty in one number (source: primitives/noul).
- **confidence**: a 0-1 statistic derived from the shape of the answer's probability distribution: 1 when concentrated, 0 when even. On every Choice and Score answer (and Box); not on Noul. Formulas: Choice (p_max - 1/n)/(1 - 1/n); Score max(0, 1 - spread/MAD_unif); Noul equivalent |2p - 1| (source: confidence).
- **probabilities**: the full distribution across your options or levels; sums to 1 and is constrained to what you supplied; the raw material for custom confidence measures (source: confidence).
- **MAD_unif**: in the Score confidence formula, the average distance from the middle level for an even spread across n levels: (1/n) * sum_i |i - (n-1)/2|; 2/3 for three levels (source: confidence).
- **legend**: Score answer field mapping each level number back to its description (string keys over HTTP, integer keys in the Python SDK); when criteria contained image references, the legend repeats the reference, not the image (source: primitives/score; images).
- **usage / Usage**: response token counts: `input_tokens` and `output_tokens` (nullable in the SDK). Image tokens are included in input_tokens with no separate charge (source: primitives/choice; sdk/python/api/types/responses; images).
- **assets**: top-level request map of images keyed by reference string. Asset fields: optional `type` ("image"), `part` (multipart part name) or `data_base64` (one required; `part` wins if both), `format` ("png"|"jpg"|"jpeg", required with data_base64) (source: images).
- **reference**: the key of an asset, written where the image belongs in state/instructions/criteria; matched as plain text; max 1,024 UTF-8 bytes each, 65,536 bytes total; every asset must be referenced (source: images).
- **Expanded request**: the request after every reference is replaced by its image; must stay under 32 MiB; each reference use adds another copy (source: images).
- **TypeSafe-Danger-Zone-Images header**: opt-in header required on every request containing an image or a Box question; 400 without it (source: images).
- **TypeSafe-Danger-Zone-Long-Context header**: opt-in header raising both context limits from 64k/32k to 262k tokens at the same price, slower and less accurate per TypeSafe; off by default and works on both Jev 1.14 and Jev 1.13 (source: https://docs.typesafe.ai/models.md#long-context).
- **Dreamer-ready**: TypeSafe's maturity label for Images and Box: not yet "ready for production"; for prototypes; format, answers, limits, and accuracy can change between releases (source: primitives/box; sdk/python/usage/basic).
- **jev-latest / jev-preview / jev-1.13.0 / jev-1.14.0**: model identifiers; requests use aliases or pinned versions, responses report the concrete version. jev-latest = stable (SDK default; 1.13.0, moving to 1.14.0 around Oct 21, 2026); jev-preview = newest including previews (1.14.0). Box needs 1.14; images work on 1.13 and 1.14 (source: primitives; https://docs.typesafe.ai/models.md).
- **Jaggedness**: TypeSafe's term for a model version's documented uneven capability profile; the Jev 1.13 jaggedness page's official table lists 9 known failure modes (11 counting the three Math and Numbers sub-sections separately), each with a "do this instead" remedy (source: https://docs.typesafe.ai/model-jaggedness/jev-1.13.md).
- **TokenBreak**: an adversarial tokenization attack that normally fails against large LLMs but which HiddenLayer says works on Jev "out of the box" (source: itsecuritynews.info).
- **Speculative fan-out**: asking every question code might need in one request, including questions asked before knowing they are relevant, and letting code ignore unused answers; pattern page /patterns/fan-out (source: primitives; demos/smart-home).
- **Composite scoring**: one Score per factor, normalized by top level number, combined with weights living in code (source: primitives/score).
- **Confidence-gated routing**: thresholding calibrated confidence to act automatically above and escalate below, with per-action thresholds; pattern page /patterns/confidence-routing (source: patterns/confidence-routing; confidence).
- **Intent routing**: routing a request to the optimal handler (deterministic code, a specialist LLM, or a human) via Choice plus confidence thresholds; pattern page /patterns/intent-routing (source: patterns/intent-routing).
- **Edge questions**: Box-verification technique: crop to the returned box and ask one Noul per edge whether the target continues past it; caught 30/36 known cuts vs 26 for a single whole-target question (source: primitives/box).
- **battery**: a dict of questions sent together in one request (e.g. guardrail hazard batteries, SDE per-field verifier batteries); the whole battery costs one call (source: cookbooks/llm_guardrails; cookbooks/sde_cascade).
- **policy (guardrails)**: a named set of threshold numbers ({review_threshold, action_threshold, severity_block}) applied in application code to a TypeSafe assessment (source: cookbooks/llm_guardrails).
- **fast search / re-ranking**: fast search (BM25, dense embeddings) narrows a corpus to a shortlist; re-ranking reorders that shortlist by scoring each query-candidate pair with a Noul and sorting by it (source: cookbooks/rerank_typesafe).
- **CLERC**: legal retrieval dataset of US court opinions used in the re-ranking cookbook; each row has a query, one gold positive, and 20 negatives (source: cookbooks/rerank_typesafe).
- **SDE cascade**: extract with a cheap model, verify with per-field TypeSafe Nouls returning P(wrong), escalate to an expensive reasoning model only when a signal fires (source: cookbooks/sde_cascade).
- **any_flag gate**: escalate if ANY per-field flag exceeds FIRE_T; max-style, never a mean; excludes the holistic judge (source: cookbooks/sde_cascade).
- **verifier heads**: per-field Noul metrics: name_desc_mismatch, type_mismatch, unreasonable, hallucinated, off_target, incomplete, format_violation for non-empty fields; absence_wrong for empty; plus display-only __overall__::judge (full pipeline adds a spurious head and a difficulty score) (source: cookbooks/sde_cascade).
- **decomposition (the TypeSafe Way)**: everything programmatically decomposed into narrow questions: "Decomposition maximizes the intelligence of every prompt, and makes the algorithm tunable and interpretable" (source: cookbooks/sde_cascade).
- **progressive disclosure**: read a whole catalog cheaply first, then only the shortlist in detail (skill suggestion's two-request design) (source: cookbooks/skill_suggestion).
- **gate questions / fits Nouls**: independent Nouls that decide whether to act on a Choice ranking at all: gates judge the request, fits judge each candidate; thresholds 0.30 in the cookbook (source: cookbooks/skill_suggestion).
- **wrong load / needless load**: skill-suggestion metrics: wrong load = covered requests where the first skill_view call was not the covering skill (loading nothing counts as a miss); needless load = uncovered requests where the agent called skill_view at all (source: cookbooks/skill_suggestion).
- **oracle arm**: measurement arm where the agent is handed the right answer; the ceiling, still 2.5%/1.2% error (source: cookbooks/skill_suggestion).
- **cooksafe / JsonCache / make_playground_link**: cookbook support package; JsonCache replays cached API calls keyed on state+questions JSON; make_playground_link builds a console.typesafe.ai/playground share URL (source: cookbooks/llm_guardrails; cookbooks/twitch_chat_filter).
- **Hermes roster / skill_view**: the 182-skill catalog (NousResearch/hermes-agent, MIT, pinned commit) and the agent tool that loads a skill by exact free-text name; the first skill_view call is what gets graded (source: cookbooks/skill_suggestion).
- **E.164**: the international phone format starting with + and the country code (+14155550177), produced in code by the phonenumbers library from TypeSafe's picked span plus classified country (source: cookbooks/pre_parsed_value_extraction_cookbook).
- **TypeSafe + LLM pairing**: Noul-detected compound requests split by an LLM into atomic commands; conversational requests fall back to an LLM; TypeSafe's speed adds negligible latency (source: demos/smart-home).
- **Content / ContentValue / JSONValue / JSONContent**: SDK type aliases: JSONValue is a JSON-like value (nestable, may contain None); JSONContent is a string or mapping/sequence of JSONValue; ContentValue may also hold assets; Content is text, an asset, or a mapping/sequence of ContentValue, with each asset sent in the request's assets and its reference in its place (source: sdk/python/api/types/common).
- **SystemOneResponse / response_model**: the frozen, strict pydantic response model, and the system_one argument (v0.7.0) accepting a custom pydantic type for the body, validated with TypeSafeAPIResponseValidationError on mismatch (source: sdk/python/api/types/responses; sdk/python/usage/basic).
- **RetryPolicy**: SDK dataclass configuring retries: max_retries, exponential backoff with jitter, http_statuses, Retry-After handling, connection/timeout toggles, extra exceptions, predicate, and a total per-call timeout budget (source: sdk/python/api/retries).
- **TypeSafeError hierarchy**: base TypeSafeError; TypeSafeAPIError with 400/401/403/404/422/429/5xx subclasses (429 carries retry_after_ms); TypeSafeAPIConnectionError (also ConnectionError); TypeSafeAPITimeoutError (also TimeoutError); TypeSafeAPIResponseValidationError with field_path (source: sdk/python/api/exceptions).
- **httpx2**: the HTTP library underpinning the SDK; all custom transport/client/timeout/limit/response types are httpx2 classes (source: sdk/python/usage/advanced).
- **typesafe_sdk.constants**: module of public env-var names and defaults (API_KEY_ENV, BASE_URL_ENV, DEFAULT_MODEL_ENV, LOG_LEVEL_ENV, DEFAULT_BASE_URL, DEFAULT_MODEL='jev-latest', DEFAULT_TIMEOUT=10.0) (source: sdk/python/api/constants).
- **ModelMetadata / ListModelsResponse**: models.list() result: tuple of entries with name (model name or alias accepted by a request's model field), description, release_date YYYY-MM-DD (source: sdk/python/api/types/responses).
- **attach_assets**: client context manager registering assets for a `with` block so str(asset) references in request strings resolve to asset data (source: sdk/python/api/clients/sync).
- **Image**: the only supported Asset type: a dataclass over image bytes (Buffer protocol) or a path, with from_base64 and from_pil constructors; loaded once on first use, format detected from bytes (source: sdk/python/api/types/assets).
- **backseat**: Twitch category label: "Unrequested gameplay advice telling the streamer what to do, including instructions phrased as a question; not a request for information"; default rule hide (source: cookbooks/twitch_chat_filter).
- **classify() / decide()**: the Twitch filter's two halves: one request (three questions) per message, then pure code mapping answers to show/highlight/dim/hide/blur so rule changes cost zero new requests (source: cookbooks/twitch_chat_filter).

---

*Conflict-resolution rule applied throughout: SDK source over docs over web. Notable applications: Score probability/legend key types (SDK integer keys vs HTTP string keys, both documented); Box confidence nullability (SDK float | None over the docs' plain float); Noul instructions optionality (SDK's criteria-backstop rule over the docs' always-required phrasing); context window (official 64k/32k over Cloudflare's 32k); long-context availability (the models page's "works on both Jev 1.14 and Jev 1.13" over systemonemodels.org's 1.14-announcement framing); batching speedup (cookbook's measured 12.2x/10.0x noted alongside the primitives page's 11.5x/9.6x citation of it).*
