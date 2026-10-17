"""Build the Jev workshop deck: Jev-Workshop.pptx"""

from deck_lib import (CLAY, CORAL, CREAM, INK, LINE, MUTED, PAPER, SAGE, SANS,
                      SERIF, SLATE, Deck)
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

ASSETS = "../assets"
OUT = "../Jev-Workshop.pptx"
FOOT = "Jev workshop  |  TypeSafe AI's System One model  |  October 2026"

d = Deck()

# ---------------------------------------------------------------- 1 title
s = d.slide()
d.text(s, "WORKSHOP  |  OCTOBER 2026", x=0.9, y=0.9, w=8, h=0.4, size=13, color=CLAY, font=SANS, bold=True)
d.text(s, "Jev", x=0.86, y=1.7, w=11, h=1.8, size=112, color=INK, font=SERIF)
d.text(s, "The first System One model", x=0.9, y=3.75, w=11, h=0.7, size=30, color=INK, font=SERIF, italic=True)
d.divider(s, 0.92, 4.75, 5.4, color=CORAL, weight=2.5)
d.text(s, "Typed questions in, calibrated decisions out: an AI primitive for software, not chat.\n"
          "What it is, how it works, its properties, and how to build with it.",
       x=0.9, y=5.0, w=9.6, h=1.0, size=16, color=SLATE, line_spacing=1.25)
d.text(s, "Every number and code sample in this deck was verified live against api.typesafe.ai while preparing this workshop.",
       x=0.9, y=6.6, w=10.5, h=0.4, size=11.5, color=MUTED, italic=True)
d.notes(s, "Welcome. Today is about a genuinely different kind of model. Not a better chatbot: a model that returns decisions instead of text. "
           "Everything shown today ran live against the real API; the notebooks in the repo reproduce every number.")

# ---------------------------------------------------------------- 2 agenda
s = d.slide(FOOT)
d.kicker(s, "Agenda")
d.title(s, "Five segments, five notebooks")
rows = [
    ["", "Segment", "Hands-on companion"],
    ["01", "Why another kind of model, and what Jev is", "01_hello_jev.ipynb"],
    ["02", "The four primitives: Choice, Score, Noul, Box", "02_primitives.ipynb"],
    ["03", "Probability vs confidence, routing on uncertainty", "03_confidence.ipynb"],
    ["04", "Architectural patterns, and the economics, measured", "04_patterns.ipynb"],
    ["05", "Real builds, sharp edges, properties reference", "05_real_world.ipynb"],
]
d.table(s, rows, x=0.55, y=1.75, w=12.2, col_widths=[0.9, 7.6, 3.7], row_h=0.72, size=16)
d.text(s, "Format: each segment is slides for the ideas, then a notebook to run the ideas against the live API.",
       x=0.55, y=6.35, w=11.5, h=0.4, size=13, color=MUTED, italic=True)
d.notes(s, "Two hours total. The deck carries concepts; notebooks carry proof. Attendees need Python 3.10+ and a TypeSafe API key from console.typesafe.ai.")

# ---------------------------------------------------------------- 2b story opener
s = d.slide(FOOT)
d.kicker(s, "The story we will follow")
d.title(s, "9:04 am. A ticket arrives.")
d.rect(s, 0.55, 1.75, 6.6, 2.7, fill=PAPER, line=LINE)
d.text(s, "support@yourcompany  |  ticket #18,402", x=0.85, y=1.95, w=6.0, h=0.3, size=11, color=MUTED, font=SANS)
d.text(s, "“Our API integration started returning 500 errors on every request about 20 minutes ago, and we can't process any customer orders until this is fixed.”",
       x=0.85, y=2.35, w=6.0, h=1.9, size=16.5, color=INK, font=SERIF, italic=True, line_spacing=1.3)
d.text(s, "A good support lead reads this and, in about two seconds, knows three things:",
       x=7.5, y=1.85, w=5.3, h=0.7, size=14.5, line_spacing=1.2)
for i, (q, a) in enumerate([
    ("Which team?", "technical, obviously"),
    ("How urgent?", "very: revenue is stopped"),
    ("How angry?", "tense, still civil"),
]):
    y = 2.6 + i * 0.62
    d.chip(s, q, x=7.5, y=y, w=1.75, fill=INK, color=CREAM, size=12)
    d.text(s, a, x=9.45, y=y + 0.03, w=3.3, h=0.35, size=13, color=SLATE, italic=True)
d.text(s, [[("No deliberation happened. ", {"bold": True}),
            ("Nobody multiplied anything or wrote a paragraph. That instant, effortless read is what psychologists call "
             "System 1 thinking, and it is exactly the reflex your software lacks. Today's question: how do we give code that reflex, "
             "with an honest measure of how sure it is?", {})]],
       x=0.55, y=4.85, w=12.2, h=1.1, size=15.5, line_spacing=1.25)
d.text(s, "Ask the room: what did your own brain do in the two seconds after reading the ticket? That introspection IS the API we are about to learn.",
       x=0.55, y=6.15, w=12.2, h=0.6, size=13, color=CLAY, italic=True)
d.notes(s, "Open with the story, not the technology. Read the ticket out loud, pause, and ask what their brain just did. "
           "Collect two or three answers; they will name routing, urgency, and tone without prompting. "
           "Then land the thesis: the workshop is about turning that two-second human read into a programmable, measurable primitive. "
           "This ticket returns on later slides, so the room keeps one running example.")

# ---------------------------------------------------------------- 3 the problem
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  Why")
d.title(s, "LLMs produce text for people. Your code needs decisions.")
d.bullets(s, [
    ("The mismatch. ", "LLMs are trained to write prose a person likes reading. Software needs a value it can branch on: a category, a score, a boolean."),
    ("The workaround we all ship. ", "Prompt a text generator to \"respond ONLY with JSON\", then parse, validate, retry, and hope the schema holds under load."),
    ("The tax. ", "Seconds of latency and dollars per thousand calls, for what is often a one-word judgment."),
    ("The risk. ", "Confident-sounding text is not a measure of certainty. There is no principled number to threshold on."),
], x=0.55, y=1.8, w=6.4, size=16.5, gap=14)
d.code(s, 'prompt = """Classify this ticket.\nRespond ONLY with valid JSON:\n{"team": ..., "urgent": ...}"""\n\nreply = llm(prompt + ticket)      # 2-8 s\ndata = json.loads(reply)          # pray\nteam = data.get("team")           # maybe?\n# retries, regex repair, schema drift...',
       x=7.3, y=1.85, w=5.5, h=3.2, title="the parse-and-hope pattern")
d.text(s, "“Models have been superhuman at chat for years, so where is all the automation?”",
       x=7.3, y=5.45, w=5.5, h=0.8, size=15, color=CLAY, font=SERIF, italic=True)
d.text(s, "Diogo Almeida, TypeSafe AI founder (launch post, Sept 2026)", x=7.3, y=6.3, w=5.5, h=0.3, size=11, color=MUTED)
d.notes(s, "Frame the pain before the product. Everyone in the room has written the code on the right. "
           "The quote sets up TypeSafe's bet: automation is blocked not by model intelligence but by the interface: text.")

# ---------------------------------------------------------------- 4 what is jev
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  What")
d.title(s, "Jev: typed questions in, calibrated decisions out")
# flow diagram in shapes
def flow_box(x, y, w, h, title, body, fill=PAPER, title_color=INK):
    d.rect(s, x, y, w, h, fill=fill, line=LINE)
    d.text(s, title, x=x + 0.18, y=y + 0.12, w=w - 0.36, h=0.35, size=14.5, bold=True, color=title_color)
    d.text(s, body, x=x + 0.18, y=y + 0.52, w=w - 0.36, h=h - 0.6, size=11.5, color=SLATE, line_spacing=1.12)

flow_box(0.55, 1.75, 3.1, 1.5, "state", "your data: a string or any\nJSON structure (ticket,\nrecord, transcript, policy)")
flow_box(0.55, 3.45, 3.1, 1.5, "questions", "typed: Choice, Score,\nNoul, Box. You define\nthe answer space.")
flow_box(4.35, 2.55, 3.4, 1.7, "Jev", "evaluates every question\nagainst the state,\nin parallel, independently", fill=INK, title_color=CREAM)
# arrows via thin rects
d.rect(s, 3.72, 2.48, 0.56, 0.06, fill=CORAL, line=None, round_=False)
d.rect(s, 3.72, 4.18, 0.56, 0.06, fill=CORAL, line=None, round_=False)
d.rect(s, 7.82, 3.37, 0.56, 0.06, fill=CORAL, line=None, round_=False)
flow_box(8.45, 2.3, 4.3, 2.2, "typed answers", "one per question ID:\n"
         "choice + probability per option\nscore on your rubric + confidence\nnoul: probability a statement is true\nbox: where something is in an image")
d.text(s, [[("your code ", {"bold": True}), ("branches, sorts, thresholds, routes. No parsing, by construction: "
        "answers are constrained to the options you supplied.", {})]],
       x=0.55, y=5.1, w=12.2, h=0.8, size=15.5)
d.text(s, [[("Why “System One”: ", {"bold": True, "color": CLAY}),
            ("Kahneman's fast, intuitive judgment, as opposed to slow System 2 reasoning. "
             "Ask what a knowledgeable person could answer in a second with the right context in front of them.", {})]],
       x=0.55, y=5.95, w=12.2, h=0.9, size=14, color=INK)
d.notes(s, "The whole model on one slide. Emphasize: questions are independent and parallel, answers come back under your IDs, "
           "and the model cannot return a value outside your schema. Impossible-to-parse output is impossible by design.")

# ---------------------------------------------------------------- 4b system 1 vs system 2
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  The idea behind the name")
d.title(s, "System 1 and System 2: two kinds of thinking, two kinds of model")
d.rect(s, 0.55, 1.62, 6.0, 2.3, fill=PAPER, line=LINE)
d.text(s, "In psychology (Kahneman, Thinking, Fast and Slow)", x=0.8, y=1.78, w=5.5, h=0.35, size=13, bold=True, font=SERIF)
d.bullets(s, [
    ("System 1: ", "fast, automatic, intuitive, near-zero effort. Reading the tone of an email, spotting the odd item on a shelf."),
    ("System 2: ", "slow, deliberate, effortful. Multiplying 17 x 24, planning an itinerary, writing a document."),
], x=0.8, y=2.2, w=5.5, size=12, gap=7)
d.rect(s, 6.85, 1.62, 6.0, 2.3, fill=PAPER, line=LINE)
d.text(s, "In AI, the analogy maps cleanly", x=7.1, y=1.78, w=5.5, h=0.35, size=13, bold=True, font=SERIF)
d.bullets(s, [
    ("System 2 models: ", "chat LLMs and reasoning models. Chains of thought, seconds of latency, dollars per Mtok. Built to deliberate and generate."),
    ("System One models (Jev): ", "snap judgments over the context in front of them. Typed answers, calibrated probabilities, ~100 ms. Built to decide, never to generate."),
], x=7.1, y=2.2, w=5.5, size=12, gap=7)
rows = [
    ["", "System One model (Jev)", "System 2 models (chat and reasoning LLMs)"],
    ["Latency", "~0.1 to 0.5 s", "seconds to minutes"],
    ["Output", "typed decision + calibrated probabilities", "free-form text, code, chains of thought"],
    ["Cost", "$0.042 / Mtok in, output free", "dollars per Mtok, output billed"],
    ["Best at", "atomic judgments: classify, score, verify, detect", "generation, multi-step reasoning, dialogue"],
    ["Fails when", "the question needs deliberation or arithmetic", "you need speed, calibration, or structured output"],
]
d.table(s, rows, x=0.55, y=4.12, w=12.2, col_widths=[1.5, 4.9, 5.8], row_h=0.4, size=11.5)
d.text(s, "Rule of thumb: if a knowledgeable person answers it in a second, it is a Jev question. If they reach for a whiteboard, decompose it into Jev questions composed in code, or hand it to a System 2 model.",
       x=0.55, y=6.62, w=12.2, h=0.45, size=11.5, color=CLAY, italic=True)
