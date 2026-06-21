import re, os

files = [
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

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if not style_match:
        print(f"SKIP: {fname}")
        continue
    
    css = style_match.group(1)
    lines = css.split('\n')
    
    # Count blank lines
    blank_lines = sum(1 for l in lines if not l.strip())
    
    # Count duplicate selectors
    selectors = re.findall(r'([.#\w][^{}]*?)\s*\{', css)
    dup_selectors = {}
    for s in selectors:
        s_clean = s.strip()
        if s_clean not in dup_selectors:
            dup_selectors[s_clean] = 0
        dup_selectors[s_clean] += 1
    
    dups = {k: v for k, v in dup_selectors.items() if v > 1}
    
    print(f"{fname}: {len(lines)} lines, {blank_lines} blank, {len(selectors)} selectors, {len(dups)} duplicate selectors")
    if dups:
        for sel, count in list(dups.items())[:5]:
            print(f"  DUPLICATE: {sel} ({count}x)")
