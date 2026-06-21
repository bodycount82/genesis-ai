#!/usr/bin/env python3
"""Fix content accuracy issues across all HTML pages."""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Define fixes: (pattern_to_find, replacement_text)
# Each fix is a list of tuples for targeted replacements per page type
FIXES = [
    # "5 novel cycles" -> "3 novel cycles" (most common issue)
    ("5 novel cycles", "3 novel cycles"),
    # "unlimited episodic memory" -> "up to 4,000 episodic memories"
    ("unlimited episodic memory", "up to 4,000 episodic memories"),
    # "7 items (Miller's Law)" -> "4 items (Cowan's constant)"
    ('7 items (Miller\'s Law)', '4 items (Cowan\'s constant)'),
    ("7 items (Miller's Law)", "4 items (Cowan's constant)"),
    # Tasks with review states
    ("per-task review", "a full-project review only"),
    ("per-task review —", "a full-project review only —"),
    # OpenAI direct provider
    ("OpenAI is a direct", "OpenAI-compatible endpoints are the primary"),
    ("OpenAI is not a direct", "OpenAI-compatible endpoints are used instead of direct"),
    # Short sleeps
    ("short sleeps", "brief rest periods"),
    # "15 minutes" context for sleep
]

# Pages that need specific additional fixes
SPECIFIC_FIXES = {
    'ai-art.html': [
        ('unlimited episodic memory', 'up to 4,000 episodic memories'),
    ],
    'biological-memory.html': [
        ('unlimited episodic memory', 'up to 4,000 episodic memories'),
        ("7 items (Miller's Law)", "4 items (Cowan's constant)"),
    ],
    'brain-network.html': [
        ('unlimited episodic memory', 'up to 4,000 episodic memories'),
        ("7 items (Miller's Law)", "4 items (Cowan's constant)"),
    ],
    'memory-consolidation.html': [
        ('unlimited episodic memory', 'up to 4,000 episodic memories'),
    ],
    'decision-engine.html': [
        ("short sleeps", "brief rest periods"),
    ],
    'meet-genesis.html': [
        ("short sleeps", "brief rest periods"),
    ],
}

fixed_files = []
total_fixes = 0

for html_file in sorted(glob.glob(os.path.join(BASE, '*.html'))):
    fname = os.path.basename(html_file)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        original = f.read()
    
    content = original
    
    # Apply specific fixes first if they exist for this file
    if fname in SPECIFIC_FIXES:
        for old, new in SPECIFIC_FIXES[fname]:
            content = content.replace(old, new)
    
    # Apply general fixes
    for old, new in FIXES:
        content = content.replace(old, new)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_files.append(fname)
        # Count how many replacements were made
        for old, new in FIXES:
            total_fixes += original.count(old)
        if fname in SPECIFIC_FIXES:
            for old, _ in SPECIFIC_FIXES[fname]:
                total_fixes += original.count(old)

print(f"Fixed {len(fixed_files)} files with {total_fixes} total replacements")
for f in fixed_files:
    print(f"  ✓ {f}")
