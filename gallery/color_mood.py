"""
GALLERY - Mood to Color: type a feeling, the color materializes.

Inspired by the voice-to-color emotion app Claire Vo built on Jev in an
afternoon. You type an emotion or a scene; a color appears. No lookup table of
"anger = red", because that misses "a calm ocean at dawn" or "melancholy".

The trick that makes it feel alive: Jev scores your text against a named palette
and returns a probability for every color. We do not just take the top one, we
BLEND the top three weighted by their probabilities. Because the probabilities
are calibrated, "warm autumn sunset" literally mixes orange, gold, and a little
red into one unique shade. The distribution becomes the paint.

Run:  uv run python color_mood.py     (best in a truecolor terminal)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "live-builds"))

from typesafe_sdk import Choice, TypeSafeClient

from _jev import ensure_key, rule

ensure_key()

# name -> (rgb, what it evokes). The evocations are what Jev matches against.
PALETTE = {
    "red":     ((214, 48, 49),  "anger, passion, heat, danger"),
    "orange":  ((230, 126, 34), "energy, warmth, autumn"),
    "gold":    ((212, 175, 55), "luxury, victory, royalty"),
    "yellow":  ((241, 196, 15), "joy, optimism, sunshine"),
    "green":   ((39, 174, 96),  "calm, nature, growth, envy"),
    "teal":    ((0, 160, 160),  "fresh, clean, modern"),
    "blue":    ((52, 120, 219), "calm, trust, cool, sadness"),
    "navy":    ((34, 49, 110),  "depth, night, serious"),
    "purple":  ((142, 68, 200), "mystery, creativity, royalty"),
    "pink":    ((240, 120, 180),"playful, sweet, love"),
    "brown":   ((140, 90, 50),  "earthy, cozy, rustic"),
    "gray":    ((130, 130, 130),"neutral, dull, boredom"),
    "black":   ((35, 35, 40),   "darkness, spooky, elegant, grief"),
    "white":   ((238, 238, 238),"purity, clean, emptiness"),
    "crimson": ((160, 20, 40),  "intensity, alarm, drama"),
}


def swatch(rgb) -> str:
    r, g, b = rgb
    return f"\x1b[48;2;{r};{g};{b}m          \x1b[0m"


def mood_color(text: str, client: TypeSafeClient):
    r = client.system_one(
        state=text,
        questions={"color": Choice(
            instructions="Which color best matches the feeling or scene in this text?",
            criteria={name: desc for name, (_, desc) in PALETTE.items()},
        )},
    )
    probs = r.choices["color"].probabilities
    top3 = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)[:3]
    total = sum(p for _, p in top3) or 1.0
    # blend the top three palette colors weighted by probability
    mix = [0.0, 0.0, 0.0]
    for name, p in top3:
        rgb = PALETTE[name][0]
        for i in range(3):
            mix[i] += rgb[i] * (p / total)
    blended = tuple(round(c) for c in mix)
    return blended, top3


INPUTS = [
    "pure, unstoppable rage",
    "a calm ocean at dawn",
    "green with envy",
    "a warm autumn sunset",
    "royal and luxurious",
    "spooky halloween night",
    "bubbly childish joy",
    "quiet melancholy",
]


def main() -> None:
    rule("MOOD TO COLOR  ·  the distribution becomes the paint")
    with TypeSafeClient() as client:
        for text in INPUTS:
            blended, top3 = mood_color(text, client)
            contrib = ", ".join(f"{n} {p:.0%}" for n, p in top3)
            print(f"\n  {swatch(blended)}  {swatch(blended)}  rgb{blended}")
            print(f'      "{text}"')
            print(f"      blended from: {contrib}")
    rule("THE IDEA")
    print("  No emotion->color table. Jev scored the palette, and we mixed the top three by")
    print("  their probabilities, so each phrase gets its own shade. Calibrated numbers are")
    print("  literally the mixing ratios. (If you see no colors, your terminal lacks truecolor.)\n")


if __name__ == "__main__":
    main()
