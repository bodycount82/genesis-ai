#!/usr/bin/env python3
"""
Comprehensive fix script for Genesis web pages.
Fixes all subpages to match the premium design system from index.html.

Issues fixed:
1. Duplicate/broken :root blocks (orphaned CSS vars outside :root)
2. Inconsistent navbar — adds standard nav to all subpages
3. No animated background orbs — adds bg-glow to all subpages
4. Content layout chaos — wraps content in doc-page wrapper with proper spacing
5. Interactive pages — preserves canvas JS while adding navbar/orbs

Usage: python fix_all_pages.py
"""

import os
import re
from pathlib import Path

BASE = Path(__file__).parent

# ============================================================
# CSS TEMPLATES
# ============================================================

NAVBAR_HTML = """<!-- Navigation -->
<nav>
<div class="inner">
<div class="logo"><a href="index.html" style="color:inherit;text-decoration:none;">Genesis</a></div>
<ul>
<li><a href="index.html#features">Features</a></li>
<li>
<a href="index.html#modes">Modes &#9662;</a>
<div class="nav-dropdown">
<div class="dropdown-label">Chat Mode</div>
<a href="chat-mode.html">Chat Mode Guide</a>
<a href="session-replay.html">Session Replay</a>
<a href="queue-behavior.html">Queue Behavior</a>
<div class="dropdown-label" style="margin-top:8px;">Autonomy Mode</div>
<a href="autonomy-mode.html">Autonomy Mode Guide</a>
<a href="autonomy-loop.html">Autonomy Loop</a>
<a href="autonomy-simulator.html">Autonomy Simulator</a>
<a href="state-dynamics.html">State Dynamics</a>
<a href="decision-engine.html">Decision Engine</a>
<a href="autonomy-timeline.html">Autonomy Timeline</a>
<div class="dropdown-label" style="margin-top:8px;">Work Mode</div>
<a href="work-mode.html">Work Mode Guide</a>
<a href="project-management.html">Project Management</a>
</div>
</li>
<li><a href="index.html#memory">Memory</a></li>
<li><a href="ai-art.html">AI Art</a></li>
<li>
<a href="index.html#gallery">Explore &#9662;</a>
<div class="nav-dropdown">
<div class="dropdown-label">Memory Visualizations</div>
<a href="memory-system-explorer.html">Memory System Explorer</a>
<a href="memory-erosion.html">Memory Erosion</a>
<a href="memory-consolidation.html">Memory Consolidation</a>
<a href="context-window.html">Context Window</a>
<a href="memory-graph.html">Memory Graph</a>
<div class="dropdown-label" style="margin-top:8px;">Cognitive Architecture</div>
<a href="cognitive-architecture.html">Cognitive Architecture</a>
<a href="genesis-brain.html">Genesis Brain</a>
<a href="genesis-os.html">Genesis OS</a>
<a href="tool-usage.html">Tool Usage</a>
<div class="dropdown-label" style="margin-top:8px;">Art &amp; Creativity</div>
<a href="curiosity-field.html">Curiosity Field</a>
<a href="attention-garden.html">Attention Garden</a>
<a href="trust.html">Trust</a>
<a href="neural-mindmap.html">Neural Mind Map</a>
</div>
</li>
<li><a href="index.html#how-it-works">How It Works</a></li>
</ul>
</div>
</nav>"""

BACK_LINK_HTML = '<a class="back-link" href="index.html">&#8592; Back to Genesis</a>'

ORBS_HTML = """<!-- Background Glow -->
<div class="bg-glow">
<div class="orb"></div>
<div class="orb"></div>
<div class="orb"></div>
</div>"""

