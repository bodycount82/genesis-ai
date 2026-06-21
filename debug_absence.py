import re

with open('absence.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find script tag - try different patterns
patterns = [
    r'<script>(.*?)</script>',
    r'<script[^>]*>(.*?)</script>',
    r'(<script[^>]*>)(.*?)(</script>)',
]

for i, pat in enumerate(patterns):
    matches = list(re.finditer(pat, content, re.DOTALL))
    print(f"Pattern {i}: {len(matches)} matches")
    if matches:
        for m in matches:
            if len(m.groups()) == 3:
                script = m.group(2)
            else:
                script = m.group(1)
            opens = script.count('(')
            closes = script.count(')')
            print(f"  ({opens} vs {closes})")
            # Show last 5 lines
            lines = script.split('\n')
            for line in lines[-6:]:
                print(f"    |{line.strip()}|")

# Also check what's right before </script>
idx = content.rfind('</script>')
print(f"\nContext before </script>:")
print(f"  |{content[idx-100:idx+10]}|")
