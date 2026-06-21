# Genesis Website — Page-by-Page Verification Plan

## Scope

All **115 HTML files** in `web page for publishing/` directory.
Each file is self-contained (no external CSS/JS files) — all styles are embedded in `<style>` tags.

---

## Phase 1: Structural & Syntax Checks (Automated)

Run once across all 115 files to catch obvious problems.

| # | Check | What to verify |
|---|-------|---------------|
| 1.1 | **DOCTYPE + HTML root** | Every file starts with `<!DOCTYPE html>` and `<html lang="en">` |
| 1.2 | **Meta charset + viewport** | `<meta charset="UTF-8">` and `<meta name="viewport" ...>` present |
| 1.3 | **Title tag** | Non-empty `<title>` in every file |
| 1.4 | **Single `<style>` block** | Exactly one `<style>` opening and one `</style>` closing per file |
| 1.5 | **Closing tags** | `</html>`, `</body>`, `</head>` present and properly closed |
| 1.6 | **No duplicate `<style>`** | No file has more than one `<style>` block (previous bug — already fixed, but re-verify) |
| 1.7 | **No orphaned `</style>`** | No extra `</style>` tags outside the main block |
| 1.8 | **Valid HTML nesting** | All `<div>`, `<section>`, `<article>`, `<ul>`, `<li>` properly nested and closed |
| 1.9 | **Image paths** | All `<img src="...">` reference valid relative paths or external URLs |
| 1.10 | **Script tags** | Any inline `<script>` blocks are syntactically valid JS; no unclosed tags |

---

## Phase 2: CSS Consistency Audit (Per-Page)

Every page has its own embedded CSS. Check each one against the **design system**.

### 2.1 Design Token Consistency

For each file's `<style>` block, verify these `:root` CSS custom properties exist and match:

| Token | Expected Value | Notes |
|-------|---------------|-------|
| `--bg` | `#0a0a0f` | Page background |
| `--surface` | `#12121a` | Card backgrounds |
| `--surface-2` | `#1a1a26` | Secondary surfaces |
| `--border` | `#2a2a3a` | Border color |
| `--text` | `#e4e4ec` | Primary text |
| `--text-dim` | `#8888a0` | Secondary text |
| `--accent` | `#7b6ff0` | Primary accent |
| `--accent-soft` | `#9d93f5` | Lighter accent for links |
| `--green` | `#4ade80` | Success/positive state |
| `--orange` | `#fb923c` | Warning state |
| `--pink` | `#f472b6` | Creative/emotional state |
| `--purple` | `#a855f7` | Secondary accent |
| `--cyan` | `#22d3ee` | Info/tech state |
| `--red` | `#f87171` | Error/danger state |
| `--yellow` | `#fbbf24` | Attention/caution |
| `--radius` | `12px` | Standard border radius |
| `--radius-lg` | `20px` | Large border radius |

**Flag if:** Any token is missing, has a different value, or the page uses hardcoded colors instead of tokens.

### 2.2 Base Reset & Typography

For each page's CSS, verify:

- `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }` present
- `body` has: font-family (system stack), background from `--bg`, color from `--text`, line-height ~1.7
- Links use `--accent-soft` color, with hover state (`#b5adfc`)
- No conflicting global resets that break layout

### 2.3 Component Style Consistency

Check each page for these standard components and verify their CSS matches the design system:

| Component | Required Styles | Where Used |
|-----------|----------------|------------|
| `.card` | `background: var(--surface)`, `border: 1px solid var(--border)`, `border-radius: 12px`, hover effect | Most pages |
| `.btn-primary` | Gradient background, glow shadow, hover lift | Landing + CTA pages |
| `.btn-secondary` | `var(--surface-2)` bg, border, hover border accent | Most pages |
| `.section-tag` | Uppercase, 0.8rem, letter-spacing 2px, accent color | Content pages |
| `.section-title` | clamp(1.8rem, 4vw, 2.5rem), font-weight 700 | All content sections |
| `.section-desc` / `.section-description` | `var(--text-dim)`, ~1.05rem, max-width 600px | All content pages |
| `.feature-card` | Grid layout, hover border glow + lift | index.html, capabilities |
| `.modes-grid` | Auto-fit grid, minmax(280px, 1fr) | index.html, modes pages |
| `.gradient-text` | Gradient background-clip text | Headings on most pages |
| `.fade-in` / `.visible` | Opacity transition for scroll animations | Most pages |

**Flag if:** Component styles differ significantly from the above (wrong colors, missing hover states, broken layout).

### 2.4 Layout Structure

For each page, verify:

