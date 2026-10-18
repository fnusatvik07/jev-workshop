"""
GALLERY - Semantic Emoji Picker: type a word, the right emojis float to the top.

A classic phone-keyboard feature, except the usual version is a keyword lookup:
type "pizza" and you get the pizza emoji only because the word "pizza" is tagged
on it. Type "I'm starving" and you get nothing.

Here we ask one yes/no (a Noul) PER emoji in a single request: "does this emoji
fit the text?". Because each question is independent, MANY emojis can score high
at once, so "I'm starving" floats the whole food group to the top, not just one
winner. All 36 judgments run in parallel in one call for a fraction of a cent.

The pattern: a batch of independent Nouls turns any option set into a ranked,
multi-select semantic match.

Run:  uv run python emoji_picker.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "live-builds"))

from typesafe_sdk import Noul, TypeSafeClient

from _jev import bar, ensure_key, rule

ensure_key()

# The vocabulary. Each emoji is an option; its description is what Jev matches on.
EMOJIS = {
    "🍕": "pizza, fast food, hungry", "🍔": "burger, fast food",
    "🍣": "sushi, japanese food", "🍎": "apple, fruit, healthy eating",
    "☕": "coffee, caffeine, morning drink", "🍺": "beer, drinks, going out",
    "🐶": "dog, puppy, pet", "🐱": "cat, kitten, pet",
    "🦁": "lion, wild animal, brave", "🐢": "turtle, slow",
    "☀️": "sun, sunny, hot weather", "🌧️": "rain, rainy, wet weather",
    "⛄": "snow, cold, winter", "🌈": "rainbow, colorful, hopeful",
    "😀": "happy, smiling, cheerful", "😢": "sad, crying, upset",
    "😡": "angry, furious, mad", "😍": "love, adoration, crush",
    "😴": "sleepy, tired, bored", "😂": "laughing, hilarious, funny",
    "🎉": "celebration, party, success", "🎂": "birthday, cake",
    "🏆": "trophy, winning, achievement", "🔥": "fire, hot, impressive",
    "✈️": "travel, flight, airplane", "🏖️": "beach, vacation, relax",
    "🚗": "car, driving, road trip", "💻": "coding, computer, programming",
    "📱": "phone, mobile, texting", "📚": "books, studying, reading",
    "🎵": "music, song, listening", "⚽": "soccer, football, sports",
    "🎮": "gaming, video games", "❤️": "love, heart, romance",
    "💰": "money, wealth, rich", "🚀": "rocket, launch, fast, startup",
}


EMOJI_LIST = list(EMOJIS.items())


def suggest(text: str, client: TypeSafeClient):
    # One request, one independent yes/no per emoji, so several can score high.
    questions = {
        f"e{i}": Noul(instructions=f"Does the emoji {e} ({desc}) fit this text?")
        for i, (e, desc) in enumerate(EMOJI_LIST)
    }
    r = client.system_one(state=text, questions=questions)
    scored = [(EMOJI_LIST[i][0], r.nouls[f"e{i}"].noul) for i in range(len(EMOJI_LIST))]
    return sorted(scored, key=lambda kv: kv[1], reverse=True)


QUERIES = [
    "I'm absolutely starving",
    "ugh it's pouring outside",
    "my dog is the best thing ever",
    "we shipped the release, let's celebrate",
    "feeling really down today",
    "time to write some python",
    "booking a trip to the beach",
]


def main() -> None:
    rule("SEMANTIC EMOJI PICKER  ·  type a word, the right emojis rise")
    with TypeSafeClient() as client:
        for q in QUERIES:
            ranked = suggest(q, client)
            risen = [e for e, p in ranked if p > 0.5] or [ranked[0][0]]
            print(f'\n  "{q}"')
            print(f"     {'  '.join(risen)}")
            for e, p in ranked[:5]:
                if p > 0.2:
                    print(f"       {e}  {bar(p, 18)} {p:.2f}")
    rule("THE IDEA")
    print("  No tags, no synonym table. One independent yes/no per emoji, all in one request,")
    print("  so a whole GROUP can rise together: 'starving' floats every food emoji, not just")
    print("  one. That is the keyboard feature in ~15 lines, by meaning.\n")


if __name__ == "__main__":
    main()
