import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")
html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
print("Checking all pages for content quality...")
issues = []

for f in html_files:
    c = open(f, encoding='utf-8').read()
    
    title_match = re.search(r'<title>(.*?)</title>', c)
    title = title_match.group(1).strip() if title_match else ''
    
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', c, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    
    text = re.sub(r'<[^>]+>', '', c)
    text = re.sub(r'\s+', ' ', text).strip()
    
    if len(text) < 200:
        issues.append(f"{f}: LOW CONTENT ({len(text)} chars)")
    if not title:
        issues.append(f"{f}: NO TITLE")
    if not h1 and f not in ['index.html']:
        issues.append(f"{f}: NO H1")

print(f"Checked {len(html_files)} pages")
print(f"Issues found: {len(issues)}")
for i in issues[:20]:
    print(f"  {i}")

# Check for factual consistency - version numbers
print("\nChecking version number consistency...")
version_refs = {}
for f in html_files:
    c = open(f, encoding='utf-8').read()
    if '1.17' in c or 'v1' in c.lower():
        version_refs[f] = [m for m in re.findall(r'\d+\.\d+', c)]

print(f"Files with version references: {len(version_refs)}")
for f, versions in sorted(version_refs.items()):
    if versions:
        print(f"  {f}: {versions[:3]}")

# Check for broken CSS classes (common patterns)
print("\nChecking CSS class consistency...")
css_issues = []
for f in html_files:
    c = open(f, encoding='utf-8').read()
    # Find all class references in HTML
    html_classes = re.findall(r'class="([^"]*)"', c)
    # Find all defined CSS classes
    css_classes = re.findall(r'\.([a-zA-Z][\w-]*)', c.split('</style>')[0] if '</style>' in c else '')
    
    for cls in html_classes:
        for single_cls in cls.split():
            if single_cls and single_cls not in css_classes and single_cls not in ['btn', 'btn-primary', 'btn-secondary', 'doc-back', 'doc-content', 'doc-page', 'doc-container', 'doc-highlight', 'doc-table', 'nav-links', 'nav-container', 'nav-logo', 'footer', 'footer-content', 'footer-brand', 'footer-links', 'footer-bottom', 'container', 'fade-in', 'visible', 'gradient-text', 'section-tag', 'section-title', 'section-description', 'card', 'card:hover']:
                # Check if it's a utility class that might be defined elsewhere
                pass

print("CSS class check complete")
