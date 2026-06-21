import os, re

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
print(f'Total HTML files: {len(html_files)}')
print()

issues_found = {}

def add_issue(fname, check, detail):
    key = (fname, check)
    issues_found[key] = detail

# 1. Extra </style> tags
print('=== CHECK: Extra </style> tags ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    style_opens = len(re.findall(r'<style\b[^>]*>', content))
    style_closes = len(re.findall(r'</style>', content))
    if style_opens != style_closes:
        add_issue(fname, 'extra_style_tags', f'opens={style_opens}, closes={style_closes}')
        print(f'  {fname}: opens={style_opens}, closes={style_closes}')

# 2. Missing DOCTYPE
print('=== CHECK: Missing DOCTYPE ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    if not content.startswith('<!DOCTYPE'):
        add_issue(fname, 'missing_doctype', 'No DOCTYPE')
        print(f'  {fname}: missing DOCTYPE')

# 3. Missing viewport meta
print('=== CHECK: Missing viewport meta ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'viewport' not in content:
        add_issue(fname, 'missing_viewport', 'No viewport meta')
        print(f'  {fname}: missing viewport')

# 4. Missing </html>
print('=== CHECK: Missing </html> ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if '</html>' not in content:
        add_issue(fname, 'missing_html_close', 'No </html>')
        print(f'  {fname}: missing </html>')

# 5. Missing <title>
print('=== CHECK: Missing/empty title ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'<title>(.*?)</title>', content)
    if not m or not m.group(1).strip():
        add_issue(fname, 'missing_title', 'Empty or missing title')
        print(f'  {fname}: missing/empty title')

# 6. Multiple :root blocks
print('=== CHECK: Multiple :root blocks ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    root_blocks = re.findall(r':root\s*\{', content)
    if len(root_blocks) > 1:
        add_issue(fname, 'multiple_root_blocks', f'{len(root_blocks)} :root blocks')
        print(f'  {fname}: {len(root_blocks)} :root blocks')

# 7. Missing box-sizing reset
print('=== CHECK: Missing box-sizing reset ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'box-sizing' not in content:
        add_issue(fname, 'missing_box_sizing', 'No box-sizing reset')
        print(f'  {fname}: missing box-sizing')

# 8. Missing or multiple h1
print('=== CHECK: Missing or multiple h1 ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    h1s = re.findall(r'<h1[^>]*>', content)
    if len(h1s) == 0:
        add_issue(fname, 'missing_h1', 'No h1 tag')
        print(f'  {fname}: missing h1')
    elif len(h1s) > 1:
        add_issue(fname, 'multiple_h1', f'{len(h1s)} h1 tags')
        print(f'  {fname}: {len(h1s)} h1 tags')

# 9. Heading level skips
print('=== CHECK: Heading level skips ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    headings = re.findall(r'<h([1-6])[^>]*>', content)
    if headings:
        for i in range(1, len(headings)):
            prev = int(headings[i-1])
            curr = int(headings[i])
            if curr > prev + 1:
                add_issue(fname, 'heading_skip', f'h{prev} -> h{curr}')
                print(f'  {fname}: h{prev} -> h{curr} (skip at position {i})')

# 10. Missing nav on content pages
print('=== CHECK: Missing nav/back-link on content pages ===')
immersive = ['absence.html','attend.html','blindsight.html','certainty.html','context-window.html',
             'curiosity-field.html','doubt.html','duration.html','emotional-states.html',
             'entanglement.html','fragment.html','fugitive.html','memory-consolidation.html',
             'memory-erosion.html','on-return.html','persistence.html','the-listener.html','the-wait.html']
for fname in html_files:
    if fname == 'index.html' or fname in immersive:
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<nav' not in content and 'back-link' not in content and 'Back to' not in content and 'index.html' not in content:
        add_issue(fname, 'missing_nav_backlink', 'No nav or back-link found')
        print(f'  {fname}: missing nav/back-link')

# 11. File sizes > 50KB
print('=== CHECK: File sizes > 50KB ===')
for fname in html_files:
    size = os.path.getsize(fname)
    if size > 50000:
        add_issue(fname, 'large_file', f'{size} bytes ({size/1024:.1f} KB)')
        print(f'  {fname}: {size} bytes ({size/1024:.1f} KB)')

# 12. CSS > 300 lines
print('=== CHECK: CSS > 300 lines ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if style_match:
        css_lines = style_match.group(1).split('\n')
        if len(css_lines) > 300:
            add_issue(fname, 'css_too_long', f'{len(css_lines)} CSS lines')
            print(f'  {fname}: {len(css_lines)} CSS lines')

# 13. Missing </body> or </html>
print('=== CHECK: Missing </body> or </html> ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if '</body>' not in content:
        add_issue(fname, 'missing_body_close', 'No </body>')
        print(f'  {fname}: missing </body>')
    if '</html>' not in content:
        add_issue(fname, 'missing_html_close2', 'No </html>')
        print(f'  {fname}: missing </html>')

# 14. href="#" placeholder links
print('=== CHECK: href="#" placeholder links ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    href_hashes = re.findall(r'href=["\']([^"\']*#[^"\']*)["\']', content)
    if href_hashes:
        add_issue(fname, 'hash_links', f'{len(href_hashes)} href="#" links')
        print(f'  {fname}: {len(href_hashes)} href="#" links')

# 15. External JS dependencies (d3)
print('=== CHECK: External d3.js dependencies ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    ext_scripts = re.findall(r'<script[^>]*src=["\']([^"\']*d3[^"\']*)["\']', content)
    if ext_scripts:
        add_issue(fname, 'external_d3', 'External d3.js dependency')
        print(f'  {fname}: external d3.js dependency')

# 16. Missing </script>
print('=== CHECK: Missing </script> ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    script_opens = len(re.findall(r'<script\b[^>]*>', content))
    script_closes = len(re.findall(r'</script>', content))
    if script_opens != script_closes:
        add_issue(fname, 'missing_script_close', f'opens={script_opens}, closes={script_closes}')
        print(f'  {fname}: opens={script_opens}, closes={script_closes}')

# 17. Unclosed parentheses in JS
print('=== CHECK: Unclosed parentheses in JS ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        opens = script.count('(')
        closes = script.count(')')
        if opens != closes:
            add_issue(fname, 'unclosed_parens', f'block {i}: {opens} ( vs {closes} )')
            print(f'  {fname}: script block {i} has {opens} ( vs {closes} )')

# 18. Missing CSS variables in :root
print('=== CHECK: Missing CSS variables in :root ===')
required_vars = ['--bg', '--surface', '--border', '--text', '--text-dim', '--accent']
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    root_match = re.search(r':root\s*\{(.*?)\}', content, re.DOTALL)
    if root_match:
        root_content = root_match.group(1)
        for var in required_vars:
            if var not in root_content:
                add_issue(fname, 'missing_css_var', f'missing {var}')
                print(f'  {fname}: missing {var}')
                break

# 19. Missing line-height on body
print('=== CHECK: Missing line-height ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'line-height' not in content:
        add_issue(fname, 'missing_line_height', 'No line-height')
        print(f'  {fname}: missing line-height')

# 20. Missing font-family on body
print('=== CHECK: Missing font-family ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'font-family' not in content:
        add_issue(fname, 'missing_font_family', 'No font-family')
        print(f'  {fname}: missing font-family')

# 21. Missing footer on non-immersive pages
print('=== CHECK: Missing footer ===')
for fname in html_files:
    if fname in immersive or fname == 'index.html':
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<footer' not in content and '</footer>' not in content:
        add_issue(fname, 'missing_footer', 'No footer')
        print(f'  {fname}: missing footer')

# 22. Missing back-link on immersive pages
print('=== CHECK: Missing back-link on immersive pages ===')
for fname in html_files:
    if fname not in immersive:
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'back-link' not in content and 'Back to' not in content and 'index.html' not in content:
        add_issue(fname, 'immersive_no_backlink', 'No back-link to home')
        print(f'  {fname}: missing back-link to home')

# 23. Missing </style>
print('=== CHECK: Missing </style> ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<style' in content and '</style>' not in content:
        add_issue(fname, 'missing_style_close', 'No </style>')
        print(f'  {fname}: missing </style>')

# 24. Missing <meta charset>
print('=== CHECK: Missing meta charset ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'charset' not in content:
        add_issue(fname, 'missing_charset', 'No charset meta')
        print(f'  {fname}: missing charset')

# 25. Missing lang attribute on html
print('=== CHECK: Missing lang="en" ===')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'lang="en"' not in content and 'lang=en' not in content:
        add_issue(fname, 'missing_lang', 'No lang="en" on html')
        print(f'  {fname}: missing lang="en"')

print()
print('=' * 60)
print('SCAN COMPLETE')
print(f'Total unique issues: {len(issues_found)}')

# Summary by issue type
from collections import Counter
issue_types = Counter()
for (fname, check), detail in issues_found.items():
    issue_types[check] += 1

print()
print('ISSUES BY TYPE:')
for check, count in issue_types.most_common():
    print(f'  {check}: {count} files')

# Summary by file
file_counts = Counter()
for (fname, check), detail in issues_found.items():
    file_counts[fname] += 1

print()
print('FILES WITH ISSUES:')
for fname, count in file_counts.most_common(30):
    print(f'  {fname}: {count} issues')
