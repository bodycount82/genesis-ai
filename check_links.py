import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")
html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
broken = {}

for f in html_files:
    c = open(f, encoding='utf-8').read()
    links = re.findall(r'href="([^"]*\.html)"', c)
    for link in links:
        base = os.path.basename(link)
        if base not in html_files and not link.startswith('http'):
            if f not in broken:
                broken[f] = []
            broken[f].append(link)

print("BROKEN LINKS:")
for f in sorted(broken):
    for l in sorted(set(broken[f])):
        print(f"  {f} -> {l}")
print(f"\nTotal files with broken links: {len(broken)}")
