# Interactive walkthrough notebooks

24 projects, each a **self-contained walkthrough** you can present live: every line of code
is in a visible cell, explained in order. You see the problem, then the Jev questions, the raw
Jev response, the decision logic in plain Python, a run on examples, an HTML/ipywidgets UI,
"try it yourself", and a recap with exercises.

```bash
uv sync
cp .env.example .env        # add TYPESAFE_API_KEY (and OPENAI_API_KEY for 06 and 09)
uv run jupyter lab apps/    # or open the folder in VS Code and pick the .venv kernel
```

Run each notebook **top to bottom** (Run All). If you hit `NameError`, the kernel restarted
(switching kernels does this), so just Run All again. The cells are pre-run so outputs show on
GitHub; the "Try it yourself" boxes need a live kernel.

## The original nine

| Notebook | What you drive |
| --- | --- |
| `01_emoji_picker_app.ipynb` | type a phrase, the matching emoji group grows and rises |
| `02_mood_to_color_app.ipynb` | type a feeling, a blended color swatch appears |
| `03_shapeshift_app.ipynb` | type an intent, a real input control (date/slider/color/rating) builds itself |
| `04_content_blocker_app.ipynb` | paste a post, see it hidden / blurred / dimmed / shown |
| `05_tool_firewall_app.ipynb` | type a tool call, get ALLOW / REVIEW / BLOCK |
| `06_model_router_app.ipynb` | ask anything, see which OpenAI model it routed to and the answer |
| `07_jev_evals_app.ipynb` | grade answers into a scorecard, hallucinations flagged |
| `08_rag_reranker_app.ipynb` | type a query, watch the right passage jump to rank 1 |
| `09_semantic_find_app.ipynb` | ask a help page, get the highlighted line and a chat answer |

## The 18 practical use cases

Built from [18 practical Jev use cases for AI agents](https://huggingface.co/blog/karmen-beatapi/18-practical-jev-use-cases-for-ai-agents).
Each follows the article's guidance: exact rules first, Jev for the ambiguous part, thresholds in code,
and always a "none" or human-review path.

| # | Use case | Notebook |
| --- | --- | --- |
| 1 | Verify that an agent actually finished | `10_agent_completion_check.ipynb` |
| 2 | Select a tool, then authorize it | `11_tool_selection.ipynb` |
| 3 | Route to a model, code path or person | `06_model_router_app.ipynb` |
| 4 | Pick a skill or sub-agent | `12_skill_router.ipynb` |
| 5 | Confidence gate in a workflow | `13_confidence_gate.ipynb` |
| 6 | Filter RAG passages before generation | `14_rag_passage_filter.ipynb` |
| 7 | Rerank a short candidate set | `08_rag_reranker_app.ipynb` |
| 8 | Check a citation against a claim | `15_citation_check.ipynb` |
| 9 | Align two entity records | `16_entity_matching.ipynb` |
| 10 | Screen LLM input and output | `17_llm_io_guard.ipynb` (also `04`, `05`) |
| 11 | Apply a fixed evaluation rubric | `07_jev_evals_app.ipynb` |
| 12 | Flag semantic issues in code changes | `18_code_review_rules.ipynb` |
| 13 | Check a document against a checklist | `19_document_checklist.ipynb` |
| 14 | Triage a support inbox | `20_support_triage.ipynb` |
| 15 | Classify within a large taxonomy | `21_taxonomy_classifier.ipynb` |
| 16 | Select among extracted candidates | `22_span_selection.ipynb` |
| 17 | Combine several scored dimensions | `23_multi_score_prioritizer.ipynb` |
| 18 | Semantic features for a classic ML model | `24_semantic_features.ipynb` |

(`_ui.py` is the older import-only UI layer used by nothing in this folder now; the terminal
versions of 01–09 still live in `../live-builds` and `../gallery`.)
