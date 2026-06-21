#!/usr/bin/env python3
"""Fix 47 content accuracy issues across all HTML pages."""
import os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Simple string replacements (no regex needed)
REPLACEMENTS = [
    ("5 novel cycle", "3 novel cycle"),
    ("unlimited episodic memory", "up to 4,000 episodic memories"),
    ("unlimited episodic memories", "up to 4,000 episodic memories"),
    ("OpenAI is a direct provider", "OpenAI-compatible endpoints are the primary"),
    ("OpenAI is not a direct provider", "OpenAI-compatible endpoints are used instead of direct OpenAI"),
    ("OpenAI not a direct provider", "OpenAI-compatible endpoints are used instead of direct OpenAI"),
    ("per-task review", "a full-project review only"),
    ("short sleeps", "brief rest periods"),
]

# Regex replacements (need to handle quotes carefully)
import re

REGEX_REPLACEMENTS = [
    # "7 items (Miller's Law)" or "7 items (Miller's Law)" -> "4 items (Cowan's constant)"
    (re.compile(r"7\s*items\s*\(\s*Mille[r\u2019]?\s*Law\s*\)"), "4 items (Cowan's constant)"),
]

fixed_files = []
total_replacements = 0

for html_file in sorted(glob.glob(os.path.join(BASE, "*.html"))):
    fname = os.path.basename(html_file)
    
    with open(html_file, "r", encoding="utf-8") as f:
        original = f.read()
    
    content = original
    
    # Simple replacements
    for old, new in REPLACEMENTS:
        count = content.count(old)
        if count > 0:
            print(f"  [{fname}] simple: '{old}' -> '{new}' ({count}x)")
            content = content.replace(old, new)
            total_replacements += count
    
    # Regex replacements
    for pattern, replacement in REGEX_REPLACEMENTS:
        new_content, count = pattern.subn(replacement, content)
        if count > 0:
            print(f"  [{fname}] regex: pattern -> '{replacement}' ({count}x)")
            content = new_content
            total_replacements += count
    
    if content != original:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        fixed_files.append(fname)

print(f"\n{'='*60}")
print(f"Fixed {len(fixed_files)} files with {total_replacements} total replacements")
for f in sorted(fixed_files):
    print(f"  OK {f}")
