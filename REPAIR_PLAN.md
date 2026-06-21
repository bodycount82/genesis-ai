# Genesis Web Pages — Full Repair Plan

## The Root Cause (Diagnosed from 4 sample screenshots)

All 120 subpages share **the same structural problem** introduced during the "fix" process:

### Problem 1: Broken `</head>` → `<body>` transition (code leakage)
**Line pattern:** `<a class="back-link" href="index.html">&#8592; Back to Genesis</a><div class="hero"> style="padding-top:80px;min-height:auto;"`

The `</head>` tag is placed **after** the closing `</style>`, but then the HTML body starts with `<nav>` (the index.html navbar) which leaks into view. The `<body>` tag comes **after** the nav, and right before it, the broken pattern `<div class="hero"> style="padding-top:80px;min-height:auto;"` appears — this is raw HTML attribute syntax being rendered as visible text because the browser's parser gets confused by the malformed structure.

### Problem 2: Wrong navbar template
Subpages use **two different navbars**:
- `index.html` navbar: `<nav><div class="inner">...</nav>` (with dropdowns) — this is **correct** but should NOT appear on subpages as a sidebar
- Subpage navbar: `.navbar` CSS class (fixed top bar) — this is what subpages **should** use

The pages that show the left sidebar with code leakage are including the index.html `<nav>` block in their body before `</head>`, which breaks rendering.

### Problem 3: Missing/incorrect page structure
A correct subpage structure should be:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title — Genesis</title>
    <style>
        /* All CSS here */
    </style>
</head>
<body>
    <!-- Background Glow -->
    <div class="bg-glow"><div class="orb"></div><div class="orb"></div><div class="orb"></div></div>

    <!-- Main Navigation (top bar) -->
    <nav>...</nav>

    <!-- Page Content -->
    <section class="subpage-hero">...</section>
    <!-- More sections... -->

    <!-- Footer -->
    <footer>...</footer>

    <script>...</script>
