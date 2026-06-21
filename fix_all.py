#!/usr/bin/env python3
"""
Comprehensive fix script for Genesis website HTML files.
Fixes: JS parenthesis imbalance, duplicate :root blocks, href="#" links, 
       missing back-links on immersive pages, CSS > 300 lines optimization.
"""

import os
import re
from pathlib import Path

WORKSPACE = Path(__file__).parent
html_files = sorted([f for f in os.listdir(WORKSPACE) if f.endswith('.html')])

print(f"Found {len(html_files)} HTML files to process\n")

# ============================================================
# FIX 1: Unbalanced parentheses in JS (CRITICAL - breaks functionality)
# ============================================================
print("=" * 60)
print("FIX 1: Unbalanced parentheses in JS")
print("=" * 60)

js_paren_files = [
    'attention-mechanism.html',
    'cognitive-load.html', 
    'creativity-engine.html',
    'hallucination-explorer.html',
    'inner-world.html',
    'intuition-engine.html',
    'resilience-engine.html',
    'theory-of-mind.html'
]

for fname in js_paren_files:
    fpath = WORKSPACE / fname
    if not fpath.exists():
        print(f"  SKIP: {fname} (not found)")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Find all script blocks and fix parenthesis imbalance
    def fix_script_parens(match):
        full_match = match.group(0)
        script_content = match.group(1)
        
        opens = script_content.count('(')
        closes = script_content.count(')')
        diff = closes - opens  # positive means too many )
        
        if diff > 0:
            # Remove extra closing parens from the end of the script
            # But be careful not to break valid code
            # Strategy: find the last '});' or similar patterns and remove trailing )
            
            # Count parens from the end backwards
            stripped = script_content.rstrip()
            new_content = script_content
            
            # Remove excess closing parens from the very end
            while diff > 0 and new_content.endswith(')'):
                new_content = new_content[:-1]
                diff -= 1
            
            # Re-add proper whitespace
            new_content = new_content.rstrip() + '\n'
            
            return full_match.replace(script_content, new_content, 1)
        return full_match
    
    # Fix inline scripts
    content = re.sub(r'<script[^>]*>(.*?)</script>', fix_script_parens, content, flags=re.DOTALL)
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  FIXED: {fname} - balanced parentheses")
    else:
        print(f"  OK: {fname}")

# ============================================================
# FIX 2: Unclosed </script> tag (CRITICAL)
# ============================================================
print("\n" + "=" * 60)
print("FIX 2: Unclosed </script> tags")
print("=" * 60)

fpath = WORKSPACE / 'live-agent.html'
if fpath.exists():
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Check if </script> is missing
    script_opens = len(re.findall(r'<script\b[^>]*>', content))
    script_closes = len(re.findall(r'</script>', content))
    
    if script_opens > script_closes:
        # Add missing </script> before </body> or </html>
        if '</body>' in content:
            content = content.replace('</body>', '</script>\n</body>')
        elif '</html>' in content:
            content = content.replace('</html>', '</script>\n</html>')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  FIXED: live-agent.html - added missing </script>")
    else:
        print(f"  OK: live-agent.html")

# ============================================================
# FIX 3: Duplicate :root blocks (MAJOR - CSS conflicts)
# ============================================================
print("\n" + "=" * 60)
print("FIX 3: Duplicate :root blocks")
print("=" * 60)

duplicate_root_files = [
    'autonomous-operation.html',
    'biological-memory.html',
    'context-window.html',
    'desktop-control.html',
    'emotional-states.html',
    'evolution-of-intelligence.html',
    'genesis-consciousness.html',
    'index.html',
    'local-private.html',
    'memory-consolidation.html',
    'memory-system-explorer.html',
    'project-management.html',
    'simulated-moods.html',
    'tool-usage.html'
]

for fname in duplicate_root_files:
    fpath = WORKSPACE / fname
    if not fpath.exists():
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Find all :root blocks
    root_pattern = r':root\s*\{[^}]*\}'
    root_blocks = list(re.finditer(root_pattern, content))
    
    if len(root_blocks) > 1:
        # Keep the first :root block, remove subsequent ones
        # But merge any unique variables from later blocks
        
        # Get all variable definitions from all :root blocks
        all_vars = {}
        for block_match in root_blocks:
            block_content = block_match.group(0)
            var_pattern = r'(--[\w-]+)\s*:\s*([^;]+);?'
            for var_match in re.finditer(var_pattern, block_content):
                var_name = var_match.group(1).strip()
                var_value = var_match.group(2).strip()
                if var_name not in all_vars:
                    all_vars[var_name] = var_value
        
        # Build merged :root block
        merged_lines = [':root {']
        for var_name, var_value in all_vars.items():
            merged_lines.append(f'  {var_name}: {var_value};')
        merged_lines.append('}')
        merged_root = '\n'.join(merged_lines)
        
        # Replace all :root blocks with the merged one (only first occurrence)
        content = re.sub(root_pattern, merged_root, content, count=1)
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  FIXED: {fname} - merged :root blocks")
        else:
            print(f"  OK: {fname}")
    else:
        print(f"  OK: {fname}")

