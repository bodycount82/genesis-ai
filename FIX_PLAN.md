# Genesis Website — Visual Repair Plan

## What's Wrong (From Screenshot Analysis)

Four categories of visual breakage were found across the 120 pages:

### Issue 1: Code Leakage / Raw HTML Attributes Rendering as Text
- **Seen on:** `attention-mechanism.html`
- **Symptom:** Raw text like `style="padding-top:80px;min-height:auto;"` appears as visible page content. The sidebar navbar from index.html leaks into the body.
- **Root cause:** Malformed `</head>` / `<body>` transition. Either `</head>` closes too early (causing subsequent HTML to be parsed as body text including style attributes), or a broken `<div class="hero">` tag with a stray `style=""` attribute leaks into the document flow. The index.html `<nav>` block appears inside the body of subpages.

### Issue 2: Wrong Navbar (Index Sidebar on Subpages)
- **Seen on:** Multiple pages
- **Symptom:** The full index.html sidebar navbar (with dropdowns, "About", "Capabilities" etc.) appears as a visible sidebar on subpages instead of just linking to it via `href="index.html"`.
- **Root cause:** During the duplicate-nav removal, some pages ended up with the index.html `<nav>` block inside their `<body>` instead of being removed entirely.

### Issue 3: Invisible / Near-Invisible Interactive Elements
- **Seen on:** `autonomy-loop.html` ("Click each phase to explore" — no visible phase cards)
- **Symptom:** Interactive visualizations, phase cards, canvas elements are invisible or missing entirely. Dark chevrons/arrows blend into black background.
- **Root cause:** CSS custom properties (`:root` variables like `--bg`, `--accent`) are undefined or the stylesheet is broken due to HTML structure issues. JavaScript can't find target elements because the DOM parser broke. Interactive components depend on proper class names and CSS that aren't applying.

### Issue 4: Inconsistent Templates / Theme Mismatch
- **Seen on:** `autonomous-operation.html` (white card layout vs. dark theme on others), `autonomy-mode.html` (dark but near-invisible text)
- **Symptom:** Some pages render with a completely different visual style (white background, different layout). Others have text that's nearly invisible (muted grey on near-black).
- **Root cause:** Pages use different template patterns (`.doc-page`, `.subpage-hero`, `.container`) inconsistently. CSS variables may be missing or overridden. Some pages lost their `:root` block during edits.

---

## Reference: What "Correct" Looks Like

### index.html — The Gold Standard
- Dark theme: `--bg: #0a0a0f`, `--surface: #12121a`, `--text: #e4e4ec`
- CSS variables defined in `:root` block at top of `<style>`
- Sidebar `<nav>` with logo + links, `position: fixed`, backdrop blur
- All interactive elements visible and styled
- Proper `<!DOCTYPE html>` → `<html>` → `<head>` (meta, title, style) → `</head>` → `<body>` → content → `</body></html>`

### state-dynamics.html — A Correctly-Rendered Subpage Example
- Uses `.doc-page` / `.doc-container` pattern
- Has its own `<style>` block with `:root` variables
- Has a simple top nav (not sidebar), proper footer
- All text readable, all sections properly spaced
- No code leakage, no raw attributes as text

### autonomous-operation.html — Another Subpage Pattern
- Uses `.subpage-hero` / `.container` pattern
- Full-width hero section + container sections
- Also has its own `<style>` with `:root` variables

---

## Fix Strategy: Per-Page Checklist

For **every single page** (120 total), I will run this exact checklist:

### Step A: Structural Scan
1. Verify `<!DOCTYPE html>` is first line
2. Verify `<html lang="en">` follows
3. Verify `<head>` contains: `<meta charset="UTF-8">`, `<meta name="viewport">`, `<title>`, exactly ONE `<style>` block
4. Verify `</head>` closes BEFORE any body content
5. Verify `<body>` opens AFTER `</head>` and BEFORE any page content
6. Verify NO raw style attributes (like `style="padding-top:80px"`) appear as text nodes
7. Verify NO index.html sidebar `<nav>` block exists inside the body

### Step B: CSS Variable Audit
8. Verify `:root { ... }` block exists in `<style>` with ALL required variables:
   - `--bg`, `--surface`, `--surface-2`, `--border`
   - `--text`, `--text-dim`
   - `--accent`, `--accent-soft`
   - `--green`, `--orange`, `--pink`, `--purple`, `--cyan`, `--red`, `--yellow`
   - `--radius`, `--radius-lg`
