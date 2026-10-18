# Interactive app notebooks

The nine projects as **runnable UIs inside Jupyter**. Each notebook has a text box
(or button) you drive live, and renders real HTML: date pickers, sliders, color
swatches, relevance-sized emoji, highlighted search, a styled feed, colored
verdict badges. Same core logic as the scripts in `../live-builds` and
`../gallery` (imported from `_ui.py`), just with a face on it.

```bash
uv sync
export TYPESAFE_API_KEY="your-typesafe-key"
export OPENAI_API_KEY="your-openai-key"     # for the router and semantic find
uv run jupyter lab apps/
```

Open any notebook, Run All, then type into the "Try it yourself" box.

| Notebook | What you drive |
| --- | --- |
| `01_emoji_picker_app.ipynb` | type a phrase, the matching emoji group grows and rises |
| `02_mood_to_color_app.ipynb` | type a feeling, a blended color swatch appears |
| `03_shapeshift_app.ipynb` | type an intent, a real input control (date/slider/color/rating) builds itself |
| `04_content_blocker_app.ipynb` | paste a post, see it hidden / blurred / dimmed / shown |
| `05_tool_firewall_app.ipynb` | type a tool call, get ALLOW / REVIEW / BLOCK |
| `06_model_router_app.ipynb` | ask anything, see which OpenAI model it routed to and the answer |
| `07_jev_evals_app.ipynb` | grade the eval set into a scorecard, hallucinations flagged |
| `08_rag_reranker_app.ipynb` | type a query, watch the right passage jump to rank 1 |
| `09_semantic_find_app.ipynb` | ask a help page, get the highlighted line and a chat answer |

The example cells are pre-run so the notebooks show output on GitHub; the "Try it
yourself" cells need a live kernel (`jupyter lab`). `_ui.py` holds every renderer
and the shared Jev + OpenAI clients, so the notebooks stay a few cells each.
