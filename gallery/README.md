# Gallery: fun, visual Jev demos you can run in 30 seconds

Small, delightful use cases that show Jev off in a way a room can *see*. Each is
one file, runs in the terminal, and was verified against the live API. These pair
with the five resume-grade projects in [`../live-builds/`](../live-builds).

```bash
uv sync
export TYPESAFE_API_KEY="your-typesafe-key"     # console.typesafe.ai/keys
export OPENAI_API_KEY="your-openai-key"         # only semantic_find needs this
uv run python gallery/emoji_picker.py
```

| File | What it does | The pattern |
| --- | --- | --- |
| `emoji_picker.py` | type a word, the matching emoji group floats to the top | a batch of independent Nouls = multi-select semantic match |
| `color_mood.py` | type a feeling, a color materializes | blend the top probabilities into one shade |
| `semantic_find.py` | semantic Ctrl-F: find by meaning, answer through chat | Jev retrieves and gates, an LLM phrases the answer |

---

## emoji_picker.py

A phone keyboard that understands meaning. One yes/no per emoji, all in one
request, so a whole group rises at once.

```
"I'm absolutely starving"          -> 🍕  🍔  🍣   (0.93, 0.82, 0.51)
"my dog is the best thing ever"    -> 🐶  😍  😀  ❤️  🔥
```

## color_mood.py

Type an emotion or scene; the color appears as a truecolor block. The top three
palette colors are blended by their probabilities, so each phrase gets its own
shade: "royal and luxurious" came back gold 66% + purple 34%.

```
"pure, unstoppable rage"   -> rgb(213, 48, 49)   red
"a calm ocean at dawn"     -> rgb(53, 120, 217)  blue
"a warm autumn sunset"     -> rgb(230, 126, 34)  orange
```

## semantic_find.py

Browser Find that reads for meaning. "how do I stop getting charged" finds the
line that says "terminate your subscription" (zero shared keywords), and an LLM
writes the one-sentence answer from it. Questions with no answer on the page
correctly come back "not found" instead of guessing. This is the core of a Chrome
Ctrl-F extension; the extension is just the DOM plumbing around it.

```
🔎 "how do I stop getting charged every month?"
   match: "You can terminate your subscription at any time from Settings > Billing."
   💬  Go to Settings > Billing and terminate your subscription.

🔎 "is there a student discount?"   -> not found on this page (answerable 0.02)
```
