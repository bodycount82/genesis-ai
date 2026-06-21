#!/usr/bin/env python3
"""Comprehensive validation of all Genesis website pages."""
import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
print(f"Checking {len(html_files)} files...\n")

results = {
    'ok': [],
    'broken_links': [],
    'missing_images': [],
    'duplicate_styles': [],
    'structural_issues': [],
    'empty_content': [],
    'inconsistent_theme': [],
    'no_navbar': [],
    'no_footer': [],
}

# Check each file
for f in html_files:
    c = open(f, encoding='utf-8').read()
    issues = []
    
    # 1. Structural checks
    if '<html' not in c: issues.append('MISSING <html>')
    if '</html>' not in c: issues.append('MISSING </html>')
    if '<head>' not in c: issues.append('MISSING <head>')
    if '</head>' not in c: issues.append('MISSING </head>')
    if '<body' not in c: issues.append('MISSING <body>')
    if '</body>' not in c: issues.append('MISSING </body>')
    if '<title>' not in c or '</title>' not in c: issues.append('MISSING/EMPTY <title>')
    
    # 2. Style tag duplicates
    sc = c.count('<style>')
    if sc > 1: issues.append(f'{sc} <style> tags')
    
    # 3. CSS variable consistency check
    has_bg_var = '--bg:' in c or 'background:#0a0a0f' in c
    has_text_var = '--text:' in c or 'color:#e4e4ec' in c
    if not has_bg_var: issues.append('INCONSISTENT THEME (no dark bg)')
    if not has_text_var: issues.append('INCONSISTENT THEME (no light text)')
    
    # 4. Navbar check
    has_navbar = 'navbar' in c or 'nav' in c.lower()
    if not has_navbar and f != 'index.html': issues.append('NO NAVBAR')
    
    # 5. Footer check
    has_footer = 'footer' in c.lower()
    if not has_footer and f != 'index.html': issues.append('NO FOOTER')
    
    # 6. Content size
    body_start = c.find('<body')
    if body_start > 0:
        body_content = c[body_start:]
        text_only = re.sub(r'<[^>]+>', '', body_content)
        text_only = re.sub(r'\s+', ' ', text_only).strip()
        if len(text_only) < 200: issues.append(f'LOW CONTENT ({len(text_only)} chars)')
    
    # 7. Broken HTML links
    links = re.findall(r'href="([^"]*\.html)"', c)
    for link in links:
        base = os.path.basename(link)
        if base not in html_files and not link.startswith('http'):
            issues.append(f'BROKEN LINK: {link}')
    
    # 8. Broken image references
    images = re.findall(r'<img[^>]*src="([^"]*)"', c)
    for img in images:
        if not img.startswith('http') and not img.startswith('data:') and not img.startswith('/'):
            img_path = os.path.join(os.path.dirname(f), img)
            if not os.path.exists(img_path):
                issues.append(f'BROKEN IMAGE: {img}')
    
    # 9. Check for unclosed tags (basic check)
    open_tags = re.findall(r'<(\w+)[^>]*?(?<!/)>', c, re.IGNORECASE)
    close_tags = re.findall(r'</(\w+)>', c, re.IGNORECASE)
    void_elements = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr'}
    unclosed = []
    for tag in open_tags:
        if tag.lower() not in void_elements and tag.lower() not in [t.lower() for t in close_tags]:
            if tag.lower() not in {'div', 'span', 'p', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'a', 'section', 'nav', 'header', 'footer', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'form', 'label', 'select', 'option'}:
                unclosed.append(tag)
    
    if issues:
        results['broken_links'].append(f'{f}: {", ".join(issues)}')
    else:
        results['ok'].append(f)

# Print summary
print("=== STRUCTURAL ISSUES ===")
for issue in results['broken_links']:
    print(f"  {issue}")

print(f"\n=== SUMMARY ===")
print(f"Total files: {len(html_files)}")
print(f"Clean: {len(results['ok'])}")
print(f"Issues found: {len(results['broken_links'])}")

# Save detailed report
with open('validation_report.txt', 'w', encoding='utf-8') as out:
    out.write(f"Validation Report - {len(html_files)} files\n")
    out.write("=" * 50 + "\n\n")
    if results['ok']:
        out.write("CLEAN FILES:\n")
        for f in results['ok']:
            out.write(f"  OK: {f}\n")
    if results['broken_links']:
        out.write("\nFILES WITH ISSUES:\n")
        for issue in results['broken_links']:
            out.write(f"  {issue}\n")
    out.write(f"\nTotal clean: {len(results['ok'])}\n")
    out.write(f"Total with issues: {len(results['broken_links'])}\n")

print("\nDetailed report saved to validation_report.txt")