d.notes(s, "This slide is the vocabulary lesson for the whole class. Kahneman's System 1 is fast pattern recognition, System 2 is slow deliberation. "
           "TypeSafe named the category after the former: Jev makes the gut-check judgments, and your code or a reasoning model does the deliberating. "
           "The two kinds of model are complements, not competitors: most production systems will use both.")

# ---------------------------------------------------------------- 4c three architectures
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  Where it sits")
d.title(s, "Three software architectures (TypeSafe's framing)")
d.image(s, f"{ASSETS}/docs_software_architectures.png", x=0.9, y=1.75, w=8.2)
d.bullets(s, [
    ("Traditional software: ", "reliable primitives composed into decision trees. Deterministic, but blind to unstructured data."),
    ("LLM agents: ", "the model chooses its next step in a loop. Powerful with a human watching; every loop is another chance to go off the rails."),
    ("AI-powered software: ", "code owns control flow; the model appears only where the system needs programmable common sense. Each AI task atomic and constrained. This is the slot Jev is built for."),
], x=9.35, y=1.9, w=3.5, size=12, gap=10)
d.text(s, "Diagram: docs.typesafe.ai, How to build with TypeSafe", x=0.9, y=6.55, w=8, h=0.3, size=10.5, color=MUTED, italic=True)
d.notes(s, "The official diagram contrasts the three shapes. The pitch is not anti-agent; it is that unattended, high-volume automation "
           "needs the third shape: a normal software workflow that inserts System One only where a judgment is required.")

# ---------------------------------------------------------------- 5 company
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  Who")
d.title(s, "TypeSafe AI, the lab behind Jev")
d.bullets(s, [
    ("Founded 2024, San Francisco. ", "CEO Diogo Almeida (ex-OpenAI, Google Brain; a co-inventor of RLHF), COO Sasha Sheng, CTO Erik Gafni."),
    ("The thesis: “Machine Native Intelligence”. ", "Large-scale automation will be ~99% machine-to-machine. Build AI with software properties: structure, reliability, testability, speed, low cost. “Building prod, not God.”"),
    ("The product. ", "Hosted API only (closed weights, waitlist). One endpoint: POST /v1/systemone. One pricing axis: input tokens."),
    ("No per-customer fine-tuning. ", "Same weights for every account; you adapt it through state, instructions, and criteria."),
], x=0.55, y=1.8, w=7.1, size=15.5, gap=13)
d.rect(s, 8.0, 1.8, 4.8, 4.9, fill=PAPER, line=LINE)
d.text(s, "Timeline", x=8.25, y=2.0, w=4.3, h=0.35, size=15, bold=True, font=SERIF)
timeline = [
    ("Sep 15, 2026", "Jev launches (jev-1.13.0), “first System One model”"),
    ("Sep 16, 2026", "Out of stealth: $40M seed led by DCVC"),
    ("Oct 9, 2026", "Reported: $870M Series A at $7.5B valuation led by a16z (Bloomberg)"),
    ("Oct 14, 2026", "Jev 1.14 ships as jev-preview: images, Box, 262k long context"),
    ("~Oct 21, 2026", "jev-latest alias scheduled to move to 1.14"),
]
y = 2.5
for date, event in timeline:
    d.text(s, date, x=8.25, y=y, w=1.55, h=0.6, size=11, bold=True, color=CLAY)
    d.text(s, event, x=9.85, y=y, w=2.85, h=0.8, size=11, color=INK, line_spacing=1.1)
    y += 0.84
d.notes(s, "Why the buzz is recent: the company is weeks out of stealth and the 1.14 release landed three days before this workshop. "
           "Series A numbers are press-reported, not company-confirmed; flagged as such. "
           "The RLHF-co-inventor pedigree matters: the founder helped create the training method he is now arguing against for automation.")

# ---------------------------------------------------------------- 6 traction + skepticism
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  The buzz, both sides")
d.title(s, "Traction is real. So are the caveats.")
d.rect(s, 0.55, 1.7, 6.0, 4.9, fill=PAPER, line=LINE)
d.text(s, "Signal", x=0.8, y=1.9, w=5, h=0.4, size=16, bold=True, font=SERIF, color=SAGE)
d.bullets(s, [
    ("Adoption: ", "~13% of Vercel paid teams tried it within 24h of launch, about 2x GPT-5.6-family uptake (InfoQ, Oct 2026)."),
    ("Measured by users: ", "median 7x speedup and 30x cost savings; 76 ms median latency across 12.7k analyzed posts (OpenChamber via InfoQ)."),
    ("The demo everyone shared: ", "Jev playing Doom from structured game state; 0.114 s vs 8.566 s for GPT-5.6 Terra on the same decision (The Register)."),
], x=0.8, y=2.4, w=5.5, size=13.5, gap=10, marker_color=SAGE)
d.rect(s, 6.85, 1.7, 6.0, 4.9, fill=PAPER, line=LINE)
d.text(s, "Noise control", x=7.1, y=1.9, w=5, h=0.4, size=16, bold=True, font=SERIF, color=CLAY)
d.bullets(s, [
    ("“No hallucinations” needs an asterisk. ", "It can still emit a confidently wrong valid value; it “delegates the hallucination problem to the user” (Armin Ronacher). Calibration is the mitigation, not magic."),
    ("Adversarial input is a live concern. ", "HiddenLayer (Oct 16, 2026) reports Jev is more steerable by prompt injection than LLMs; TypeSafe's own jaggedness page agrees it does not treat state as hostile."),
    ("Closed and new. ", "Hosted only, no open weights, versioning started at 1.13 three weeks ago. Pin versions, test on your data."),
], x=7.1, y=2.4, w=5.5, size=13.5, gap=10, marker_color=CLAY)
d.notes(s, "This slide is the credibility slide: show you know both columns. The left column is why we are in this room; "
           "the right column is what responsible adoption looks like. The security finding directly motivates the guardrails design in notebook 05: "
           "never let Jev alone gate adversarial traffic; combine thresholds, review bands, and testing on real attacks.")

# ---------------------------------------------------------------- 6b basics: what is a model
s = d.slide(FOOT)
d.kicker(s, "Foundations  |  Zero assumed knowledge")
d.title(s, "First, the basics: what is a model, actually?")
d.bullets(s, [
    ("A model is a function with knobs. ", "Billions of adjustable numbers called parameters (or weights). Text goes in as tokens (word pieces), numbers flow through the knobs, an output comes out."),
    ("Training = turning the knobs. ", "Show the model an example, measure how wrong its output is, nudge every knob a tiny step in the direction that makes it less wrong. Repeat, trillions of times. That is gradient descent; nobody sets any knob by hand."),
    ("Pretraining ", "is that loop on a huge slice of the internet with one task: predict the next token. The result, a base model, is a brilliant text-continuer with no goal: not helpful, not safe, not decisive."),
    ("Post-training decides what it becomes. ", "The same base model can be turned into a chatbot, a reasoning engine, or a decision model, purely by what you reward next. That choice is the next three slides."),
], x=0.55, y=1.8, w=6.6, size=14.5, gap=12)
# training loop diagram
def loop_box(x, y, w, h, title, body, fill=PAPER, tc=INK):
    d.rect(s, x, y, w, h, fill=fill, line=LINE)
    d.text(s, title, x=x + 0.15, y=y + 0.08, w=w - 0.3, h=0.3, size=12.5, bold=True, color=tc)
    d.text(s, body, x=x + 0.15, y=y + 0.42, w=w - 0.3, h=h - 0.5, size=10.5, color=SLATE, line_spacing=1.1)
loop_box(7.5, 1.85, 2.3, 1.05, "1. example in", "“The capital of\nFrance is …”")
d.rect(s, 9.85, 2.32, 0.4, 0.06, fill=CORAL, line=None, round_=False)
loop_box(10.3, 1.85, 2.45, 1.05, "2. model", "billions of knobs\nproduce an output")
loop_box(10.3, 3.3, 2.45, 1.05, "3. compare", "output vs truth:\nhow wrong was it?")
d.rect(s, 11.5, 2.92, 0.06, 0.37, fill=CORAL, line=None, round_=False)
loop_box(7.5, 3.3, 2.3, 1.05, "4. nudge knobs", "every parameter\nmoves a tiny step")
d.rect(s, 9.85, 3.77, 0.4, 0.06, fill=CORAL, line=None, round_=False)
d.rect(s, 8.6, 2.92, 0.06, 0.37, fill=CORAL, line=None, round_=False)
d.text(s, "repeat ~trillions of times", x=7.5, y=4.5, w=5.2, h=0.3, size=11, color=MUTED, italic=True, align=PP_ALIGN.CENTER)
d.rect(s, 7.5, 5.05, 5.25, 1.45, fill=INK, line=None)
d.text(s, "The whole secret of 'training'", x=7.75, y=5.2, w=4.8, h=0.3, size=12.5, bold=True, color=CREAM, font=SERIF)
d.text(s, "is choosing WHAT counts as 'wrong' in step 3. Change the definition of wrong, and the same loop produces a completely different animal.",
       x=7.75, y=5.55, w=4.8, h=0.9, size=11.5, color=RGBColor(0xED, 0xEA, 0xE3), line_spacing=1.15)
d.notes(s, "This slide assumes nothing. Vocabulary established: parameters/weights/knobs, tokens, gradient descent as 'nudge all knobs to be less wrong', "
           "pretraining as next-token prediction, base model as raw material. The dark box is the bridge to the next three slides: "
           "RLHF, RLVR, and RLCD are the SAME loop with three different definitions of wrong.")

# ---------------------------------------------------------------- 6c basics: RLHF step by step
s = d.slide(FOOT)
d.kicker(s, "Foundations  |  Recipe 1 of 3")
d.title(s, "How RLHF actually works (the chatbot recipe)")
steps = [
    ("Step 1: collect human preferences", "Give the model one prompt, sample two answers, A and B. A human picks the one they like better. Do this tens of thousands of times.", "prompt -> answer A vs answer B -> 'B is better'"),
    ("Step 2: train a taste model", "Train a second model, the reward model, to predict which answer the human would prefer. It becomes a cheap, automatic judge of 'what people like'.", "answer -> reward model -> score 0.87"),
    ("Step 3: optimize against taste", "The chatbot generates, the reward model scores, and every knob is nudged toward higher-scoring answers (the RL part, usually PPO). Loop until the model reliably produces what people prefer.", "generate -> score -> nudge knobs -> repeat"),
]
for i, (t, body, mono) in enumerate(steps):
    x = 0.55 + i * 4.18
    d.rect(s, x, 1.75, 3.95, 3.3, fill=PAPER, line=LINE)
    d.chip(s, str(i + 1), x=x + 0.2, y=1.95, w=0.38, fill=CORAL, size=13)
    d.text(s, t.split(": ")[1], x=x + 0.72, y=1.97, w=3.1, h=0.65, size=13.5, bold=True, font=SERIF)
    d.text(s, body, x=x + 0.2, y=2.7, w=3.55, h=1.7, size=12, color=INK, line_spacing=1.18)
    d.text(s, mono, x=x + 0.2, y=4.5, w=3.55, h=0.4, size=10, color=CLAY, font="Menlo")