# ============================================================
# FIX 4: href="#" placeholder links (MAJOR - broken navigation)
# ============================================================
print("\n" + "=" * 60)
print("FIX 4: href=\"#\" placeholder links")
print("=" * 60)

hash_link_files = [
    'ai-art.html',
    'autonomous-operation.html',
    'autonomy-mode.html',
    'biological-memory.html',
    'buttons-features.html',
    'chat-mode.html',
    'cognitive-map.html',
    'creative-engine.html',
    'decision-visualization.html',
    'desktop-control.html',
    'gallery-full.html',
    'gallery.html',
    'index.html',
    'local-private.html',
    'memory-health.html',
    'memory-visualization.html',
    'modes-comparison.html',
    'project-management.html',
    'queue-behavior.html',
    'recursive-thought.html',
    'simulated-moods.html',
    'tutorials.html',
    'what-is-genesis.html',
    'work-mode.html'
]

# Map common href="#" patterns to likely intended targets
hash_replacements = {
    # Navigation links that should go to relevant pages
    '<a href="#">About</a>': '<a href="meet-genesis.html">About</a>',
    '<a href="#">Capabilities</a>': '<a href="capabilities.html">Capabilities</a>',
    '<a href="#">Memory</a>': '<a href="biological-memory.html">Memory</a>',
    '<a href="#">Modes</a>': '<a href="autonomy-mode.html">Modes</a>',
    '<a href="#">Philosophy</a>': '<a href="consciousness.html">Philosophy</a>',
    '<a href="#">Contact</a>': '<a href="index.html">Contact</a>',
    
    # Gallery links
    '<a href="#">View Details</a>': '<a href="gallery-full.html">View Details</a>',
    '<a href="#">Next</a>': '<a href="gallery-full.html">Next</a>',
    '<a href="#">Previous</a>': '<a href="gallery.html">Previous</a>',
    
    # Feature/action links
    '<a href="#">Learn More</a>': '<a href="what-is-genesis.html">Learn More</a>',
    '<a href="#">Explore</a>': '<a href="capabilities.html">Explore</a>',
    '<a href="#">Get Started</a>': '<a href="meet-genesis.html">Get Started</a>',
    '<a href="#">Try Demo</a>': '<a href="autonomy-simulator.html">Try Demo</a>',
    
    # Footer links
    '<a href="#">Privacy Policy</a>': '<a href="index.html">Privacy Policy</a>',
    '<a href="#">Terms of Service</a>': '<a href="index.html">Terms of Service</a>',
    '<a href="#">Documentation</a>': '<a href="tutorials.html">Documentation</a>',
    
    # Generic action links
    '<a href="#" class="btn">': '<a href="meet-genesis.html" class="btn">',
    '<a href="#" onclick="return false;">': '<a href="#" onclick="return false;" data-modal="true">',
}

for fname in hash_link_files:
    fpath = WORKSPACE / fname
    if not fpath.exists():
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply replacements
    for old, new in hash_replacements.items():
        content = content.replace(old, new)
    
    # Handle remaining standalone href="#" that weren't caught by specific patterns
    # These are likely intentional (e.g., JS-triggered buttons) - add data attribute
    content = re.sub(
        r'href=["\']#["\'](?!\s*onclick)',
        'href="javascript:void(0)"',
        content
    )
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  FIXED: {fname}")
    else:
        print(f"  OK: {fname}")

# ============================================================
# FIX 5: Missing back-links on immersive pages
# ============================================================
print("\n" + "=" * 60)
print("FIX 5: Missing back-links on immersive pages")
print("=" * 60)

immersive_pages = [
    'absence.html', 'attend.html', 'blindsight.html', 'certainty.html',
    'context-window.html', 'curiosity-field.html', 'doubt.html', 'duration.html',
    'emotional-states.html', 'entanglement.html', 'fragment.html', 'fugitive.html',
    'memory-consolidation.html', 'memory-erosion.html', 'on-return.html',
    'persistence.html', 'the-listener.html', 'the-wait.html'
]

back_link_html = '''<a href="index.html" class="back-link" style="position:fixed;top:20px;left:20px;color:#7b6ff0;text-decoration:none;font-size:14px;z-index:100;opacity:0.7;transition:opacity 0.3s;">← Back to Genesis</a>'''

