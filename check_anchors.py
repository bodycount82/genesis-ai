import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all anchor targets (id or name attributes)
ids = re.findall(r'id=["\']([^"\']+)["\']', content)
names = re.findall(r'name=["\']([^"\']+)["\']', content)

print('Anchor IDs found:')
for id in sorted(set(ids)):
    print(f'  #{id}')

print()
print('Anchor names found:')
for name in sorted(set(names)):
    print(f'  #{name}')

# Find all href="#..." links
hrefs = re.findall(r'href=["\']#([^"\']+)["\']', content)
print()
print('href="#..." links:')
for h in hrefs:
    print(f'  #{h}')

# Check which anchors are missing
print()
print('Missing anchors:')
all_targets = set(ids + names)
for h in hrefs:
    if h not in all_targets:
        print(f'  #{h} - NOT FOUND')
    else:
        print(f'  #{h} - OK')
