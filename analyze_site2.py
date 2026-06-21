#!/usr/bin/env python3
"""Analyze the Genesis website for issues."""
import os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
html_files = [f for f in os.listdir('.') if f.endswith('.html')]
print(f'Total HTML files: {len(html_files)}')

all_links = set()
missing_pages = []
broken_structure = []
duplicate_styles = []
empty_pages = []
no_nav = []

for f in sorted(html_files):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Check basic structure
    issues = []
    if '<html' not in content:
        issues.append('missing <html>')
    if '</html>' not in content:
        issues.append('missing </html>')
    if '<head>' not in content:
        issues.append('missing <head>')
    if '<body>' not in content:
        issues.append('missing <body>')
    if '<title>' not in content:
        issues.append('missing <title>')
    
    # Check style tags
    style_count = content.count('<style>')
    if style_count > 1:
        duplicate_styles.append(f)
    if '</style>' not in content and style_count > 0:
        issues.append('unclosed </style>')
    
    if issues:
        broken_structure.append((f, issues))
    
    # Check for nav links
    if 'href=' not in content or content.count('href="') < 2:
        no_nav.append(f)
    
    # Find all HTML page links - better regex
    links = re.findall(r'href="([^"]*\.html)"', content)
    for l in links:
        base = os.path.basename(l)
        all_links.add(base)
        if base not in html_files:
            missing_pages.append((f, base))
    
    # Check page size
    if len(content.strip()) < 500:
        empty_pages.append((f, len(content)))

print(f'\nUnique HTML links across all pages: {len(all_links)}')
missing_set = set(missing_pages)
print(f'Missing referenced pages: {len(missing_set)}')
for referrer, missing in sorted(missing_set):
    print(f'  {referrer} -> {missing}')

print(f'\nBroken structure ({len(broken_structure)}):')
for f, issues in broken_structure[:15]:
    print(f'  {f}: {issues}')

print(f'\nDuplicate style tags: {len(duplicate_styles)}')
for f in duplicate_styles[:10]:
    print(f'  {f}')

print(f'\nEmpty pages (<500 chars): {len(empty_pages)}')
for f, size in empty_pages:
    print(f'  {f} ({size} chars)')

print(f'\nPages with no nav links: {len(no_nav)}')
for f in no_nav[:10]:
    print(f'  {f}')

# Check for queue-behavior.html reference in index
with open('index.html', 'r', encoding='utf-8') as fh:
    idx = fh.read()
if 'queue-behavior.html' in idx:
    print('\n*** queue-behavior.html is referenced in index.html but DOES NOT EXIST ***')

# Check all_pages.txt
with open('all_pages.txt', 'r', encoding='utf-8') as fh:
    listed = set(l.strip() for l in fh if l.strip())

actual = set(html_files)
extra_in_list = listed - actual
missing_from_list = actual - listed

print(f'\nall_pages.txt inconsistencies:')
print(f'  Listed but missing from disk: {len(extra_in_list)}')
for f in sorted(extra_in_list)[:10]:
    print(f'    {f}')
print(f'  On disk but not in list: {len(missing_from_list)}')
for f in sorted(missing_from_list)[:10]:
    print(f'    {f}')

# Check for JavaScript errors
bad_scripts = []
for f in sorted(html_files):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, s in enumerate(scripts):
        if 'document.addEventListener' in s and 'DOMContentLoaded' not in s:
            bad_scripts.append((f, i))

if bad_scripts:
    print(f'\nScripts without DOMContentLoaded: {len(bad_scripts)}')
    for f, i in bad_scripts[:10]:
        print(f'  {f}, script #{i}')

# Check for broken image references
broken_images = []
for f in sorted(html_files):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    images = re.findall(r'<img[^>]*src="([^"]*)"', content)
    for img in images:
        if not img.startswith('http') and not img.startswith('data:') and not img.startswith('/'):
            img_path = os.path.join(os.path.dirname(f), img)
            if not os.path.exists(img_path):
                broken_images.append((f, img))

if broken_images:
    print(f'\nBroken image references ({len(broken_images)}):')
    for f, img in broken_images[:10]:
        print(f'  {f}: {img}')
