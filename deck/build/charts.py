"""Generate the deck's charts in the house palette."""

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "font.family": "Helvetica Neue",
    "text.color": "#1F1E1D",
    "axes.edgecolor": "#DEDACE",
    "axes.labelcolor": "#1F1E1D",
    "xtick.color": "#5E6B7A",
    "ytick.color": "#5E6B7A",
    "figure.facecolor": "#F0EEE6",
    "axes.facecolor": "#F0EEE6",
    "savefig.facecolor": "#F0EEE6",
    "axes.grid": False,
})

CREAM, INK, CORAL, CLAY, SLATE, SAGE, MUTED = (
    "#F0EEE6", "#1F1E1D", "#D97757", "#BD5D3A", "#5E6B7A", "#7D8B6A", "#8A8780",
)
OUT = "../assets"


def save(fig, name):
    fig.savefig(f"{OUT}/{name}", dpi=220, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("wrote", name)


# 1. Price comparison, log scale ------------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 3.6))
labels = ["Jev 1.13 / 1.14", "small LLM tier", "mid LLM tier", "frontier LLM tier"]
prices = [0.042, 0.25, 3.0, 15.0]
colors = [CORAL, SLATE, SLATE, SLATE]
bars = ax.barh(labels[::-1], prices[::-1], color=colors[::-1], height=0.58)
ax.set_xscale("log")
ax.set_xlim(0.01, 40)
for bar, price in zip(bars, prices[::-1]):
    ax.text(price * 1.25, bar.get_y() + bar.get_height() / 2, f"${price:,.3f}".rstrip("0").rstrip("."),
            va="center", fontsize=12, fontweight="bold", color=INK)
ax.set_xlabel("input price, $ per million tokens (log scale)", fontsize=11)
ax.tick_params(labelsize=12)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.set_title("Jev output tokens are free; LLM tiers are indicative published input prices, Oct 2026",
             fontsize=9.5, color=MUTED, loc="left", pad=8)
save(fig, "price_compare.png")

# 2. Batching experiment (our live measurement) ---------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.2))
for ax, (title, pair, unit) in zip(axes, [
    ("wall-clock seconds", (0.83, 0.12), "s"),
    ("input tokens billed", (2840, 467), ""),
]):
    bars = ax.bar(["8 separate calls", "1 batched call"], pair, color=[SLATE, CORAL], width=0.52)
    for b, v in zip(bars, pair):
        label = f"{v:,.2f}{unit}" if v < 10 else f"{v:,.0f}"
        ax.text(b.get_x() + b.get_width() / 2, v * 1.03, label, ha="center", fontsize=12,
                fontweight="bold", color=INK)
    ax.set_title(title, fontsize=12, color=INK)
    ax.set_ylim(0, max(pair) * 1.22)
    ax.tick_params(labelsize=11)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
fig.suptitle("Same 8-question checklist, same answers: measured live for this workshop",
             fontsize=10, color=MUTED, x=0.02, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.93])
save(fig, "batching.png")

# 3. Calibration concept ---------------------------------------------------
fig, ax = plt.subplots(figsize=(4.4, 3.9))
xs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
ax.plot([0, 1], [0, 1], color=CORAL, lw=2.5, label="calibrated: P(correct) = stated p")
ax.plot(xs, [0.0, 0.33, 0.52, 0.66, 0.78, 0.86], color=SLATE, lw=2.5, ls="--",
        label="overconfident model")
ax.fill_between([0, 1], [0, 1], [0.0, 0.86], color=SLATE, alpha=0.06)
ax.set_xlabel("probability the model reports", fontsize=11)
ax.set_ylabel("how often it is actually right", fontsize=11)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(fontsize=9.5, frameon=False, loc="upper left")
ax.tick_params(labelsize=10)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
save(fig, "calibration.png")

# 4. Choice probabilities on an ambiguous ticket ---------------------------
fig, ax = plt.subplots(figsize=(4.6, 3.3))
opts = ["returns", "billing", "shipping"]
probs = [0.61, 0.35, 0.04]
bars = ax.bar(opts, probs, color=[CORAL, SLATE, MUTED], width=0.55)
for b, v in zip(bars, probs):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.025, f"{v:.2f}", ha="center",
            fontsize=13, fontweight="bold", color=INK)