d.rect(s, 0.55, 5.35, 12.2, 1.25, fill=RGBColor(0xEA, 0xDF, 0xD4), line=None)
d.text(s, [[("The catch: ", {"bold": True, "color": CLAY}),
            ("the model is optimized to PLEASE the judge, not to be right. Pleasing rewards confident-sounding answers (hallucination), "
             "agreeing with the user (sycophancy), and collapsing onto one crowd-pleasing style (mode dropping). "
             "Perfect for chat. Poisonous for a number your code must trust.", {})]],
       x=0.8, y=5.52, w=11.7, h=0.95, size=13.5, line_spacing=1.2)
d.notes(s, "Walk the three cards slowly; this is the full RLHF mechanism: preference data, reward model, PPO loop. "
           "Fun fact for the room: TypeSafe's founder co-invented this recipe (InstructGPT/ChatGPT lineage), which is why his critique of it carries weight. "
           "End on the catch: step 3 optimizes for human approval, and approval is not accuracy.")

# ---------------------------------------------------------------- 6d basics: RLVR
s = d.slide(FOOT)
d.kicker(s, "Foundations  |  Recipe 2 of 3")
d.title(s, "RLVR: reward what can be checked")
steps = [
    ("Pick checkable problems", "Math with known answers, code with unit tests, puzzles with verifiable solutions. No human taste needed."),
    ("Let the model think out loud", "It writes a long chain of thought, then an answer. Those 'thinking tokens' are generated text: slow, and billed."),
    ("Reward only verified wins", "Did the code pass the tests? Did the answer match? Nudge knobs toward chains of thought that END correct."),
]
for i, (t, body) in enumerate(steps):
    x = 0.55 + i * 4.18
    d.rect(s, x, 1.75, 3.95, 2.35, fill=PAPER, line=LINE)
    d.chip(s, str(i + 1), x=x + 0.2, y=1.95, w=0.38, fill=SLATE, size=13)
    d.text(s, t, x=x + 0.72, y=1.97, w=3.1, h=0.65, size=13.5, bold=True, font=SERIF)
    d.text(s, body, x=x + 0.2, y=2.7, w=3.55, h=1.3, size=12, color=INK, line_spacing=1.18)
d.text(s, [[("What it produces: ", {"bold": True}),
            ("reasoning models (the 'thinking' models you have used). Genuinely strong on hard, multi-step problems. "
             "The cost: seconds to minutes of latency and output-token bills, because deliberation IS generated text. "
             "This is the System 2 machine: brilliant on a whiteboard, wrong tool for a two-second judgment call.", {})]],
       x=0.55, y=4.45, w=12.2, h=1.3, size=15, line_spacing=1.25)
d.text(s, "Where you have met these: chat assistants are RLHF; 'extended thinking' and o-style models are RLVR. Jev is neither.",
       x=0.55, y=5.9, w=12.2, h=0.5, size=13, color=CLAY, italic=True)
d.notes(s, "Keep this one brisk: the audience has used reasoning models. The point to land is the cost structure: "
           "RLVR quality rides on generated thinking tokens, so you pay in both seconds and dollars. "
           "That sets up the question RLCD answers: what if the judgment does not need any text at all?")

# ---------------------------------------------------------------- 6e basics: RLCD step by step
s = d.slide(FOOT)
d.kicker(s, "Foundations  |  Recipe 3 of 3, Jev's recipe")
d.title(s, "RLCD: reward honest probabilities")
steps = [
    ("Ask a closed question", "A question with a fixed answer space and a known real outcome: 'which team did this ticket actually go to?'"),
    ("Model answers in probabilities", "No text. It puts probability on each option: billing 0.12, technical 0.88, sales 0.00."),
    ("Score against reality", "A proper scoring rule pays out for honesty: claiming 0.99 and being wrong costs far more than admitting 0.60. Hedging everything at 0.33 earns nothing."),
    ("Nudge toward calibration", "Knobs move so that stated probability tracks real frequency: things it calls 0.8 should come true about 80% of the time."),
]
for i, (t, body) in enumerate(steps):
    x = 0.55 + i * 3.12
    d.rect(s, x, 1.75, 2.9, 2.9, fill=PAPER, line=LINE)
    d.chip(s, str(i + 1), x=x + 0.18, y=1.95, w=0.38, fill=CORAL, size=13)
    d.text(s, t, x=x + 0.65, y=1.97, w=2.1, h=0.9, size=12.5, bold=True, font=SERIF)
    d.text(s, body, x=x + 0.18, y=2.95, w=2.55, h=1.6, size=11, color=INK, line_spacing=1.16)
d.rect(s, 0.55, 4.95, 12.2, 1.5, fill=INK, line=None)
d.text(s, "Notice what is missing from this loop: text.", x=0.8, y=5.12, w=11.7, h=0.35, size=14.5, bold=True, color=CREAM, font=SERIF)
d.text(s, "There is no generation step to hallucinate in, no judge of style to flatter. The ONLY way to score well is to know the answer "
          "when it is knowable, and to say 'not sure' honestly when it is not. That property, calibration, is what your code will threshold on all afternoon.",
       x=0.8, y=5.5, w=11.7, h=0.85, size=12.5, color=RGBColor(0xED, 0xEA, 0xE3), line_spacing=1.2)
d.notes(s, "Mirror the RLHF slide deliberately: same loop, different definition of wrong. RLHF's judge is human taste; RLVR's judge is a verifier; "
           "RLCD's judge is reality plus a proper scoring rule. If someone asks what 'proper scoring rule' means: a payout scheme where "
           "your expected reward is maximized by reporting your true belief, like the Brier score; overconfidence is punished quadratically. "
           "Then the dark box: no text anywhere in the loop, which is why Jev cannot be a chatbot and does not hallucinate prose; "
           "it can still be wrong, but it is honestly wrong, with the uncertainty attached.")

# ---------------------------------------------------------------- 7 RLCD
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  How it is trained, recap")
d.title(s, "RLHF makes chatbots. RLCD makes decisions.")
rows = [
    ["", "RLHF", "RLVR", "RLCD  (Jev)"],
    ["Optimizes for", "responses people prefer", "verifiable task rewards", "calibrated decisions"],
    ["Produces", "chatbots and assistants", "reasoning models", "System One models"],
    ["Output", "fluent text", "chains of thought + answer", "typed values + probabilities"],
    ["Failure style", "sycophancy, confident hallucination, mode dropping", "slow, expensive", "wrong value, but with honest uncertainty attached"],
]
d.table(s, rows, x=0.55, y=1.75, w=12.2, col_widths=[1.9, 3.3, 3.0, 4.0], row_h=0.78, size=13.5)
d.text(s, [[("Mode dropping: ", {"bold": True}), ("preference training narrows the output distribution toward a favored style. "
        "Great for pleasant chat, bad for honest probabilities. RLCD's contract is the opposite: no text, just decisions whose "
        "probabilities are optimized against outcomes.", {})]],
       x=0.55, y=5.85, w=12.2, h=1.0, size=13.5, color=INK)
d.notes(s, "RLHF was co-invented by the founder, used for InstructGPT and ChatGPT. RLVR gave us reasoning models. "
           "RLCD is the third branch: reinforcement learning for calibrated decisions. "
           "The point is not that RLHF is bad; it is that human preference and machine trustworthiness are different optimization targets.")

# ---------------------------------------------------------------- 7b training story in pictures
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  How it is trained, in pictures")
d.title(s, "The official diagrams: three branches, and why not RLHF")
d.rect(s, 0.55, 1.7, 6.6, 3.5, fill=PAPER, line=LINE)
d.image(s, f"{ASSETS}/docs_training_paths.png", x=0.85, y=2.15, w=6.0)
d.text(s, "Pretrained language models branch three ways: RLHF to chatbots, RLVR to reasoning models, RLCD to decision models. Jev takes the highlighted path.",
       x=0.85, y=4.65, w=6.0, h=0.6, size=11.5, color=SLATE, line_spacing=1.15)
d.rect(s, 7.45, 1.7, 5.35, 3.5, fill=PAPER, line=LINE)
d.image(s, f"{ASSETS}/docs_mode_dropping.png", x=7.75, y=1.95, w=4.75)
d.text(s, "Mode dropping: preference training narrows a base model's distribution toward a favored style. Pleasant text, distorted probabilities.",
       x=7.75, y=4.65, w=4.75, h=0.6, size=11.5, color=SLATE, line_spacing=1.15)
d.text(s, [[("Why it matters for you: ", {"bold": True, "color": CLAY}),
            ("a model optimized to please cannot also be trusted to report honest uncertainty. "
             "RLCD's contract (no text, calibrated probabilities) is what makes the thresholds in Part 3 meaningful.", {})]],
       x=0.55, y=5.65, w=12.2, h=0.9, size=14)
d.text(s, "Diagrams: docs.typesafe.ai, AI primer", x=0.55, y=6.55, w=8, h=0.3, size=10.5, color=MUTED, italic=True)
d.notes(s, "Both figures come straight from TypeSafe's AI primer. Left: the three post-training branches. "
           "Right: mode dropping, the milder cousin of GAN mode collapse; RLHF rewards a style, which suppresses honest spread. "
           "If attendees want depth, the primer is a 10-minute read: docs.typesafe.ai/introduction/machine-learning-primer.")

# ---------------------------------------------------------------- 8 calibration
s = d.slide(FOOT)
d.kicker(s, "Part 1  |  The property that makes it usable")
d.title(s, "Calibration: probabilities you can price risk with")
d.image(s, f"{ASSETS}/calibration.png", x=0.55, y=1.8, w=5.1)
d.bullets(s, [
    ("The definition. ", "Across many predictions, outcomes given 0.2 happen about 20% of the time; outcomes given 0.8 happen about 80%."),
    ("Groups, not guarantees. ", "Calibration says nothing about one specific answer. It makes thresholds and expected-cost math meaningful."),
    ("The contrast. ", "An overconfident model's 0.9 means “probably”. A calibrated model's 0.9 is a number you can put in a formula next to the cost of being wrong."),
    ("The payoff. ", "“I don't know” becomes a usable signal: mid-range values route to review instead of silently guessing."),
], x=6.1, y=1.9, w=6.6, size=15, gap=13)
d.notes(s, "This is the slide to slow down on. Calibration is WHY thresholds in the rest of the workshop mean anything. "
           "Exercise 3 in notebook 03 shows how to test calibration on your own labeled data.")

# ---------------------------------------------------------------- 8b under the hood: transformer
s = d.slide(FOOT)
d.kicker(s, "Under the hood  |  1 of 5")
d.title(s, "The machine itself: a transformer, in one slide")
d.bullets(s, [
    ("Tokens to vectors. ", "Text is split into tokens (word pieces); each becomes a vector of numbers (an embedding). From here on, everything is matrix math."),
    ("A stack of attention blocks. ", "Each layer does two things: attention (every token looks at every other token and decides what matters to it) and an MLP (per-token transformation). Dozens of layers deep."),
    ("The parameters ", "are the matrices inside those blocks: the 'billions of knobs' from the foundations section. They are what training changes; the architecture never changes at inference time."),
    ("Backprop in one sentence. ", "Run forward, compute a loss (a single number for 'how wrong'), then the chain rule walks backward through every layer assigning blame to every knob, and the optimizer (Adam) nudges each one. Same machinery for EVERY recipe on the next slides; only the loss differs."),
], x=0.55, y=1.8, w=7.1, size=14.5, gap=12)
for i, (label, body) in enumerate([
    ("tokens", "“My card was\ncharged twice”"),
    ("embeddings", "vectors, one\nper token"),
    ("N x blocks", "attention + MLP,\nrepeated"),
    ("output head", "what comes out\n(next slides)"),
]):
    y = 1.85 + i * 1.22
    fill, tc = (INK, CREAM) if label == "N x blocks" else (PAPER, INK)
    d.rect(s, 8.15, y, 4.5, 1.02, fill=fill, line=LINE if fill == PAPER else None)
    d.text(s, label, x=8.4, y=y + 0.1, w=1.9, h=0.4, size=13, bold=True, color=tc)
    d.text(s, body, x=10.3, y=y + 0.12, w=2.25, h=0.85, size=10.5,
           color=SLATE if fill == PAPER else RGBColor(0xCF, 0xCB, 0xC2), line_spacing=1.1)
    if i < 3:
        d.rect(s, 10.35, y + 1.04, 0.06, 0.18, fill=CORAL, line=None, round_=False)
