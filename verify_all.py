import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")
html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
print(f"Total files: {len(html_files)}")

missing_nav = []
missing_footer = []
dup_style = []
broken_links = {}

for f in html_files:
    c = open(f, encoding='utf-8').read()
    has_nav = 'navbar' in c or ('nav' in c and 'href=' in c)
    has_foot = 'footer' in c.lower()
    ds = c.count('<style>')
    
    if not has_nav and f not in ['index.html']:
        missing_nav.append(f)
    if not has_foot and f not in ['index.html']:
        missing_footer.append(f)
    if ds > 1:
        dup_style.append(f)
    
    # Check links
    links = re.findall(r'href="([^"]*\.html)"', c)
    for link in links:
        base = os.path.basename(link)
        if base not in html_files and not link.startswith('http'):
            if f not in broken_links:
                broken_links[f] = []
            broken_links[f].append(link)

print(f"Pages without navbar (excl index): {len(missing_nav)}")
print(f"Pages without footer (excl index): {len(missing_footer)}")
print(f"Duplicate style tags: {len(dup_style)}")
print(f"Broken links: {sum(len(v) for v in broken_links.values())} across {len(broken_links)} files")

# Check content size of each page
small_pages = []
for f in html_files:
    c = open(f, encoding='utf-8').read()
    # Strip HTML tags to get text
    text = re.sub(r'<[^>]+>', '', c)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) < 100:
        small_pages.append((f, len(text)))

print(f"\nPages with very little content (<100 chars): {len(small_pages)}")
for f, size in small_pages[:10]:
    print(f"  {f}: {size} chars")

# Verify all new pages exist
new_pages = ['creative-engine.html', 'decision-visualization.html', 'gallery.html',
             'memory-health.html', 'memory-visualization.html', 'queue-behavior.html',
             'recursive-thought.html']
print(f"\nNew pages status:")
for p in new_pages:
    exists = p in html_files
    print(f"  {p}: {'OK' if exists else 'MISSING'}")

# Verify all_pages.txt is complete
listed = set(open('all_pages.txt', encoding='utf-8').read().strip().split('\n'))
actual = set(html_files)
missing_from_list = actual - listed
print(f"\nall_pages.txt: {len(listed)} listed, {len(actual)} on disk")
if missing_from_list:
    print(f"Missing from list: {', '.join(sorted(missing_from_list))}")