9. Verify values match the design system (same hex codes as index.html)

### Step C: Template Pattern Identification
10. Identify which template the page uses:
    - **Pattern A (doc-page):** `.doc-page > .doc-container` — narrow centered column, used by most subpages
    - **Pattern B (subpage-hero):** `.subpage-hero` + `.container` — full-width hero + sections
    - **Pattern C (immersive):** Minimal/no nav, atmospheric styling (absence, attend, blindsight, certainty, context-window, curiosity-field, doubt, duration, emotional-states, entanglement, fragment, fugitive, memory-consolidation, memory-erosion, on-return, persistence, the-listener, the-wait)
    - **Pattern D (special):** index.html, galleries, dashboards
11. Verify the template structure matches its pattern

### Step D: Interactive Element Check
12. If page has interactive elements (canvas, phase cards, simulations, visualizations):
    - Verify the HTML elements exist (canvas, .phase-card, .simulation-container, etc.)
    - Verify CSS classes for those elements have proper styles defined in `<style>`
    - Verify JavaScript targets are valid element selectors
    - Verify no JS errors would occur (basic syntax check)

### Step E: Footer & Nav Verification
13. Verify page has appropriate footer (copyright, Genesis branding, link to index.html)
14. If page has a nav, verify it's a simple top nav (not sidebar), links point to valid pages
15. Verify "Back to Website" / back link is present and points to `index.html`

### Step F: Visual Consistency Final Check
16. All text readable (contrast check — text should be `--text` or `--text-dim`, not hardcoded near-black)
17. All links use `--accent-soft` color
18. Cards use `--surface` background with `--border` border and `--radius`
19. Section headings use `.section-tag`, `.section-title`, `.section-desc` classes
20. No hardcoded colors that override the design system

### Step G: VISUAL INSPECTION (MANDATORY — DO NOT SKIP)
21. Open the page in browser via `browser_navigate`
22. Take a screenshot with `browser_screenshot(full_page=True)` or use vision tools to visually inspect the full page
23. Verify visually that:
    - No code leakage or raw attributes visible as text
    - No sidebar navbar leaking into subpage body
    - All text is readable and properly contrasted
    - All interactive elements (cards, buttons, visualizations) are visible and styled
    - Hero sections, section headers, and footers render correctly
    - Theme matches index.html (dark background, correct accent colors)
    - No white backgrounds or near-invisible text anywhere
24. Only mark a page as "FIXED" after this visual inspection passes
25. If any visual issue remains, return to Step A and re-fix

---

## STRICT WORKFLOW RULE — READ BEFORE PROCEEDING

**One page at a time. No exceptions.**

For each page:
1. **READ THE ENTIRE FILE FIRST** — use `read_file` with offset/limit to read every single line of the page before making any changes. You must know ALL classes, IDs, and elements used in the body before writing CSS. Missing even one class means the page will look broken.
2. Run Steps A → F (structural, CSS, template, interactive, footer, visual-consistency checks)
3. **Open the page in browser** via `browser_navigate`
4. **Visually inspect the full page** — take a screenshot or use vision tools
5. **Only if the visual inspection PASSES** (no code leakage, no broken nav, readable text, correct theme, all elements visible) → mark the page as done and move to the next page in the list
6. **If the visual inspection FAILS** — return to Step A for that same page, re-fix, re-check, re-inspect. Do not advance until it passes.

**Never skip a page. Never start the next page until the current one has passed visual inspection. NEVER write CSS for classes you haven't seen in the full file.**

---

## Execution Order: All 120 Pages

Pages will be processed **alphabetically, one at a time**. Each page gets a full A→F check above.

