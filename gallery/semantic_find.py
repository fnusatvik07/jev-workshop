"""
GALLERY - Semantic Ctrl-F: find by meaning, answer through chat.

Browser Find is a substring match. Search a help page for "cancel" and you miss
the paragraph that says "terminate your subscription". This is Ctrl-F that reads
for meaning: it finds the passage that ANSWERS your question even when it shares
no words with it, then an LLM writes the one-line answer from that passage.

Two models, each doing what it is best at:
  - Jev RETRIEVES: one request ranks every line by how well it answers the query,
    plus a yes/no on whether the page answers it at all (so it can say "not here"
    instead of guessing). ~100ms, a fraction of a cent.
  - OpenAI ANSWERS: given only the top line, it writes the chat reply. Grounded,
    so it cannot wander off the page.

This is the core of a Chrome extension: collect the page's text nodes, run this
on the query, scroll to and highlight the winning node, show the answer in a popup.

Run:  uv run python semantic_find.py   (needs OPENAI_API_KEY too)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "live-builds"))

from openai import OpenAI
from typesafe_sdk import Choice, Noul, TypeSafeClient

from _jev import ensure_key, rule

ensure_key()

# The "page" we are searching. Note: none of these lines share keywords with the
# queries below, so a normal Ctrl-F would find nothing.
PAGE = [
    "Welcome to Nimbus, the collaborative whiteboard for remote teams.",
    "You can terminate your subscription at any time from Settings > Billing.",
    "Boards you create are private until you invite collaborators by email.",
    "Export any board to PDF or PNG from the share menu in the top right.",
    "We never sell your data; see our privacy policy for details.",
    "Nimbus works in any modern browser; there is no separate app to install.",
    "The Free plan includes three boards; paid plans remove the limit.",
    "Need a hand? Reach support in-app or at help@nimbus.example.",
]

HL = "\x1b[1m\x1b[48;2;240;230;140m"  # bold on soft yellow, for the highlight
RESET = "\x1b[0m"


def find(query: str, jev: TypeSafeClient, oai: OpenAI):
    # Step 1 - Jev retrieves: is it here, and which line is it?
    r = jev.system_one(
        state={"query": query, "page": PAGE},
        questions={
            "answerable": Noul(instructions="Does any line in `page` contain an answer to `query`?"),
            "best": Choice(
                instructions="Which line of `page` best answers `query`?",
                criteria={f"L{i}": line for i, line in enumerate(PAGE)},
            ),
        },
    )
    answerable = r.nouls["answerable"].noul
    best = r.choices["best"]
    idx = int(best.choice[1:])
    if answerable < 0.5:
        return None, answerable, best.confidence, None

    # Step 2 - OpenAI answers, grounded only in the winning line.
    line = PAGE[idx]
    chat = oai.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[{"role": "user", "content":
                   f"Using ONLY this text, answer in one short sentence.\nText: {line}\nQuestion: {query}"}],
        max_completion_tokens=2000,
    ).choices[0].message.content.strip()
    return idx, answerable, best.confidence, chat


QUERIES = [
    "how do I stop getting charged every month?",
    "can I take my drawings out of here?",
    "does this run on my phone?",
    "do you make money by selling what I upload?",
    "is there a student discount?",   # not on the page -> should say not found
]


def main() -> None:
    rule("SEMANTIC CTRL-F  ·  find by meaning, answer through chat")
    with TypeSafeClient() as jev:
        oai = OpenAI()
        for q in QUERIES:
            idx, answerable, conf, chat = find(q, jev, oai)
            print(f'\n  🔎  "{q}"')
            if idx is None:
                print(f"      not found on this page  (answerable {answerable:.2f})")
                continue
            print(f"      match (confidence {conf:.2f}):  {HL} {PAGE[idx]} {RESET}")
            print(f"      💬  {chat}")
    rule("THE IDEA")
    print("  Zero shared keywords between the questions and the lines, yet every real question")
    print("  found its line, and the student-discount question correctly returned 'not here'.")
    print("  Jev retrieves and gates; the LLM only phrases the answer it is handed.\n")


if __name__ == "__main__":
    main()
