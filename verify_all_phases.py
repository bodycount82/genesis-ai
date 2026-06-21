#!/usr/bin/env python3
"""
Genesis Website — Full Verification Script
Runs all automated checks across all 115 HTML files.
Outputs: VERIFICATION_REPORT.md and ISSUES_LOG.md
"""

import os
import re
from collections import defaultdict
from datetime import datetime

BASE_DIR = r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing"

# Design tokens to verify
DESIGN_TOKENS = {
    "--bg": "#0a0a0f",
    "--surface": "#12121a",
    "--surface-2": "#1a1a26",
    "--border": "#2a2a3a",
    "--text": "#e4e4ec",
    "--text-dim": "#8888a0",
    "--accent": "#7b6ff0",
    "--accent-soft": "#9d93f5",
    "--green": "#4ade80",
    "--orange": "#fb923c",
    "--pink": "#f472b6",
    "--purple": "#a855f7",
    "--cyan": "#22d3ee",
    "--red": "#f87171",
    "--yellow": "#fbbf24",
    "--radius": "12px",
    "--radius-lg": "20px",
}

# Immersive pages (Pattern B — intentionally no nav/footer)
IMMERSIVE_PAGES = {
    "absence.html", "attend.html", "blindsight.html", "certainty.html",
    "context-window.html", "curiosity-field.html", "doubt.html", "duration.html",
    "emotional-states.html", "entanglement.html", "fragment.html", "fugitive.html",
    "memory-consolidation.html", "memory-erosion.html", "on-return.html",
    "persistence.html", "the-listener.html", "the-wait.html",
}

# Special pages (Pattern C)
SPECIAL_PAGES = {
    "index.html", "gallery.html", "gallery-full.html",
    "agent-dashboard.html", "mission-control.html",
}

class Issue:
    def __init__(self, severity, page, check, detail):
        self.severity = severity  # Critical, Major, Minor, Info
        self.page = page
        self.check = check
        self.detail = detail

    def __repr__(self):
        return f"[{self.severity}] {self.page}: {self.check} — {self.detail}"


def get_html_files():
    """Get all .html files in the directory."""
    files = []
    for f in sorted(os.listdir(BASE_DIR)):
        if f.endswith(".html"):
            files.append(f)
    return files


