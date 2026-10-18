"""
PROJECT 4 - Shapeshift: a UI that builds itself from what you type.

One text box. The user types what they want in plain language, and the RIGHT
input control materializes: a date-time picker, a slider, a color picker, a
star rating, a location search. No menu of modes, no "click here to add a
field". The interface adapts to intent.

The move that makes this a System One job: a UI needs a DECISION (which control,
which sub-fields are present, which enumerated value), not prose. One Jev
request answers a Choice over control types plus several yes/no feature flags in
parallel, and code renders the control from those typed answers. Jev decides the
SHAPE; code (and a regex or two) fills the free-text values, since Jev never
generates text.

Resume line: "Built an adaptive (generative) UI that renders the correct input
controls from natural language using parallel typed classification at ~100ms."

Run:  uv run python shapeshift.py
"""

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

from _jev import bar, ensure_key, rule

ensure_key()

QUESTIONS = {
    "control": Choice(
        instructions="What single input control best fits what the user is trying to specify?",
        criteria={
            "datetime_picker": "Choosing a date and/or time",
            "slider": "Setting a number within a range, like volume or brightness",
            "color_picker": "Choosing a color",
            "location_search": "Choosing a place or address",
            "star_rating": "Giving a rating or score",
            "toggle": "Turning something on or off",
            "file_upload": "Attaching or uploading a file",
            "text_field": "Free text with none of the above",
        },
    ),
    "needs_time": Noul(instructions="Does the request involve a specific time of day, not just a date?"),
    "needs_confirm": Noul(instructions="Is this an action that should ask the user to confirm before running?"),
    "is_recurring": Noul(instructions="Does the request describe something repeating or recurring?"),
    "urgency": Score(
        instructions="How urgent does the request sound?",
        criteria=["Whenever", "Soon", "Right now"],
    ),
}

# How each control renders. Pure presentation, driven by the typed answers.
RENDER = {
    "datetime_picker": lambda f: f"[ 📅 date picker ]{'  [ ⏰ time ]' if f['needs_time'] else ''}"
                                 f"{'  [ 🔁 repeat ]' if f['is_recurring'] else ''}",
    "slider":          lambda f: "[ 0 |————●————| 100 ]",
    "color_picker":    lambda f: "[ 🎨 ▇▇▇ color swatches ]",
    "location_search": lambda f: "[ 📍 search places...        ]",
    "star_rating":     lambda f: "[ ☆ ☆ ☆ ☆ ☆ ]",
    "toggle":          lambda f: "[ OFF (●  ) ON ]",
    "file_upload":     lambda f: "[ ⬆ drop a file or browse ]",
    "text_field":      lambda f: "[ type here...                ]",
}


def shapeshift(text: str, client: TypeSafeClient) -> dict:
    r = client.system_one(state=text, questions=QUESTIONS)
    flags = {k: r.nouls[k].noul > 0.5 for k in ("needs_time", "needs_confirm", "is_recurring")}
    ctrl = r.choices["control"]
    return {"control": ctrl.choice, "confidence": ctrl.confidence,
            "flags": flags, "urgency": r.scores["urgency"].score}


INPUTS = [
    "remind me to call the dentist next tuesday at 3pm",
    "set the thermostat to a comfortable temperature",
    "pick an accent color for my profile",
    "where should we meet for lunch?",
    "how would you rate your support experience today?",
    "turn on dark mode",
    "attach your resume to the application",
    "every morning, send me the weather",
]


def main() -> None:
    rule("SHAPESHIFT  ·  the input control builds itself from your words")
    with TypeSafeClient() as client:
        for text in INPUTS:
            d = shapeshift(text, client)
            widget = RENDER[d["control"]](d["flags"])
            extras = []
            if d["flags"]["needs_confirm"]:
                extras.append("+ confirm step")
            if d["urgency"] >= 1.5:
                extras.append("! urgent styling")
            extra = ("   " + ", ".join(extras)) if extras else ""
            print(f'\n  you type:  "{text}"')
            print(f"  it becomes: {widget}{extra}")
            print(f"              control={d['control']}  confidence {bar(d['confidence'])} {d['confidence']:.2f}")
    rule("THE IDEA")
    print("  Same box, eight different interfaces, chosen by meaning. The model picked the")
    print("  control and the feature flags; code rendered them. Low confidence is your cue")
    print("  to fall back to a plain text field instead of guessing a wrong widget.\n")


if __name__ == "__main__":
    main()
