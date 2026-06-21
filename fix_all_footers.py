#!/usr/bin/env python3
"""
Fix all footer issues across HTML files:
1. Remove duplicate first footers (keep only site-footer)
2. Fix CSS grid layouts so nav sections spread horizontally
3. Ensure consistent 4-column layout
"""

import os
import re
from pathlib import Path

BASE = Path(__file__).parent

def fix_file(filepath):
    """Process a single HTML file and return whether it was changed."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # ============================================================
        # FIX 1: Remove duplicate old-style <footer class="footer"> 
        # when there's also a <footer class="site-footer">
        # ============================================================
        if '<footer class="footer">' in content and '<footer class="site-footer">' in content:
            # Find the old footer block and remove it entirely
            pattern = re.compile(
                r'\s*<!--\s*Footer\s*-->\s*'
                r'<footer class="footer">.*?</footer>',
                re.DOTALL
            )
            match = pattern.search(content)
            if match:
                content = content[:match.start()] + content[match.end():]
        
        # ============================================================
        # FIX 2: Fix CSS - add display: contents to .site-footer .footer-links
        # so footer-section children become direct grid items under footer-content
        # ============================================================
        if '.site-footer' in content and 'repeat(3,' in content:
            # Check if we already have the fix
            if '.site-footer .footer-links' not in content or \
               ('.site-footer .footer-links' in content and 
                'display:' not in content.split('.site-footer .footer-links')[1].split('}')[0] if '.site-footer .footer-links' in content else True):
                
                # Find the site-footer .footer-content line and add after it
                footer_content_match = re.search(
                    r'(\.site-footer \s*\.footer-content\s*\{[^}]+\})', 
                    content
                )
                if footer_content_match:
                    insert_text = '\n.site-footer .footer-links { display: contents; }'
                    content = (content[:footer_content_match.end()] + 
                              insert_text + 
                              content[footer_content_match.end():])
        
        # ============================================================
        # FIX 3: Fix regular footer-content grid columns
        # Change "2fr 1fr 1fr" to "minmax(200px, 240px) 1fr" for brand + links wrapper
        # Only if it's NOT a site-footer (those use repeat(3,...))
        # ============================================================
        if '.site-footer' not in content or 'repeat(3,' not in content:
            old_grid = re.search(r'(grid-template-columns:\s*)2fr\s+1fr\s+1fr', content)
            if old_grid:
                content = content.replace('2fr 1fr 1fr', 'minmax(200px, 240px) 1fr')
        
        # ============================================================
        # FIX 4: Add padding to footer-content for proper margins
        # ============================================================
        if '.footer-content' in content and 'padding:' not in content.split('.footer-content')[1].split('}')[0] if '.footer-content' in content else True:
            old = r'(margin-bottom:\s*32px;\s*)\}'
            new = r'\1padding: 0 32px; }'
            # Only apply to non-site-footer footers
            if '.site-footer' not in content:
                content = re.sub(old, new, content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ERROR processing {filepath.name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    html_files = sorted([f for f in BASE.iterdir() if f.suffix == '.html' and f.name != 'index.html'])
    
    fixed_count = 0
    total = len(html_files)
    
    print(f"Found {total} HTML files to process\n")
    
    for i, filepath in enumerate(html_files, 1):
        changed = fix_file(filepath)
        status = "[FIX]" if changed else "[OK] "
        try:
            line = f"[{i}/{total}] {status} - {filepath.name}"
            print(line.encode('utf-8').decode())
        except:
            print(f"[{i}/{total}] {status} - {filepath.name}")
    
    print(f"\n{'='*60}")
    print(f"Fixed: {fixed_count}/{total} files")


if __name__ == '__main__':
    main()