d.notes(s, "This section exists for the 'how does it REALLY work' crowd; it can be skipped for non-technical rooms. "
           "Pitch at the whiteboard level: embeddings, attention as 'every token votes on what to look at', MLPs, and backprop as blame assignment via the chain rule. "
           "The punchline to set up now: every recipe that follows (pretraining, RLHF, RLVR, RLCD) uses this exact machine and this exact backprop; "
           "the entire difference lives in the output head and the loss function.")

# ---------------------------------------------------------------- 8c under the hood: decode loop
s = d.slide(FOOT)
d.kicker(s, "Under the hood  |  2 of 5")
d.title(s, "Why LLMs are slow: generation is a serial loop")
d.bullets(s, [
    ("One forward pass per output token. ", "An LLM produces text by predicting one token, appending it, and running again. A 500-token answer is 500 sequential passes. The KV cache saves recomputation, not serialism."),
    ("Thinking costs tokens. ", "Reasoning models get their quality from long chains of thought, which are generated text: more output tokens, more serial passes, more seconds, more dollars."),
    ("So output is the expensive axis. ", "For LLMs, latency and cost scale with how much the model SAYS. That is the axis Jev deletes."),
], x=0.55, y=1.8, w=6.6, size=15, gap=13)
d.code(s, 'context = prompt\nwhile not done:          # SERIAL: cannot parallelize\n    logits = model(context)   # full forward pass\n    token  = sample(logits)   # ONE token\n    context += token          # and again...\n\n# 500-token answer = 500 passes\n# "thinking" = even more passes before the answer',
       x=7.5, y=1.85, w=5.3, h=2.9, title="the autoregressive decode loop")
d.text(s, [[("Contrast, next slides: ", {"bold": True, "color": CLAY}),
            ("a decision does not need to be SAID one token at a time. It can be read off in a single evaluation.", {})]],
       x=7.5, y=5.1, w=5.3, h=0.9, size=14, line_spacing=1.2)
d.notes(s, "The decode loop is the single most important piece of systems intuition in this section. "
           "Every token costs a full trip through the network, and tokens are emitted strictly one after another. "
           "Speculative decoding and batching help throughput, not the fundamental serial dependency per stream. "
           "Reasoning quality bought with thinking tokens is quality bought with wall-clock and money.")

# ---------------------------------------------------------------- 8d under the hood: RLHF engineering
s = d.slide(FOOT)
d.kicker(s, "Under the hood  |  3 of 5")
d.title(s, "RLHF at the engineering level")
rows = [
    ["Piece", "What it is", "The loss / signal"],
    ["Reward model", "the same transformer with a scalar output head: text in, one 'how much will a human like this' number out", "pairwise loss on human A/B picks (Bradley-Terry): score the preferred answer higher"],
    ["Policy (the chatbot)", "the model being trained; it generates full answers (rollouts) during training", "maximize reward-model score via policy gradients (PPO)"],
    ["KL penalty", "a tether to the original reference model", "punishes drifting too far, so the policy cannot collapse into reward-hacking gibberish"],
]
d.table(s, rows, x=0.55, y=1.75, w=12.2, col_widths=[2.0, 5.3, 4.9], row_h=0.92, size=12.5)
d.text(s, [[("Note what the gradient pushes toward: ", {"bold": True}),
            ("whatever the reward model scores highly. The reward model learned human taste, so the gradient literally optimizes "
             "'sound good to people'. Truthfulness only matters where the taste model happens to notice. Same backprop as pretraining; "
             "the loss is the only thing that changed, and the loss is approval.", {})]],
       x=0.55, y=5.5, w=12.2, h=1.1, size=14, line_spacing=1.25)
d.notes(s, "For a sharp audience, add: the policy update is PPO with clipped objectives; rollouts are expensive because each one is a full "
           "autoregressive generation; and the KL term is why chat models feel 'pulled' toward their base style. "
           "The teaching point stays simple: reward = predicted human approval, so every failure mode of approval (confidence theater, sycophancy) "
           "gets optimized IN.")

# ---------------------------------------------------------------- 8e under the hood: RLCD engineering
s = d.slide(FOOT)
d.kicker(s, "Under the hood  |  4 of 5")
d.title(s, "RLCD at the engineering level: different head, different loss")
d.bullets(s, [
    ("Documented by TypeSafe: ", "Jev never decodes text. It returns probability distributions over the options YOU supplied, ingests the state once, and evaluates every question in parallel. Trained with RLCD so the probabilities are calibrated."),
    ("The standard engineering for that contract: ", "replace the next-token head with scoring over the supplied answer space: each option or level gets a score, softmax turns scores into the distribution you receive. No decode loop exists."),
    ("The loss is a proper scoring rule ", "(think log loss or Brier) against what ACTUALLY happened: probability quality is not a side effect, it IS the training objective. Backprop and the transformer underneath are unchanged."),
    ("Honest labeling: ", "TypeSafe has not published Jev's internals. 'Documented' above is from their docs and primer; 'standard engineering' is how this model class is built, flagged as inference."),
], x=0.55, y=1.8, w=7.0, size=14, gap=12)
d.rect(s, 7.95, 1.8, 4.85, 4.5, fill=PAPER, line=LINE)
d.text(s, "LLM head vs decision head", x=8.2, y=2.0, w=4.4, h=0.35, size=14, bold=True, font=SERIF)
d.text(s, "LLM:  state -> [transformer] ->\n  logits over 50,000 vocabulary\n  tokens -> decode loop,\n  token by token\n\nJev:  state + your options ->\n  [transformer] -> scores over\n  YOUR 3 options -> softmax ->\n  done. One evaluation,\n  a handful of numbers out.",
       x=8.2, y=2.5, w=4.4, h=2.7, size=11.5, font="Menlo", color=INK, line_spacing=1.2)
d.text(s, "The answer space shrinks from 'all possible text' to 'the options you supplied'. That is where the speed, the price, and the impossibility of malformed output all come from.",
       x=8.2, y=5.35, w=4.4, h=0.9, size=11, color=SLATE, italic=True, line_spacing=1.12)
d.notes(s, "The one-slide answer to 'how is backpropagation different': it is NOT. Same transformer, same chain rule, same Adam. "
           "What differs is the output head (score the supplied options instead of 50k vocabulary logits) and the loss "
           "(proper scoring rule against outcomes instead of next-token cross-entropy or human approval). "
           "Be scrupulous about the honesty bullet: internals are unpublished; we teach the documented contract plus standard practice for the class, labeled as such.")

# ---------------------------------------------------------------- 8f under the hood: proper scoring + speed
s = d.slide(FOOT)
d.kicker(s, "Under the hood  |  5 of 5")
d.title(s, "Why honesty wins, and why it comes back in 100 ms")
d.image(s, f"{ASSETS}/proper_scoring.png", x=0.55, y=1.8, w=5.9)
d.text(s, "If an event truly happens 80% of the time, expected loss is minimized ONLY by reporting 0.8. Overclaiming 0.99 costs more. Calibration is the minimum of the objective, not a bolt-on.",
       x=0.55, y=5.9, w=5.9, h=0.8, size=12, color=SLATE, italic=True, line_spacing=1.15)
d.bullets(s, [
    ("No decode loop. ", "The judgment happens inside the forward evaluation; there is nothing to emit token by token."),
    ("Tiny output. ", "A few numbers per question instead of hundreds of tokens. This is why output is literally free: there is almost no decode phase to bill."),
    ("One state, N questions in parallel. ", "The state is ingested once; every question is evaluated against it simultaneously (documented). An extra question adds tokens, not a round trip."),
    ("The bill follows the architecture. ", "LLM cost scales with what it says; Jev cost scales with what it reads. 500 serial passes vs roughly one evaluation is the whole latency story."),
], x=6.85, y=1.9, w=6.0, size=13.5, gap=11)
d.notes(s, "Left: the mathematical reason calibration emerges, with two truths plotted; the dot is the minimum. "
           "Right: the systems reason for the speed and the free output tokens. Close the section by connecting back: "
           "the decode loop slide showed where LLM latency lives; Jev's contract deletes that axis entirely, "
           "and the pricing page (output free) is the commercial shadow of that architecture choice.")

# ---------------------------------------------------------------- 8g under the hood: recap table
s = d.slide(FOOT)
d.kicker(s, "Under the hood  |  Recap")
d.title(s, "One machine, four objectives")
rows = [
    ["", "Pretraining", "RLHF", "RLVR", "RLCD (Jev)"],
    ["Training data", "internet text", "human A/B preferences", "checkable problems", "questions with known outcomes"],
    ["Loss / reward", "next-token cross-entropy", "reward model score + KL tether", "did the answer verify?", "proper scoring rule on outcomes"],
    ["Gradient pushes toward", "plausible continuation", "human approval", "correct final answers", "honest probabilities"],
    ["Output at inference", "text", "text", "text + chains of thought", "distributions over your options"],
    ["Characteristic failure", "aimless", "confident hallucination, sycophancy", "slow and expensive", "wrong but honestly uncertain"],
]
d.table(s, rows, x=0.55, y=1.75, w=12.2, col_widths=[2.2, 2.4, 2.7, 2.3, 2.6], row_h=0.78, size=12)
d.text(s, "Same transformer. Same backpropagation. The loss function is the product decision.",
       x=0.55, y=6.6, w=12.2, h=0.4, size=13.5, color=CLAY, italic=True)
d.notes(s, "The recap students photograph. If one sentence survives the section, make it the italic one at the bottom: "
           "the four model families on this table differ by objective, not machinery. "
           "That also explains why Jev cannot write prose (nothing in its loop ever rewarded prose) and why an RLHF chatbot "
           "cannot give you calibrated probabilities (nothing in its loop ever rewarded them).")

# ---------------------------------------------------------------- 9 anatomy
s = d.slide(FOOT)
d.kicker(s, "Part 2  |  The API")
d.title(s, "One endpoint. Three fields in, three out.")
d.code(s, '{\n  "model": "jev-latest",\n  "state": "Help! Payouts failing for 3 days.",\n  "questions": {\n    "is_urgent": {\n      "type": "noul",\n      "instructions": "Does this convey urgency?"\n    },\n    "department": {\n      "type": "choice",\n      "instructions": "Which team handles this?",\n      "criteria": {\n        "billing":   "Payments, refunds",\n        "technical": "Bugs, outages",\n        "sales":     "Pricing, accounts"\n      }\n    }\n  }\n}',
       x=0.55, y=1.75, w=6.0, h=4.9, title="POST https://api.typesafe.ai/v1/systemone")
d.code(s, '{\n  "model": "jev-1.13.0",\n  "answers": {\n    "is_urgent": {\n      "type": "noul",\n      "noul": 0.95\n    },\n    "department": {\n      "type": "choice",\n      "choice": "billing",\n      "probabilities": {\n        "billing": 0.88,\n        "technical": 0.12,\n        "sales": 0.0\n      },\n      "confidence": 0.81\n    }\n  },\n  "usage": {"input_tokens": 318, "output_tokens": 34}\n}',
       x=6.85, y=1.75, w=6.0, h=4.9, title="response (authorization: Bearer $TYPESAFE_API_KEY)")