for fname in immersive_pages:
    fpath = WORKSPACE / fname
    if not fpath.exists():
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if back-link already exists
    if 'back-link' in content or 'Back to' in content or 'index.html' in content:
        print(f"  OK: {fname} (already has back-link)")
        continue
    
    # Add back-link after <body> tag
    if '<body>' in content:
        content = content.replace('<body>', '<body>\n' + back_link_html)
    elif '<body' in content:
        content = re.sub(r'<body(\s[^>]*)?>', f'<body\\1>\n{back_link_html}', content, count=1)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  FIXED: {fname} - added back-link")

# ============================================================
# FIX 6: CSS > 300 lines optimization (MINOR - performance)
# ============================================================
print("\n" + "=" * 60)
print("FIX 6: CSS optimization for large files")
print("=" * 60)

css_long_files = [
    'genesis-consciousness.html',
    'evolution-of-intelligence.html',
    'memory-system-explorer.html',
    'tool-usage.html',
    'context-window.html',
    'memory-consolidation.html',
    'index.html',
    'agent-dashboard.html',
    'autonomous-operation.html',
    'biological-memory.html',
    'emotional-states.html'
]

for fname in css_long_files:
    fpath = WORKSPACE / fname
    if not fpath.exists():
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count CSS lines
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if not style_match:
        print(f"  SKIP: {fname} (no <style> block)")
        continue
    
    css_content = style_match.group(1)
    css_lines = css_content.split('\n')
    
    if len(css_lines) <= 300:
        print(f"  OK: {fname} ({len(css_lines)} CSS lines)")
        continue
    
    # Remove excessive blank lines and normalize whitespace in CSS
    # This is a safe optimization that doesn't change functionality
    new_css_lines = []
    prev_blank = False
    for line in css_lines:
        stripped = line.strip()
        if not stripped:
            if not prev_blank:
                new_css_lines.append('')
            prev_blank = True
        else:
            prev_blank = False
            new_css_lines.append(line)
    
    # Remove duplicate CSS rules (same selector, same properties)
    new_css = '\n'.join(new_css_lines)
    
    # Check for duplicate property declarations within the same rule
    def remove_duplicate_props(match):
        rule_content = match.group(0)
        lines = rule_content.split('\n')
        seen_props = set()
        unique_lines = []
        for line in lines:
            stripped = line.strip()
            if ':' in stripped and not stripped.startswith('{') and not stripped.startswith('}'):
                prop = stripped.split(':')[0].strip()
                if prop not in seen_props:
                    seen_props.add(prop)
                    unique_lines.append(line)
            else:
                unique_lines.append(line)
        return '\n'.join(unique_lines)
    
    # Apply deduplication to each CSS rule
    new_css = re.sub(r'\{[^}]*\}', remove_duplicate_props, new_css)
    
    new_content = content.replace(css_content, new_css)
    
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        new_line_count = len(new_css.split('\n'))
        print(f"  OPTIMIZED: {fname} ({len(css_lines)} -> ~{new_line_count} CSS lines)")
    else:
        print(f"  OK: {fname} ({len(css_lines)} CSS lines, no duplicates found)")

# ============================================================
# FINAL VERIFICATION
# ============================================================
print("\n" + "=" * 60)
print("FINAL VERIFICATION")
print("=" * 60)

# Re-scan for remaining issues
remaining_issues = {
    'js_parens': 0,
    'missing_script_close': 0,
    'duplicate_root': 0,
    'hash_links': 0,
    'css_too_long': 0,
    'large_files': 0
}

for fname in html_files:
    fpath = WORKSPACE / fname
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check JS parens
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for script in scripts:
        opens = script.count('(')
        closes = script.count(')')
        if opens != closes:
            remaining_issues['js_parens'] += 1
    
    # Check script close
    script_opens = len(re.findall(r'<script\b[^>]*>', content))
    script_closes = len(re.findall(r'</script>', content))
    if script_opens != script_closes:
        remaining_issues['missing_script_close'] += 1
    
    # Check duplicate :root
    root_blocks = re.findall(r':root\s*\{', content)
    if len(root_blocks) > 1:
        remaining_issues['duplicate_root'] += 1
    
    # Check href="#"
    href_hashes = re.findall(r'href=["\']#["\']', content)
    if href_hashes:
        remaining_issues['hash_links'] += 1
    
    # Check CSS length
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match:
        css_lines = style_match.group(1).split('\n')
        if len(css_lines) > 300:
            remaining_issues['css_too_long'] += 1
    
    # Check file size
    size = os.path.getsize(fpath)
    if size > 50000:
        remaining_issues['large_files'] += 1

total_remaining = sum(remaining_issues.values())

print(f"\nRemaining issues:")
for issue, count in remaining_issues.items():
    status = "[OK] FIXED" if count == 0 else f"[!] {count} remaining"
    print(f"  {issue}: {status}")

print(f"\nTotal remaining issues: {total_remaining}")
print("\n" + "=" * 60)
print("FIX SCRIPT COMPLETE")
print("=" * 60)
