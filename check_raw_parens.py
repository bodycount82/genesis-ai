import re

files = [
    'attention-garden.html',
    'attention-mechanism.html',
    'cognitive-load.html',
    'creativity-engine.html',
    'hallucination-explorer.html',
    'inner-world.html',
    'intuition-engine.html',
    'resilience-engine.html',
    'theory-of-mind.html'
]

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(scripts):
        opens = script.count('(')
        closes = script.count(')')
        diff = closes - opens
        
        if diff != 0:
            print(f"UNBALANCED: {fname} (block {i}): {opens} ( vs {closes}) diff={diff}")
            # Show last 5 lines
            lines = script.split('\n')
            for line in lines[-6:]:
                print(f"  |{line.strip()}|")
        else:
            print(f"OK: {fname} (block {i}): {opens} vs {closes}")