d.notes(s, "Point out: question IDs are chosen by you and never sent to the model, so instructions must contain the full question. "
           "The response model field is the versioned ID that actually answered: log it. "
           "Python SDK: pip install typesafe-sdk, then client.system_one(state=..., questions=...) with typed Choice/Score/Noul objects.")

# ---------------------------------------------------------------- 10 primitives overview
s = d.slide(FOOT)
d.kicker(s, "Part 2  |  The primitives")
d.title(s, "Four question types, four shapes of answer")
rows = [
    ["Type", "Answers", "Returns", "Maps onto"],
    ["Choice", "which of these options?", "choice + probability per option + confidence", "a switch over code paths"],
    ["Score", "which level on my rubric?", "score (can land between levels) + probabilities + confidence", "a threshold or a ranking"],
    ["Noul", "is this true?", "one number: probability of yes (0 to 1)", "an if statement"],
    ["Box  (preview)", "where is it in this image?", "four fractional edges + confidence", "a crop or an overlay"],
]
d.table(s, rows, x=0.55, y=1.75, w=12.2, col_widths=[1.7, 3.1, 4.6, 2.8], row_h=0.8, size=13.5)
d.text(s, [[("Choosing: ", {"bold": True, "color": CLAY}),
            ("prefer the type whose answer your code can act on directly. And the rule that pays for the workshop: "
             "ask every question you might need in ONE request. Questions are evaluated in parallel; "
             "an extra question barely moves latency and costs only its own tokens.", {})]],
       x=0.55, y=5.9, w=12.2, h=1.0, size=14.5)
d.notes(s, "Up to 255 options per Choice, 2 to 10 levels per Score, Noul criteria optional, Box needs jev-preview plus the images header. "
           "No limit on question count per request; the bound is context size.")

# ---------------------------------------------------------------- 10b scenario: the ticket, answered
s = d.slide(FOOT)
d.kicker(s, "Scenario 1  |  Text")
d.title(s, "Our 9:04 ticket, as one Jev call")
d.rect(s, 0.55, 1.75, 4.6, 2.5, fill=PAPER, line=LINE)
d.text(s, "state  (the ticket, verbatim)", x=0.8, y=1.92, w=4.1, h=0.3, size=11, color=MUTED, font="Menlo")
d.text(s, "“Our API integration started returning 500 errors on every request about 20 minutes ago, and we can't process any customer orders until this is fixed.”",
       x=0.8, y=2.3, w=4.1, h=1.8, size=12.5, color=INK, font=SERIF, italic=True, line_spacing=1.25)
rows = [
    ("Choice", "Which team should handle this?", "technical", "confidence 1.00", SAGE),
    ("Score", "How frustrated does the customer appear?", "0.67 of 2", "leaning 'frustrated but civil'", SLATE),
    ("Noul", "The message conveys urgency", "0.99", "about as yes as it gets", CORAL),
]
y = 1.75
for qtype, question, answer, gloss, color in rows:
    d.rect(s, 5.45, y, 7.35, 0.76, fill=PAPER, line=LINE)
    d.chip(s, qtype, x=5.65, y=y + 0.2, w=0.95, fill=color, size=11)
    d.text(s, question, x=6.75, y=y + 0.09, w=3.6, h=0.6, size=11.5, color=INK, line_spacing=1.05)
    d.text(s, answer, x=10.45, y=y + 0.09, w=2.2, h=0.32, size=13, bold=True, color=INK)
    d.text(s, gloss, x=10.45, y=y + 0.42, w=2.25, h=0.3, size=9.5, color=MUTED, italic=True)
    y += 0.9
d.text(s, [[("One request. 428 input tokens. $0.000018. ", {"bold": True}),
            ("The support lead's two-second read is now a programmable reflex that runs on every ticket, "
             "every time, with its uncertainty attached. (Answers above are the documented quickstart output for this exact ticket.)", {})]],
       x=0.55, y=4.55, w=12.2, h=1.0, size=15, line_spacing=1.25)
d.text(s, "Walk the mapping out loud: the ticket is the state, each thing the human 'just knew' became one typed question, and each answer is a value code can branch on.",
       x=0.55, y=5.75, w=12.2, h=0.65, size=13, color=CLAY, italic=True)
d.notes(s, "This is the payoff of the opening story: same ticket, same three judgments, now as an API call. "
           "Point at the chips left to right: a Choice for routing, a Score for tone, a Noul for urgency. "
           "Then the economics line: at $0.000018 per ticket, nobody will ever ration this. Notebook 01 runs this exact call.")

# ---------------------------------------------------------------- 11 choice
s = d.slide(FOOT)
d.kicker(s, "Part 2  |  Primitive 1 of 4")
d.title(s, "Choice: one option from a defined set")
d.bullets(s, [
    ("criteria ", "is a map of option name to description. Both are sent to the model; write descriptions that separate neighbors. Use None when the name is enough."),
    ("Always add an escape hatch. ", "An “other / none of the above” option gives honest probability somewhere to go."),
    ("The distribution is the feature. ", "An ambiguous ticket splits probability; code can CC the runner-up team when its share is over 0.25."),
    ("Structured descriptions ", "(what / not_for / examples) sharpen confusable options."),
], x=0.55, y=1.8, w=6.3, size=15, gap=12)
d.image(s, f"{ASSETS}/choice_dist.png", x=7.1, y=1.85, w=5.7)
d.code(s, 'Choice(\n  instructions="Which team should handle this?",\n  criteria={\n    "returns":  "Exchanges, wrong or damaged items",\n    "shipping": "Delivery status, delays, lost packages",\n    "billing":  "Charges, invoices, payment problems",\n  },\n)',
       x=7.1, y=5.0, w=5.7, h=1.75)
d.notes(s, "The chart is a real documented response: wrong size AND double charge belongs to two teams, and the split says so. "
           "Confidence 0.42 is the model being honest, not failing. Notebook 02 reproduces this live.")

# ---------------------------------------------------------------- 12 score
s = d.slide(FOOT)
d.kicker(s, "Part 2  |  Primitive 2 of 4")
d.title(s, "Score: a position on a rubric you define")
d.bullets(s, [
    ("criteria ", "is an ordered list, low to high: 2 to 10 levels. A level's number is its array position."),
    ("score is the probability-weighted mean ", "of level numbers, so it can land between levels: 1*0.57 + 2*0.43 = 1.43."),
    ("Describe situations, not degrees. ", "“Broken, but a workaround exists” beats “moderately severe”. Levels that are bare numbers return noise (live anti-example in notebook 02)."),
    ("One dimension per question. ", "“Punctual and smart” is two questions; split and weight in code."),
    ("Normalize before combining: ", "divide by len(criteria) - 1."),
], x=0.55, y=1.8, w=6.3, size=15, gap=11)
d.image(s, f"{ASSETS}/score_dist.png", x=7.1, y=1.95, w=5.7)
d.text(s, "Same score can hide different distributions: 1.0 may be “all on level 1” or “half on 0, half on 2”. Read probabilities and confidence alongside score.",
       x=7.1, y=5.6, w=5.7, h=0.9, size=12.5, color=SLATE, italic=True)
d.notes(s, "The Safari bug is the teaching example: a workaround exists for most users but not all, so the model splits 0.57/0.43 "
           "and the fractional score ranks it between levels. Python SDK keys score probabilities and legend by int.")

# ---------------------------------------------------------------- 13 noul
s = d.slide(FOOT)
d.kicker(s, "Part 2  |  Primitive 3 of 4")
d.title(s, "Noul: the probability that a statement is true")
d.bullets(s, [
    ("One number. ", "Near 1: strong yes. Near 0: strong no. Near 0.5: the model is telling you it cannot tell. No separate confidence; with two outcomes the value says it all."),
    ("Phrase high = yes. ", "“Is the message free of personal data?” inverts your thresholds."),
    ("One proposition per Noul. ", "“Angry AND wants a refund” is two questions."),
    ("It is not a dial. ", "The value is probability of yes, never a measure of degree. Measuring degree is a Score's job."),
    ("Optional criteria ", "pin down a subtle yes/no boundary with explicit true and false descriptions."),
], x=0.55, y=1.8, w=5.6, size=14.5, gap=11)
d.image(s, f"{ASSETS}/noul_ladder.png", x=6.4, y=1.95, w=6.4)
d.notes(s, "The ladder is recorded jev-1.13.0 output from the docs, reproduced live in notebook 02. "
           "The middle band is the design feature: 'Are you a bot?' hints without asking and lands at 0.40; "
           "production code sends that band to a person. Threshold placement follows cost of error: raise it when false yes is expensive.")

# ---------------------------------------------------------------- 14a images
s = d.slide(FOOT)
d.kicker(s, "Part 2  |  Preview capability")
d.title(s, "Images: pictures go anywhere text goes")
d.bullets(s, [
    ("Placement: ", "an image can sit in the state, inside a question's instructions, or as the criteria themselves: define Choice options by example pictures."),
    ("Mechanics: ", "list each image once in the request's assets map under a reference string; write the reference wherever the image belongs. The SDKs do this for you: Image(Path(\"door.jpg\"))."),
    ("Opt-in and experimental: ", "every image request needs the header TypeSafe-Danger-Zone-Images: true. “Dreamer-ready”: prototypes yes, production not yet."),
    ("Limits: ", "PNG/JPEG only, 16 MiB per file, sides 280 to 1568 px, 32 MiB per request. Billed as ordinary input tokens."),
    ("Field report from building this deck: ", "image calls run seconds, not milliseconds; raise the SDK timeout or the default 10 s cap plus retries will stack into minutes."),
], x=0.55, y=1.8, w=6.9, size=14, gap=11)
d.rect(s, 7.75, 1.75, 5.05, 4.95, fill=PAPER, line=LINE)
d.image(s, f"{ASSETS}/docs_image_anatomy.png", x=8.25, y=1.95, w=4.05)
d.text(s, "Official diagram: one request, three image placements (state, instructions, criteria), all declared in assets.",
       x=8.0, y=6.15, w=4.6, h=0.5, size=11, color=SLATE, line_spacing=1.12, italic=True)
d.notes(s, "The anatomy diagram is from docs.typesafe.ai/images: door.jpg is the state, badge.jpg lives inside a Noul's instructions, "
           "thumb.jpg defines a Choice option. References are plain strings matched anywhere in request text, so use UUIDs in production. "
           "Jev 1.13 and 1.14 both accept images; Box questions need 1.14.")

# ---------------------------------------------------------------- 14b box
s = d.slide(FOOT)
d.kicker(s, "Part 2  |  Primitive 4 of 4, preview")
d.title(s, "Box: where is it in the image?")
d.bullets(s, [
    ("What it returns: ", "the smallest rectangle around the target: four edges (top, bottom, left, right) as fractions of image size, plus confidence. Resolution-independent by construction."),
    ("Needs Jev 1.14: ", "send model=\"jev-preview\" plus the images header. Box takes no criteria; instructions need not be a question: “the coffee mug in `photo`” is enough."),
    ("There is no “not found”. ", "A Box always returns edges, even for an absent target. Pair it with a Noul (“Is there a mug in `photo`?”) and ignore the box when the Noul is low."),
    ("Low confidence has remedies: ", "re-ask on a crop, pad the box before cropping, or verify each edge with a Noul (“does the mug continue past the left edge?”)."),
], x=0.55, y=1.8, w=6.5, size=14, gap=11)
d.rect(s, 7.45, 1.75, 5.35, 3.15, fill=PAPER, line=LINE)
d.image(s, f"{ASSETS}/docs_box_edges.png", x=8.25, y=1.92, w=3.75)
d.text(s, "Official diagram: edges as fractions from the top-left corner.", x=7.7, y=4.52, w=4.9, h=0.35, size=10.5, color=SLATE, italic=True)
d.image(s, f"{ASSETS}/box_annotated.png", x=7.45, y=5.0, w=2.5)
d.text(s, "Our live test (notebook 02): Jev 1.14 boxed the red circle; vertical edges accurate, horizontal loose, confidence honestly reported at 0.24.",
       x=10.1, y=5.1, w=2.7, h=1.7, size=11, color=SLATE, line_spacing=1.15, italic=True)
