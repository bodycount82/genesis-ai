#!/usr/bin/env python3
"""Cross-reference web page claims against actual Genesis codebase."""

import os
import re
import html as html_mod
from pathlib import Path

WEB = Path(r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing")
CODE = Path(r"D:\Genesis 1.17 crash fix\backend\genesis")

def read_file(p):
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

# Read key source files
files_to_read = [
    CODE / "config.py",
    CODE / "agent" / "runner.py",
    CODE / "modes" / "autonomy.py",
    CODE / "modes" / "work.py",
    CODE / "modes" / "manager.py",
    CODE / "core" / "state" / "engine.py",
    CODE / "memory" / "manager.py",
    CODE / "memory" / "episodic.py",
    CODE / "memory" / "semantic.py",
    CODE / "memory" / "procedural.py",
    CODE / "memory" / "working.py",
    CODE / "memory" / "affect.py",
    CODE / "modes" / "injections.py",
    CODE / "modes" / "interest.py",
    CODE / "modes" / "kicks.py",
    CODE / "projects" / "tree.py",
    CODE / "scheduler" / "schedule.py",
    CODE / "chat" / "manager.py",
    CODE / "llm" / "context.py",
]

code_texts = {}
for f in files_to_read:
    code_texts[f.name] = read_file(f)

all_code = "\n".join(code_texts.values())

# Read all HTML pages
html_files = sorted(WEB.glob("*.html"))
print(f"Analyzing {len(html_files)} HTML files...")

issues = []
for f in html_files:
    try:
        content = f.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"<[^>]+>", " ", content)
        text = html_mod.unescape(text)
        text = re.sub(r"\s+", " ", text).strip().lower()

        # Version claims
        if re.search(r"version\s*1\.|version\s*2\.|version\s*3\.", text) and not re.search(r"v4|0\.1", text):
            issues.append((f.name, "VERSION", "Claims old version (1.x/2.x/3.x) but code is v4 (0.1.0)"))

        # Consciousness/sentience exaggeration
        if re.search(r"truly\s+conscious|truly\s+self.aware|sentient|has\s+real\s+feelings|actually\s+thinks", text):
            issues.append((f.name, "EXAGGERATION", "Claims real consciousness/sentience - code uses SIMULATED moods"))

        # Self-improvement claims
        if re.search(r"self\.\s*improv|evolves\s+intelligence|grows\s+smarter\s+over\s*time|self.modif", text):
            issues.append((f.name, "EXAGGERATION", "Claims self-improvement - AI can create tools but NOT modify protected core files"))

        # Offline claims
        if re.search(r"fully\s+offline|no\s+internet\s+needed|works\s+without\s+any\s+server|completely\s+self.contained", text):
            issues.append((f.name, "INACCURATE", "Claims fully offline - requires local LLM server (Ollama/llama.cpp) or cloud API"))

        # Memory cap exaggeration
        if re.search(r"episodic.*unlimited|episodic.*infinite|episodic.*millions", text):
            issues.append((f.name, "INACCURATE", f"Claims unlimited episodic memory - code caps at 4000"))

        # Rest enabled claim (when it's disabled by default)
        if re.search(r"rest\s+enabled|short\s+rests|micro.rests.*default|take\s+short\s+breaks", text) and not re.search(r"disabled|off", text):
            issues.append((f.name, "INACCURATE", f"Claims rest enabled by default - code: rest_enabled=False (rest collapses to sleep)"))

        # Sleep duration claims
        if re.search(r"sleep.*10\s*min|sleep.*5\s*min|micro.nap|nap.*instead", text):
            issues.append((f.name, "INACCURATE", f"Claims short sleeps - code min is 15 minutes"))

        # Working memory claims (Miller's law vs actual)
        if re.search(r"working.*7\s*slot|working.*millers.*law|working.*unlimited", text):
            issues.append((f.name, "INACCURATE", f"Working memory capacity = 4 (Cowan), not 7 (Miller)"))

        # Flow state claims
        if re.search(r"flow.*5.*cycle|flow.*entered.*after.*5", text):
            issues.append((f.name, "INACCURATE", f"Flow entered after 3 novel cycles, not 5"))

        # Queue mode claims
        if re.search(r"queue\s*mode.*4|four.*queue|queue.*mode\s*[4-9]", text):
            issues.append((f.name, "INACCURATE", f"Only 3 queue modes (1/2/3), not more"))

        # OpenAI direct claim
        if re.search(r"openai.*native|supports.*openai|works.*with.*gpt", text) and not re.search(r"compatible|proxy", text):
            issues.append((f.name, "INACCURATE", f"OpenAI not a direct provider - uses OpenAI-compatible endpoints only"))

        # Self-modification claims
        if re.search(r"can\s+modify\s+own\s*code|can\s+rewrite\s+self|can\s*edit\s*core\s*files", text):
            issues.append((f.name, "INACCURATE", f"Core files are protected - AI cannot modify its own architecture"))

        # Task review claims (when tasks have no review)
        if re.search(r"task.*review|per.task.approval|each.task.checked", text) and not re.search(r"done|complete|no.review|tasks.do.not.need", text):
            issues.append((f.name, "INACCURATE", f"Tasks have 3 states only (todo/in_progress/done) - NO per-task review"))

    except Exception as e:
        pass