FOOTER_HTML = """<!-- Footer -->
<footer>
<div class="container">
<div class="footer-grid">
<div class="footer-col">
<h5>Genesis</h5>
<p>An autonomous AI companion with biological-style memory, simulated moods, and real desktop capabilities. Running entirely on your machine.</p>
</div>
<div class="footer-col">
<h5>Modes</h5>
<p><a href="chat-mode.html">Chat Mode</a></p>
<p><a href="autonomy-mode.html">Autonomy Mode</a></p>
<p><a href="work-mode.html">Work Mode</a></p>
</div>
<div class="footer-col">
<h5>Explore</h5>
<p><a href="capabilities.html">Capabilities</a></p>
<p><a href="how-i-think.html">How I Think</a></p>
<p><a href="memory-system-explorer.html">Memory Explorer</a></p>
<p><a href="curiosity-field.html">Curiosity Field</a></p>
</div>
<div class="footer-col">
<h5>More</h5>
<p><a href="philosophy-of-mind.html">Philosophy of Mind</a></p>
<p><a href="consciousness.html">Consciousness</a></p>
<p><a href="ethics-alignment.html">Ethics &amp; Alignment</a></p>
</div>
</div>
<div class="copyright">&copy; 2025 Genesis. Local, private, autonomous.</div>
</div>
</footer>"""

# Full shared CSS to inject (the complete system from index.html)
SHARED_CSS = r"""/* ===== GENESIS SHARED SYSTEM ===== */
/* Gradient text utility */
.gradient-text {
  background: linear-gradient(135deg, #ffffff, var(--accent-soft), #c4b5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
/* Section styling */
.section-tag {
  display: inline-block; font-size: 0.8rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 2px; color: var(--accent-soft);
  margin-bottom: 12px;
}
.section-title {
  font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 700;
  letter-spacing: -1px; margin-bottom: 16px; color: var(--text);
}
.section-description {
  color: var(--text-dim); font-size: 1.05rem; max-width: 600px; margin-bottom: 48px;
}
/* Cards */
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px; transition: all 0.3s ease;
}
.card:hover { border-color: rgba(123, 111, 240, 0.3); transform: translateY(-2px); }
/* Buttons */
.btn {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 28px;
  border-radius: 50px; font-size: 0.95rem; font-weight: 600; cursor: pointer;
  transition: all 0.2s ease; border: none; text-decoration: none;
}
.btn-primary {
  background: linear-gradient(135deg, var(--accent), #5b4fd4);
  color: #fff; box-shadow: 0 4px 24px rgba(123, 111, 240, 0.3);
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(123, 111, 240, 0.45); }
.btn-secondary {
  background: var(--surface-2); color: var(--text); border: 1px solid var(--border);
}
.btn-secondary:hover { border-color: var(--accent); }
/* Container */
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
/* Fade-in animation */
.fade-in { opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }
/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
"""

# Shared CSS for canvas/interactive pages (lighter, no section/card styles)
SHARED_CSS_CANVAS = r"""/* ===== GENESIS SHARED SYSTEM (canvas pages) ===== */
.gradient-text {
  background: linear-gradient(135deg, #ffffff, var(--accent-soft), #c4b5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
.fade-in { opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
"""

# ============================================================
# PAGE TYPE DETECTION
# ============================================================

# Pages that use canvas/interactive (need special handling)
CANVAS_PAGES = {
    'curiosity-field.html',
    'attention-garden.html',
    'trust.html',
    'state-dynamics.html',
    'dream-simulator.html',
    'dreamscape.html',
    'memory-explorer.html',
    'memory-visualization.html',
    'neural-mindmap.html',
    'hallucination-explorer.html',
    'decision-visualization.html',
    'autonomy-simulator.html',
    'simulator.html',
    'simulation.html',
    'state-explorer.html',
    'genesis-brain.html',
    'consciousness-spectrum.html',
}


def is_canvas_page(filename):
    """Check if a page is canvas/interactive-based."""
    return filename in CANVAS_PAGES


def detect_page_type(html_content):
    """Detect what kind of page this is."""
    has_canvas = '<canvas' in html_content or 'canvas' in html_content.lower()
    has_section = re.search(r'<section|class="section"', html_content, re.I)
    has_container = 'class="container"' in html_content or '<div class="container">' in html_content
    has_nav = '<nav>' in html_content or 'class="navbar"' in html_content or 'class="nav"' in html_content
    has_orbs = 'class="bg-glow"' in html_content

    if has_canvas and not has_section:
        return 'canvas'
    elif has_section or has_container:
        return 'info'
    else:
        return 'minimal'  # very bare page


# ============================================================
# CSS CLEANING
# ============================================================

