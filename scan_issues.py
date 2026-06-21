import glob, os

files = sorted(glob.glob('*.html'))
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read().lower()
    
    found = []
    if 'novel cycle' in content:
        for line in content.split('\n'):
            if 'novel cycle' in line:
                found.append(('novel_cycle', line.strip()[:100]))
    if 'unlimited episodic memory' in content:
        for line in content.split('\n'):
            if 'unlimited episodic memory' in line:
                found.append(('unlimited_mem', line.strip()[:100]))
    if 'miller' in content:
        for line in content.split('\n'):
            if 'miller' in line:
                found.append(('miller', line.strip()[:100]))
    if 'per-task review' in content:
        for line in content.split('\n'):
            if 'per-task review' in line:
                found.append(('per_task_review', line.strip()[:100]))
    if 'short sleep' in content:
        for line in content.split('\n'):
            if 'short sleep' in line:
                found.append(('short_sleep', line.strip()[:100]))
    
    if found:
        print(f"=== {os.path.basename(f)} ===")
        for kind, text in found:
            print(f"  [{kind}] {text}")