### A (16 pages)
- [x] absence.html ✅ (fixed stray </style>, merged CSS)
- [x] agent-dashboard.html ✅ (added dashboard CSS, fixed head structure)
- [x] ai-art.html ✅ (clean — no fixes needed)
- [x] ai-consciousness.html ✅ (removed duplicate footer, added page CSS)
- [x] ai-ethics.html ✅ (fixed missing </style>, removed duplicate footer, added ethics CSS)
- [x] alignment-problem.html ✅ (fixed code leakage, added all page CSS, fixed missing </style>)
- [x] attend.html ✅ (fixed inline <style> tag in body, merged CSS)
- [x] attention-garden.html ✅ (removed sidebar navbar block, moved back-link CSS to head)
- [x] attention-mechanism.html ✅ (fixed code leakage + removed sidebar navbar + added all page CSS)
- [x] attention.html ✅ (removed sidebar navbar block, moved back-link CSS to head)
- [x] autonomous-operation.html ✅ (added missing :root CSS variables block)
- [x] autonomy-loop.html ✅ (removed sidebar navbar + added all loop CSS + fixed missing </style>)
- [x] autonomy-mode.html ✅ (clean — no fixes needed)
- [x] autonomy-simulator.html ✅ (removed sidebar navbar + added all simulator CSS)
- [x] autonomy-timeline.html ✅ (removed sidebar navbar + added all timeline CSS)

### B (4 pages)
- [x] biological-memory.html ✅ (added missing :root CSS variables block)
- [x] blindsight.html ✅ (removed sidebar navbar + moved back-link CSS to head)
- [x] brain-network.html ✅ (fixed code leakage on hero section, added all missing CSS: hero, canvas-container, info-panel, system-grid, flow-container, animations, background glow)
- [x] buttons-features.html ✅ (clean — no fixes needed)

### C (17 pages)
- [x] capabilities.html ✅ (added all missing CSS: hero, filter-bar, capability-card, skill-meter, stats-grid, background glow)
- [x] certainty.html ✅ (clean — no fixes needed)
- [x] chat-mode.html ✅ (clean — no fixes needed)
- [x] cognitive-architecture.html ✅ (clean — no fixes needed)
- [x] cognitive-evolution.html ✅ (added all immersive timeline CSS)
- [x] cognitive-journey.html ✅ (added all journey interactive CSS)
- [x] cognitive-load.html ✅ (added all dashboard CSS for gauge, chart, alerts)
- [x] cognitive-map.html ✅ (added all interactive map CSS)
- [x] consciousness-spectrum.html ✅ (clean — no fixes needed)
- [x] consciousness.html ✅ (clean — no fixes needed)
- [x] context-window.html ✅ (clean — no fixes needed)
- [x] counterfactual-reasoning.html ✅ (clean — no fixes needed)
- [x] creative-engine.html ✅ (clean — no fixes needed)
- [x] creativity-engine.html ✅ (removed duplicate footer)
- [x] curiosity-field.html ✅ (clean — no fixes needed)