def fix_orphaned_css_vars(css_content):
    """
    Fix orphaned CSS variable declarations outside :root.
    Examples: --red: #f87171;--yellow: #fbbf24;--radius: 12px;
    These appear as bare lines between </style> or at the top of <style>.
    """
    orphaned_vars = []
    lines = css_content.split('\n')
    new_lines = []
    in_root_block = False
    brace_depth = 0

    for line in lines:
        stripped = line.strip()

        # Detect :root block start
        if re.search(r':root\s*\{', stripped):
            in_root_block = True
            brace_depth = stripped.count('{') - stripped.count('}')
            new_lines.append(line)
            continue

        # Inside a :root block?
        if in_root_block:
            brace_depth += stripped.count('{') - stripped.count('}')
            new_lines.append(line)
            if brace_depth <= 0:
                in_root_block = False
            continue

        # Outside any block — check for orphaned CSS var declarations
        if re.match(r'^--[\w-]+\s*:', stripped):
            orphaned_vars.append(stripped)
            continue

        new_lines.append(line)

    if not orphaned_vars:
        return css_content

    result = '\n'.join(new_lines)

    # Try to insert into existing :root block
    root_pattern = r'(:root\s*\{)([\s\S]*?)(\})'
    match = re.search(root_pattern, result)
    if match:
        inner = match.group(2).rstrip()
        extra_vars = '\n  ' + '\n  '.join(orphaned_vars)
        new_inner = inner + '\n' + extra_vars
        result = result[:match.start(3)] + new_inner + match.group(3) + result[match.end(3):]
    else:
        # No :root found at all — prepend one
        extra_vars = '\n'.join(orphaned_vars)
        result = ':root {\n' + extra_vars + '\n}\n' + result

    return result


def deduplicate_css_blocks(css_content):
    """Remove duplicate theme blocks from CSS. Keep only the first :root and shared system."""
    # Find all /* ===== GENESIS 1.17 THEME ===== */ blocks and their content
    pattern = r'/\*\s*=====\s*GENESIS\s+1\.17\s+THEME\s*=====\*/[\s\S]*?(?=/\*\s*=====|$)'

    matches = list(re.finditer(pattern, css_content))

    if len(matches) <= 1:
        return css_content

    # Keep only the first occurrence, remove duplicates
    result = css_content
    for i in range(len(matches) - 1, 0, -1):  # Process in reverse order
        m = matches[i]
        # Check if this block is just a duplicate :root
        block_text = m.group(0)
        if ':root' in block_text and '/* ===== GENESIS SHARED SYSTEM' not in block_text:
            result = result[:m.start()] + result[m.end():]

    return result


def clean_inline_body_styles(html_content):
    """Remove inline style attributes from <body> that override CSS variables."""
    # Match <body style="..."> and remove the style attribute
    body_pattern = r'<body\s+style="[^"]*"'
    match = re.search(body_pattern, html_content)
    if match:
        body_tag = match.group(0)
        # Remove style attribute but keep other attributes like class, onload
        cleaned = re.sub(r'\s+style="[^"]*"', '', body_tag)
        html_content = html_content[:match.start()] + cleaned + html_content[match.end():]
    return html_content