d.notes(s, "Demo moment: notebook 02 generates the scene with PIL, calls jev-preview, and draws the returned box. "
           "The loose horizontal edges plus 0.24 confidence are the honest-preview story: the model knows when it is unsure, "
           "and the docs give three concrete remedies. Edge-check benchmark from the docs: on 36 test crops, per-edge Nouls caught 30 of 36 cut-offs.")

# ---------------------------------------------------------------- 14c scenario: the doorbell
s = d.slide(FOOT)
d.kicker(s, "Scenario 2  |  Image")
d.title(s, "The doorbell camera: four questions about one photo")
d.image(s, f"{ASSETS}/porch_annotated.png", x=0.55, y=1.8, w=5.2)
d.text(s, "The green box is Jev's answer, drawn by our code: left 0.50, top 0.67, right 0.70, bottom 0.87.",
       x=0.55, y=5.85, w=5.2, h=0.6, size=11.5, color=SLATE, italic=True)
rows = [
    ("Noul", "Is there a person in `porch`?", "0.05", "nobody there: do not ping the phone"),
    ("Noul", "Is there a delivered package in `porch`?", "0.97", "notify: 'package delivered'"),
    ("Choice", "Is the door open or closed?", "closed 0.99", "no alert needed"),
    ("Box", "the parcel on the mat in `porch`", "see photo", "confidence 0.85: crop it for the thumbnail"),
]
y = 1.8
for qtype, question, answer, action in rows:
    d.rect(s, 6.1, y, 6.7, 0.78, fill=PAPER, line=LINE)
    d.chip(s, qtype, x=6.3, y=y + 0.21, w=0.95, fill=INK, size=11)
    d.text(s, question, x=7.4, y=y + 0.08, w=3.0, h=0.65, size=11, color=INK, line_spacing=1.05)
    d.text(s, answer, x=10.5, y=y + 0.08, w=2.1, h=0.3, size=12.5, bold=True, color=INK)
    d.text(s, action, x=10.5, y=y + 0.4, w=2.2, h=0.35, size=9, color=MUTED, italic=True)
    y += 0.92
d.text(s, [[("We ran this exact call while building this deck ", {"bold": True}),
            ("(jev-1.14.0, one request, 1,229 input tokens, about $0.00005). Four judgments about one frame, "
             "and the fourth answer is a location the code can crop to. Every doorbell, every frame, for less than a cent a day.", {})]],
       x=0.55, y=6.3, w=12.2, h=0.7, size=13, line_spacing=1.2)
d.notes(s, "The image twin of the ticket scenario. Walk the rows as the product behavior they become: no person, so no 3am ping; "
           "package at 0.97, so send the delivery notification; door closed, so nothing to flag; Box at 0.85 confidence, so crop the thumbnail. "
           "Ask the room: what threshold would YOU demand on 'person at door' before waking someone at 3am? There is no right answer; "
           "there is only the cost of a false ping vs a missed visitor. That is next section's topic. "
           "Reminder: images need the danger-zone header and jev-preview for Box; notebook 02 has the runnable version.")

# ---------------------------------------------------------------- 14d quiz: pick the primitive
s = d.slide(FOOT)
d.kicker(s, "Quick check  |  You call it")
d.title(s, "Which primitive would you reach for?")
quiz = [
    ("A", "“Does this outbound email contain a password, API key, or other secret?”"),
    ("B", "“Which of our 40 product categories does this new listing belong to?”"),
    ("C", "“How complete is this bug report, from 'just says broken' to 'steps plus environment'?”"),
    ("D", "“Where is the signature on this scanned contract, and is it even signed?”"),
]
xs = [0.55, 6.85, 0.55, 6.85]
ys = [1.8, 1.8, 3.75, 3.75]
for (label, q), x, y in zip(quiz, xs, ys):
    d.rect(s, x, y, 5.95, 1.75, fill=PAPER, line=LINE)
    d.chip(s, label, x=x + 0.22, y=y + 0.22, w=0.42, fill=CORAL, size=13)
    d.text(s, q, x=x + 0.85, y=y + 0.2, w=4.9, h=1.4, size=14, color=INK, font=SERIF, italic=True, line_spacing=1.2)
d.divider(s, 0.55, 5.85, 12.2)
d.text(s, [[("Answers  ", {"bold": True, "color": CLAY}),
            ("A: Noul (threshold it; phrase so high = yes).  B: Choice with a none_of_the_above escape option.  "
             "C: Score with described situations as levels.  D: a Box paired with a Noul, because a Box always returns edges, even on an unsigned page.", {})]],
       x=0.55, y=6.05, w=12.2, h=0.7, size=12.5, color=INK, line_spacing=1.2)
d.notes(s, "Run it as a show of hands per card before revealing the answer line. A and B go fast. "
           "C is the one people get wrong (many say Noul: 'is it complete?'); use it to re-land 'Noul is probability of yes, not a dial'. "
           "D tests whether the Box-has-no-not-found gotcha stuck. Two minutes, big retention payoff.")

# ---------------------------------------------------------------- 15 probability vs confidence
s = d.slide(FOOT)
d.kicker(s, "Part 3  |  The two numbers")
d.title(s, "Probability tells you what. Confidence tells you whether to act.")
d.rect(s, 0.55, 1.75, 6.0, 2.3, fill=PAPER, line=LINE)
d.text(s, "probabilities", x=0.8, y=1.95, w=5.5, h=0.35, size=15, bold=True, color=CORAL)
d.text(s, "The answer's full distribution over YOUR options or levels. Sums to 1. What the model believes.",
       x=0.8, y=2.4, w=5.5, h=0.8, size=13.5, line_spacing=1.15)
d.text(s, "Never a value outside the schema you supplied.", x=0.8, y=3.35, w=5.5, h=0.5, size=12.5, color=SLATE, italic=True)
d.rect(s, 6.85, 1.75, 6.0, 2.3, fill=PAPER, line=LINE)
d.text(s, "confidence", x=7.1, y=1.95, w=5.5, h=0.35, size=15, bold=True, color=SLATE)
d.text(s, "One 0-to-1 statistic computed from that distribution's shape: 1 when probability piles on one outcome, 0 when spread evenly.",
       x=7.1, y=2.4, w=5.5, h=0.8, size=13.5, line_spacing=1.15)
d.text(s, "A sensible default, not magic: the formulas are published.", x=7.1, y=3.35, w=5.5, h=0.5, size=12.5, color=SLATE, italic=True)
d.text(s, "The published formulas (verified against the API in notebook 03):", x=0.55, y=4.35, w=12, h=0.4, size=14, bold=True)
rows = [
    ["Type", "Formula", "Intuition"],
    ["Choice", "(p_max - 1/n) / (1 - 1/n)", "how far the winner sits above an even split"],
    ["Score", "1 - (prob-weighted distance from top level) / (even-spread distance)", "nearby probability hurts less than far-away probability"],
    ["Noul", "none returned; use |2p - 1| if you need one", "distance from a coin flip"],
]
d.table(s, rows, x=0.55, y=4.85, w=12.2, col_widths=[1.4, 6.2, 4.6], row_h=0.52, size=12.5)
d.notes(s, "Key distinction for Scores: probability split across ADJACENT levels keeps more confidence than the same split across opposite ends; "
           "a Choice treats all options as unordered. Alternatives worth trying: top probability, and top-to-second ratio. "
           "Anti-pattern from TypeSafe's own guide: if you only ever take the best option, you do not need a confidence threshold at all.")

# ---------------------------------------------------------------- 16 three paths
s = d.slide(FOOT)
d.kicker(s, "Part 3  |  Using it")
d.title(s, "Three paths, and thresholds that scale with risk")
rows = [
    ["Confidence", "Behavior", "Example"],
    ["high", "act automatically", "route the ticket, show the balance"],
    ["medium", "proceed with caution", "ask the user to confirm, flag for review"],
    ["low", "do not act", "human agent, clarifying question, fallback system"],
]
d.table(s, rows, x=0.55, y=1.75, w=7.3, col_widths=[1.5, 2.6, 3.2], row_h=0.62, size=13.5)
d.code(s, 'a = r.choices["intent"]\n\nif a.confidence < 0.5:\n    route_to_human()            # genuinely unsure\nelif a.choice == "check_balance":\n    show_balance()              # low stakes: 0.5 ok\nelif a.choice == "approve_transfer":\n    if a.confidence > 0.85:     # high stakes:\n        confirm_then_execute()  #   high bar\n    else:\n        ask_user_to_confirm()',
       x=8.15, y=1.75, w=4.65, h=3.6)
d.text(s, [[("One system, different gates per action. ", {"bold": True}),
            ("Reading a balance at 0.6 risks a wrong screen; approving a transfer at 0.6 risks money. "
             "The risk tolerance lives in code, in named constants, reviewable in a pull request. "
             "Start conservative, test against your data, adjust.", {})]],
       x=0.55, y=4.5, w=7.3, h=1.6, size=14.5, line_spacing=1.2)
d.notes(s, "This is the single most transferable pattern of the workshop. Notebook 03 runs this router over live utterances including "
           "'approve it I guess? actually wait' which lands in the confirm band exactly as designed.")

# ---------------------------------------------------------------- 16b quiz: confidence 0.55
s = d.slide(FOOT)
d.kicker(s, "Quick check  |  Same number, different answer")
d.title(s, "The model says: approve_transfer, confidence 0.55. Now what?")
options = [
    ("Approve it", "the model did pick approve_transfer, after all"),
    ("Ask the user to confirm", "act, but put a human click in the loop"),
    ("Route to a person", "0.55 is barely better than a shrug"),
]
for i, (t, body) in enumerate(options):
    x = 0.55 + i * 4.18
    d.rect(s, x, 1.8, 3.95, 1.55, fill=PAPER, line=LINE)
    d.chip(s, str(i + 1), x=x + 0.2, y=2.0, w=0.38, fill=SLATE, size=13)
    d.text(s, t, x=x + 0.72, y=2.0, w=3.1, h=0.4, size=14.5, bold=True, font=SERIF)
    d.text(s, body, x=x + 0.2, y=2.5, w=3.55, h=0.7, size=12, color=SLATE, italic=True, line_spacing=1.12)
d.rect(s, 0.55, 3.75, 12.2, 1.6, fill=RGBColor(0xEA, 0xDF, 0xD4), line=None)
d.text(s, [[("Trick question: the number alone cannot tell you. ", {"bold": True, "color": CLAY}),
            ("The same 0.55 means 'go ahead' for showing a balance (worst case: a wrong screen) and 'absolutely not' for moving money "
             "(worst case: an irreversible transfer). Thresholds are priced by the cost of being wrong, per action. "
             "For a transfer, 0.55 clears no sane bar: option 2 or 3, never 1.", {})]],
       x=0.8, y=3.95, w=11.7, h=1.3, size=14, line_spacing=1.25)
d.text(s, "Second round, same number: choice = check_balance, confidence 0.55. Hands up for 'just show it'. (Correct: yes. Worst case is a re-ask.)",
       x=0.55, y=5.6, w=12.2, h=0.6, size=13, color=CLAY, italic=True)