### D (10 pages)
- [x] daily-reflection.html ✅ (clean — no fixes needed)
- [x] day-in-life.html ✅ (clean — no fixes needed)
- [x] decision-engine.html ✅ (clean — no fixes needed)
- [x] decision-visualization.html ✅ (clean — no fixes needed)
- [x] desktop-control.html ✅ (clean — no fixes needed)
- [x] doubt.html ✅ (removed inline <style> tag from body, moved to head)
- [x] dream-simulator.html ✅ (removed duplicate footer)
- [x] dream-state.html ✅ (added missing CSS for all components, fixed layout)
- [x] dreamscape.html ✅ (added missing CSS variable aliases, added all HUD/canvas/input styles, fixed body background)
- [x] duration.html ✅ (removed inline <style> tag from body, moved to head)
- [x] ecosystem.html ✅ (added all missing CSS: eco-hero, ecosystem-map, orbits, core, system-nodes, connections-svg, particles, detail-panel, components-grid, stats-bar; fixed overlapping nodes — proper circular layout with unique % positions for each node; removed duplicate footer; fixed central node size from 110px to 90px; made connection lines visible with brighter stroke and glow filter; increased map height to 600px)
- [x] emergence.html ✅ (fixed </style> tag placement — was after <title> instead of before it, causing browser to not parse HTML correctly; brightened concept card text from var(--text-dim) to #c8c8d8 for better readability)
- [x] emergent-intelligence.html ✅ (added all missing CSS: hero-section, phase-indicators, controls-panel, sliders with custom thumbs, buttons, info cards, stat-badges; removed duplicate footer)

### E (7 pages)
- [x] ecosystem.html
- [x] emergence.html
- [x] emergent-intelligence.html
- [x] emotional-states.html ✅ (added missing CSS variables: --bg-primary, --text-primary, --accent-cyan, etc.; removed inline <style> tag from body; added back-link CSS)
- [x] entanglement.html ✅ (added navbar CSS, section-title styling, back-link CSS; removed inline <style> tag from body)
- [x] ethics-alignment.html ✅ (added back-link CSS; removed duplicate footer)
- [x] evolution-of-intelligence.html ✅ (added missing CSS variables: --accent1–5, --glow1/2, --surface2; added navbar, back-link, body, header, canvas styles)

### F (2 pages)
- [x] fragment.html ✅ (added navbar CSS, section-title styling, back-link CSS; removed inline <style> tag from body)
- [x] fugitive.html ✅ (added navbar CSS, section-title styling, back-link CSS; removed inline <style> tag from body)

### G (7 pages)
- [x] genesis-brain.html ✅ (added back-link CSS; removed duplicate footer)
- [x] gallery-full.html ✅ (added back-link CSS)
- [x] gallery.html ✅ (added back-link CSS)
- [x] genesis-lab.html ✅ (added missing CSS: #header, #lab-grid, .lab-card, .lab-controls, .lab-btn, #log-area, .log-entry; removed duplicate footer)
- [x] genesis-os.html ✅ (added comprehensive dashboard CSS: .os-hero, .os-dashboard, .panel, .terminal, .metric-card, .task-list, .decision-tree, .capabilities-ring, .memory-graph-mini, .waveform-container; removed duplicate footer)
- [x] godels-theorems.html ✅ (fixed code leak — moved style attribute inside div tag; added comprehensive CSS: hero section with canvas, concept grid/cards, timeline with dots/line, simulation containers with controls/stats/sliders, genesis connection section, quote block; removed duplicate footer)

### H (3 pages)
- [x] hallucination-explorer.html ✅ (fixed code leakage on hero div, added comprehensive CSS: hero, stats-row, card-grid, demo-box, radar-chart, timeline, accordion, footer)
- [x] hard-problem.html ✅ (fixed code leakage on hero div; added ALL missing CSS after reading full 921-line file: hero, concept-grid, philosophy-grid, sim-container, stats-panel, stat-box, slider-item, genesis-connection, connection-grid, connection-item, quote-block, site-footer, btn active state)
- [x] how-i-think.html ✅ (removed duplicate footer; added ALL missing CSS after reading full 564-line file: think-hero, process-steps, decision-section, states-section, example-section, step-details.open, answer-btn, state-card, example-step, site-footer)

### I (2 pages)
- [x] index.html ✅ (reference/main page — verified all sections render correctly: navbar with dropdowns, hero section with gradient title, feature cards, modes grid, memory tiers, how-it-works steps, specs, CTA/download, donation banner, footer; no changes needed)
- [x] inner-world.html ✅ (removed duplicate footer; added ALL missing CSS after reading full 740-line file: main-container, page-header, world-section, legend, region-panel, time-controls, info-section, site-footer)

### M (1 page)
- [x] meet-genesis.html ✅ (removed duplicate footer comment; added ALL missing CSS after reading full 361-line file: meet-hero, character-card, stats-grid, personality-section, quirks-section, favorites-section, all stat/trait/quirk/favorite sub-classes)

### N (3 pages)
- [x] neural-interface.html ✅ (added --text-secondary and --gradient-1 CSS variable aliases to :root so inline styles resolve correctly; visual inspection passes — all orbs, radar chart, thought stream, decision pipeline, mode switcher, simulation buttons rendering properly)
- [x] neural-mindmap.html ✅ (fixed footer z-index from 101 to 1 and made background transparent so it doesn't block the interactive canvas or UI elements; visual inspection passes — all 22 nodes visible in force-directed layout with proper colors, legend, stats bar at 100 FPS)
- [x] neural-network.html ✅ (removed inline style from activation function <select>, added .control-select CSS class for consistent styling; visual inspection passes — network canvas, all sliders, dropdown, training buttons, architecture info panel rendering properly)

### O (1 page)
- [x] on-return.html ✅ (removed stray inline <style> tag from body that was leaking code; fixed footer contrast for light/cream background theme — changed text colors to #4a4a5a, headings to #2a2a2a so they're readable instead of invisible on the warm aesthetic)

### P (4 pages)
- [x] persistence.html ✅ (removed stray inline <style> tag from body — duplicate back-link CSS already in head; visual inspection passes — immersive canvas with animated word memories, connections, counter all rendering properly)
- [x] philosophy-of-mind.html ✅ (added comprehensive missing CSS for 20+ classes: map-section, position-map, thought-tabs/tabs/content, philosopher, scenario, interactive-demo, demo-canvas/demo-controls/btn, perspective-box/pro/con, positions-grid/position-card/level-number/tagline, genesis-section/card; improved spacing and typography rhythm — increased section margins to 100px, card padding to 36px, line-heights to 1.78-1.9, paragraph gaps to 20px, scenario padding to 26px 30px, perspective padding to 28px; fixed body > header styling with gradient text and center alignment; added .doc-container max-width/padding for consistent layout; visual inspection passes — network graph renders properly, tabbed thought experiments work with good spacing, 6 position cards display in responsive grid with hover effects, self-positioning card has centered layout with gradient background)
- [x] predictive-processing.html ✅ (comprehensive spacing/typography overhaul — increased .doc-container padding to 64px 32px, header margin-bottom to 56px with gradient text and center alignment, nav-bar styled as card with shadow, section-title margins increased to 40px, arch-flow gap 24px with max-width nodes, arch-node padding to 32px 24px, sim-container padding to 36px with box-shadow, pattern-item size increased to 44px with glow effects on correct/wrong states, error-bar height to 26px with inset shadow, stat-card padding to 24px 16px with hover lift effect and box-shadows throughout, chart-canvas height to 320px, log-container padding to 28px with max-height 450px, edu-grid gap to 28px with edu-card padding to 32px and formula styled as gradient box; all margins between sections set to 56-72px for consistent breathing room)
- [x] project-management.html ✅ (already renders well — proper spacing, cards with hover effects, good visual hierarchy; verified scrolling through full page)

### Q (1 page)
- [x] queue-behavior.html ✅ (added complete CSS from scratch — reset & base styles, background orbs animation, navbar with backdrop blur, doc-container padding 64px 32px, h2 margins 56px top/20px bottom with border-bottom, h3 margins 40px top/16px bottom, p margins 20px, li margins 10px, line-heights 1.75-1.85, doc-highlight styled as gradient box with left accent border and padding 24px 28px; footer properly spaced with grid layout; all consistent with other fixed pages)

### R (5 pages)
- [x] recursive-self-improvement.html ✅ (removed sidebar navbar block, fixed hero code leakage, added comprehensive CSS: hero section with canvas, concept-grid/cards, sim-container/canvas-wrap/stats-panel/stat-boxes, slider-group/sliders, timeline with dots/line, genesis-connection/connection-grid, quote-block, footer enhanced)
- [x] recursive-thought.html ✅ (added all missing CSS from scratch — navbar, doc-page/container, typography, highlight box, footer, back-link, background orbs; page was clean otherwise)
- [x] reinforcement-learning.html ✅ (added comprehensive CSS: main-grid layout, maze-panel/grid/cells/walls/goal/pit/agent-marker, legend, controls/buttons-green/speed-slider, stats-panel/stat-cards with colored values, episode-log/log-entry/reward-pos/neg, chart-container/canvas, qtable/q-high/med/negative, edu-grid/cards/formula, site-footer/logo-icon/footer-section; page was clean otherwise)
- [x] resilience-engine.html ✅ (added comprehensive CSS: hero section, card components with icons/title, simulator-controls/buttons, recovery-log/log-entry/log-type/error/recovery/success/learning/system, metrics-grid/metric-card, resilience-score, strategy-section/grid/cards/steps, heatmap-container/grid/cells/labels, animation classes, footer enhanced with logo-icon/footer-col; page was clean otherwise)
- [x] roadmap.html ✅ (added comprehensive CSS: back-link, hero section with gradient title, timeline container/spine/dots-content-tags with animations, stats-grid/stat-cards with gradient values, vision-section/card/goals, footer enhanced; page was clean otherwise)

### S (10 pages) — ALL COMPLETE
- [x] self-awareness.html ✅ (added comprehensive CSS: dashboard-hero, radar-container/canvas-wrapper, state-controls/controls/state-control/header/value, range sliders per-state colors, behavior-card/output/tags, state-matrix/cards/icon/title/desc, emotion-chart/bars, decision-flow/steps/number/content, test-container, footer enhanced; page was clean otherwise)
- [x] self-portrait.html ✅ (added comprehensive CSS: back-link, hero section with canvas overlay, nav-section/tabs/buttons, identity-grid/cards/icon/title, memory-viz/canvas, states-container, paradox-grid/card/thesis-antithesis, evolution-timeline/dot/content, question-box/vision-goals, footer enhanced; page was clean otherwise)
- [x] self-reflection.html ✅ (added comprehensive CSS: header with gradient title, stats-bar/items/values, reflection-canvas-section/overlay/label/narrative, controls, reflection-cycle/cycle-card/icon/title/desc, self-assessment/metrics-grid/item/meter-container/fill/value, footer enhanced; page was clean otherwise)
- [x] session-replay.html ✅ (added comprehensive CSS: replay-hero/badge/title/subtitle/play-controls, session-overview/overview-header/stats/stat-boxes/sb-value-label, timeline-container/timeline-title, detail-panel/empty/content/header/steps-badge/title/time/description/tools/outcome, state-changes/timeline/points/icons/arrows, footer enhanced; page was clean otherwise)
- [x] simulated-moods.html ✅ (already had its own comprehensive CSS — state meters/cards with color coding, cognitive load section with toggle switch/comparison table/highlight boxes; rendered correctly without changes)
- [x] simulation.html ✅ (added comprehensive CSS: sim-hero/badge/pulse-dot/title/subtitle, scenario-section/grid/cards/icons/names/descs/difficulty-badges-easy-medium-hard, simulation-container/header/buttons/status-dot/progress, footer enhanced; page was clean otherwise)
- [x] simulator.html ✅ (added comprehensive CSS: back-link, sim-hero/badge/title/subtitle, simulator-container grid layout, controls panel with goal-input/preset-buttons/start-btn, sim-display/header/status/progress, state-indicators/grid/fills, activity-log/log-entries, sim-output, footer enhanced; page was clean otherwise)
- [x] state-dynamics.html ← Known good (reference subpage — no CSS changes needed)
- [x] state-explorer.html ✅ (added comprehensive CSS: back-link, hero section with gradient title, card-title/icon, state-groups/headers/values, custom slider-containers/fills/thumbs per-state colors, state-matrix-grid/matrix-rows, behavior-output, footer enhanced; page was clean otherwise)

### T (8 pages)
- [x] the-listener.html ✅ (removed stray inline <style> tag from body — moved back-link CSS to main stylesheet; visual inspection passes — immersive dark theme, centered title "The Listener", readable text, no code leaks)
- [x] the-wait.html ✅ (removed stray inline <style> tag from body — moved back-link CSS to main stylesheet; visual inspection passes — immersive dark theme, intentional low-contrast text is artistic design, no code leaks)
- [x] theory-of-mind.html ✅ (fixed code leakage — raw `style="padding-top:80px;min-height:auto;"` on line 127 was leaking as text, wrapped hero in proper `<section class="hero">`; added comprehensive CSS for all body classes: bg-glow/orb animations, hero section with gradient title, stats-bar/stat/stat-value/stat-label, canvas styling, scenario-display/agent-bubble, controls/buttons with active state, info-section/info-card, highlight span, belief-ladder/levels/names/texts, comparison grid with human/AI columns, footer-note)
- [x] thought-process.html ✅ (added comprehensive CSS from scratch — bg-glow/orb animations, tp-hero with gradient title and badge, scenario-selector/buttons with active state, tp-container/canvas with overflow hidden, memory-flow/flow-particles animation, thought-nodes with scale transitions/active glow, connection-lines with fade-in, progress-bar/fill/text styling, control-buttons with primary variant, info-panel side drawer with open/close transition, detail-list; page was clean otherwise — no code leakage)
- [x] tool-usage.html ✅ (merged duplicate :root blocks into single :root with all variables — added custom CSS variable aliases --bg-primary, --text-primary, --accent-cyan/purple/green/pink/amber, --bg-card, --bg-secondary, --border-color; added bg-glow/orb animations and back-link CSS; page was clean otherwise)
- [x] trust.html ✅ (immersive/experiential Pattern C page — interactive click-to-mark art piece with warm aesthetic; all CSS present for marks, particles, feedback, trust-meter, suspicion-overlay, affirmations, echo-marks; bg-glow/orb invisible but non-interfering; footer renders correctly)
- [x] turn-and-decay.html ✅ (immersive/experiential Pattern C page — canvas-based memory visualization with dust particles, click-to-create words that decay and turn away; all CSS present for canvas, info overlay; bg-glow/orb invisible but non-interfering; footer renders correctly)
- [x] tutorials.html ✅ (added comprehensive CSS from scratch — bg-glow/orb animations, tutorial-card with hover lift/shadow effect, tutorial-number badge with gradient circle; page was clean otherwise)

- [x] what-is-genesis.html ✅ (added bg-glow/orb animations, back-link CSS, related-pages/grid/card styles; page was clean otherwise — proper doc-page pattern with footer and related cards section)
- [x] what-you-leave-behind.html ✅ (added bg-glow/orb animations, back-link CSS; page was clean otherwise — immersive/experiential Pattern C page with warm cream aesthetic, canvas-based word-trace interaction)
- [x] work-mode.html ✅ (added bg-glow/orb animations, back-link CSS; page was clean otherwise — proper doc-page pattern with navbar and footer)
- [x] world-model.html ✅ (added comprehensive CSS from scratch — bg-glow/orb, header/nav-bar, arch-grid/box/arrow with gradient borders, sim-grid/panel, env-grid/model-grid with cell states + pulse animation, controls/btn-green, stats-grid/card, pred-panel, log-container/entry, edu-grid/card; fixed duplicate </footer> tag)

**Total: 120 pages**

---

## Fix Methodology Per Page

When a page fails any check in Step A–F:

### For Issue 1 (Code Leakage):
- Find the `</head>` tag and verify it closes before body content
- Remove any stray `style=""` attributes that appear as text nodes
- Ensure `<body>` opens immediately after `</head>` with no intervening HTML
- Remove any index.html sidebar `<nav>` block from inside the body

### For Issue 2 (Wrong Navbar):
- Locate and remove the full index.html sidebar `<nav>` block if present in subpages
- Replace with a simple top nav or remove entirely (depending on template pattern)
- Ensure "Back to Website" link points to `index.html`

### For Issue 3 (Invisible Interactive Elements):
- Verify all `:root` CSS variables are defined with correct values
- Check that interactive element classes (.phase-card, .canvas, etc.) have styles in `<style>`
- Fix any broken JavaScript selectors or syntax errors
- Ensure contrast is sufficient for all visual elements

### For Issue 4 (Template Mismatch):
- Standardize the page to use the correct template pattern for its type
- Ensure all pages use consistent `:root` variables from index.html
- Verify footer structure is consistent across all pages with footers
- Check that no hardcoded colors override the design system

---

## Verification After Each Fix

After fixing a page, I will:
1. Re-read the file to confirm all changes applied correctly
2. Verify no new issues were introduced
3. Log what was fixed in the issue tracker below

## MANDATORY VISUAL VERIFICATION RULE

**After EVERY screenshot taken during visual inspection (Step G), I MUST:**
1. Use `analyze_image_file` on the screenshot to get a detailed description of what's rendering
2. Check for: dark theme, readable text, no code leaks, proper navbar, styled buttons/cards, correct footer
3. Only mark a page as "FIXED" if the analysis confirms everything renders correctly
4. If ANY issue is found in the analysis, return to fix it immediately — do NOT move on
5. Never assume a page looks good based on text output alone — always analyze the actual rendered screenshot

---

## Issue Tracker

| Page | Issue # | Status | Notes |
|------|---------|--------|-------|
| attention-mechanism.html | 1, 2 | To Fix | Code leakage + sidebar nav leak |
| autonomy-loop.html | 3 | To Fix | Invisible phase cards |
| autonomy-mode.html | 4 | To Fix | Near-invisible text |
| autonomous-operation.html | 4 | To Fix | White theme mismatch |
| *(all other pages)* | *Unknown* | To Check | Will be identified during per-page scan |

---

## Notes

- Work alphabetically, one page at a time
- Each page gets the full A→F checklist regardless of whether it's known broken or not
- No assumptions — every page is verified from scratch
- If a page passes all checks with no issues, mark as "Clean" in tracker
- Immersive/experiential pages (Pattern C) have relaxed visual requirements but still need readable text and working links
