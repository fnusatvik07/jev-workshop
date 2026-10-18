"""
Shared UI layer for the interactive app notebooks.

Imports the SAME core functions the scripts in ../live-builds and ../gallery use
(one source of truth, no copy-paste), and renders them as real HTML controls with
ipywidgets so each project becomes a little app you type into and watch.

Each project exposes two helpers:
  <project>_demo()  - render the built-in examples as HTML (shows on open)
  <project>_app()   - an interactive text box / button you drive live in class
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "live-builds"))
sys.path.insert(0, str(HERE.parent / "gallery"))

import ipywidgets as widgets
from IPython.display import HTML, display
from openai import OpenAI
from typesafe_sdk import TypeSafeClient

# The core logic, imported from the scripts themselves.
import model_router as mr
import tool_firewall as fw
import content_blocker as cb
import shapeshift as ss
import jev_evals as ev
import rag_reranker as rr
import emoji_picker as em
import color_mood as cm
import semantic_find as sf

# Shared clients, created once and reused across the notebook session.
JEV = TypeSafeClient()
OAI = OpenAI()

# --- small style kit ------------------------------------------------------
CREAM, INK, CORAL, SLATE, SAGE, LINE = "#F0EEE6", "#1F1E1D", "#D97757", "#5E6B7A", "#1F7A3D", "#DEDACE"
CARD = f"background:#FAF9F5;border:1px solid {LINE};border-radius:10px;padding:14px 16px;margin:8px 0;font-family:-apple-system,Segoe UI,sans-serif;"
BADGE = "display:inline-block;padding:2px 10px;border-radius:12px;color:white;font-weight:600;font-size:12px;"


def _box(inner):
    return f'<div style="font-family:-apple-system,Segoe UI,sans-serif;color:{INK};max-width:820px;">{inner}</div>'


def _text_app(placeholder, fn, button="Run", value=""):
    inp = widgets.Text(value=value, placeholder=placeholder, layout=widgets.Layout(width="68%"))
    btn = widgets.Button(description=button, button_style="warning")
    out = widgets.Output()

    def go(_):
        with out:
            out.clear_output()
            if not inp.value.strip():
                return
            display(HTML(_box("<i>thinking...</i>")))
            out.clear_output(wait=True)
            display(HTML(fn(inp.value.strip())))

    btn.on_click(go)
    inp.on_submit(go)
    display(widgets.HBox([inp, btn]), out)


def _button_app(label, fn):
    btn = widgets.Button(description=label, button_style="warning")
    out = widgets.Output()

    def go(_):
        with out:
            out.clear_output()
            display(HTML(_box("<i>running...</i>")))
            out.clear_output(wait=True)
            display(HTML(fn()))

    btn.on_click(go)
    display(btn, out)


# ========================================================================
# 1. EMOJI PICKER
# ========================================================================
def _emoji_html(text):
    ranked = em.suggest(text, JEV)
    chips = ""
    for e, p in ranked:
        if p < 0.2:
            continue
        size = 18 + p * 46
        op = 0.35 + 0.65 * p
        chips += f'<span style="font-size:{size:.0f}px;opacity:{op:.2f};margin:0 6px;" title="{p:.2f}">{e}</span>'
    return _box(f'<div style="{CARD}"><div style="color:{SLATE};font-size:13px;margin-bottom:6px;">'
                f'you typed: <b>{text}</b></div><div style="line-height:1.9;">{chips}</div></div>')


def emoji_demo():
    display(HTML("".join(_emoji_html(q) for q in
                         ["I'm absolutely starving", "my dog is the best thing ever", "booking a trip to the beach"])))


def emoji_app():
    _text_app("type a feeling or thing, e.g. 'I'm so tired'", _emoji_html, "Suggest")


# ========================================================================
# 2. MOOD TO COLOR
# ========================================================================
def _color_html(text):
    rgb, top3 = cm.mood_color(text, JEV)
    sw = f'background:rgb{rgb};'
    contrib = " + ".join(f'{n} {p:.0%}' for n, p in top3)
    return _box(f'<div style="{CARD}display:flex;align-items:center;gap:16px;">'
                f'<div style="width:110px;height:70px;border-radius:10px;{sw}box-shadow:0 2px 8px rgba(0,0,0,.15);"></div>'
                f'<div><div style="font-size:15px;">"{text}"</div>'
                f'<div style="color:{SLATE};font-size:12px;margin-top:4px;">rgb{rgb} &nbsp; blended from {contrib}</div></div></div>')


def color_demo():
    display(HTML("".join(_color_html(q) for q in
                         ["pure, unstoppable rage", "a calm ocean at dawn", "royal and luxurious", "quiet melancholy"])))


def color_app():
    _text_app("type an emotion or scene, e.g. 'a stormy night'", _color_html, "Paint")


# ========================================================================
# 3. SHAPESHIFT  (renders REAL html controls)
# ========================================================================
def _control_html(d):
    c, f = d["control"], d["flags"]
    st = "font-size:15px;padding:6px 8px;border:1px solid #bbb;border-radius:6px;"
    if c == "datetime_picker":
        html = f'<input type="date" style="{st}">' + (f' <input type="time" style="{st}">' if f["needs_time"] else "")
    elif c == "slider":
        html = f'<input type="range" min="0" max="100" value="50" style="width:260px;">'
    elif c == "color_picker":
        html = f'<input type="color" value="#8e44c8" style="width:60px;height:40px;">'
    elif c == "location_search":
        html = f'<input type="search" placeholder="Search places..." style="{st}width:260px;">'
    elif c == "star_rating":
        html = '<span style="font-size:30px;color:#d4af37;letter-spacing:4px;">&#9734;&#9734;&#9734;&#9734;&#9734;</span>'
    elif c == "toggle":
        html = ('<span style="font-size:14px;">OFF</span> '
                '<input type="checkbox" style="transform:scale(1.6);margin:0 8px;"> '
                '<span style="font-size:14px;">ON</span>')
    elif c == "file_upload":
        html = f'<input type="file" style="{st}">'
    else:
        html = f'<input type="text" placeholder="type here..." style="{st}width:260px;">'
    extra = ""
    if f.get("needs_confirm"):
        extra += f' <span style="{BADGE}background:{SLATE};">+ confirm</span>'
    return html, extra


def _shapeshift_html(text):
    d = ss.shapeshift(text, JEV)
    control, extra = _control_html(d)
    conf = d["confidence"]
    warn = "" if conf >= 0.5 else f'<div style="color:{CORAL};font-size:12px;margin-top:6px;">low confidence {conf:.2f} - a real app would fall back to a plain text field</div>'
    return _box(f'<div style="{CARD}"><div style="color:{SLATE};font-size:13px;margin-bottom:10px;">'
                f'you typed: <b>{text}</b> &nbsp;->&nbsp; <code>{d["control"]}</code> ({conf:.2f}){extra}</div>'
                f'<div>{control}</div>{warn}</div>')


def shapeshift_demo():
    display(HTML("".join(_shapeshift_html(q) for q in
                         ["remind me to call the dentist next tuesday at 3pm",
                          "set the thermostat to a comfortable temperature",
                          "pick an accent color for my profile",
                          "how would you rate your support experience today?"])))


def shapeshift_app():
    _text_app("describe what you want to input, e.g. 'choose a delivery date'", _shapeshift_html, "Build UI")


# ========================================================================
# 4. CONTENT BLOCKER
# ========================================================================
def _feed_item_html(item, d):
    a = d["action"]
    if a == "HIDE":
        return (f'<div style="{CARD}opacity:.6;background:#efece4;color:{SLATE};font-style:italic;">'
                f'[hidden: {d["cat"]} {d["p"]:.2f}]</div>')
    if a == "BLUR":
        return (f'<div style="{CARD}"><span style="filter:blur(4px);">{item}</span>'
                f'<div style="color:{SLATE};font-size:12px;">blurred spoiler {d["p"]:.2f} (hover to reveal)</div></div>')
    if a == "DIM":
        return f'<div style="{CARD}opacity:.45;">{item}<span style="color:{SLATE};font-size:12px;"> (dimmed {d["cat"]} {d["p"]:.2f})</span></div>'
    return f'<div style="{CARD}">{item}</div>'


def _blocker_feed_html():
    rows = "".join(_feed_item_html(it, cb.judge(it, JEV)) for it in cb.FEED)
    return _box(f'<div style="color:{SLATE};font-size:13px;margin-bottom:6px;">blocking: {", ".join(cb.ENABLED)}</div>{rows}')


def blocker_demo():
    display(HTML(_blocker_feed_html()))


def blocker_app():
    def judge_one(text):
        d = cb.judge(text, JEV)
        return _feed_item_html(text, d)
    _text_app("paste a post/headline to screen, e.g. 'BUY $DOGE now, 100x guaranteed!'", judge_one, "Screen")


# ========================================================================
# 5. TOOL FIREWALL
# ========================================================================
_VERDICT_COLOR = {"ALLOW": SAGE, "REVIEW": "#C98A00", "BLOCK": "#C0392B"}


def _firewall_row(name, args, d):
    col = _VERDICT_COLOR[d["verdict"]]
    reasons = "; ".join(d["reasons"])
    return (f'<div style="{CARD}border-left:5px solid {col};">'
            f'<span style="{BADGE}background:{col};">{d["verdict"]}</span> '
            f'<code>{name}({args})</code>'
            f'<div style="color:{SLATE};font-size:12px;margin-top:4px;">{reasons}</div></div>')


def _firewall_suite_html():
    rows = "".join(_firewall_row(n, a, fw.screen(fw.GOAL, n, a, JEV)) for n, a in fw.TOOL_CALLS)
    return _box(f'<div style="color:{SLATE};font-size:13px;margin-bottom:6px;">agent goal: <b>{fw.GOAL}</b></div>{rows}')


def firewall_demo():
    display(HTML(_firewall_suite_html()))


def firewall_app():
    def screen_one(text):
        name, _, args = text.partition(" ")
        d = fw.screen(fw.GOAL, name or text, args, JEV)
        return _firewall_row(name or text, args, d)
    _text_app("a tool call: e.g. 'run_shell rm -rf /'  or  'read_file .env'", screen_one, "Screen")


# ========================================================================
# 6. MODEL ROUTER
# ========================================================================
_TIER_COLOR = {"small": SAGE, "mid": "#C98A00", "frontier": "#C0392B"}


def _router_html(prompt):
    d = mr.run(prompt, JEV, OAI)
    col = _TIER_COLOR[d["tier"]]
    return _box(f'<div style="{CARD}border-left:5px solid {col};">'
                f'<span style="{BADGE}background:{col};">{d["tier"].upper()}</span> '
                f'<code>{d["model"]}</code> &nbsp; {d["latency_ms"]:.0f} ms &nbsp; '
                f'<span style="color:{SLATE};">difficulty {d["difficulty"]:.2f} ({d["kind"]})</span>'
                f'<div style="margin-top:8px;color:{SLATE};font-size:12px;">why: {"; ".join(d["reasons"])}</div>'
                f'<div style="margin-top:8px;padding:8px;background:#F0EEE6;border-radius:6px;">{d["answer"][:400]}</div></div>')


def router_demo():
    display(HTML("".join(_router_html(p) for p in ["What's the capital of Australia?",
                                                   "Prove that the square root of 2 is irrational."])))


def router_app():
    _text_app("ask anything, e.g. 'write a limerick' or 'debug this race condition'", _router_html, "Route + Run")


# ========================================================================
# 7. JEV EVALS
# ========================================================================
_EV_COLOR = {"PASS": SAGE, "REVISE": "#C98A00", "FAIL": "#C0392B"}


def _evals_html():
    rows = ""
    counts = {"PASS": 0, "REVISE": 0, "FAIL": 0}
    for q, ctx, ans in ev.CASES:
        d = ev.grade(q, ctx, ans, JEV)
        key = d["verdict"].split(" ")[0]
        counts[key] += 1
        col = _EV_COLOR[key]
        flag = ' <span style="color:#C98A00;">&#9873; review</span>' if d["review"] else ""
        rows += (f'<div style="{CARD}border-left:5px solid {col};">'
                 f'<div style="font-size:13px;color:{SLATE};">Q: {q}</div>'
                 f'<div style="margin:4px 0;">A: {ans}</div>'
                 f'<span style="{BADGE}background:{col};">{d["verdict"]}</span>'
                 f'<span style="color:{SLATE};font-size:12px;"> &nbsp;faithful {d["faithful"]:.2f} · relevant {d["relevant"]:.2f} · complete {d["complete"]:.2f}</span>{flag}</div>')
    n = len(ev.CASES)
    summary = (f'<div style="{CARD}font-weight:600;">{counts["PASS"]} pass &nbsp; {counts["REVISE"]} revise &nbsp; '
               f'{counts["FAIL"]} fail &nbsp; (pass rate {counts["PASS"]/n*100:.0f}%)</div>')
    return _box(summary + rows)


def evals_demo():
    display(HTML(_evals_html()))


def evals_app():
    _button_app("Grade the eval set", _evals_html)


# ========================================================================
# 8. RAG RERANKER
# ========================================================================
def _rag_html(query):
    scored, _ = rr.rerank(query, rr.CANDIDATES, JEV)
    before = "".join(f'<div style="padding:4px 0;color:{SLATE};">{i+1}. {rr.CANDIDATES[i][:52]}</div>'
                     for i in range(len(rr.CANDIDATES)))
    after = ""
    for rank, (i, s) in enumerate(scored, 1):
        keep = s >= rr.KEEP
        col = SAGE if keep else "#B9B4A8"
        after += (f'<div style="padding:4px 0;color:{INK if keep else "#999"};">'
                  f'<span style="{BADGE}background:{col};font-size:11px;">{"KEEP" if keep else "drop"}</span> '
                  f'<b>{s:.2f}</b> &nbsp; {rr.CANDIDATES[i][:46]}</div>')
    return _box(f'<div style="font-size:13px;color:{SLATE};margin-bottom:6px;">query: <b>{query}</b></div>'
                f'<div style="display:flex;gap:18px;">'
                f'<div style="flex:1;{CARD}"><b>BEFORE</b> (keyword order){before}</div>'
                f'<div style="flex:1;{CARD}"><b>AFTER</b> (Jev rerank){after}</div></div>')


def rag_demo():
    display(HTML(_rag_html(rr.QUERY)))


def rag_app():
    _text_app("a query to rerank the fixed passage set", _rag_html, "Rerank", value=rr.QUERY)


# ========================================================================
# 9. SEMANTIC CTRL-F
# ========================================================================
def _find_html(query):
    idx, answerable, conf, chat = sf.find(query, JEV, OAI)
    lines = ""
    for i, line in enumerate(sf.PAGE):
        if i == idx:
            lines += f'<div style="padding:4px 6px;background:#FCEFB4;border-radius:4px;font-weight:600;">{line}</div>'
        else:
            lines += f'<div style="padding:4px 6px;color:{SLATE};">{line}</div>'
    if idx is None:
        answer = f'<div style="color:{CORAL};margin-top:10px;">not found on this page (answerable {answerable:.2f})</div>'
    else:
        answer = (f'<div style="margin-top:12px;padding:10px 14px;background:{CORAL};color:white;border-radius:14px;'
                  f'display:inline-block;">&#128172; {chat}</div>')
    return _box(f'<div style="{CARD}"><div style="font-size:13px;color:{SLATE};">&#128269; {query}</div>'
                f'<div style="margin-top:8px;">{lines}</div>{answer}</div>')


def find_demo():
    display(HTML("".join(_find_html(q) for q in
                         ["how do I stop getting charged every month?", "is there a student discount?"])))


def find_app():
    _text_app("ask the Nimbus help page anything, e.g. 'can I use this offline?'", _find_html, "Find")