- `.container` class exists with `max-width: 1100px`, `margin: 0 auto`, `padding: 0 24px`, `position: relative; z-index: 1`
- `section` elements have adequate padding (`100px 0` for hero, `80px 0` for content)
- Grid layouts use proper `display: grid` with correct `grid-template-columns`
- Flex layouts use proper `display: flex` with `align-items` and `justify-content`

---

## Phase 3: Page Architecture Verification (Per-Page)

Each page falls into one of three **architectural patterns**. Verify the right pattern is applied.

### Pattern A: Full Content Page (90+ pages)

**Required elements:**
1. `<nav>` with logo + navigation links
2. `<main>` or `<section>` content area
3. `<footer>` with copyright + links
4. Background glow orbs (`.bg-glow`) — optional but preferred on main pages

**Verify:**
- Nav has `.logo` with gradient text, `position: fixed`, `backdrop-filter: blur(20px)`
- Nav links point to valid `.html` files in the same directory
- Footer has consistent structure: copyright line, Genesis branding, link to index.html
- Page has proper `<header>` or hero section if it's a main landing page

### Pattern B: Immersive/Experiential Page (26 pages)

**These pages intentionally lack nav/footer for artistic effect:**
`absence.html`, `attend.html`, `blindsight.html`, `certainty.html`, `context-window.html`, `curiosity-field.html`, `doubt.html`, `duration.html`, `emotional-states.html`, `entanglement.html`, `fragment.html`, `fugitive.html`, `memory-consolidation.html`, `memory-erosion.html`, `on-return.html`, `persistence.html`, `the-listener.html`, `the-wait.html`

**Verify:**
- No nav/footer is **intentional** (not a bug) — these pages should have minimal, atmospheric styling
- They may still have `.bg-glow` for atmosphere
- Content is self-contained and readable without navigation
- They link back to index.html somewhere in the content

### Pattern C: Special Pages

| Page | Pattern | Notes |
|------|---------|-------|
| `index.html` | Full landing page | Must have nav + footer + bg-glow + all sections |
| `gallery.html`, `gallery-full.html` | Gallery layout | Grid of images/cards with lightbox or expanded view |
| `agent-dashboard.html`, `mission-control.html` | Dashboard layout | Data visualization, status panels |

---

## Phase 4: Content-to-Code Correctness Verification (Per-Page)

This is the **most critical phase**. For each page, verify that what the text **claims** Genesis can do actually matches what the **code simulates/implements**.

### 4.1 Claim Verification Framework

For every claim made in the page content, check:

| Claim Type | How to Verify |
|-----------|--------------|
| "Genesis has memory" | Does the page/code show memory structures, data structures, or simulation of memory? |
| "Three modes (Chat/Autonomy/Work)" | Is there actual mode-switching code, UI elements, or state management? |
| "Biological-style memory" | Are there references to episodic/semantic/procedural memory in the code? |
| "Simulated moods" | Is there mood/state tracking code (mood values, valence, cognitive load)? |
| "Desktop control" | Does the page show actual desktop automation code or screenshots? |
| "Browser control" | Is there browser automation code visible? |
| "Self-modifying code" | Are there examples of the AI creating/altering its own tools? |
| "Recursive self-improvement" | Does the code show self-reflection loops or meta-cognition? |

**Flag if:** A claim is made in text but no corresponding code, UI element, or simulation exists to support it.

### 4.2 Specific Page Checks

Go through each page and verify:

#### index.html (Landing Page)
- [ ] Hero section accurately describes Genesis capabilities
- [ ] Feature cards link to real subpages
- [ ] Three modes section correctly describes Chat/Autonomy/Work
- [ ] All CTA buttons link to valid pages
- [ ] No overclaiming — every feature mentioned exists in the codebase

#### capability-focused pages (verify each claim against actual code):
- `capabilities.html` — list of features must match what's implemented
- `biological-memory.html` — memory architecture described must match code
- `emotional-states.html` — mood system described must match code
- `autonomy-mode.html` — autonomous behavior described must match code
- `chat-mode.html` — chat functionality described must match code
- `work-mode.html` — work mode described must match code
- `memory-system-explorer.html` — memory visualization must actually render
- `memory-graph.html` — graph visualization must be functional
- `dream-simulator.html` — dream simulation must have actual logic
- `autonomy-simulator.html` — autonomy simulator must have working UI

#### philosophical/conceptual pages:
- `consciousness.html`, `ai-consciousness.html`, `philosophy-of-mind.html` — verify claims are framed as exploration/philosophy, not false assertions of sentience
- `hard-problem.html`, `godels-theorems.html` — verify technical accuracy of explanations
- `ethics-alignment.html`, `ai-ethics.html` — verify ethical frameworks described are consistent

