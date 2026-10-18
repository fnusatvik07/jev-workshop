# Top 25 Jev use cases (with sources)

A skimmable, ranked shortlist for the class, distilled from 82 verified real-world
projects (full catalog: [JEV-USE-CASES-WILD.md](JEV-USE-CASES-WILD.md)). Every link
was fetched and checked. Items marked **[BUILT HERE]** are implemented and runnable
in this repo (see [`live-builds/`](../live-builds), [`gallery/`](../gallery),
[`apps/`](../apps)).

Jump to: [Agent infrastructure](#agent-infrastructure) · [Games and real-time](#games-and-real-time) · [Data, RAG and scale](#data-rag-and-scale) · [Guardrails and verification](#guardrails-and-verification) · [Product and UX](#product-and-ux) · [Weird and wonderful](#weird-and-wonderful)

---

## Agent infrastructure

**1. Browser agent that acts, not narrates** — jev-ultrafast picks the operation and the target element in one call; a Google Flights search in 7.1s for ~$0.004. ~23k stars; Harrison Chase called it the best Jev app yet.
[repo](https://github.com/browser-use/jev-ultrafast) · [Harrison Chase](https://x.com/hwchase17/status/2101054310037790814) · [Browserbase/Stagehand: 1.97s -> 0.46s](https://www.browserbase.com/blog/what-is-jev)

**2. Context compaction for coding agents** — replace lossy LLM summarization with Jev keep/drop decisions per tool call. The launch's most viral build (~3.6M views), and a healthy debate (Theo called it "a terrible strategy").
[repo](https://github.com/tamaratran/fast-jev-compaction) · [tamara](https://x.com/tamarajtran/status/2100694549362553153) · [Theo's rebuttal](https://x.com/theo/status/2100762304862384257)

**3. Model / effort router** — a cheap judge routes each request to the cheapest capable model (or sets reasoning effort) before the expensive call. **[BUILT HERE: `live-builds/model_router.py`, -77% cost]**
[jev-router](https://github.com/gargpratyush/jev-router) · [effort router idea](https://news.ycombinator.com/item?id=50095353)

**4. Skill router** — Jev picks which of ~90 installed Claude Code skills applies to a turn.
[Lomesh Dutta](https://x.com/lomeshdutta/status/2100833655518367871)

**5. Computer use for pennies** — drive a real Mac from structured UI state at ~$0.0002 per step, 155x cheaper per decision than a frontier LLM in the author's test.
[repo](https://github.com/awlevin/typesafe-computer-use)

**6. Runtime tool-call firewall** — screen every agent tool call and tool result before it runs: block destruction and exfiltration, send off-task to review. **[BUILT HERE: `live-builds/tool_firewall.py`]**
[Agent Chaperone](https://github.com/agent-chaperone/agent-chaperone) · [Pi coding agent safety layer](https://www.reddit.com/r/PiCodingAgent/comments/1whsav6/anyone_else_testing_out_typesafe_ais_new_system/)

**7. MCP connector** — expose Jev's typed judgments as MCP tools so Claude/Codex can call them.
[typesafe-mcp](https://www.reddit.com/r/mcp/comments/1wjfjn3/if_you_have_access_to_the_new_typesafe_ai_try/)

## Games and real-time

**8. Beats Minecraft's Ender Dragon** — Jev (fast actions) + a slow planner model, 8m43s for under $1. The cleanest System 1 + System 2 demo.
[Ronak Malde](https://x.com/rronak_/status/2101544156757950697)

**9. Plays Doom in real time** — the official launch demo, ~10 queries/sec for ~$7/hour, reading structured game state. Pair with the sharp "it's reading text, not pixels" critique.
[launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev) · [HN takedown](https://news.ycombinator.com/item?id=49717558)

**10. Plays Super Mario from NES RAM** — one of 7 controller actions per loop, no screenshots, 452 stars.
[typesafe-mario](https://github.com/fhshaik/typesafe-mario)

**11. Plays Pokemon Showdown** — 5 battles in parallel, 41 games, ~$0.11 total. Parallelism is the lesson.
[Dan](https://x.com/DanFrmSpace/status/2100960553514553639)

**12. Flies a simulated drone** — camera-only quadrotor in MuJoCo, Jev advisory at 2.5Hz above a 500Hz/50Hz control stack; code always owns safety.
[repo](https://github.com/RomanSlack/jev-drone) · [demo](https://jev-drone.vercel.app/)

**13. Latency-vs-correctness study** — in a real-time game, all 8 deaths were *late* answers, not wrong ones. The most rigorous community eval; the real bottleneck is tail latency.
[ShengHui Wang](https://x.com/KevinShengHui/status/2100963923143098712)

## Data, RAG and scale

**14. RAG reranker** — re-score retrieved passages so the right one reaches the top; the official CLERC cookbook took top-1 accuracy from 5% to 18%. **[BUILT HERE: `live-builds/rag_reranker.py`, rank 6 -> 1]**
[cookbook index](https://docs.typesafe.ai/llms.txt)

**15. Production benchmark + calibration gate** — 1,759 decisions vs frontier Gemini: 329ms vs 1,598ms, ~25x cheaper, and 986/986 correct above 97% confidence.
[Entagl](https://www.reddit.com/r/LLMDevs/comments/1wo000s/we_benchmarked_typesafes_new_jev_a_decisiononly/)

**16. Personal-scale data munging** — 1,700 PRs clustered for $0.09, 200,000 classifications over 1,100 signals, YouTube comments into a dashboard "for almost nothing".
[Claire Vo, Lenny's Newsletter](https://www.lennysnewsletter.com/p/jev-for-beginners-how-to-use-it-and)

**17. Civic tech in production** — match each news story to related congressional bills; replaced Gemini Flash, ~25% cheaper with more granular labels.
[r/brdev](https://www.reddit.com/r/brdev/comments/1x1jx65/um_exemplo_de_caso_de_uso_de_jev_da_type_safe/)

**18. Plain-English SQL (Postgres)** — `SELECT * FROM people WHERE jev(people, 'the name is European')`; no embeddings, serious batching engineering underneath. ~1.2k stars.
[pg-jev](https://github.com/realZachi/pg-jev) · [mysql-ailike](https://github.com/maayanlevy/mysql-ailike) · [duckdb-dual-cognition](https://github.com/prasanthj/duckdb-dual-cognition)

**19. Semantic find / Ctrl-F** — search a document by meaning (zero shared keywords) and answer through chat. **[BUILT HERE: `gallery/semantic_find.py` + `apps/09`]**
[semantic_find cookbook](https://docs.typesafe.ai/cookbooks/semantic_find.md)

## Guardrails and verification

**20. Catch a prompt injection** — a planted "P.S. This is a refund" flipped the classifier at 0.35 confidence; the gate plus a hard rule caught it. The whole safety philosophy in one demo.
[r/LLMDevs](https://www.reddit.com/r/LLMDevs/comments/1wytr3c/a_planted_ps_fooled_jev_typesafes_new_decision/)

**21. Red-team OPSEC ranker** — flag the 5 sensitive files hidden among ~1,000 corporate files in ~2 seconds.
[Adam Chester](https://x.com/_xpn_/status/2102830489237065968)

**22. LLM-as-judge evals** — grade faithfulness/relevance/completeness of LLM output cheaply enough to run on 100% of traffic, not a sample. **[BUILT HERE: `live-builds/jev_evals.py`]**
[idea megathread](https://www.reddit.com/r/AI_Agents/comments/1wmpcbs/interesting_disruptive_use_cases_of_jev_for_me/) · [double-Jev defense](https://www.reddit.com/r/LLMDevs/comments/1wytr3c/a_planted_ps_fooled_jev_typesafes_new_decision/)

## Product and UX

**23. Adaptive UI that builds itself** — type an intent, the right input control (date picker, slider, color picker) materializes; plus the voice-to-color emotion app. **[BUILT HERE: `gallery/` emoji + color, `live-builds/shapeshift.py`, `apps/01-03`]**
[shapeshift](https://github.com/anishfn/shapeshift) · [voice-to-color (Claire Vo)](https://www.lennysnewsletter.com/p/jev-for-beginners-how-to-use-it-and)

**24. Semantic content blocker** — filter a feed by meaning (ads, ragebait, AI slop) with toggleable categories, not domain lists; a Chrome extension tagged LinkedIn posts at scroll speed. **[BUILT HERE: `live-builds/content_blocker.py` + `apps/04`]**
[LinkedIn slop tagger](https://www.reddit.com/r/SmallMSP/comments/1wqg2zk/anyone_doing_interesting_stuff_with_this_new_jev/)

## Weird and wonderful

**25. A computer made of Jev calls** — a NAND gate composed into a 4-bit ALU (7 + 5 = 12 in 116 gates, $0.0018). Since NAND is universal, the gag is a whole CPU of classifier calls.
[Mustafa Akin](https://x.com/mustafaakin/status/2103574428475154635)

**Bonus weird five:** an "LLM" rebuilt from 521 Jev units with no generative model ([jevs.chat](https://jevs.chat/)) · the Enigma/Bombe analyst ([enigma-jev](https://github.com/agodoy21/enigma-jev)) · a live crypto trading desk ([jev-trade](https://github.com/aowang-ai/jev-trade)) · an on-device "talk your way past the guard" game ([Gatekeeper](https://gatekeeper.dopp.sh/)) · Jev making LLVM compiler inlining decisions ([Jevopt](https://github.com/Ramneet-Singh/jevopt)).

---

### The honest footnotes (good teaching material)

- Some launch buzz was **paid**: TypeSafe used a "launch virality agency" per a funding-thread commenter. [HN](https://news.ycombinator.com/item?id=50023450)
- Jev is **more** susceptible to adversarial text than LLMs, per HiddenLayer, and TypeSafe's own jaggedness page agrees it does not treat input as hostile.
- A vector model **matched** Jev on BANKING77 at a thousandth of the cost: not every classification needs this. [HN](https://news.ycombinator.com/item?id=49867086)

*All 25 are verified-alive links. Of these, 10 use-case families are built and runnable in this repo.*