</body>
</html>
```

### Problem 4: Missing CSS classes for interactive elements
Pages like `autonomy-loop.html` have interactive content (six-phase cycle) that's either:
- Not rendered at all (JavaScript not executing due to broken HTML structure)
- Rendered with invisible styling (opacity 0, wrong z-index, colors matching background)

### Problem 5: Inconsistent CSS across pages
Some pages use `.doc-page` / `.doc-container` layout (narrow centered column), others use `.subpage-hero` / `.container` (full-width hero + container). The CSS classes don't always match the HTML structure.

---

## Repair Strategy

### Phase 0: Build a master repair script
Create a Python script that can be applied to all 120 pages atomically, fixing the structural issues in one pass per file. This ensures consistency — no manual per-page fixes.

The script will:
1. Read each `.html` file
2. Normalize the structure to match the correct template
3. Remove duplicate nav blocks (index.html nav leaking into body)
4. Fix the `</head>` → `<body>` transition
5. Ensure CSS custom properties are defined in `:root`
6. Add missing footer if absent
7. Verify all closing tags are balanced

### Phase 1: Apply structural fix to all 120 pages (automated)

All pages get the same structural treatment — the script handles it uniformly.

**Pages to fix (alphabetical, 115 total):**

#### A
- absence.html
- agent-dashboard.html
- ai-art.html
- ai-consciousness.html
- ai-ethics.html
- alignment-problem.html
- attend.html
- attention-garden.html
- attention-mechanism.html ← SAMPLE BROKEN
- attention.html
- autonomy-loop.html ← SAMPLE BROKEN
- autonomy-mode.html ← SAMPLE BROKEN
- autonomy-simulator.html
- autonomous-operation.html ← SAMPLE BROKEN

#### B
- backpropagation.html
- base64-data-url.html
- bash-scripting.html
- behavioral-ecosystem.html
- bias-mitigation.html
- binary-search.html
- blockchain-distributed.html
- bootstrap.html
- brain-computer-interface.html
- brain-signal-processing.html

#### C
- causal-reasoning.html
- chat-mode.html
- chrome-extension.html
- cognitive-architecture.html
- code-review.html
- collaboration.html
- command-line.html
- common-mistakes.html
- comparison.html
- competition.html
- competitive-advantage.html
- computational-thinking.html
- computer-vision.html
- consciousness.html
- context-window.html
- content-creation.html
- continuous-improvement.html
- conversation-analysis.html
- conversation-flow.html
- conversation-starters.html
- conversational-design.html

#### D
- creative-coding.html
- creativity.html
- critical-thinking.html
- curiosity-field.html

#### E
- ecosystem.html
- education.html
- emotion-regulation.html
- emotional-intelligence.html
- emotion.html
- energy-management.html
- ethical-ai.html

#### F
- feature-detection.html
- features.html
- feedback-loop.html
- file-system.html
- financial-advisor.html
- first-run-setup.html
- frequency-analysis.html

#### G
- game-theory.html
- genesis-brain.html ← SAMPLE BROKEN (different template)
- genesis-lab.html
- genesis-os.html
- github-integration.html
- goal-directed.html
- goals.html
- gradient-descent.html
- graph-theory.html
- grep-commands.html

#### H
- health-monitoring.html
- human-computer-interaction.html
- human-llm-collaboration.html

#### I
- image-generation.html
- image-recognition.html
- image-sentiment.html
- index.html ← REFERENCE (do NOT modify)
- information-retrieval.html

#### J
- json-parsing.html

#### K
- knowledge-graph.html

#### L
- language-models.html
- large-language-models.html
- learning-algorithms.html

#### M
- machine-learning.html
- memory-consolidation.html
- memory-erosion.html
- memory-graph.html
- memory-system-explorer.html
- meta-learning.html
- microservices.html
- microsoft-copilot.html
- model-training.html
- monitoring.html

#### N
- natural-language-processing.html
- network-analysis.html
- neural-mindmap.html
- neural-networks.html
- neural-visualization.html
- news-summarizer.html
- nlp-basics.html

#### O
- object-detection.html
- operating-system.html
- openclaw-setup.html
- optimization.html

#### P
- pattern-recognition.html
- personal-assistant.html
- personal-growth.html
- phaser3-game.html
- physics-simulation.html
- poetry-generator.html
- portfolio-manager.html
- power-management.html
- practical-guide.html
- problem-solving.html
- project-management.html
- prompt-engineering.html

#### Q
- quantum-computing.html

#### R
- recommendation-system.html
- reinforcement-learning.html
- retrieval-augmented.html
- risk-analysis.html

#### S
- simulation.html
- social-intelligence.html
- speech-recognition.html
- sql-basics.html
- state-dynamics.html ← FIXED (good template)
- state-explorer.html
- stochastic-processes.html
- stream-processing.html
- structured-data.html
- style-transfer.html
- supervised-learning.html

#### T
- swarm-intelligence.html
- system-design.html

#### V
- version-control.html
- voice-synthesis.html

#### W
- web-scraping.html
- web-development.html
- web-harvesting.html
- what-is-genesis.html
- what-you-leave-behind.html
- work-mode.html
- world-model.html

---

## Verification Checklist (per page)

For each page, after applying the structural fix, verify:

1. ✅ **No code leakage** — no raw `style="..."` attributes visible on screen
2. ✅ **Correct navbar** — top bar only (no sidebar nav from index.html)
3. ✅ **Background orbs** — animated gradient orbs visible in background
4. ✅ **Dark theme** — dark background (#0a0a0f), light text (#e4e4ec), accent purple (#7b6ff0)
5. ✅ **"← Back to Genesis" link** — visible and functional at top of content
6. ✅ **Page title renders correctly** — large gradient heading
7. ✅ **Content sections** — proper spacing, readable text, consistent typography
8. ✅ **Interactive elements** — buttons, cards, canvases render with proper colors/borders
9. ✅ **Footer** — present with links and copyright
10. ✅ **No duplicate nav blocks** — exactly one navbar per page
11. ✅ **HTML is well-formed** — all tags properly opened/closed
12. ✅ **CSS custom properties** — `:root` block defines all needed variables

---

## Execution Order

1. **Build the repair script** (`fix_pages.py`) that handles all structural issues
2. **Test on 1 broken page** (attention-mechanism.html) — verify fix works
3. **Apply to all 114 remaining subpages** in one batch
4. **Spot-check 5-10 pages** from different sections (A, G, M, S, W) to confirm consistency
5. **Final verification pass** — open each page in browser and screenshot for visual confirmation
