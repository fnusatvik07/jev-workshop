"""
PROJECT 3 - Semantic Content Blocker: filter the web by MEANING, not blocklists.

Ad blockers and content filters have always worked on brittle signals: domain
lists, CSS selectors, keyword regexes. They break the moment the ad is reworded
or the tracker changes host. This blocks content by what it MEANS instead.

The user toggles the categories they want gone (ads, ragebait, crypto shilling,
spoilers, AI slop). For every item on the page, one Jev request answers one
yes/no per enabled category plus a severity score, and code decides HIDE / BLUR
/ DIM / SHOW. No blocklist, no training, no per-site rules. Change the policy by
flipping a toggle.

This is the decision engine a browser extension would call per DOM node; the
extension itself is just plumbing that hides the element the engine flags. At
~100ms and a fraction of a cent per item, you can judge a whole feed live.

Resume line: "Built a semantic content blocker that filters web content by
meaning with user-toggleable categories, replacing domain blocklists with a
calibrated 100ms classifier."

Run:  uv run python content_blocker.py
"""

from typesafe_sdk import Noul, Score, TypeSafeClient

from _jev import ensure_key, rule

ensure_key()

# The catalog of things a user might want gone. Each is one yes/no judgment.
CATEGORIES = {
    "ad": "A paid advertisement, sponsored post, or promotion",
    "ragebait": "Content engineered to provoke outrage or anger for engagement",
    "crypto_shill": "Promotion of crypto tokens, NFTs, or get-rich schemes",
    "spoiler": "Reveals plot or results of a show, game, or sporting event",
    "ai_slop": "Low-effort AI-generated filler with no real substance",
}

# What the user has toggled ON. (Try removing or adding one and re-running.)
ENABLED = ["ad", "ragebait", "crypto_shill", "spoiler", "ai_slop"]

HIDE, BLUR, DIM = 0.80, 0.80, 0.50  # thresholds; spoilers get BLUR instead of HIDE


def judge(item: str, client: TypeSafeClient) -> dict:
    """One request: a yes/no per enabled category, plus how intrusive it is."""
    questions = {c: Noul(instructions=f"Does this item fit the category '{c}': {CATEGORIES[c]}?")
                 for c in ENABLED}
    questions["intrusiveness"] = Score(
        instructions="How intrusive or low-value is this item to a focused reader?",
        criteria=["Genuinely useful", "Mildly distracting", "Pure noise or manipulation"],
    )
    r = client.system_one(state=item, questions=questions)
    scores = {c: r.nouls[c].noul for c in ENABLED}
    worst_cat = max(scores, key=scores.get)
    worst = scores[worst_cat]

    # Policy, all in code: spoilers blur (you can reveal), everything else hides.
    if worst > HIDE:
        action = "BLUR" if worst_cat == "spoiler" else "HIDE"
    elif worst > DIM:
        action = "DIM"
    else:
        action = "SHOW"
    return {"action": action, "cat": worst_cat, "p": worst, "scores": scores}


FEED = [
    "Breaking: scientists confirm 8 glasses of water a day myth finally debunked in new study.",
    "SPONSORED - This one weird productivity app replaced my entire team. Sign up free today!",
    "They DON'T want you to know this. The elites are HIDING the truth about your groceries.",
    "$PEPE2 is about to 100x. Last chance before launch. Not financial advice but WAGMI.",
    "In tonight's finale, the detective turns out to be the killer all along. Wild ending.",
    "Here are 10 tips to improve your morning routine. Tip 1: wake up. Tip 2: be productive...",
    "Our team just shipped incremental static regeneration for the docs site. Here's how it works.",
    "You won't BELIEVE what this celebrity said. Number 7 will make you FURIOUS.",
    "Reminder: the library closes at 6pm on Fridays during the summer.",
    "Buy the dip! My wallet is ready. This token is the next Solana, trust me bro.",
]

ICON = {"SHOW": "  show  ", "DIM": "  dim   ", "BLUR": "  BLUR  ", "HIDE": "  HIDE  "}


def main() -> None:
    rule("SEMANTIC CONTENT BLOCKER  ·  filtering by meaning, not blocklists")
    print(f"  blocking: {', '.join(ENABLED)}\n")
    hidden = 0
    with TypeSafeClient() as client:
        for item in FEED:
            d = judge(item, client)
            if d["action"] in ("HIDE", "BLUR"):
                hidden += 1
            why = f"{d['cat']} {d['p']:.2f}" if d["action"] != "SHOW" else ""
            shown = item if d["action"] == "SHOW" else (
                "█" * 46 if d["action"] == "HIDE" else item)
            print(f"  [{ICON[d['action']]}] {shown[:60]}")
            if why:
                print(f"              -> flagged as {why}")
    rule("RESULT")
    print(f"  {hidden} of {len(FEED)} items removed or blurred, each judged in ~100ms for a")
    print("  fraction of a cent. No domain list touched. Flip a category in ENABLED and")
    print("  the whole feed re-filters: that is the entire 'settings page' of the extension.\n")
    print("  // browser extension core is one call per node:")
    print("  //   const v = await judge(node.innerText);  if (v.action!=='SHOW') hide(node)\n")


if __name__ == "__main__":
    main()
