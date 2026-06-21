#!/usr/bin/env python3
"""Fix 47 content accuracy issues across all HTML pages."""
import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))

# Define replacements as (search_pattern, replacement) tuples
# Using case-insensitive search to be safe
REPLACEMENTS = [
    # "5 novel cycles" -> "3 novel cycles" (27 files)
    (r'(?i)5\s*novel\s*cycle', '3 novel cycle'),
    
    # "unlimited episodic memory" -> "up to 4,000 episodic memories" (4 files)
    (r'(?i)unlimited\s+episodic\s+memor(y|ies)', r'up to 4,000 episodic memories'),
    
    # "7 items (Miller's Law)" -> "4 items (Cowan's constant)" (2 files)
    (r'7\s*items\s*\(\s*Miller[\'']?\s*Law\s*\)', '4 items (Cowan\'s constant)'),
    
    # "OpenAI is a direct" / "OpenAI not a direct provider" -> correct wording (1 file)
    (r'(?i)OpenAI is a direct provider', 'OpenAI-compatible endpoints are the primary'),
    (r'(?i)OpenAI is not a direct provider', 'OpenAI-compatible endpoints are used instead of direct OpenAI'),
    (r'(?i)OpenAI not a direct provider', 'OpenAI-compatible endpoints are used instead of direct OpenAI'),
    
    # "per-task review" -> "full-project review only" (7 files)
    (r'(?i)per-task\s+review', 'a full-project review only'),
    (r'(?i)tasks have 3 states only \(todo/in_progress/done\) - no per-task review',
     'tasks have 3 states only (todo/in_progress/done) — a full-project review only'),
    
    # "short sleeps" -> "brief rest periods" (2 files)
    (r'(?i)\bshort\s+sleeps\b', 'brief rest periods'),
]

fixed_files = []
total_replacements = 0

for html_file in sorted(glob.glob(os.path.join(BASE, '*.html'))):
    fname = os.path.basename(html_file)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        original = f.read()
    
    content = original
    
    for pattern, replacement in REPLACEMENTS:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            print(f"  [{fname}] '{pattern}' -> '{replacement}' ({count}x)")
            content = new_content
            total_replacements += count
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_files.append(fname)

print(f"\n{'='*60}")
print(f"Fixed {len(fixed_files)} files with {total_replacements} total replacements")
for f in sorted(fixed_files):
    print(f"  ✓ {f}")
