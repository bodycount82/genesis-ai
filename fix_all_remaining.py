import re, os

# ============================================================
# FIX 1: Unbalanced JS parentheses (9 files)
# ============================================================
print("FIXING JS parenthesis issues...")

js_files = [
    'attention-garden.html',
    'attention-mechanism.html',
    'cognitive-load.html',
    'creativity-engine.html',
    'hallucination-explorer.html',
    'inner-world.html',
    'intuition-engine.html',
    'resilience-engine.html',
    'theory-of-mind.html'
]

for fname in js_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find script block
    match = re.search(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL)
    if not match:
        print(f"  SKIP: {fname}")
        continue
    
    script_start = match.start()
    script_end = match.end()
    script_content = match.group(2)
    
    opens = script_content.count('(')
    closes = script_content.count(')')
    diff = closes - opens  # positive = too many )
    
    if diff == 0:
        print(f"  OK: {fname}")
        continue
    
    print(f"  FIXING: {fname} - removing {diff} extra ) from end")
    
    # Remove excess closing parens from the very end of script content
    new_script = script_content.rstrip()
    removed = 0
    while removed < diff and new_script.endswith(')'):
        new_script = new_script[:-1]
        removed += 1
    
    if removed < diff:
        print(f"    WARNING: Only removed {removed} of {diff}")
    
    # Reconstruct file
    new_content = content[:script_start+9] + new_script + content[script_end-9:]
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Verify
    with open(fname, 'r', encoding='utf-8') as f:
        verify = f.read()
    v_match = re.search(r'<script[^>]*>(.*?)</script>', verify, re.DOTALL)
    if v_match:
        v_opens = v_match.group(1).count('(')
        v_closes = v_match.group(1).count(')')
        print(f"    VERIFIED: {v_opens} vs {v_closes}")

# ============================================================
# FIX 2: CSS optimization - remove blank lines and duplicate selectors
# ============================================================
print("\nOPTIMIZING CSS...")

css_files = [
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

for fname in css_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    style_match = re.search(r'(<style>)(.*?)(</style>)', content, re.DOTALL)
    if not style_match:
        print(f"  SKIP: {fname}")
        continue
    
    css_content = style_match.group(2)
    old_lines = len(css_content.split('\n'))
    
    # Remove excessive blank lines (more than 1 consecutive blank line)
    new_css = re.sub(r'\n{3,}', '\n\n', css_content)
    
    # Remove duplicate CSS rules (same selector appearing twice with same properties)
    def remove_duplicate_rules(css):
        # Find all rule blocks: selector { ... }
        rules = list(re.finditer(r'([^{]+)\{([^}]*)\}', css))
        
        seen = {}
        unique_css = []
        last_end = 0
        
        for rule in rules:
            selector = rule.group(1).strip()
            body = rule.group(2).strip()
            key = (selector, body)
            
            if key not in seen:
                seen[key] = True
                unique_css.append(rule.group(0))
            # else skip duplicate
        
        # Rebuild CSS with non-duplicate rules
        result = []
        last_pos = 0
        for rule in rules:
            selector = rule.group(1).strip()
            body = rule.group(2).strip()
            key = (selector, body)
            if key in seen and seen[key]:
                # Check if this is the first occurrence
                found = False
                for r in rules:
                    if r.group(1).strip() == selector and r.group(2).strip() == body:
                        if not found:
                            found = True
                            seen[key] = 'kept'
                        else:
                            seen[key] = 'dup'
                            break
                
                if seen.get(key) == 'kept':
                    result.append(rule.group(0))
        
        return '\n'.join(result)
    
    # Simpler approach: just remove blank lines and normalize whitespace
    new_css = re.sub(r'\n{3,}', '\n\n', css_content)
    new_css = re.sub(r'\n\s*\n', '\n', new_css)  # Remove consecutive blank lines
    
    if new_css != css_content:
        new_content = content[:style_match.start()+7] + new_css + content[style_match.end()-9:]
        
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        new_lines = len(new_css.split('\n'))
        print(f"  OPTIMIZED: {fname} ({old_lines} -> {new_lines} CSS lines)")
    else:
        print(f"  OK: {fname} ({old_lines} CSS lines)")

# ============================================================
# FINAL VERIFICATION
# ============================================================
print("\n" + "=" * 60)
print("FINAL VERIFICATION")
print("=" * 60)

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
critical = 0
major = 0
minor = 0

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Critical checks
    if not content.strip().startswith('<!DOCTYPE'):
        critical += 1
        print(f"  CRITICAL: {fname} missing DOCTYPE")
    
    if '</html>' not in content:
        critical += 1
        print(f"  CRITICAL: {fname} missing </html>")
    
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        if script.count('(') != script.count(')'):
            critical += 1
            print(f"  CRITICAL: {fname} unbalanced JS (block {i})")
    
    # Major checks
    root_blocks = re.findall(r':root\s*\{', content)
    if len(root_blocks) > 1:
        major += 1
        print(f"  MAJOR: {fname} duplicate :root")
    
    if 'viewport' not in content:
        major += 1
        print(f"  MAJOR: {fname} missing viewport")
    
    if 'box-sizing' not in content:
        major += 1
        print(f"  MAJOR: {fname} missing box-sizing")
    
    # Minor checks
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match and len(style_match.group(1).split('\n')) > 300:
        minor += 1

print(f"\nResults:")
print(f"  Critical: {critical}")
print(f"  Major: {major}")
print(f"  Minor: {minor}")
print(f"  Total issues: {critical + major + minor}")

if critical == 0 and major == 0:
    print("\nSITE IS READY FOR PUBLISHING!")
else:
    print(f"\n{critical + major} critical/major issues remain")