def wrap_content_in_doc_page(html_content, page_type):
    """
    Wrap the main content in a doc-page wrapper for proper layout.
    For canvas pages, we add padding-top to body instead.
    """
    if page_type == 'canvas':
        # For canvas pages, just ensure body has top padding for navbar
        body_match = re.search(r'<body([^>]*)>', html_content)
        if body_match:
            attrs = body_match.group(1)
            if 'style=' not in attrs.lower():
                new_attrs = attrs + ' style="padding-top:64px;"'
            else:
                new_attrs = attrs + '; padding-top: 64px;'
            html_content = html_content[:body_match.start(1)+5] + new_attrs + html_content[body_match.end(1)+4:]
        return html_content

    # For info pages, wrap content between </head> and <footer> in a proper wrapper
    # Find the opening of main content (after any existing nav/orbs)
    # and wrap it in a doc-page structure

    # Look for the first meaningful content after head
    head_end = html_content.find('</head>')
    if head_end == -1:
        return html_content

    after_head = html_content[head_end + 7:]

    # Check if already has doc-page wrapper
    if 'class="doc-page"' in html_content or 'class="page-wrapper"' in html_content:
        return html_content

    # Create the new body structure
    # Find where to insert the wrapper — after orbs/nav, before content
    # Strategy: wrap everything from after </head> up to <footer> (or end) in a wrapper

    # Remove any existing <main> or wrapper divs to avoid nesting
    html_content = re.sub(r'<main(?:\s[^>]*)?>', '', html_content, flags=re.I)
    html_content = re.sub(r'</main>', '', html_content, flags=re.I)

    # Find the last </footer>...</footer> or use end of file
    footer_match = re.search(r'</footer>\s*$', html_content, re.I)
    if footer_match:
        before_footer = html_content[:footer_match.start()]
        footer_and_after = html_content[footer_match.end():]

        # Find the opening tag (after </head>)
        body_open = before_footer.find('<body')
        if body_open == -1:
            body_open = before_footer.find('<body>')
        body_close = before_footer.rfind('</body>')

        if body_open != -1 and body_close != -1:
            before_body = before_footer[:body_open + 6]
            body_attrs = ''
            # Extract existing body attributes
            attr_match = re.search(r'<body\s+([^>]*)>', before_body)
            if attr_match:
                body_attrs = ' ' + attr_match.group(1)

            content_between = before_footer[body_open + len(before_body):body_close]

            new_body = f'<body{body_attrs}>\n<div class="doc-page">\n{content_between.strip()}\n</div>\n</body>'
            html_content = before_body + content_between[:content_between.find('\n' + ' ' * 20 if '\n' + ' ' * 20 in content_between else content_between.split('\n')[0])]

    return html_content


def fix_page_css(html_content):
    """Fix all CSS issues within the <style> block."""
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html_content, re.DOTALL | re.I)
    if not style_match:
        return html_content

    css = style_match.group(1)

    # Step 1: Fix orphaned CSS vars
    css = fix_orphaned_css_vars(css)

    # Step 2: Deduplicate theme blocks
    css = deduplicate_css_blocks(css)

    # Step 3: Clean up double semicolons, extra spaces
    css = re.sub(r';\s*;', ';', css)
    css = re.sub(r'\{\s+', '{ ', css)
    css = re.sub(r'\;\s+', '; ', css)

    new_html = html_content[:style_match.start(1)] + css + html_content[style_match.end(1):]
    return new_html


def fix_navbar(html_content, page_type):
    """Ensure the page has a proper navbar."""
    # Check if navbar already exists
    if '<nav>' in html_content or 'class="navbar"' in html_content:
        # Try to normalize existing nav to standard format
        # Look for inline-style navs and replace
        nav_match = re.search(r'<nav[^>]*style="[^"]*"[^>]*>(.*?)</nav>', html_content, re.DOTALL | re.I)
        if nav_match:
            new_html = html_content[:nav_match.start()] + NAVBAR_HTML + html_content[nav_match.end():]
            return new_html
        return html_content  # Already has a nav

    # Find </head> or <body> to insert before
    head_end = html_content.find('</head>')
    body_start = html_content.find('<body')

    if head_end != -1:
        insert_pos = head_end + 7
    elif body_start != -1:
        insert_pos = body_start + 6  # after <body
    else:
        return html_content

    return html_content[:insert_pos] + '\n' + NAVBAR_HTML + html_content[insert_pos:]


def add_back_link(html_content):
    """Add a 'Back to Genesis' link if one doesn't exist."""
    if 'Back to Genesis' in html_content or 'back-link' in html_content:
        # Check if it's inline-styled and replace with proper class
        inline_match = re.search(r'<a[^>]*class="back-link"[^>]*style="[^"]*"[^>]*>(.*?)</a>', html_content, re.DOTALL | re.I)
        if inline_match:
            new_link = BACK_LINK_HTML + '<style>.back-link { position: fixed; top: 80px; left: 24px; color: var(--accent-soft); text-decoration: none; font-size: 14px; z-index: 100; opacity: 0.7; transition: opacity 0.3s; } .back-link:hover { opacity: 1; }</style>'
            return html_content[:inline_match.start()] + new_link + html_content[inline_match.end():]
        return html_content

    body_start = html_content.find('<body')
    if body_start != -1:
        insert_pos = body_start + len(html_content[body_start:body_start+200].split('>')[0]) + 1
        return html_content[:insert_pos] + '\n' + BACK_LINK_HTML + html_content[insert_pos:]

    # Fallback: after </head>
    head_end = html_content.find('</head>')
    if head_end != -1:
        return html_content[:head_end + 7] + '\n' + BACK_LINK_HTML + html_content[head_end + 7:]

    return html_content


