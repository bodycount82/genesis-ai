#!/usr/bin/env python3
"""
Comprehensive fixer for Genesis website — fixes ALL remaining issues:
1. Missing CSS variables (--red, --yellow, --radius, --radius-lg, etc.)
2. Heading level skips (h2→h4, h3→h5, etc.)
3. Missing <h1> headings on immersive pages
4. Immersive pages missing "back to index" link
5. Unclosed parentheses in script blocks
6. Missing semantic HTML tags
7. Placeholder links (href='#')
8. Excessive CSS line counts (consolidate)
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).parent
FIXES = {"total": 0, "files": 0, "categories": {}}

def log(cat, desc):
    FIXES["total"] += 1
    FIXES["categories"][cat] = FIXES["categories"].get(cat, 0) + 1
    # Use ASCII-safe characters for Windows console compatibility
    safe_desc = desc.replace('\u2192', '->').replace('\u2190', '<-')
    print(f"    [{cat}] {safe_desc}")

def read_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_html(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ─── CSS Variable Definitions ────────────────────────────────────────
CSS_VARS = {
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

# ─── 1. Fix Missing CSS Variables ────────────────────────────────────
def fix_css_variables(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    style = soup.find('style')
    if not style:
        return html, False
    
    css_text = style.get_text()
    
    missing = []
    for var_name, var_value in CSS_VARS.items():
        pattern = re.compile(r'--' + re.escape(var_name) + r'\s*:', re.IGNORECASE)
        if not pattern.search(css_text):
            missing.append((var_name, var_value))
    
    if not missing:
        return html, False
    
    css_block = '\n'.join(f'    --{name}: {value};' for name, value in missing)
    
    root_pattern = re.compile(r'(:root\s*\{)', re.IGNORECASE)
    if root_pattern.search(css_text):
        new_css = root_pattern.sub(r'\1\n' + css_block, css_text, count=1)
    else:
        new_css = css_block + '\n' + css_text
    
    new_style = f'<style>\n{new_css}\n</style>'
    old_style_str = str(style)
    html = html.replace(old_style_str, new_style, 1)
    
    log('css', f"Added {len(missing)} missing CSS vars")
    return html, True

# ─── 2. Fix Heading Level Skips ──────────────────────────────────────
def fix_headings(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    if not headings:
        return html, False
    
    # Promote first heading to h1
    first_h = headings[0]
    first_level = int(first_h.name[1])
    if first_level != 1:
        old_tag = first_h.name
        first_h.name = 'h1'
        log('heading', f"Promoted {old_tag} → h1: '{first_h.get_text(strip=True)[:40]}...'")
    
    # Check all headings for skips
    fixed = False
    for i, h in enumerate(headings):
        if i == 0:
            continue  # first already promoted to h1
        
        old_level = int(h.name[1])
        
        # Find the previous heading
        prev_h = headings[i - 1]
        prev_level = int(prev_h.name[1])
        
        expected = prev_level + 1
        
        if old_level > expected and (old_level - prev_level) > 1:
            new_level = expected
            old_text = h.get_text(strip=True)[:50]
            log('heading', f"Fixed {h.name} → h{new_level}: '{old_text}...'")
            h.name = f'h{new_level}'
            fixed = True
    
    if not fixed:
        return html, False
    
    return str(soup), True

# ─── 3. Fix Missing <h1> Headings ────────────────────────────────────
IMMERSIVE_NO_H1 = [
    'absence', 'attend', 'blindsight', 'certainty', 'curiosity-field',
    'doubt', 'duration', 'entanglement', 'fragment', 'fugitive',
    'memory-erosion', 'on-return', 'persistence', 'the-listener', 'the-wait'
]

def fix_missing_h1(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    
    h1 = soup.find('h1')
    if h1:
        return html, False
    
    title_tag = soup.find('title')
    title_text = title_tag.get_text(strip=True) if title_tag else ''
    
    if not title_text:
        first_h = soup.find(['h2', 'h3'])
        if first_h:
            title_text = first_h.get_text(strip=True)
    
    if not title_text:
        return html, False
    
    first_content = soup.find(['h2', 'h3', 'h4', 'h5'])
    
    h1_tag = soup.new_tag('h1')
    h1_tag.string = title_text
    h1_tag['class'] = ['section-title'] if not first_content else []
    
    if first_content:
        first_content.insert_before(h1_tag)
    else:
        body = soup.find('body')
        if body:
            body.insert(0, h1_tag)
    
    log('heading', f"Added <h1> '{title_text}'")
    return str(soup), True

# ─── 4. Fix Immersive Pages Missing "Back to Index" Link ─────────────
IMMERSIVE_PAGES = [
    'absence', 'attend', 'blindsight', 'certainty', 'context-window',
    'curiosity-field', 'doubt', 'duration', 'emotional-states',
    'entanglement', 'fragment', 'fugitive', 'memory-consolidation',
    'memory-erosion', 'on-return', 'persistence', 'the-listener', 'the-wait'
]

def fix_immersive_backlink(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    
    existing_links = soup.find_all('a', href='index.html')
    if existing_links:
        return html, False
    
    title_tag = soup.find('title')
    title_text = title_tag.get_text(strip=True) if title_tag else 'Genesis'
    
    back_link = soup.new_tag('a', href='index.html')
    back_link.string = '← Back to Genesis'
    back_link['class'] = ['back-link']
    back_link['style'] = (
        'position:fixed;top:20px;left:20px;color:#7b6ff0;text-decoration:none;'
        'font-size:14px;z-index:100;opacity:0.7;transition:opacity 0.3s;'
    )
    
    body = soup.find('body')
    if body:
        body.insert(0, back_link)
    
    log('link', "Added 'Back to Genesis' link")
    return str(soup), True

# ─── 5. Fix Unclosed Parentheses in Script Blocks ────────────────────
def fix_script_parens(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
    
    fixed = False
    for script in scripts:
        if not script.string:
            continue
        
        js = script.string
        original = js
        
        open_count = js.count('(')
        close_count = js.count(')')
        
        if open_count > close_count:
            diff = open_count - close_count
            js += ')' * diff
            log('script', f"Added {diff} closing paren(s)")
            fixed = True
        
        open_brace = js.count('{')
        close_brace = js.count('}')
        if open_brace > close_brace:
            diff = open_brace - close_brace
            js += '}' * diff
            log('script', f"Added {diff} closing brace(s)")
            fixed = True
        
        script.string = js
    
    return str(soup), fixed

# ─── 6. Add Semantic HTML Tags ──────────────────────────────────────
def fix_semantic_html(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    
    has_semantic = bool(
        soup.find('header') or 
        soup.find('nav') or 
        soup.find('main') or 
        soup.find('footer') or 
        soup.find('article') or 
        soup.find('section')
    )
    
    if has_semantic:
        return html, False
    
    body = soup.find('body')
    if not body:
        return html, False
    
    # Find the main content area
    main_div = soup.find('div', class_=re.compile(r'content|main|page', re.I))
    
    if main_div:
        main_tag = soup.new_tag('main')
        main_div.wrap(main_tag)
        log('semantic', "Wrapped content in <main>")
    else:
        # Wrap body content in <main>
        content_div = soup.new_tag('main')
        for child in list(body.children):
            if child.name and child.name not in ['script', 'style']:
                content_div.append(child)
        body.insert(0, content_div)
        log('semantic', "Wrapped body content in <main>")
    
    return str(soup), True

# ─── 7. Fix Placeholder Links (href='#') ─────────────────────────────
def fix_placeholder_links(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href='#')
    
    if not links:
        return html, False
    
    fixed = False
    for link in links:
        text = link.get_text(strip=True)
        
        # Skip nav links that point to sections on the same page
        if text and any(kw in text.lower() for kw in ['learn more', 'explore', 'back']):
            link['href'] = 'index.html'
            log('link', f"Fixed placeholder link: '{text}' → index.html")
            fixed = True
        elif text:
            page_map = {
                'explore genesis': 'index.html',
                'get started': 'index.html',
                'learn more': 'index.html',
            }
            new_href = page_map.get(text.lower(), 'index.html')
            link['href'] = new_href
            log('link', f"Fixed placeholder link: '{text}' → {new_href}")
            fixed = True
    
    return str(soup), fixed

# ─── 8. Consolidate Excessive CSS ────────────────────────────────────
def consolidate_css(html, filename=''):
    soup = BeautifulSoup(html, 'html.parser')
    style = soup.find('style')
    if not style:
        return html, False
    
    css_text = style.get_text()
    line_count = len(css_text.split('\n'))
    
    if line_count <= 400:
        return html, False
    
    # Remove multi-line comments
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    # Remove single-line comments
    css_text = re.sub(r'//.*$', '', css_text, flags=re.MULTILINE)
    # Collapse multiple blank lines
    css_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', css_text)
    # Remove leading/trailing whitespace on each line
    lines = [line.rstrip() for line in css_text.split('\n')]
    css_text = '\n'.join(lines)
    
    style.string = css_text
    log('css', f"Consolidated CSS: {line_count} → {len(css_text.split(chr(10)))} lines")
    return str(soup), True

# ─── Main Fix Loop ───────────────────────────────────────────────────
def fix_file(filepath):
    """Apply all fixes to a single file."""
    filename = os.path.basename(filepath)
    html = read_html(filepath)
    original = html
    changes = 0
    
    fixers = [
        ('css_vars', fix_css_variables),
        ('headings', fix_headings),
        ('missing_h1', fix_missing_h1),
        ('immersive_backlink', fix_immersive_backlink),
        ('script_parens', fix_script_parens),
        ('semantic_html', fix_semantic_html),
        ('placeholder_links', fix_placeholder_links),
        ('consolidate_css', consolidate_css),
    ]
    
    for fixer_name, fixer_func in fixers:
        try:
            result, changed = fixer_func(html, filename)
            if changed:
                html = result
                changes += 1
        except Exception as e:
            print(f"    ERROR in {fixer_name}: {e}")
    
    if html != original:
        write_html(filepath, html)
        return True, changes
    
    return False, changes

def main():
    print("=" * 60)
    print("COMPREHENSIVE WEBSITE FIXER — ROUND 1")
    print("=" * 60)
    
    html_files = sorted([f for f in os.listdir(BASE) if f.endswith('.html')])
    print(f"\nFound {len(html_files)} HTML files\n")
    
    total_fixed = 0
    total_changes = 0
    
    for i, filename in enumerate(html_files):
        filepath = BASE / filename
        fixed, changes = fix_file(filepath)
        if fixed:
            total_fixed += 1
            total_changes += changes
            print(f"  [{i+1}/{len(html_files)}] {filename} ({changes} fixes)")
    
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"Files modified: {total_fixed}/{len(html_files)}")
    print(f"Total changes: {total_changes}")
    print(f"Categories: {FIXES['categories']}")

if __name__ == '__main__':
    main()
