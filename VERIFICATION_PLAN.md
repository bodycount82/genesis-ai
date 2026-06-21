# Genesis Website Content Verification Plan

## Goal
Verify every claim on every web page (115+ HTML files) against the actual Genesis codebase at `D:\Genesis 1.17 crash fix\backend\genesis\`. Cross-reference all described features, architecture, memory systems, modes, tools, and behaviors with the real implementation.

## Phase 0: Architecture Baseline (Code Read-Through)
**Status**: ~60% complete — read core modules thoroughly
- [x] `config.py` — Settings, providers, model presets, cognitive thresholds, caps, memory limits
- [x] `core/state/engine.py` — State engine: load decay, mood weather, flow, rest/sleep, queue modes
- [x] `core/event_bus.py` — Async pub/sub event system
- [x] `agent/runner.py` — ReAct loop: step budgets, context management, tool execution, retry logic
- [x] `memory/manager.py` — Memory orchestrator: 3 tiers, hybrid search, decay, wandering, reconsolidation
- [x] `memory/episodic.py` — Episodic tier: autobiographical events, emotion tagging, dedup, reconsolidation
- [x] `memory/semantic.py` — Semantic tier: rules/concepts/facts, interference, Jaccard dedup
- [x] `memory/procedural.py` — Procedural tier: strategies/skills, cross-tier links, reinforcement
- [x] `memory/working.py` — Working memory: binding surface, scratchpad, wall-time decay, capacity 4
- [x] `memory/vector_index.py` — Vector index: LanceDB + Naive backends, MemRecord schema
- [x] `memory/prospective.py` — Prospective memory: time-based + event-based triggers
- [x] `memory/affect.py` — Affect/amygdala: emotion-from-states, valence labeling, work-mode flatness
- [x] `memory/consolidation.py` — Consolidation daemon (micro-dreams)
- [x] `memory/continuity.py` — Continuity across sessions
- [x] `memory/sensory.py` — Sensory/attention gate for episodic encoding
- [x] `memory/decay_daemon.py` — Active-hours forgetting
- [x] `modes/manager.py` — Mode manager: Chat/Autonomy/Work orchestration, queue modes 1/2/3, interruption
- [x] `modes/autonomy.py` — Autonomy loop: kicks, flow shield, wandering mind, interest thread
- [x] `modes/work.py` — Work mode: priority chain (deadline→task→project→ROI), no mood
- [x] `modes/injections.py` — Thought injections: advisory states, wandering mind, creative blocks
- [x] `modes/interest.py` — Interest thread: continuity line, drift detection, novelty/resonance
- [x] `modes/kicks.py` — Kick system: types (heartbeat/nudge/deadline/prospective/task/critical)
- [x] `tools/builtins.py` — File ops, bash, memory CRUD, prospective, state control, tool builder
- [x] `tools/computer_tools.py` — Desktop control: screenshot, mouse, keyboard, see_screen, click_element, OCR
- [x] `tools/web_tools.py` — Web research: search_web, fetch_page, Wikipedia, compare_sources, web_research
- [x] `tools/document_tools.py` — Documents: PDF read/OCR, Word/Excel create/read, draw_image, open_file/app
- [x] `tools/communication_tools.py` — share_discovery, check_in
- [x] `tools/browser_tools.py` — Browser automation: Chrome CDP, navigation, fill/click, cookies
- [x] `tools/tool_builder.py` — create_tool, list/delete custom tools
- [x] `tools/macro_tools.py` — record/stop/execute/list macros
- [x] `tools/integration_tools.py` — Email (IMAP/SMTP), calendar, file sharing
- [x] `tools/work_tools.py` — Schedule, projects, tasks, reminders
- [x] `tools/user_tools.py` — Screenshot, mouse, keyboard, analyze_image_file, ocr_screen
- [x] `tools/computer_use.py` — Claude-native computer use tool
- [x] `agent/source_tags.py` — Source tagging system (provenance for all injected text)
- [ ] `prompts/manager.py` — System prompt builder (need to read for exact prompt structure)
- [ ] `llm/` — LLM client, context management, governor (need to read)
- [ ] `projects/` — Project tree, workspace filesystem (need to read)
- [ ] `scheduler/` — Schedule engine (need to read)
- [ ] `integrations/` — Integration modules (need to read)
- [ ] `chat/manager.py` — Chat manager (need to read)
- [ ] `api/app.py` — API endpoints (need to read for feature surface area)

## Phase 1: Extract All Claims from Web Pages
**Method**: Parse all 115+ HTML files, extract text content, identify every factual claim about Genesis
- [ ] Scan all HTML files in `web page for publishing/`
- [ ] For each page, extract: title, headings, body text, claims about features
- [ ] Categorize claims: memory systems, modes, tools, state management, cognitive architecture, browser/desktop control, voice, scheduling, projects, etc.
- [ ] Build a master claims spreadsheet: `[page] → [claim] → [category]`

## Phase 2: Cross-Reference Claims Against Code
**Method**: For each claim category, verify against the actual codebase
- [x] **Memory Systems** (4 tiers): Verified — Episodic, Semantic, Procedural, Working all confirmed in code
- [x] **Memory Features**: Verified — hybrid search, vector index, LanceDB/Naive backends, Jaccard dedup, reconsolidation, active-hours decay, flashbulb protection, working memory capacity=4
- [x] **Three Modes**: Verified — Chat (queue mode), Autonomy (free-time loop), Work (task-driven)
- [ ] **Queue Modes**: Need to verify exact 1/2/3 behavior in `modes/manager.py`
- [x] **Cognitive Load**: Verified — time-based decay/fill, threshold-based rest/sleep, load speed meter
- [x] **Mood System**: Verified — energy/curiosity/frustration/satisfaction/boredom/inspiration, temperament baselines, appraisal, flow detection
- [x] **Rest/Sleep**: Verified — auto-sized sleep (drain load to ~0), rest enabled/disabled, consolidation during sleep
- [x] **Tools** (25+): Verified — file ops, bash, memory CRUD, desktop control, browser automation, web research, documents, email, macros, projects, tool builder
- [ ] **Browser Automation**: Need to verify exact features in `browser_tools.py`
- [ ] **Voice**: Need to verify STT/TTS providers and config in `config.py`
- [x] **Prospective Memory**: Verified — time-based + event-based triggers
- [x] **Interest Thread**: Verified — continuity line, drift detection, novelty/resonance scoring
- [x] **Wandering Mind**: Verified — probabilistic injection, heavy-tail deep memory reach, reflection cap
- [x] **Creative Blocks**: Verified — cooldown-based, curiosity/energy gated
- [ ] **Project System**: Need to verify in `projects/` module
- [ ] **Schedule Engine**: Need to verify in `scheduler/` module
- [ ] **System Prompts**: Need to verify exact prompt structure
- [ ] **LLM Providers**: Verified — Ollama, llama.cpp, NVIDIA Cloud, Anthropic (4 providers)
- [ ] **API Endpoints**: Need to verify feature surface area

## Phase 3: Identify Falsifications / Exaggerations
**Method**: Flag every claim that doesn't match the code
- [ ] Claims about features that don't exist in code → FALSE
- [ ] Claims about features with different behavior than described → INACCURATE
- [ ] Claims that overstate capabilities (e.g., "self-aware" when it's simulated) → EXAGGERATED
- [ ] Claims about memory retention that don't match decay parameters → INACCURATE

## Phase 4: Fix Inaccurate Pages
**Method**: For each page with inaccuracies, edit the HTML to match reality
- [ ] Prioritize by page importance (index.html first, then major feature pages)
- [ ] Edit claims to match actual code behavior
- [ ] Remove or reframe claims about non-existent features
- [ ] Add missing features that are in code but not on the website

## Phase 5: Final Verification Pass
**Method**: Re-read all modified pages and run automated checks
- [ ] Verify all internal links still resolve
- [ ] Verify CSS/theme consistency
- [ ] Verify no broken HTML elements
- [ ] Spot-check random pages for accuracy

## Key Facts Already Verified from Code

### Memory System (4 Tiers) — ACCURATE
- **Episodic**: Autobiographical events, emotion-tagged at birth (immutable valence), Jaccard dedup ≥0.85, reconsolidation-on-recall (labile window), active-hours decay, flashbulb protection (graded resistance via reinforcement × emotion)
- **Semantic**: Rules/concepts/facts, Jaccard dedup ≥0.8, interference path (0.5–0.8 Jaccard + embedding overlap → overwrites with halved importance), neutral emotion default
- **Procedural**: Strategies/skills, Jaccard dedup ≥0.7, reinforcement = use_count, cross-tier link to semantic neighbor, low-use pruning (~180 wall-days)
- **Working**: Binding surface (not storage), capacity=4 (Cowan's figure), reconstructed per cycle, scratchpad with wall-time TTL (900s), overflow → lossy summary

### Memory Features — ACCURATE
- Hybrid search: vector (embedding cosine) + keyword (token overlap)
- Emotional retrieval boost: |emotion| × 0.3
- Testing effect: every recall strengthens (asymptotic importance toward 8.5)
- Reconsolidation: most-relevant trace re-tinted by current mood, labile window 600s, cooldown 1800s
- Decay: active-hours based for episodic; wall-time for semantic/procedural
- Caps: episodic=4000, semantic=1500, procedural=400 (back-pressure only)
- Wandering mind: probabilistic, heavy-tail deep memory reach, max 5 consecutive → reflection question

### Three Modes — ACCURATE
- **Chat**: Queue mode (messages queue during response), 3 sub-modes (1=drain after, 2=guidance mid-response, 3=interrupt now)
- **Autonomy**: Free-time loop (20s kick timeout), kicks from multiple sources, flow shield, wandering mind, interest thread, cognitive fatigue → rest/sleep
- **Work**: Task-driven priority chain (deadline → scheduled task → project task → ROI generation), emotions suppressed (affect-flat), faster cadence

### Cognitive Architecture — ACCURATE
- State engine: 1 Hz tick loop, mood weather with drifting baselines + noise
- Cognitive load: time-based fill/decay, threshold-gated rest/sleep (default: sleep-only path)
- Sleep auto-sized to drain load to ~0 (consolidation floor of 3+ min)
- Flow state: 3 consecutive novel cycles → flow entered; satisfaction <6 or energy <4 → flow exited
- Appraisal system: goal-coupled emotions (satisfaction = progress × goal-value, frustration = blockage × low-coping)
- Temperament: slowly random-walking baselines for curiosity/satisfaction/energy

### Tools (25+) — ACCURATE
- File ops: read/write/edit/patch, paged reading, binary detection
- Bash: workspace-scoped, danger command blocking, timeout
- Memory CRUD: remember_event/fact/strategy, search_memory, recall_strategies, forget
- Prospective: remember_to_do (time), add_prospective (event trigger)
- Desktop control: screenshot, mouse_click/move/drag, keyboard_type/hotkey, see_screen, click_element, ocr_screen, analyze_screen
- Browser automation: real Chrome CDP, fill/click/scroll/navigate, cookie accept
- Web research: search_web (DuckDuckGo + Wikipedia), fetch_page, fetch_wikipedia, compare_sources, web_research
- Documents: read_pdf (with OCR fallback), write_word, read_excel, draw_image, open_file/open_app
- Communication: share_discovery, check_in
- Tool builder: create_tool, list_custom_tools, delete_tool
- Macros: record/stop/execute/list macros
- Projects/Schedule: create_project, add_task, complete_task, get_schedule, etc.

### LLM Providers — ACCURATE
- 4 providers: Ollama (local), llama.cpp (local), NVIDIA Cloud, Anthropic
- Template presets per provider with sensible defaults
- API keys from env vars, never persisted to settings.json