ax.set_ylim(0, 1.0)
ax.set_ylabel("probability", fontsize=11)
ax.set_title('"Wrong size AND charged twice": choice = returns, confidence = 0.42',
             fontsize=10, color=MUTED, loc="left", pad=8)
ax.tick_params(labelsize=12)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
save(fig, "choice_dist.png")

# 5. Score distribution: the Safari bug ------------------------------------
fig, ax = plt.subplots(figsize=(4.6, 3.3))
levels = ["0\ncosmetic", "1\nworkaround\nexists", "2\nblocking,\nno workaround"]
probs = [0.0, 0.57, 0.43]
bars = ax.bar(levels, probs, color=[MUTED, CORAL, CLAY], width=0.55)
for b, v in zip(bars, probs):
    if v > 0:
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}", ha="center",
                fontsize=13, fontweight="bold", color=INK)
ax.axvline(x=1.43, color=INK, lw=1.8, ls=":", ymax=0.82)
ax.text(1.43, 0.62, " score = 1.43", fontsize=11, fontweight="bold", color=INK)
ax.set_ylim(0, 0.75)
ax.set_ylabel("probability per level", fontsize=11)
ax.set_title("Safari-only export crash: split between levels 1 and 2, confidence 0.35",
             fontsize=10, color=MUTED, loc="left", pad=8)
ax.tick_params(labelsize=10)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
save(fig, "score_dist.png")

# 6. Noul escalation ladder -------------------------------------------------
fig, ax = plt.subplots(figsize=(7.6, 3.4))
messages = [
    "Thanks, that fixed it!",
    "How do I reset my password?",
    "I need this sorted today, whatever it takes.",
    "Are you a bot?",
    "Any way to speak to someone about my invoice?",
    "I have asked three times. A real person, please?",
]
vals = [0.02, 0.07, 0.26, 0.40, 0.84, 0.99]
colors = [SAGE if v < 0.2 else (CORAL if v > 0.8 else SLATE) for v in vals]
bars = ax.barh(messages[::-1], vals[::-1], color=colors[::-1], height=0.6)
for b, v in zip(bars, vals[::-1]):
    ax.text(v + 0.015, b.get_y() + b.get_height() / 2, f"{v:.2f}", va="center",
            fontsize=11.5, fontweight="bold", color=INK)
ax.axvline(0.2, color=MUTED, lw=1.2, ls=":")
ax.axvline(0.8, color=MUTED, lw=1.2, ls=":")
ax.text(0.09, 5.75, "NO zone", fontsize=9.5, color=MUTED, ha="center")
ax.text(0.5, 5.75, "send to review", fontsize=9.5, color=MUTED, ha="center")
ax.text(0.9, 5.75, "YES zone", fontsize=9.5, color=MUTED, ha="center")
ax.set_xlim(0, 1.12)
ax.set_xlabel('noul value for "Is the customer asking for a human agent?"  (jev-1.13.0, recorded in docs)', fontsize=10)
ax.tick_params(labelsize=10.5)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
save(fig, "noul_ladder.png")

# 7. Proper scoring rule: honesty is the only minimum ----------------------
import numpy as np
fig, ax = plt.subplots(figsize=(5.4, 3.6))
q = np.linspace(0.01, 0.99, 200)
for p_true, color, label in [(0.8, CORAL, "truth: happens 80% of the time"),
                             (0.5, SLATE, "truth: happens 50% of the time")]:
    exp_loss = p_true * (1 - q) ** 2 + (1 - p_true) * q ** 2   # expected Brier loss
    ax.plot(q, exp_loss, color=color, lw=2.5, label=label)
    ax.axvline(p_true, color=color, lw=1.2, ls=":")
    ax.plot([p_true], [p_true * (1 - p_true)], "o", color=color, ms=7)
ax.annotate("minimum sits exactly at the\ntrue probability: report 0.99\nwhen truth is 0.8 and you lose",
            xy=(0.8, 0.16), xytext=(0.33, 0.42), fontsize=9.5, color="#1F1E1D",
            arrowprops=dict(arrowstyle="->", color="#8A8780"))
ax.set_xlabel("probability the model reports", fontsize=11)
ax.set_ylabel("expected training loss (Brier)", fontsize=11)
ax.set_ylim(0, 0.65)
ax.legend(fontsize=9, frameon=False, loc="upper right")
ax.tick_params(labelsize=10)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
save(fig, "proper_scoring.png")
