#!/usr/bin/env python3
import re
from pathlib import Path

content = Path('index.html').read_text(encoding='utf-8')

# Find all href="#" matches
matches = list(re.finditer(r'href="#"', content))
print(f'Matches found: {len(matches)}')

for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 100)
    context = content[start:end]
    clean = ''.join(c if ord(c) < 128 else '?' for c in context)
    print(f'Context: ...{clean}...')
    print(f'Position: {m.start()}')

# Also check for any href with just #
all_hrefs = list(re.finditer(r'href\s*=\s*["\']([^"\']*)["\']', content))
print(f'\nAll href attributes: {len(all_hrefs)}')
for m in all_hrefs:
    val = m.group(1)
    if val == '#' or val.startswith('#') and len(val) <= 20:
        start = max(0, m.start() - 50)
        end = min(len(content), m.end() + 50)
        clean = ''.join(c if ord(c) < 128 else '?' for c in content[start:end])
        print(f'  Anchor: {val} -> ...{clean}...')

# Check for d3.js in the 3 files
for fname in ['genesis-brain.html', 'memory-graph.html', 'neural-interface.html']:
    fc = Path(fname).read_text(encoding='utf-8')
    has_d3 = 'd3js.org' in fc
    print(f'\n{fname}: d3.js present = {has_d3}')
    if has_d3:
        for i, line in enumerate(fc.split('\n')):
            if 'd3js' in line:
                clean = ''.join(c if ord(c) < 128 else '?' for c in line.strip()[:200])
                print(f'  Line {i+1}: {clean}')

# Check CSS vars on a sample file
sample = Path('absence.html').read_text(encoding='utf-8')
root_match = re.search(r':root\s*\{([^}]+)\}', sample)
if root_match:
    existing = set()
    for var_name in ['--red', '--yellow', '--radius', '--radius-lg']:
        if var_name in root_match.group(1):
            existing.add(var_name)
    missing = {'--red', '--yellow', '--radius', '--radius-lg'} - existing
    print(f'\nabsence.html CSS vars: existing={existing}, missing={missing}')

# Check heading skips on a sample file
headings = re.findall(r'<h([1-6])', sample)
print(f'absence.html headings: {headings}')

# Check for h1 in immersive pages
for fname in ['absence.html', 'attend.html', 'blindsight.html']:
    fc = Path(fname).read_text(encoding='utf-8')
    has_h1 = '<h1' in fc.lower() or '<H1' in fc
    print(f'{fname}: has h1 = {has_h1}')

# Check back links on immersive pages
for fname in ['absence.html', 'attend.html', 'blindsight.html']:
    fc = Path(fname).read_text(encoding='utf-8')
    has_back = 'index.html' in fc
    print(f'{fname}: has back link = {has_back}')

# Check CSS vars on context-window.html (was missing ALL 16 tokens)
ctx = Path('context-window.html').read_text(encoding='utf-8')
root_match = re.search(r':root\s*\{([^}]+)\}', ctx)
if root_match:
    existing = set()
    all_tokens = ['--bg', '--surface', '--surface-2', '--border', '--text', '--text-dim',
                  '--accent', '--accent-soft', '--green', '--orange', '--pink', '--purple',
                  '--cyan', '--red', '--yellow', '--radius', '--radius-lg']
    for var_name in all_tokens:
        if var_name in root_match.group(1):
            existing.add(var_name)
    missing = set(all_tokens) - existing
    print(f'\ncontext-window.html CSS vars: {len(existing)}/17 present, missing={missing}')

# Check CSS vars on emotional-states.html
em = Path('emotional-states.html').read_text(encoding='utf-8')
root_match = re.search(r':root\s*\{([^}]+)\}', em)
if root_match:
    existing = set()
    all_tokens = ['--bg', '--surface', '--surface-2', '--border', '--text', '--text-dim',
                  '--accent', '--accent-soft', '--green', '--orange', '--pink', '--purple',
                  '--cyan', '--red', '--yellow', '--radius', '--radius-lg']
    for var_name in all_tokens:
        if var_name in root_match.group(1):
            existing.add(var_name)
    missing = set(all_tokens) - existing
    print(f'emotional-states.html CSS vars: {len(existing)}/17 present, missing={missing}')

# Check CSS vars on tool-usage.html
tu = Path('tool-usage.html').read_text(encoding='utf-8')
root_match = re.search(r':root\s*\{([^}]+)\}', tu)
if root_match:
    existing = set()
    all_tokens = ['--bg', '--surface', '--surface-2', '--border', '--text', '--text-dim',
                  '--accent', '--accent-soft', '--green', '--orange', '--pink', '--purple',
                  '--cyan', '--red', '--yellow', '--radius', '--radius-lg']
    for var_name in all_tokens:
        if var_name in root_match.group(1):
            existing.add(var_name)
    missing = set(all_tokens) - existing
    print(f'tool-usage.html CSS vars: {len(existing)}/17 present, missing={missing}')

# Check CSS vars on memory-consolidation.html
mc = Path('memory-consolidation.html').read_text(encoding='utf-8')
root_match = re.search(r':root\s*\{([^}]+)\}', mc)
if root_match:
    existing = set()
    all_tokens = ['--bg', '--surface', '--surface-2', '--border', '--text', '--text-dim',
                  '--accent', '--accent-soft', '--green', '--orange', '--pink', '--purple',
                  '--cyan', '--red', '--yellow', '--radius', '--radius-lg']
    for var_name in all_tokens:
        if var_name in root_match.group(1):
            existing.add(var_name)
    missing = set(all_tokens) - existing
    print(f'memory-consolidation.html CSS vars: {len(existing)}/17 present, missing={missing}')

print('\nDone.')