def read_file(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_file_size_kb(filename):
    path = os.path.join(BASE_DIR, filename)
    return os.path.getsize(path) / 1024


# ============================================================
# PHASE 1: Structural & Syntax Checks
# ============================================================

def phase1_checks(filename, html):
    issues = []

    # 1.1 DOCTYPE + HTML root
    if not html.strip().startswith("<!DOCTYPE html>"):
        issues.append(Issue("Critical", filename, "1.1", "Missing or incorrect DOCTYPE"))
    if "<html" not in html.lower():
        issues.append(Issue("Critical", filename, "1.1", "Missing <html> root element"))
    elif 'lang="en"' not in html.lower():
        issues.append(Issue("Minor", filename, "1.1", '<html> missing lang="en"'))

    # 1.2 Meta charset + viewport
    if '<meta charset="UTF-8">' not in html and '<meta charset=\'UTF-8\'>' not in html:
        issues.append(Issue("Critical", filename, "1.2", 'Missing <meta charset="UTF-8">'))
    if 'name="viewport"' not in html.lower():
        issues.append(Issue("Major", filename, "1.2", 'Missing viewport meta tag'))

    # 1.3 Title tag
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    if not title_match:
        issues.append(Issue("Critical", filename, "1.3", "Missing <title> tag"))
    elif not title_match.group(1).strip():
        issues.append(Issue("Major", filename, "1.3", "<title> is empty"))

    # 1.4 Single <style> block
    style_opens = len(re.findall(r'<style(?![^>]*\bclass\b)[^>]*>', html, re.IGNORECASE))
    style_closes = len(re.findall(r'</style>', html, re.IGNORECASE))
    if style_opens == 0:
        issues.append(Issue("Major", filename, "1.4", "No <style> block found"))
    elif style_opens > 1:
        issues.append(Issue("Critical", filename, "1.4", f"Found {style_opens} <style> blocks (expected 1)"))

    # 1.5 Closing tags
    if '</html>' not in html.lower():
        issues.append(Issue("Critical", filename, "1.5", "Missing </html> closing tag"))
    if '</body>' not in html.lower():
        issues.append(Issue("Critical", filename, "1.5", "Missing </body> closing tag"))
    if '</head>' not in html.lower():
        issues.append(Issue("Major", filename, "1.5", "Missing </head> closing tag"))

    # 1.6 Duplicate <style> (re-check)
    if style_opens > 1:
        issues.append(Issue("Critical", filename, "1.6", f"Duplicate <style> blocks: {style_opens} found"))

    # 1.7 Orphaned </style>
    if style_closes > style_opens:
        issues.append(Issue("Major", filename, "1.7", f"Extra </style> tags: {style_closes} closes vs {style_opens} opens"))

    # 1.8 Check basic nesting — count open/close divs/sections
    div_opens = len(re.findall(r'<div(?![^>]*</div>)', html))
    div_closes = html.count('</div>')
    # This is a rough check; proper nesting needs an HTML parser

    # 1.9 Image paths
    img_tags = re.findall(r'<img[^>]+>', html, re.IGNORECASE)
    for tag in img_tags:
        src_match = re.search(r'src=["\'](.*?)["\']', tag)
        if src_match:
            src = src_match.group(1)
            # Skip external URLs
            if src.startswith('http') or src.startswith('//'):
                continue
            # Check relative path exists
            if not src.startswith('/'):
                img_path = os.path.join(BASE_DIR, src)
                if not os.path.exists(img_path):
                    issues.append(Issue("Minor", filename, "1.9", f"Image not found: {src}"))

    # 1.10 Script tags
    script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
    for i, block in enumerate(script_blocks):
        # Check for obvious syntax issues
        if block.count('{') != block.count('}'):
            issues.append(Issue("Major", filename, "1.10", f"Unclosed braces in script block {i+1}"))
        if block.count('(') != block.count(')'):
            issues.append(Issue("Major", filename, "1.10", f"Unclosed parentheses in script block {i+1}"))

    return issues


# ============================================================
# PHASE 2: CSS Consistency Audit
# ============================================================

def phase2_checks(filename, html):
    issues = []

    # Extract the <style> block
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    if not style_match:
        issues.append(Issue("Major", filename, "2.1", "No CSS found — page has no styling"))
        return issues

    css = style_match.group(1)

    # 2.1 Design tokens
    root_match = re.search(r':root\s*\{([^}]*)\}', css, re.DOTALL)
    if not root_match:
        issues.append(Issue("Major", filename, "2.1", ":root CSS variables block missing"))
    else:
        root_css = root_match.group(1)
        for token, expected in DESIGN_TOKENS.items():
            # Check if token is defined
            pattern = rf'{re.escape(token)}\s*:\s*([^;]+);'
            match = re.search(pattern, root_css)
            if not match:
                issues.append(Issue("Minor", filename, "2.1", f"Missing CSS variable: {token}"))

    # 2.2 Base reset
    if 'box-sizing: border-box' not in css:
        issues.append(Issue("Major", filename, "2.2", "Missing box-sizing: border-box reset"))
    if 'margin: 0' not in css and 'margin:0' not in css:
        issues.append(Issue("Minor", filename, "2.2", "Missing margin reset"))

    # Body styles
    body_match = re.search(r'body\s*\{([^}]*)\}', css, re.DOTALL)
    if body_match:
        body_css = body_match.group(1)
        if 'font-family' not in body_css:
            issues.append(Issue("Major", filename, "2.2", "body missing font-family"))
        if 'background' not in body_css and 'background-color' not in body_css:
            issues.append(Issue("Minor", filename, "2.2", "body missing background color"))
        if 'line-height' not in body_css:
            issues.append(Issue("Minor", filename, "2.2", "body missing line-height"))
    else:
        issues.append(Issue("Major", filename, "2.2", "No body{} rule found in CSS"))

    # 2.3 Component styles
    component_checks = {
        '.card': 'background',
        '.btn-primary': 'background',
        '.section-title': 'font-weight',
        '.section-desc': 'color',
        '.gradient-text': 'background-clip',
    }

    for comp, prop in component_checks.items():
        if comp not in css:
            # Only flag if the page should have this component (check HTML)
            if f'class="{comp.strip(".")}"' in html or f"class='{comp.strip('.')}'" in html:
                issues.append(Issue("Minor", filename, "2.3", f"Component {comp} used in HTML but not defined in CSS"))

    # 2.4 Layout structure
    if '.container' not in css:
        issues.append(Issue("Major", filename, "2.4", ".container class missing from CSS"))
    else:
        container_match = re.search(r'\.container\s*\{([^}]*)\}', css, re.DOTALL)
        if container_match:
            cont_css = container_match.group(1)
            if 'max-width' not in cont_css:
                issues.append(Issue("Minor", filename, "2.4", ".container missing max-width"))

    return issues


# ============================================================
# PHASE 3: Page Architecture Verification
# ============================================================

def phase3_checks(filename, html):
    issues = []

    has_nav = '<nav' in html.lower() or '<header' in html.lower()
    has_footer = '<footer' in html.lower()

    if filename in IMMERSIVE_PAGES:
        # Pattern B — no nav/footer expected
        if has_nav and has_footer:
            issues.append(Issue("Info", filename, "3.1", "Has nav+footer but is an immersive page (may be intentional)"))
        # Should link back to index.html
        if 'index.html' not in html:
            issues.append(Issue("Minor", filename, "3.2", "Immersive page doesn't link back to index.html"))
    elif filename in SPECIAL_PAGES:
        # Pattern C — special pages
        pass  # Handled individually
    else:
        # Pattern A — should have nav + footer
        if not has_nav:
            issues.append(Issue("Major", filename, "3.1", "Pattern A page missing <nav> or <header>"))
        if not has_footer:
            issues.append(Issue("Minor", filename, "3.1", "Pattern A page missing <footer>"))

    # Check for nav links pointing to valid pages
    href_matches = re.findall(r'href=["\']([^"\']+\.html)["\']', html)
    for href in href_matches:
        if href.startswith('#') or href.startswith('http'):
            continue
        target = os.path.basename(href)
        if target and not os.path.exists(os.path.join(BASE_DIR, target)):
            issues.append(Issue("Major", filename, "3.3", f"Broken link to {href}"))

    return issues


# ============================================================
# PHASE 5: Cross-Reference & Link Integrity
# ============================================================

def phase5_checks(filename, html, all_files):
    issues = []

    # Find all internal .html links
    href_matches = re.findall(r'href=["\']([^"\']+\.html)["\']', html)
    for href in href_matches:
        if href.startswith('#') or href.startswith('http'):
            continue
        target = os.path.basename(href)
        if target and target not in all_files:
            issues.append(Issue("Major", filename, "5.1", f"Dead link: {href}"))

    # Check for placeholder links
    hash_links = re.findall(r'href=["\']#([^"\']*)["\']', html)
    for link in hash_links:
        if link == '':  # bare #
            issues.append(Issue("Minor", filename, "5.2", f"Placeholder link: href='#'"))

    return issues


# ============================================================
# PHASE 6: Semantic HTML & Accessibility
# ============================================================

def phase6_checks(filename, html):
    issues = []

    # Count h1 tags — should be exactly one
    h1_count = len(re.findall(r'<h1[^>]*>', html, re.IGNORECASE))
    if h1_count == 0:
        issues.append(Issue("Major", filename, "6.1", "No <h1> heading found"))
    elif h1_count > 1:
        issues.append(Issue("Minor", filename, "6.1", f"Multiple <h1> tags found ({h1_count})"))

    # Check heading hierarchy — look for skipped levels
    headings = re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', html, re.DOTALL | re.IGNORECASE)
    if headings:
        prev_level = 0
        for level_text in headings:
            level = int(level_text[0])
            if prev_level > 0 and level > prev_level + 1:
                issues.append(Issue("Minor", filename, "6.1", f"Heading level skipped: h{prev_level} → h{level}"))
            prev_level = level

    # Check for semantic tags
    has_semantic = any(tag in html.lower() for tag in ['<header', '<main', '<footer', '<nav', '<section', '<article'])
    if not has_semantic:
        issues.append(Issue("Minor", filename, "6.2", "Page uses no semantic HTML tags"))

    # Check images have alt attributes
    img_tags = re.findall(r'<img[^>]+>', html, re.IGNORECASE)
    for tag in img_tags:
        if 'alt=' not in tag.lower():
            issues.append(Issue("Minor", filename, "6.3", "<img> missing alt attribute"))

    return issues


# ============================================================
# PHASE 7: Performance & Best Practices
# ============================================================

def phase7_checks(filename, html):
    issues = []

    # File size
    size_kb = get_file_size_kb(filename)
    if size_kb > 50:
        issues.append(Issue("Minor", filename, "7.1", f"Large file: {size_kb:.1f}KB"))

    # CSS line count
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    if style_match:
        css_lines = style_match.group(1).split('\n')
        if len(css_lines) > 300:
            issues.append(Issue("Minor", filename, "7.2", f"Excessive CSS: {len(css_lines)} lines"))

    # External dependencies
    external_scripts = re.findall(r'src=["\'](https?://[^"\']+)["\']', html)
    for ext in external_scripts:
        if 'localhost' not in ext and '127.0.0.1' not in ext:
            issues.append(Issue("Info", filename, "7.3", f"External dependency: {ext[:60]}..."))

    return issues


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("=" * 60)
    print("Genesis Website — Full Verification")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    all_files = get_html_files()
    print(f"\nFound {len(all_files)} HTML files")

    all_issues = []
    per_page = defaultdict(list)

    for i, filename in enumerate(all_files, 1):
        print(f"  [{i}/{len(all_files)}] Checking {filename}...", end=" " if i < len(all_files) else "\n")
        try:
            html = read_file(filename)
        except Exception as e:
            all_issues.append(Issue("Critical", filename, "READ", f"Failed to read file: {e}"))
            per_page[filename].append(all_issues[-1])
            continue

        # Run all phase checks
        page_issues = []
        for phase_fn in [phase1_checks, phase2_checks, phase3_checks, phase6_checks, phase7_checks]:
            page_issues.extend(phase_fn(filename, html))
        page_issues.extend(phase5_checks(filename, html, all_files))
        all_issues.extend(page_issues)
        per_page[filename].extend(page_issues)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'=' * 60}")

    severity_counts = defaultdict(int)
    for issue in all_issues:
        severity_counts[issue.severity] += 1

    for sev in ["Critical", "Major", "Minor", "Info"]:
        if severity_counts[sev]:
            print(f"  {sev}: {severity_counts[sev]}")

    # Pages with issues
    pages_with_issues = {k: v for k, v in per_page.items() if v}
    clean_pages = [f for f in all_files if f not in pages_with_issues]
    print(f"\nPages with issues: {len(pages_with_issues)}")
    print(f"Clean pages: {len(clean_pages)}")

    # Write VERIFICATION_REPORT.md
    write_report(all_files, per_page, all_issues, clean_pages)

    # Write ISSUES_LOG.md
    write_issues_log(all_issues)

    print("\nReports written:")
    print("  -> VERIFICATION_REPORT.md")
    print("  -> ISSUES_LOG.md")