d.notes(s, "Poll the room on the three cards first; you will get a spread, which is the point. "
           "The reveal is that stakes, not confidence, choose the behavior; confidence only says how sure the model is, never whether that is sure ENOUGH. "
           "The second round (check_balance at the same 0.55) cements it: same number, opposite decision, because the downside is trivial.")

# ---------------------------------------------------------------- 16c scale story
s = d.slide(FOOT)
d.kicker(s, "Scenario 3  |  Scale")
d.title(s, "9:00 am, Monday: 500 tickets in the queue")
# ticket grid -> jev -> lanes
for i in range(24):
    col, row = i % 6, i // 6
    d.rect(s, 0.75 + col * 0.62, 1.95 + row * 0.62, 0.5, 0.5, fill=PAPER, line=LINE)
d.text(s, "500 tickets\n(24 drawn)", x=0.75, y=4.55, w=3.6, h=0.6, size=11, color=MUTED, italic=True)
d.rect(s, 4.75, 2.6, 0.5, 0.06, fill=CORAL, line=None, round_=False)
d.rect(s, 5.4, 2.0, 2.3, 1.3, fill=INK, line=None)
d.text(s, "Jev", x=5.4, y=2.25, w=2.3, h=0.4, size=16, bold=True, color=CREAM, align=PP_ALIGN.CENTER, font=SERIF)
d.text(s, "5 questions each,\none call per ticket", x=5.4, y=2.7, w=2.3, h=0.5, size=10, color=RGBColor(0xCF, 0xCB, 0xC2), align=PP_ALIGN.CENTER)
d.rect(s, 7.85, 2.6, 0.5, 0.06, fill=CORAL, line=None, round_=False)
lanes = [("technical", SAGE, "187"), ("billing", SLATE, "154"), ("sales", MUTED, "121"), ("human review", CORAL, "38")]
for i, (lane, color, n) in enumerate(lanes):
    y = 1.85 + i * 0.78
    d.rect(s, 8.5, y, 4.3, 0.62, fill=PAPER, line=LINE)
    d.chip(s, lane, x=8.7, y=y + 0.14, w=1.6, fill=color, size=10.5)
    d.text(s, n + " tickets", x=10.5, y=y + 0.14, w=2.1, h=0.35, size=12, color=INK, bold=True)
d.text(s, "illustrative split; the review lane is every low-confidence answer, surfaced instead of guessed",
       x=8.5, y=5.0, w=4.3, h=0.55, size=10, color=MUTED, italic=True)
d.bullets(s, [
    ("The bill: ", "500 calls x ~500 tokens = 250k tokens = about one cent. The entire Monday-morning queue, triaged with uncertainty attached, for $0.01."),
    ("The time: ", "at ~0.3 s per call, under 3 minutes sequentially; seconds with a small concurrent pool (the Twitch cookbook runs 8-wide)."),
    ("The alternative you were pricing: ", "an LLM pass over 500 tickets costs dollars and minutes, so you ration it. At Jev prices, rationing stops being a design constraint."),
], x=0.55, y=5.35, w=12.2, size=13, gap=8)
d.notes(s, "This is the economics slide told as a morning. The grid-to-lanes picture is the whole architecture: "
           "a loop in code, one call per item, lanes decided by thresholds, and the honest 38 that go to a person. "
           "Numbers are illustrative but the arithmetic is real and runs in notebook 04. "
           "Segue: so what do speed and price actually look like against LLMs? Next slide, the chart.")

# ---------------------------------------------------------------- 17 speed and price
s = d.slide(FOOT)
d.kicker(s, "Part 4  |  Properties that change architecture")
d.title(s, "Fast enough for request paths, cheap enough for everywhere")
d.image(s, f"{ASSETS}/price_compare.png", x=0.55, y=1.8, w=7.2)
d.bullets(s, [
    ("Latency: ", "company claims 70 to 500 ms; our measurements from this workshop: ~280 ms per text call including network. Fast enough to sit in front of every LLM call."),
    ("Price: ", "$0.042 per million input tokens, output free. A 5-question triage request is ~500 tokens: about $21 per million tickets."),
    ("What this unlocks: ", "screen every message both directions, score every passage in RAG, classify entire agent traces, ask speculative questions by default."),
], x=8.05, y=1.9, w=4.8, size=13.5, gap=11)
d.text(s, "Indicative LLM tier prices for scale; check current vendor pricing. The point is orders of magnitude, not decimals.",
       x=0.55, y=6.3, w=7.2, h=0.4, size=11, color=MUTED, italic=True)
d.notes(s, "The economics ARE the product. At these prices the question flips from 'can we afford an AI check here' to "
           "'why would we not check'. That reframing drives every pattern in part 4.")

# ---------------------------------------------------------------- 18 batching measured
s = d.slide(FOOT)
d.kicker(s, "Part 4  |  We measured it")
d.title(s, "Batching questions: our live experiment")
d.image(s, f"{ASSETS}/batching.png", x=0.55, y=1.8, w=7.4)
d.bullets(s, [
    ("The setup: ", "an 8-question compliance checklist over one policy paragraph; 8 separate calls vs 1 call with 8 questions."),
    ("Result: ", "6.8x faster, 6.1x fewer input tokens, answers numerically identical (within 0.01)."),
    ("Why: ", "every call pays to resend the state and a round trip; a batch pays once."),
    ("Docs' version at 13 questions: ", "11.5x cheaper, 9.6x faster. The ratio grows with question count and state size."),
], x=8.15, y=1.9, w=4.7, size=13.5, gap=11)
d.text(s, "Run it yourself: notebook 04, cell 6. No limit on questions per request; the bound is context (64k per request, 32k state plus any one question).",
       x=0.55, y=6.3, w=12, h=0.4, size=12, color=MUTED, italic=True)
d.notes(s, "This chart was generated from a real run during preparation. Invite the room to re-run notebook 04 and watch their own numbers land "
           "in the same ballpark. If questions do not all fit in context, reuse the same state across a few requests.")

# ---------------------------------------------------------------- 19 pattern fan-out
s = d.slide(FOOT)
d.kicker(s, "Part 4  |  Pattern 1 of 4")
d.title(s, "Speculative fan-out: ask everything, let code choose")
d.bullets(s, [
    ("The idea. ", "Send every question your code MIGHT need, including ones that only matter for some inputs. Code ignores the irrelevant answers."),
    ("Why it is nearly free. ", "Questions evaluate in parallel; an extra question adds a few tokens, not a round trip."),
    ("The example. ", "Triage asks category, bug severity, repro steps, refund requested, frustration, all at once. A feature request simply never reads the severity answer."),
    ("Independence guarantee. ", "One question's answer is never hidden context for another; adding a question cannot change the others' results."),
], x=0.55, y=1.8, w=6.4, size=15, gap=12)
d.code(s, 'r = client.system_one(state=ticket, questions={\n  "category":     Choice(...),   # always used\n  "bug_severity": Score(...),    # only if bug\n  "has_repro":    Noul(...),     # only if bug\n  "refund_asked": Noul(...),     # only if billing\n  "frustration":  Score(...),    # always used\n})\n\nif r.choices["category"].choice == "bug_report":\n    if (r.scores["bug_severity"].score > 1.5\n            and r.nouls["has_repro"].noul > 0.6):\n        escalate_to_engineering()',
       x=7.3, y=1.8, w=5.5, h=4.3)
d.notes(s, "Coding agents fall into one-question-per-call more than people do; TypeSafe ships an agent skill that teaches them to batch. "
           "The full decision tree resolves from one call.")

# ---------------------------------------------------------------- 20 pattern composite
s = d.slide(FOOT)
d.kicker(s, "Part 4  |  Pattern 2 of 4")
d.title(s, "Composite scoring: the model judges, your weights decide")
d.bullets(s, [
    ("Resist the one-big-question urge. ", "“Rate this candidate 1-10” hides several judgments behind one number you cannot tune."),
    ("Instead: ", "one Score per dimension (Python depth, leadership, system design), normalized by each scale's top level, combined with weights in code."),
    ("The payoff. ", "Senior-IC weights and manager weights produce different rankings from the SAME model judgments. Priorities change in a constants file, under code review, not in a prompt."),
    ("Judgment vs policy. ", "The model owns the former, your code owns the latter. Keep them separable and both become testable."),
], x=0.55, y=1.8, w=6.4, size=15, gap=12)
d.code(s, 'norm = lambda qid: (r.scores[qid].score\n        / (len(DIMENSIONS[qid].criteria) - 1))\n\nic_fit = (0.45 * norm("python_depth")\n        + 0.10 * norm("team_leadership")\n        + 0.45 * norm("system_design"))\n\nem_fit = (0.15 * norm("python_depth")\n        + 0.55 * norm("team_leadership")\n        + 0.30 * norm("system_design"))',
       x=7.3, y=1.8, w=5.5, h=3.3)
d.text(s, "Also feeds classical ML: use the probabilities as features for a downstream model when you have labeled outcomes.",
       x=7.3, y=5.4, w=5.5, h=0.8, size=12.5, color=SLATE, italic=True)
d.notes(s, "Notebook 04 ranks three resumes under both weight profiles live. When the ranking disagrees with your team's intuition, "
           "you adjust a coefficient and rerun: fast, auditable iteration.")

# ---------------------------------------------------------------- 21 pattern routing
s = d.slide(FOOT)
d.kicker(s, "Part 4  |  Patterns 3 and 4 of 4")
d.title(s, "Confidence-gated routing + intent routing")
d.rect(s, 0.55, 1.75, 6.0, 4.75, fill=PAPER, line=LINE)
d.text(s, "Confidence-gated routing", x=0.8, y=1.95, w=5.5, h=0.4, size=15.5, bold=True, font=SERIF)
d.bullets(s, [
    "Confidence is a second decision axis: the answer says what, confidence says whether to act on it.",
    "A floor (for example 0.5) catches genuine uncertainty for everything; each action then sets its own bar by stakes.",
    "Checking a balance clears at 0.6; approving a transfer wants 0.85 plus a confirmation.",
], x=0.8, y=2.5, w=5.5, size=13.5, gap=10)
d.rect(s, 6.85, 1.75, 6.0, 4.75, fill=PAPER, line=LINE)
d.text(s, "Intent routing", x=7.1, y=1.95, w=5.5, h=0.4, size=15.5, bold=True, font=SERIF)
d.bullets(s, [
    "Jev sits in front as the fast, cheap classifier; expensive handlers are invoked only when needed.",
    "order_status: deterministic code, no LLM at all. product_question: a specialist LLM with the right context loaded.",
    "complaint: a complexity Score decides between an LLM and a person.",
    "The routing call costs fractions of a cent per thousand messages and saves an LLM invocation on most of them.",
], x=7.1, y=2.5, w=5.5, size=13.5, gap=10)
d.notes(s, "Both run live in notebooks 03 and 04. The combined shape, classify cheaply, gate on confidence, spend money only where "
           "deterministic code cannot go, is the canonical production architecture for Jev.")

# ---------------------------------------------------------------- 22 use case categories
s = d.slide(FOOT)
d.kicker(s, "Part 4  |  Where it fits")
d.title(s, "Five use-case families (TypeSafe's own map)")
cards = [
    ("AI automation software", "Code owns control flow; Jev handles semantic decisions. Run it a million times in the background, no human co-pilot."),
    ("Real-time applications", "Frontier intelligence at ~150 ms: decisions faster than human perception, inside UIs and game loops."),
    ("AI map-reduce over big data", "100x cheaper means you can afford giant corpora: search, classify traces, extract features at dataset scale."),
    ("Universal verification", "Check prompts, extractions, citations, reasoning traces, and tool calls of OTHER AIs at a fraction of the LLM's cost."),
    ("Harness engineering", "Make your agent harness smarter: model routing, semantic retrieval, error detection, guardrails."),
]
xs = [0.55, 4.7, 8.85, 0.55, 4.7]
ys = [1.75, 1.75, 1.75, 4.25, 4.25]
for (title, body), x, y in zip(cards, xs, ys):
    d.rect(s, x, y, 3.95, 2.3, fill=PAPER, line=LINE)
    d.text(s, title, x=x + 0.2, y=y + 0.16, w=3.55, h=0.65, size=14.5, bold=True, font=SERIF)
    d.text(s, body, x=x + 0.2, y=y + 0.82, w=3.55, h=1.4, size=11.5, color=SLATE, line_spacing=1.15)
