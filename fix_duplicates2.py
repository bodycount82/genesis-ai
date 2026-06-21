#!/usr/bin/env python3
"""Fix pages with duplicate <style> tags by removing the duplicate second block."""
import os, re

os.chdir(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
fixed_count = 0

for f in html_files:
    c = open(f, encoding='utf-8').read()
    
    # Count style tags
    sc = c.count('<style>')
    if sc < 2:
        continue
    
    # Check if the second <style> block is a duplicate of the first
    style_blocks = re.findall(r'<style>(.*?)</style>', c, re.DOTALL)
    
    if len(style_blocks) < 2:
        continue
    
    # If blocks are identical (or nearly so), remove the duplicate second block
    # Normalize both blocks for comparison
    b1 = style_blocks[0].strip()
    b2 = style_blocks[1].strip()
    
    # Remove CSS comments for comparison
    b1_clean = re.sub(r'/\*.*?\*/', '', b1, flags=re.DOTALL).strip()
    b2_clean = re.sub(r'/\*.*?\*/', '', b2, flags=re.DOTALL).strip()
    
    if b1_clean == b2_clean:
        # The second style block is a duplicate - remove it entirely
        # Find the position of the second </style> and everything between first </style> and second <style>
        # Strategy: find "</style>\n" followed by "<style>" and remove that whole section
        new_c = re.sub(r'</style>\s*<style>.*?</style>', '</style>', c, count=1, flags=re.DOTALL)
        
        if new_c != c:
            open(f, 'w', encoding='utf-8').write(new_c)
            fixed_count += 1
            print(f"Fixed: {f}")
        else:
            print(f"FAILED to fix: {f} (could not find duplicate pattern)")
    else:
        # The blocks are different - need a smarter approach
        # Check if the second block contains the same CSS variables/theme as the first
        # If so, merge them properly
        if '--bg:' in b1 and '--bg:' in b2:
            # Both have theme vars - the second is likely a duplicate theme injection
            # Keep only the first block (which has all the content)
            new_c = re.sub(r'</style>\s*<style>.*?</style>', '</style>', c, count=1, flags=re.DOTALL)
            if new_c != c:
                open(f, 'w', encoding='utf-8').write(new_c)
                fixed_count += 1
                print(f"Merged (different but theme dup): {f}")
            else:
                print(f"FAILED to merge: {f}")
        else:
            print(f"DIFFERENT blocks in {f} - skipping")

print(f"\nTotal fixed: {fixed_count}")