def write_report(all_files, per_page, all_issues, clean_pages):
    lines = []
    lines.append("# Genesis Website — Verification Report")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Total files checked:** {len(all_files)}")

    # Summary table
    severity_counts = defaultdict(int)
    for issue in all_issues:
        severity_counts[issue.severity] += 1

    lines.append("\n## Summary")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|----------|-------|")
    for sev in ["Critical", "Major", "Minor", "Info"]:
        if severity_counts[sev]:
            lines.append(f"| {sev} | {severity_counts[sev]} |")
    lines.append(f"| **Total** | **{len(all_issues)}** |")

    lines.append(f"\n- **Clean pages:** {len(clean_pages)}")
    lines.append(f"- **Pages with issues:** {len(per_page) - len(clean_pages)}")

    # Per-page results
    lines.append("\n## Per-Page Results")
    lines.append("")

    for filename in all_files:
        page_issues = per_page.get(filename, [])
        if not page_issues:
            lines.append(f"### ✅ {filename}")
            lines.append("")
            lines.append("- No issues found")
            lines.append("")
        else:
            lines.append(f"### ❌ {filename} ({len(page_issues)} issues)")
            lines.append("")
            for issue in page_issues:
                icon = {"Critical": "🔴", "Major": "🟠", "Minor": "🟡", "Info": "🔵"}.get(issue.severity, "⚪")
                lines.append(f"- {icon} **[{issue.severity}]** `{issue.check}`: {issue.detail}")
            lines.append("")

    # Clean pages list
    lines.append("\n## Clean Pages (No Issues)")
    lines.append("")
    for p in sorted(clean_pages):
        lines.append(f"- {p}")

    with open(os.path.join(BASE_DIR, "VERIFICATION_REPORT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_issues_log(all_issues):
    lines = []
    lines.append("# Genesis Website — Issues Log")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Total issues:** {len(all_issues)}")

    # Group by severity
    for sev in ["Critical", "Major", "Minor", "Info"]:
        sev_issues = [i for i in all_issues if i.severity == sev]
        if not sev_issues:
            continue
        lines.append(f"\n## {sev} ({len(sev_issues)} issues)")
        lines.append("")

        # Group by page
        by_page = defaultdict(list)
        for issue in sev_issues:
            by_page[issue.page].append(issue)

        for page, issues in sorted(by_page.items()):
            lines.append(f"### {page}")
            lines.append("")
            for issue in issues:
                lines.append(f"- **{issue.check}**: {issue.detail}")
            lines.append("")

    with open(os.path.join(BASE_DIR, "ISSUES_LOG.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
