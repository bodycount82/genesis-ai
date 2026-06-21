import re, os

files = [
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

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all :root blocks
    root_pattern = r':root\s*\{[^}]*\}'
    matches = list(re.finditer(root_pattern, content))
    
    if len(matches) < 2:
        print(f"SKIP: {fname} ({len(matches)} :root blocks)")
        continue
    
    # Check if first block has ---- (4 dashes) - that's the duplicate to remove
    first_block = matches[0].group(0)
    if '----' in first_block:
        # Remove the first :root block entirely
        new_content = content[:matches[0].start()] + content[matches[0].end():]
        
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"FIXED: {fname} - removed first :root block (had ---- prefix)")
    else:
        # Check if second block has ---- 
        if len(matches) >= 2:
            second_block = matches[1].group(0)
            if '----' in second_block:
                new_content = content[:matches[1].start()] + content[matches[1].end():]
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"FIXED: {fname} - removed second :root block (had ---- prefix)")
            else:
                print(f"SKIP: {fname} (no ---- found in either block)")
        else:
            print(f"SKIP: {fname}")

print("\nDone!")