d.rect(s, 8.85, 4.25, 3.95, 2.3, fill=INK, line=None)
d.text(s, "Industry examples", x=9.05, y=4.41, w=3.55, h=0.4, size=14.5, bold=True, font=SERIF, color=CREAM)
d.text(s, "support triage, insurance claims, financial crime, legal and compliance, e-commerce catalogs, trust and safety, recruiting, demand forecasting",
       x=9.05, y=4.87, w=3.55, h=1.5, size=11.5, color=RGBColor(0xCF, 0xCB, 0xC2), line_spacing=1.15)
d.notes(s, "The use-case map at docs.typesafe.ai/concepts/use-case-map has a worked accordion per industry. "
           "For this audience: universal verification and harness engineering are the ones adjacent to our agent-platform work, "
           "guardrails on every tool call become affordable.")

# ---------------------------------------------------------------- 23 cookbook wall
s = d.slide(FOOT)
d.kicker(s, "Part 4  |  Receipts")
d.title(s, "The cookbooks publish measured results")
rows = [
    ["Cookbook", "What it builds", "Published result"],
    ["Parallel questions", "13-question regulatory briefing, batched", "12.2x cheaper, 10.0x faster, same answers"],
    ["Re-ranking (CLERC legal)", "BM25 shortlist, then one Noul per query-candidate pair", "top-1 accuracy 5% to 18%; top-10 38% to 62%"],
    ["Skill suggestion", "pick at most 1 of 182 agent skills, two-stage", "rank 182 in one request, re-check top 3"],
    ["SDE cascade", "extract with mini model, verify with Jev, escalate the rest", "most of a reasoning model's quality at a fraction of cost"],
    ["Hierarchical classification", "beam search over Choice probabilities", "deep patent/retail/biomedical trees, parallel beams"],
    ["Guardrails for LLMs", "screen every message, hazard Nouls + severity", "pass / review / block from one request per message"],
    ["Entity alignment", "450 candidate pairs, one Score + 3 companion Nouls", "duplicate detection across two product catalogs"],
]
d.table(s, rows, x=0.55, y=1.7, w=12.2, col_widths=[2.6, 5.2, 4.4], row_h=0.62, size=12, header_fill=INK)
d.text(s, "All 20+ at docs.typesafe.ai/cookbooks, each with runnable code. Notebook 05 builds two of them in miniature.",
       x=0.55, y=6.5, w=12, h=0.35, size=12, color=MUTED, italic=True)
d.notes(s, "These are TypeSafe's published numbers, not ours; we reproduced the batching claim ourselves (previous slide) and got the same shape. "
           "The re-ranking rows are the strongest third-party-verifiable claims: public dataset, published methodology.")

# ---------------------------------------------------------------- 24 sharp edges
s = d.slide(FOOT)
d.kicker(s, "Part 5  |  The honest slide")
d.title(s, "Nine documented failure modes (Jev 1.13 jaggedness)")
rows = [
    ["Failure mode", "Do this instead"],
    ["Literal reading: answers what you wrote, not what you meant", "write the exact condition; boundary cases into criteria"],
    ["Math, numbers, counting", "keep arithmetic in code; one Noul per item, sum yourself"],
    ["Date and time comparison", "extract parts as Choices; compare in code (notebook 05, live)"],
    ["Indirection, double negatives", "reduce hops; point at state by backticked path"],
    ["Large state full of irrelevant detail (context rot)", "filter in code first; send only what the question needs"],
    ["Adversarial content can steer answers", "precise criteria; test on real attacks; never Jev alone as the gate"],
    ["Contradictory instructions vs criteria", "align them; never map true to no"],
    ["Choice option order can bias the answer", "reorder options; check consistency"],
    ["Generation: it cannot produce text", "a generative model, or a Choice over pre-parsed candidates"],
]
d.table(s, rows, x=0.55, y=1.7, w=12.2, col_widths=[6.1, 6.1], row_h=0.49, size=11.5)
d.notes(s, "TypeSafe publishes this list themselves and dates the review (last reviewed Oct 2, 2026). Teach the smell test: "
           "if code can compute it exactly, the model has nothing to add. Notebook 05 demos counting and the ambiguous-date trap live, "
           "including the confidence gate catching 11/05/2026 splitting between May and November.")

# ---------------------------------------------------------------- 25 not list
s = d.slide(FOOT)
d.kicker(s, "Part 5  |  Scope")
d.title(s, "What Jev is not")
d.bullets(s, [
    ("Not a chat model. ", "It cannot write replies, summaries, or explanations. Pair it with an LLM when you need words."),
    ("Not a coding-agent brain. ", "There is no model=“jev-latest” setting that powers Claude Code or Cursor. Jev goes inside the software your agent writes."),
    ("Not a calculator or a clock. ", "Arithmetic, counting, date math: code's job, always."),
    ("Not a reasoning engine. ", "Multi-hop System 2 tasks get decomposed into atomic questions composed in code, or handed to a reasoning model."),
    ("Not fine-tunable. ", "Same weights for everyone; your domain lives in state, instructions, criteria."),
], x=0.55, y=1.85, w=7.6, size=16, gap=14)
d.rect(s, 8.55, 1.95, 4.25, 4.2, fill=PAPER, line=LINE)
d.text(s, "The mental model", x=8.8, y=2.2, w=3.75, h=0.4, size=15, bold=True, font=SERIF)
d.text(s, "Code owns the workflow.\n\nJev answers the judgment calls.\n\nLLMs write the words,\nwhen words are needed.",
       x=8.8, y=2.75, w=3.75, h=3.0, size=15.5, color=INK, font=SERIF, italic=True, line_spacing=1.2)
d.notes(s, "The 'coding agents' page exists because people kept asking. Worth repeating the division of labor out loud: "
           "deterministic rules in code, judgment in Jev, generation in LLMs. Most production systems will use all three.")

# ---------------------------------------------------------------- 26 properties reference
s = d.slide(FOOT)
d.kicker(s, "Part 5  |  Reference card")
d.title(s, "Properties your team will ask about")
rows = [
    ["", "Jev 1.13 (jev-latest)", "Jev 1.14 (jev-preview)"],
    ["Released", "Sep 15, 2026", "Oct 14, 2026"],
    ["Price", "$0.042 / Mtok input, output free", "same"],
    ["Context", "64k per request / 32k per question", "same; 262k with long-context header"],
    ["Input", "text (string, object, array)", "text + images (preview header)"],
    ["Box questions", "no", "yes"],
]
d.table(s, rows, x=0.55, y=1.7, w=7.6, col_widths=[1.7, 3.0, 2.9], row_h=0.56, size=12.5)
d.bullets(s, [
    ("Rate limits: ", "tokens/sec and requests/sec per organization; SDKs retry 429/529 with backoff and honor retry-after."),
    ("Errors: ", "400 bad request, 401 auth, 413 too large, 422 validation (names the field), 429 rate limit, 529 overloaded."),
    ("Versioning: ", "aliases move on release (latest moves to 1.14 ~Oct 21); responses report the versioned model. Pin versions once thresholds are tuned."),
    ("Data: ", "not trained on customer requests; ZDR available for enterprise."),
    ("Language: ", "English primary; others accepted with lower accuracy, so watch confidence."),
], x=8.4, y=1.8, w=4.45, size=12, gap=9)
d.text(s, "Full distilled documentation: reference/JEV-REFERENCE.md in the workshop folder.",
       x=0.55, y=6.4, w=10, h=0.35, size=12, color=MUTED, italic=True)
d.notes(s, "This slide is the one to hand to the platform team. The danger-zone headers (images, long context) are per-request opt-ins, "
           "which is a nice API design detail: experimental surface is impossible to enable by accident.")

# ---------------------------------------------------------------- 27 getting started
s = d.slide(FOOT)
d.kicker(s, "Part 5  |  Go build")
d.title(s, "Getting started, four ways")
cards = [
    ("1. Playground", "console.typesafe.ai/playground: paste a state, add questions, read answers. No code. Best first five minutes."),
    ("2. Python SDK", "pip install typesafe-sdk\nexport TYPESAFE_API_KEY=...\nclient.system_one(state=..., questions=...)"),
    ("3. HTTP", "POST api.typesafe.ai/v1/systemone with Bearer auth. Any language, no SDK required."),
    ("4. Agent skill", "claude plugin marketplace add typesafe-ai/skills, then claude plugin install typesafe@typesafe-ai: your coding agent learns the API, the primitives, and to batch questions."),
]
y = 1.8
for title, body in cards:
    d.rect(s, 0.55, y, 7.3, 1.08, fill=PAPER, line=LINE)
    d.text(s, title, x=0.8, y=y + 0.12, w=1.9, h=0.4, size=14, bold=True, font=SERIF)
    d.text(s, body, x=2.8, y=y + 0.12, w=4.9, h=0.9, size=11.5, color=SLATE, line_spacing=1.1)
    y += 1.22
d.rect(s, 8.3, 1.8, 4.5, 4.7, fill=INK, line=None)
d.text(s, "Your lab, after this deck", x=8.55, y=2.05, w=4.0, h=0.4, size=15, bold=True, font=SERIF, color=CREAM)
d.text(s, "01  hello jev: first calls, cost math\n02  primitives: all four, with anti-examples\n03  confidence: formulas verified live\n04  patterns: the 6.8x batching experiment\n05  real world: guardrails, search,\n      the sharp edges, reference",
       x=8.55, y=2.6, w=4.0, h=3.0, size=12.5, color=RGBColor(0xED, 0xEA, 0xE3), font=SANS, line_spacing=1.3)
d.text(s, "A full run of all five notebooks costs under one cent.", x=8.55, y=5.9, w=4.0, h=0.4, size=11, color=MUTED, italic=True)
d.notes(s, "Send attendees to the Playground during the break; it is the fastest way to internalize the state-plus-questions model. "
           "The agent skill matters for teams: it is how their coding agents stop writing one-question-per-call integrations.")

# ---------------------------------------------------------------- 28 closing
s = d.slide()
d.text(s, "The one-sentence takeaway", x=0.9, y=1.5, w=8, h=0.4, size=13, color=CLAY, font=SANS, bold=True)
d.text(s, "Code owns the workflow.\nJev answers the judgment calls.",
       x=0.86, y=2.1, w=11.6, h=2.2, size=44, color=INK, font=SERIF, line_spacing=1.1)
d.divider(s, 0.92, 4.6, 5.4, color=CORAL, weight=2.5)
d.text(s, "docs.typesafe.ai          console.typesafe.ai/playground          docs.typesafe.ai/cookbooks",
       x=0.9, y=4.9, w=11.5, h=0.4, size=14, color=SLATE, font=SANS)
d.text(s, "Workshop materials: jev-workshop/ (five executed notebooks, this deck, and JEV-REFERENCE.md)",
       x=0.9, y=5.45, w=11.5, h=0.4, size=12.5, color=MUTED)
d.notes(s, "Close with the division of labor, then open Q&A. Common first questions: pricing at scale (slide 17), "
           "security posture (slide 6 and 24), and when NOT to use it (slide 25).")

print("slides:", d.n)
print("saved:", d.save(OUT))