#### experiential pages:
- `absence.html`, `the-wait.html`, `fugitive.html` — verify these are artistic pieces, not broken pages
- `dreamscape.html`, `dream-state.html` — verify dream simulation has actual visual/interactive elements

---

## Phase 5: Cross-Reference & Link Integrity

### 5.1 Internal Links

For each of the 115 files:

| Check | Method |
|-------|--------|
| All `href="*.html"` point to existing files | Compare against file list |
| All `href="../*.html"` resolve correctly | Account for directory structure |
| No `href="#"` placeholder links (except intentional anchors) | Manual review of nav/footer |
| Nav links are consistent across all pages with navs | Cross-check nav HTML |
| Footer links are consistent across all pages with footers | Cross-check footer HTML |

### 5.2 Navigation Consistency

Build a **nav map** — every page that has a `<nav>` should have the same link structure:

| Nav Item | Should Link To |
|----------|---------------|
| Logo/Home | `index.html` |
| About | `meet-genesis.html` or similar |
| Capabilities | `capabilities.html` |
| Memory | `biological-memory.html` or memory hub |
| Modes | `autonomy-mode.html` or modes comparison |
| Philosophy | `consciousness.html` or philosophy page |

**Flag if:** Any nav has broken, missing, or inconsistent links.

---

## Phase 6: Semantic HTML & Accessibility

### 6.1 Semantic Structure

For each page, verify:

- [ ] Uses `<header>`, `<main>`, `<footer>`, `<nav>`, `<section>`, `<article>` appropriately
- [ ] Heading hierarchy is logical (`h1` → `h2` → `h3` — no skipping levels)
- [ ] Every `h1` is unique per page (only one per page)
- [ ] Lists use `<ul>`/`<ol>` with `<li>` elements properly
- [ ] Links have descriptive text (not "click here")

### 6.2 Accessibility

- [ ] All images have `alt` attributes
- [ ] Color contrast meets WCAG AA (dark bg `#0a0a0f` with text `#e4e4ec` = ~12:1, good)
- [ ] No content that relies solely on color to convey meaning
- [ ] Interactive elements are keyboard-accessible (no JS-only click handlers without keyboard fallback)

---

## Phase 7: Performance & Best Practices

### 7.1 Code Quality

For each file:

| Check | Threshold |
|-------|-----------|
| File size | < 50KB (uncompressed) — flag if larger |
| CSS in `<style>` | < 300 lines — flag if excessive |
| Inline JS | Minimal, no massive inline scripts |
| No external dependencies | All styles/scripts are self-contained |
| No duplicate content blocks | Same text repeated across multiple pages |

### 7.2 Responsive Design

Verify each page:

- [ ] `viewport` meta tag present (all should have it)
- [ ] Grid layouts use `repeat(auto-fit, minmax(...))` or media queries
- [ ] No fixed-width containers that break on mobile (< 480px)
- [ ] Font sizes use `clamp()` or responsive units
- [ ] Touch targets are at least 44x44px

---

## Phase 8: Final Deliverable

After completing all checks, produce:

1. **`VERIFICATION_REPORT.md`** — Full report with per-page results
2. **`ISSUES_LOG.md`** — All issues found, categorized by severity (Critical / Major / Minor)
3. **`FIXED_FILES/`** — Directory with corrected versions of any files that need changes

### Severity Definitions

| Severity | Action |
|----------|--------|
| **Critical** | Page is broken, links are dead, CSS is missing, content is misleading | Fix immediately |
| **Major** | Styling inconsistency, missing component styles, broken cross-links | Fix in this pass |
| **Minor** | Typo, spacing issue, non-critical CSS tweak | Note and fix if time allows |
| **Info** | Suggestion for improvement, not a bug | Log for reference |

---

## Execution Order

1. **Phase 1** — Run automated checks on all 115 files (fast, ~5 min)
2. **Phase 2** — CSS consistency audit (systematic, ~30 min)
3. **Phase 3** — Page architecture verification (~15 min)
4. **Phase 4** — Content-to-code correctness (deep dive, ~2 hours)
5. **Phase 5** — Cross-reference & link integrity (automated + manual, ~20 min)
6. **Phase 6** — Semantic HTML & accessibility (~30 min)
7. **Phase 7** — Performance & best practices (~15 min)
8. **Phase 8** — Compile final report

**Total estimated time: ~4 hours**

---

## Notes

- Work through pages in alphabetical order within each phase for consistency
- Keep a running log of issues as you go
- Take screenshots of any visual issues found
- When fixing, always note the original value and the fix applied
- If a page is intentionally different (e.g., immersive/experiential), note it as "by design" rather than an issue