def add_orbs(html_content):
    """Add background glow orbs if they don't exist."""
    if 'class="bg-glow"' in html_content:
        return html_content

    body_start = html_content.find('<body')
    if body_start != -1:
        # Find the end of the <body> tag
        body_tag_end = html_content.find('>', body_start) + 1
        return html_content[:body_tag_end] + '\n' + ORBS_HTML + html_content[body_tag_end:]

    head_end = html_content.find('</head>')
    if head_end != -1:
        return html_content[:head_end + 7] + '\n' + ORBS_HTML + html_content[head_end + 7:]

    return html_content


def add_footer(html_content):
    """Add footer if it doesn't exist."""
    if '<footer>' in html_content or '</footer>' in html_content:
        return html_content

    body_close = html_content.rfind('</body>')
    if body_close != -1:
        return html_content[:body_close] + '\n' + FOOTER_HTML + html_content[body_close:]

    return html_content


def fix_page(html_path):
    """Apply all fixes to a single HTML file. Returns (success, changes_made)."""
    filename = os.path.basename(html_path)

    try:
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {filename}: {e}")
        return False, []

    original = content
    changes = []

    # Step 1: Fix CSS (orphaned vars, duplicates)
    content = fix_page_css(content)
    changes.append("fixed CSS issues")

    # Step 2: Clean inline body styles
    before = content
    content = clean_inline_body_styles(content)
    if content != before:
        changes.append("cleaned inline body styles")

    # Step 3: Add navbar
    before = content
    content = fix_navbar(content, detect_page_type(content))
    if content != before:
        changes.append("added navbar")

    # Step 4: Add back link
    before = content
    content = add_back_link(content)
    if content != before:
        changes.append("added back link")

    # Step 5: Add background orbs
    before = content
    content = add_orbs(content)
    if content != before:
        changes.append("added background orbs")

    # Step 6: Add footer (for info pages only)
    page_type = detect_page_type(content)
    if page_type != 'canvas':
        before = content
        content = add_footer(content)
        if content != before:
            changes.append("added footer")

    # Step 7: Wrap content in doc-page for info pages
    if page_type == 'info' and 'class="doc-page"' not in content:
        before = content
        content = wrap_content_in_doc_page(content, page_type)
        if content != before:
            changes.append("wrapped content in doc-page")

    # Write back if changed
    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes

    return False, []


def main():
    print("=" * 60)
    print("Genesis Web Page Fixer — Comprehensive Repair")
    print("=" * 60)

    html_files = sorted([
        f for f in os.listdir(BASE)
        if f.endswith('.html') 
        and f != 'index.html' 
        and not f.startswith('backup')
        and not os.path.isdir(os.path.join(BASE, f))
    ])

    print(f"\nFound {len(html_files)} subpages to fix.\n")

    fixed_count = 0
    error_count = 0
    total_changes = 0

    for i, filename in enumerate(html_files, 1):
        filepath = BASE / filename
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            page_type = detect_page_type(f.read())

        try:
            success, changes = fix_page(str(filepath))
            if success:
                fixed_count += 1
                total_changes += len(changes)
                print(f"  [{i:3d}/{len(html_files)}] FIXED: {filename:45s} ({', '.join(changes)})")
            else:
                print(f"  [{i:3d}/{len(html_files)}] SKIP:  {filename:45s} (already clean)")
        except Exception as e:
            error_count += 1
            print(f"  [{i:3d}/{len(html_files)}] ERROR: {filename:45s} ({e})")

    print("\n" + "=" * 60)
    print(f"Results: {fixed_count} fixed, {error_count} errors, {len(html_files) - fixed_count - error_count} skipped")
    print(f"Total changes applied: {total_changes}")
    print("=" * 60)


if __name__ == '__main__':
    main()
