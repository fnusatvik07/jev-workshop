"""Shared helpers for the live-build demos.

Keeps the demo files themselves short enough to read on a projector:
API-key loading and a couple of pretty-printers live here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


def ensure_key() -> None:
    """Find TYPESAFE_API_KEY in the environment or any .env up the tree."""
    if os.environ.get("TYPESAFE_API_KEY"):
        return
    for folder in [Path.cwd(), *Path.cwd().parents]:
        if (folder / ".env").exists():
            load_dotenv(folder / ".env")
            if os.environ.get("TYPESAFE_API_KEY"):
                return
    raise SystemExit("Set TYPESAFE_API_KEY (get a key at console.typesafe.ai/keys)")


def bar(p: float, width: int = 24) -> str:
    """A unicode progress bar for a 0..1 probability."""
    filled = round(p * width)
    return "█" * filled + "·" * (width - filled)


def rule(title: str = "") -> None:
    line = "─" * 72
    print(f"\n{line}\n{title}\n{line}" if title else line)