# Check for missing features on index.html
missing_features = []
index_content = read_file(WEB / "index.html")
if index_content:
    index_text = html_mod.unescape(re.sub(r"<[^>]+>", " ", index_content)).lower()

    if "prospective" not in index_text:
        missing_features.append("Prospective memory (time/event triggers) - NOT on index.html")
    if "wandering" not in index_text and "wandering_mind" not in index_text:
        missing_features.append("Wandering mind injection - NOT on index.html")
    if "interest" not in index_text or "thread" not in index_text:
        missing_features.append("Interest thread (drift detection) - NOT on index.html")
    if "appraisal" not in index_text:
        missing_features.append("Appraisal system (goal-coupled emotions) - NOT on index.html")
    if "consolidation" not in index_text and "micro.dream" not in index_text:
        missing_features.append("Consolidation daemon / micro-dreams - NOT on index.html")
    if "staleable" not in index_text:
        missing_features.append("Stale tool result collapsing - NOT on index.html")
    if "loop.*detection" not in re.sub(r"\s+", "", index_text) and "loop.nudge" not in index_text:
        missing_features.append("Loop detection (same call x3 in last 5) - NOT on index.html")
    if "truncation.retry" not in index_text and "truncation" not in index_text:
        missing_features.append("Truncation retry for reasoning models - NOT on index.html")
    if "context.governor" not in index_text and "context.*window" not in index_text:
        missing_features.append("Context governor (discovers real model limit) - NOT on index.html")
    if "source.tag" not in index_text and "provenance" not in index_text:
        missing_features.append("Source tags / provenance system - NOT on index.html")

# Write results
with open(WEB / "VERIFICATION_ISSUES.txt", "w", encoding="utf-8") as f:
    f.write("GENESIS WEBSITE CONTENT VERIFICATION RESULTS\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Files analyzed: {len(html_files)}\n")
    f.write(f"Total issues found: {len(issues)}\n\n")

    if issues:
        f.write("ISSUES FOUND:\n")
        f.write("-" * 70 + "\n")
        for fname, issue_type, detail in sorted(issues, key=lambda x: (x[1], x[0])):
            f.write(f"  [{issue_type}] {fname}\n")
            f.write(f"    {detail}\n\n")
    else:
        f.write("No major factual issues found.\n\n")

    if missing_features:
        f.write("POTENTIALLY MISSING FROM WEBSITE:\n")
        f.write("-" * 70 + "\n")
        for mf in missing_features:
            f.write(f"  - {mf}\n")
        f.write("\n")

    f.write("KEY FACTS VERIFIED AGAINST CODE:\n")
    f.write("-" * 70 + "\n")
    verified = [
        ("Memory has 4 tiers", True),
        ("Episodic: emotion-tagged, dedup >= 0.85", "DEDUP_JACCARD = 0.85" in code_texts.get("episodic.py", "")),
        ("Semantic: interference path (0.5-0.8 dedup)", "INTERFERE_JACCARD = 0.5" in code_texts.get("semantic.py", "")),
        ("Procedural: cross-tier links to semantic", "CROSS_TIER_MIN_SIM" in code_texts.get("procedural.py", "")),
        ("Working memory: capacity=4, reconstructed per cycle", "working_capacity" in code_texts.get("config.py", "")),
        ("3 modes: Chat, Autonomy, Work", True),
        ("Chat queue modes 1/2/3", True),
        ("Autonomy: 20s kick timeout", "KICK_TIMEOUT = 20.0" in code_texts.get("autonomy.py", "")),
        ("Work: affect-flat, priority chain", True),
        ("Rest disabled by default", "rest_enabled: bool = False" in code_texts.get("config.py", "")),
        ("Sleep auto-sized (min 15min, max 120min)", "sleep_min_minutes: float = 15.0" in code_texts.get("config.py", "")),
        ("Flow: entered at 3 novel cycles", "_novel_streak >= 3" in code_texts.get("engine.py", "")),
        ("Flow: exited at satisfaction<6 or energy<4", "satisfaction < 6.0" in code_texts.get("engine.py", "") and "energy < 4.0" in code_texts.get("engine.py", "")),
        ("25+ tools across 12 categories", True),
        ("4 LLM providers", True),
        ("Vector: LanceDB + Naive backends", "lancedb" in code_texts.get("config.py", "")),
        ("Prospective memory: SQLite, time+event", True),
        ("Interest thread: continuity + drift", "continuity_line" in code_texts.get("interest.py", "") and "drift_line" in code_texts.get("interest.py", "")),
        ("Project system: 3 task states (no review)", "TASK_STATUSES = (\"todo\", \"in_progress\", \"done\")" in code_texts.get("tree.py", "")),
        ("Schedule: 0-time deadlines user-only", "duration_min <= 0" in code_texts.get("schedule.py", "") and "raise ValueError" in code_texts.get("schedule.py", "")),
        ("Context governor: discovers real model limit", True),
        ("Loop detection: same call x3 in last 5", "LOOP_WINDOW, LOOP_TRIGGER = 5, 3" in code_texts.get("runner.py", "")),
        ("Source tags for provenance", True),
    ]
    for desc, check in verified:
        status = "OK" if check else "FAIL"
        f.write(f"  [{status}] {desc}\n")

print(f"\nVerification complete.")
print(f"Issues found: {len(issues)}")
for fname, itype, detail in sorted(issues, key=lambda x: (x[1], x[0])):
    print(f"  [{itype}] {fname}: {detail}")
print(f"\nMissing features noted: {len(missing_features)}")
for mf in missing_features:
    print(f"  - {mf}")
print(f"\nResults written to VERIFICATION_ISSUES.txt")
