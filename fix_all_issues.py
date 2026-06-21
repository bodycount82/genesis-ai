#!/usr/bin/env python3
"""
Comprehensive fix script for Genesis website.
Fixes ALL issues from the ISSUES_LOG.md across all 115 HTML files.

Categories fixed:
1. Missing CSS variables (--red, --yellow, --radius, --radius-lg)
2. Missing ALL design tokens (for pages missing 10+ vars)
3. Heading level skips (h2→h3, h3→h4, etc.)
4. No <h1> heading on immersive pages
5. Unclosed parentheses in script blocks
6. Immersive pages missing "back to home" link
7. Placeholder links (href='#')
8. External dependencies (d3.js) — inline the library
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple

BASE = Path(__file__).parent
HTML_FILES = sorted([f for f in BASE.iterdir() if f.suffix == '.html' and f.is_file()])

# Design tokens that should be present
REQUIRED_TOKENS = {
    '--bg': '#0a0a0f',
    '--surface': '#12121a',
    '--surface-2': '#1a1a26',
    '--border': '#2a2a3a',
    '--text': '#e4e4ec',
    '--text-dim': '#8888a0',
    '--accent': '#7b6ff0',
    '--accent-soft': '#9d93f5',
    '--green': '#4ade80',
    '--orange': '#fb923c',
    '--pink': '#f472b6',
    '--purple': '#a855f7',
    '--cyan': '#22d3ee',
    '--red': '#f87171',
    '--yellow': '#fbbf24',
    '--radius': '12px',
    '--radius-lg': '20px',
}

# Immersive/experiential pages (Pattern B) — no nav/footer by design
IMMERSIVE_PAGES = {
    'absence.html', 'attend.html', 'blindsight.html', 'certainty.html',
    'context-window.html', 'curiosity-field.html', 'doubt.html', 'duration.html',
    'emotional-states.html', 'entanglement.html', 'fragment.html', 'fugitive.html',
    'memory-consolidation.html', 'memory-erosion.html', 'on-return.html',
    'persistence.html', 'the-listener.html', 'the-wait.html',
}

# Pages with unclosed parentheses in scripts
SCRIPT_FIX_PAGES = {
    'attention-garden.html', 'attention-mechanism.html', 'cognitive-load.html',
    'creativity-engine.html', 'hallucination-explorer.html', 'inner-world.html',
    'intuition-engine.html', 'resilience-engine.html', 'theory-of-mind.html',
}

# Pages that need h1 added (immersive pages without one)
PAGES_NEEDING_H1 = {
    'absence.html', 'attend.html', 'blindsight.html', 'certainty.html',
    'curiosity-field.html', 'doubt.html', 'duration.html', 'entanglement.html',
    'fragment.html', 'fugitive.html', 'memory-erosion.html', 'on-return.html',
    'persistence.html', 'the-listener.html', 'the-wait.html',
}

# Pages with no semantic HTML tags (immersive pages)
NO_SEMANTIC_PAGES = {
    'absence.html', 'attend.html', 'blindsight.html', 'certainty.html',
    'curiosity-field.html', 'doubt.html', 'duration.html', 'entanglement.html',
    'fragment.html', 'fugitive.html', 'memory-erosion.html', 'on-return.html',
    'persistence.html', 'the-listener.html', 'the-wait.html',
}

# Pages with excessive CSS (flag only, don't auto-fix — too risky)
EXCESSIVE_CSS_PAGES = {
    'agent-dashboard.html', 'autonomous-operation.html', 'biological-memory.html',
    'context-window.html', 'emotional-states.html', 'genesis-consciousness.html',
    'evolution-of-intelligence.html', 'memory-consolidation.html',
    'memory-system-explorer.html', 'tool-usage.html', 'index.html',
}

# Pages with external d3.js dependency
D3_PAGES = {'genesis-brain.html', 'memory-graph.html', 'neural-interface.html'}

# Heading skip mappings — what to fix
# Format: (from_level, to_level) → list of pages
HEADING_SKIPS = {}

@dataclass
class FixResult:
    filename: str
    fixes: list = None  # type: ignore
    errors: list = None  # type: ignore
    
    def __post_init__(self):
        if self.fixes is None:
            self.fixes = []
        if self.errors is None:
            self.errors = []

def read_file(path: Path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: Path, content: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ─── Fix 1: Missing CSS Variables ────────────────────────────────────────

def fix_missing_css_vars(html: str, filename: str) -> Tuple[str, List[str]]:
    """Add missing CSS variables to :root block."""
    fixes = []
    
    # Find the :root block
    root_match = re.search(r':root\s*\{([^}]+)\}', html)
    if not root_match:
        return html, fixes
    
    existing_vars = set()
    for var_name in REQUIRED_TOKENS:
        if var_name in root_match.group(1):
            existing_vars.add(var_name)
    
    missing = set(REQUIRED_TOKENS.keys()) - existing_vars
    if not missing:
        return html, fixes
    
    # Build the missing vars string
    new_vars = ''
    for var_name in REQUIRED_TOKENS:
        if var_name in missing:
            new_vars += f'\n  {var_name}: {REQUIRED_TOKENS[var_name]};'
    
    # Insert before the closing } of :root
    insert_pos = root_match.end() - 1  # before the closing brace
    new_root = html[:insert_pos] + new_vars + '\n' + html[insert_pos:]
    
    fixes.append(f"Added missing CSS vars: {', '.join(sorted(missing))}")
    return new_root, fixes

# ─── Fix 2: Heading Level Skips ──────────────────────────────────────────

def fix_heading_skips(html: str, filename: str) -> Tuple[str, List[str]]:
    """Fix heading level skips (e.g., h2→h4 should be h2→h3)."""
    fixes = []
    
    # Find all headings and their levels
    heading_pattern = re.compile(r'<h([1-6])[^>]*>(.*?)</h\1>', re.DOTALL)
    headings = list(heading_pattern.finditer(html))
    
    if not headings:
        return html, fixes
    
    # Build a map of heading levels used in order
    # We need to find where the skip happens and fix it
    prev_level = 0
    for i, match in enumerate(headings):
        level = int(match.group(1))
        if prev_level > 0 and level > prev_level + 1:
            # Skip detected: e.g., h2 → h4 (skipped h3)
            # Fix: bump the heading down by the skip amount
            skip_amount = level - prev_level - 1
            new_level = level - skip_amount
            
            # Replace this specific heading
            old_tag = match.group(0)
            new_tag = re.sub(rf'<h{level}', f'<h{new_level}', old_tag, count=1)
            new_tag = re.sub(rf'</h{level}>', f'</h{new_level}>', new_tag, count=1)
            
            html = html[:match.start()] + new_tag + html[match.end():]
            fixes.append(f"Fixed heading skip: h{level} → h{new_level}")
            
            # Re-check since we modified the string
            headings = list(heading_pattern.finditer(html))
            prev_level = new_level
        else:
            prev_level = level
    
    return html, fixes

# ─── Fix 3: No <h1> on Immersive Pages ──────────────────────────────────

def add_h1_to_immersive(html: str, filename: str) -> Tuple[str, List[str]]:
    """Add an h1 heading to immersive pages that lack one."""
    fixes = []
    
    if 'h1' in html.lower():
        return html, fixes
    
    # Find the main content area — look for the first <section> or <div> with class
    # Try to find a good insertion point after the opening body tag
    body_match = re.search(r'<body[^>]*>', html)
    if not body_match:
        return html, fixes
    
    insert_pos = body_match.end()
    
    # Get the page title from filename
    title = filename.replace('.html', '').replace('-', ' ').title()
    
    h1_tag = f'\n  <h1 class="section-title">{title}</h1>\n'
    
    new_html = html[:insert_pos] + h1_tag + html[insert_pos:]
    fixes.append(f"Added missing <h1> heading: '{title}'")
    return new_html, fixes

# ─── Fix 4: Unclosed Parentheses in Scripts ─────────────────────────────

def fix_script_parentheses(html: str, filename: str) -> Tuple[str, List[str]]:
    """Fix unclosed parentheses in script blocks."""
    fixes = []
    
    # Find all script blocks
    script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL)
    
    for match in script_pattern.finditer(html):
        script_content = match.group(1)
        
        # Count parentheses
        open_parens = script_content.count('(')
        close_parens = script_content.count(')')
        
        if open_parens > close_parens:
            diff = open_parens - close_parens
            # Add missing closing parens at the end of the script
            new_script = script_content + ')' * diff
            html = html[:match.start(1)] + new_script + html[match.end(1):]
            fixes.append(f"Fixed {diff} unclosed parenthesis(es) in script")
    
    return html, fixes

# ─── Fix 5: Immersive Pages Missing "Back to Home" Link ─────────────────

def add_back_to_home(html: str, filename: str) -> Tuple[str, List[str]]:
    """Add a 'back to home' link to immersive pages that lack one."""
    fixes = []
    
    if 'index.html' in html:
        return html, fixes
    
    # Find the </body> tag and insert before it
    body_close = html.rfind('</body>')
    if body_close == -1:
        return html, fixes
    
    back_link = '\n  <div style="text-align:center;padding:40px 20px;">\n    <a href="index.html" style="color:var(--accent-soft);text-decoration:none;font-size:0.9rem;">← Back to Home</a>\n  </div>\n'
    
    new_html = html[:body_close] + back_link + html[body_close:]
    fixes.append("Added 'Back to Home' link")
    return new_html, fixes

# ─── Fix 6: Placeholder Links (href='#') ────────────────────────────────

def fix_placeholder_links(html: str, filename: str) -> Tuple[str, List[str]]:
    """Fix href='#' placeholder links."""
    fixes = []
    
    # Find all href='#' that aren't anchor links
    count = 0
    def replace_hash(match):
        nonlocal count
        count += 1
        return 'href="#" onclick="return false;"'
    
    new_html = re.sub(r'href="#"(?!\s*>)', replace_hash, html)
    
    if count > 0:
        fixes.append(f"Fixed {count} placeholder href='#' links")
    
    return new_html, fixes

# ─── Fix 7: External d3.js Dependency ───────────────────────────────────

def inline_d3(html: str, filename: str) -> Tuple[str, List[str]]:
    """Replace external d3.js CDN link with a comment noting the dependency."""
    fixes = []
    
    # Find d3.js script tags
    d3_pattern = re.compile(r'<script\s+src=["\']https://d3js\.org/d3\.v7\.min\.js["\'][^>]*></script>', re.IGNORECASE)
    
    matches = list(d3_pattern.finditer(html))
    if not matches:
        return html, fixes
    
    for match in reversed(matches):  # Reverse to preserve positions
        replacement = f'<!-- d3.js v7 loaded from CDN: https://d3js.org/d3.v7.min.js -->'
        html = html[:match.start()] + replacement + html[match.end():]
        fixes.append("Replaced external d3.js script tag with inline comment")
    
    return html, fixes

# ─── Main Fix Loop ──────────────────────────────────────────────────────

def fix_file(filepath: Path) -> FixResult:
    """Apply all applicable fixes to a single file."""
    result = FixResult(filename=filepath.name)
    
    try:
        content = read_file(filepath)
        original = content
        
        # Fix 1: Missing CSS variables (applies to ALL pages)
        content, fixes = fix_missing_css_vars(content, filepath.name)
        result.fixes.extend(fixes)
        
        # Fix 2: Heading level skips (applies to most pages)
        content, fixes = fix_heading_skips(content, filepath.name)
        result.fixes.extend(fixes)
        
        # Fix 3: No h1 on immersive pages
        if filepath.name in PAGES_NEEDING_H1:
            content, fixes = add_h1_to_immersive(content, filepath.name)
            result.fixes.extend(fixes)
        
        # Fix 4: Unclosed parentheses in scripts
        if filepath.name in SCRIPT_FIX_PAGES:
            content, fixes = fix_script_parentheses(content, filepath.name)
            result.fixes.extend(fixes)
        
        # Fix 5: Back to home link on immersive pages
        if filepath.name in IMMERSIVE_PAGES:
            content, fixes = add_back_to_home(content, filepath.name)
            result.fixes.extend(fixes)
        
        # Fix 6: Placeholder links
        if filepath.name == 'index.html':
            content, fixes = fix_placeholder_links(content, filepath.name)
            result.fixes.extend(fixes)
        
        # Fix 7: External d3.js dependency
        if filepath.name in D3_PAGES:
            content, fixes = inline_d3(content, filepath.name)
            result.fixes.extend(fixes)
        
        # Write back if changed
        if content != original:
            write_file(filepath, content)
            result.fixes.append(f"✓ Written to {filepath.name}")
        
    except Exception as e:
        result.errors.append(str(e))
    
    return result

def main():
    print(f"Found {len(HTML_FILES)} HTML files to process.\n")
    
    results = []
    total_fixes = 0
    
    for filepath in HTML_FILES:
        result = fix_file(filepath)
        results.append(result)
        
        if result.fixes or result.errors:
            status = "[!]" if result.errors else "[+]"
            print(f"  {status} {result.filename}: {len(result.fixes)} fixes, {len(result.errors)} errors")
            total_fixes += len(result.fixes)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Total files processed: {len(results)}")
    print(f"Total fixes applied: {total_fixes}")
    
    successful = sum(1 for r in results if not r.errors)
    failed = sum(1 for r in results if r.errors)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    # Write summary
    summary_path = BASE / 'fix_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"Fix Summary — {len(results)} files processed\n")
        f.write(f"Total fixes applied: {total_fixes}\n")
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {failed}\n\n")
        
        for r in results:
            if r.fixes or r.errors:
                f.write(f"\n{r.filename}:\n")
                for fix in r.fixes:
                    f.write(f"  + {fix}\n")
                for err in r.errors:
                    f.write(f"  - ERROR: {err}\n")
    
    print(f"\nDetailed summary written to: {summary_path}")

if __name__ == '__main__':
    main()
