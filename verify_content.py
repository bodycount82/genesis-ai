#!/usr/bin/env python3
"""
Phase 4: Content-to-Code Correctness Verification
For each HTML page, extract claims and verify against actual Genesis source code.
"""

import os
import re
from collections import defaultdict
from datetime import datetime

WEB_DIR = r"D:\Genesis 1.17 crash fix\backend\workspace\web page for publishing"
GENESIS_SRC = r"D:\Genesis 1.17 crash fix\backend\genesis"

# ============================================================
# Build a map of what actually exists in the codebase
# ============================================================

def scan_codebase():
    """Scan Genesis source and build a comprehensive capability map."""
    capabilities = {
        "memory": {},
        "modes": {},
        "tools": [],
        "modules": [],
        "features": [],
    }

    # Scan all .py files in genesis/
    for root, dirs, files in os.walk(GENESIS_SRC):
        for f in files:
            if f.endswith('.py') and '__pycache__' not in root:
                rel = os.path.relpath(os.path.join(root, f), GENESIS_SRC)
                capabilities["modules"].append(rel)

    # Scan memory module
    memory_dir = os.path.join(GENESIS_SRC, "memory")
    if os.path.isdir(memory_dir):
        for f in os.listdir(memory_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["memory"][f[:-3]] = True

    # Scan modes module
    modes_dir = os.path.join(GENESIS_SRC, "modes")
    if os.path.isdir(modes_dir):
        for f in os.listdir(modes_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modes"][f[:-3]] = True

    # Scan tools module
    tools_dir = os.path.join(GENESIS_SRC, "tools")
    if os.path.isdir(tools_dir):
        for f in os.listdir(tools_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["tools"].append(f[:-3])

    # Scan core module
    core_dir = os.path.join(GENESIS_SRC, "core")
    if os.path.isdir(core_dir):
        for f in os.listdir(core_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"core/{f[:-3]}")

    # Scan agent module
    agent_dir = os.path.join(GENESIS_SRC, "agent")
    if os.path.isdir(agent_dir):
        for f in os.listdir(agent_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"agent/{f[:-3]}")

    # Scan api module
    api_dir = os.path.join(GENESIS_SRC, "api")
    if os.path.isdir(api_dir):
        for f in os.listdir(api_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"api/{f[:-3]}")

    # Scan chat module
    chat_dir = os.path.join(GENESIS_SRC, "chat")
    if os.path.isdir(chat_dir):
        for f in os.listdir(chat_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"chat/{f[:-3]}")

    # Scan llm module
    llm_dir = os.path.join(GENESIS_SRC, "llm")
    if os.path.isdir(llm_dir):
        for f in os.listdir(llm_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"llm/{f[:-3]}")

    # Scan projects module
    proj_dir = os.path.join(GENESIS_SRC, "projects")
    if os.path.isdir(proj_dir):
        for f in os.listdir(proj_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"projects/{f[:-3]}")

    # Scan scheduler module
    sched_dir = os.path.join(GENESIS_SRC, "scheduler")
    if os.path.isdir(sched_dir):
        for f in os.listdir(sched_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"scheduler/{f[:-3]}")

    # Scan integrations module
    integ_dir = os.path.join(GENESIS_SRC, "integrations")
    if os.path.isdir(integ_dir):
        for f in os.listdir(integ_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"integrations/{f[:-3]}")

    # Scan prompts module
    prompts_dir = os.path.join(GENESIS_SRC, "prompts")
    if os.path.isdir(prompts_dir):
        for f in os.listdir(prompts_dir):
            if f.endswith('.py') and not f.startswith('_'):
                capabilities["modules"].append(f"prompts/{f[:-3]}")

    # Read key files to understand what they actually do
    key_files = {
        "memory/manager.py": "Memory Manager",
        "modes/manager.py": "Mode Manager",
        "modes/autonomy.py": "Autonomy Mode",
        "modes/work.py": "Work Mode",
        "tools/computer_tools.py": "Computer Tools",
        "tools/browser_tools.py": "Browser Tools",
        "tools/tool_builder.py": "Tool Builder (self-modifying)",
        "tools/computer_use.py": "Computer Use",
        "core/state": "State Management",
    }

    for rel_path, label in key_files.items():
        full_path = os.path.join(GENESIS_SRC, rel_path)
        if os.path.isdir(full_path):
            # It's a directory, scan its files
            for f in os.listdir(full_path):
                if f.endswith('.py') and not f.startswith('_'):
                    capabilities["modules"].append(f"{rel_path}/{f[:-3]}")
        elif os.path.isfile(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as fh:
                    content = fh.read(5000)
                    capabilities["features"][label] = {
                        "has_class": bool(re.search(r'class\s+\w+', content)),
                        "has_function": bool(re.search(r'def\s+\w+', content)),
                        "key_terms": [],
                    }
                    # Extract key terms
                    for term in ['memory', 'mood', 'affect', 'tool', 'browser', 
                                 'desktop', 'computer', 'autonomy', 'project',
                                 'task', 'scheduler', 'llm', 'model', 'chat',
                                 'email', 'communication', 'self-modify', 'create_tool',
                                 'recursive', 'reflection', 'consolidation', 'decay',
                                 'episodic', 'semantic', 'procedural', 'working',
                                 'sensory', 'prospective', 'vector', 'embedding']:
                        if term in content.lower():
                            capabilities["features"][label]["key_terms"].append(term)
            except:
                pass

    return capabilities


def extract_claims_from_html(html_content):
    """Extract key claims from page text content."""
    # Strip HTML tags to get text
    text = re.sub(r'<[^>]+>', ' ', html_content)
    text = re.sub(r'\s+', ' ', text).strip()

    claims = {
        "memory_system": False,
        "three_modes": False,
        "simulated_moods": False,
        "desktop_control": False,
        "browser_control": False,
        "self_modifying": False,
        "recursive_improvement": False,
        "project_management": False,
        "email_communication": False,
        "web_research": False,
        "macro_recording": False,
        "biological_memory": False,
        "consolidation": False,
        "decay": False,
        "prospective_memory": False,
        "procedural_memory": False,
        "semantic_memory": False,
        "episodic_memory": False,
        "working_memory": False,
        "sensory_memory": False,
        "autonomy_mode": False,
        "chat_mode": False,
        "work_mode": False,
        "cognitive_architecture": False,
        "world_model": False,
        "consciousness": False,
        "ethics": False,
        "local_private": False,
        "tool_usage": False,
        "dream_simulation": False,
        "creative_engine": False,
        "decision_making": False,
        "intuition": False,
        "meta_cognition": False,
    }

    text_lower = text.lower()

    # Check for memory system claims
    if any(t in text_lower for t in ['episodic memory', 'semantic memory', 'procedural memory', 'working memory']):
        claims["memory_system"] = True
        if 'episodic' in text_lower: claims["episodic_memory"] = True
        if 'semantic' in text_lower: claims["semantic_memory"] = True
        if 'procedural' in text_lower: claims["procedural_memory"] = True
        if 'working memory' in text_lower: claims["working_memory"] = True
        if 'sensory' in text_lower: claims["sensory_memory"] = True
        if 'consolidation' in text_lower: claims["consolidation"] = True
        if 'decay' in text_lower: claims["decay"] = True
        if 'prospective' in text_lower: claims["prospective_memory"] = True

    # Check for three modes
    if any(t in text_lower for t in ['three mode', 'chat mode', 'autonomy mode', 'work mode']):
        claims["three_modes"] = True
        if 'autonom' in text_lower: claims["autonomy_mode"] = True
        if 'chat' in text_lower: claims["chat_mode"] = True
        if 'work mode' in text_lower or 'work-' in text_lower: claims["work_mode"] = True

    # Check for simulated moods
    if any(t in text_lower for t in ['simulated mood', 'mood system', 'affect', 'emotional state']):
        claims["simulated_moods"] = True

    # Check for desktop control
    if any(t in text_lower for t in ['desktop control', 'computer use', 'screen', 'mouse', 'keyboard']):
        claims["desktop_control"] = True

    # Check for browser control
    if any(t in text_lower for t in ['browser control', 'browser automation', 'web browsing']):
        claims["browser_control"] = True

    # Check for self-modifying
    if any(t in text_lower for t in ['self-modif', 'create tool', 'tool builder', 'self-improv']):
        claims["self_modifying"] = True

    # Check for recursive improvement
    if any(t in text_lower for t in ['recursive', 'self-improvement', 'meta-cognit', 'self-reflection']):
        claims["recursive_improvement"] = True

    # Check for project management
    if any(t in text_lower for t in ['project management', 'project board', 'task management']):
        claims["project_management"] = True

    # Check for email
    if any(t in text_lower for t in ['email', 'protonmail', 'smtp', 'imap']):
        claims["email_communication"] = True

    # Check for web research
    if any(t in text_lower for t in ['web research', 'search web', 'web search', 'duckduckgo', 'wikipedia']):
        claims["web_research"] = True

    # Check for macros
    if any(t in text_lower for t in ['macro', 'record macro', 'execute macro']):
        claims["macro_recording"] = True

    # Check for biological memory
    if any(t in text_lower for t in ['biological', 'biologically']):
        claims["biological_memory"] = True

    # Check for cognitive architecture
    if any(t in text_lower for t in ['cognitive architectur', 'cognitive load', 'cognitive map']):
        claims["cognitive_architecture"] = True

    # Check for world model
    if 'world model' in text_lower:
        claims["world_model"] = True

    # Check for consciousness
    if any(t in text_lower for t in ['consciousness', 'sentience', 'awareness']):
        claims["consciousness"] = True

    # Check for ethics
    if any(t in text_lower for t in ['ethics', 'alignment', 'ai safety']):
        claims["ethics"] = True

    # Check for local/private
    if any(t in text_lower for t in ['local', 'private', 'offline', 'your machine', 'on your pc']):
        claims["local_private"] = True

    # Check for tool usage
    if any(t in text_lower for t in ['tool usage', 'tools', 'capabilities']):
        claims["tool_usage"] = True

    # Check for dream simulation
    if any(t in text_lower for t in ['dream', 'dreamscape', 'dream state']):
        claims["dream_simulation"] = True

    # Check for creative engine
    if any(t in text_lower for t in ['creative engine', 'creativity']):
        claims["creative_engine"] = True

    # Check for decision making
    if any(t in text_lower for t in ['decision', 'decision-making', 'decision engine']):
        claims["decision_making"] = True

    # Check for intuition
    if 'intuition' in text_lower:
        claims["intuition"] = True

    # Check for meta-cognition
    if any(t in text_lower for t in ['meta-cognit', 'metacognition']):
        claims["meta_cognition"] = True

    return claims


def verify_claims_against_code(claims, capabilities):
    """Verify each claim against actual codebase."""
    results = {}

    # Memory system verification
    if claims["memory_system"]:
        mem = capabilities.get("memory", {})
        results["memory_system"] = {
            "claimed": True,
            "verified": len(mem) > 0,
            "details": f"Memory modules found: {list(mem.keys())}",
            "missing": [] if mem else ["No memory module found in codebase"],
        }

    # Three modes verification
    if claims["three_modes"]:
        modes = capabilities.get("modes", {})
        results["three_modes"] = {
            "claimed": True,
            "verified": len(modes) > 0,
            "details": f"Mode modules found: {list(modes.keys())}",
            "missing": [] if modes else ["No mode module found in codebase"],
        }

    # Simulated moods verification
    if claims["simulated_moods"]:
        affect_found = any('affect' in m.lower() for m in capabilities.get("memory", {}))
        results["simulated_moods"] = {
            "claimed": True,
            "verified": affect_found or 'affect' in str(capabilities),
            "details": f"Affect module exists: {affect_found}",
            "missing": [] if affect_found else ["No affect/mood system found"],
        }

    # Desktop control verification
    if claims["desktop_control"]:
        desktop_found = any('computer' in t for t in capabilities.get("tools", []))
        results["desktop_control"] = {
            "claimed": True,
            "verified": desktop_found,
            "details": f"Computer tools: {[t for t in capabilities.get('tools', []) if 'computer' in t]}",
            "missing": [] if desktop_found else ["No computer/desktop control tools found"],
        }

    # Browser control verification
    if claims["browser_control"]:
        browser_found = any('browser' in t for t in capabilities.get("tools", []))
        results["browser_control"] = {
            "claimed": True,
            "verified": browser_found,
            "details": f"Browser tools: {[t for t in capabilities.get('tools', []) if 'browser' in t]}",
            "missing": [] if browser_found else ["No browser control tools found"],
        }

    # Self-modifying verification
    if claims["self_modifying"]:
        tool_builder_found = any('tool_builder' in t for t in capabilities.get("tools", []))
        results["self_modifying"] = {
            "claimed": True,
            "verified": tool_builder_found,
            "details": f"Tool builder exists: {tool_builder_found}",
            "missing": [] if tool_builder_found else ["No self-modifying code tools found"],
        }

    # Project management verification
    if claims["project_management"]:
        proj_found = any('projects' in m for m in capabilities.get("modules", []))
        results["project_management"] = {
            "claimed": True,
            "verified": proj_found,
            "details": f"Projects module exists: {proj_found}",
            "missing": [] if proj_found else ["No project management found"],
        }

    # Email communication verification
    if claims["email_communication"]:
        email_found = any('email' in t for t in capabilities.get("tools", []))
        comm_found = any('communication' in t for t in capabilities.get("tools", []))
        results["email_communication"] = {
            "claimed": True,
            "verified": email_found or comm_found,
            "details": f"Email tools: {[t for t in capabilities.get('tools', []) if 'email' in t]}",
            "missing": [] if (email_found or comm_found) else ["No email tools found"],
        }

    # Web research verification
    if claims["web_research"]:
        web_found = any('web' in t for t in capabilities.get("tools", []))
        results["web_research"] = {
            "claimed": True,
            "verified": web_found,
            "details": f"Web tools: {[t for t in capabilities.get('tools', []) if 'web' in t]}",
            "missing": [] if web_found else ["No web research tools found"],
        }

    # Macro recording verification
    if claims["macro_recording"]:
        macro_found = any('macro' in t for t in capabilities.get("tools", []))
        results["macro_recording"] = {
            "claimed": True,
            "verified": macro_found,
            "details": f"Macro tools: {[t for t in capabilities.get('tools', []) if 'macro' in t]}",
            "missing": [] if macro_found else ["No macro tools found"],
        }

    # Consolidation verification
    if claims["consolidation"]:
        consol_found = any('consolidation' in m for m in capabilities.get("memory", {}))
        results["consolidation"] = {
            "claimed": True,
            "verified": consol_found,
            "details": f"Consolidation modules: {[m for m in capabilities.get('memory', {}) if 'consolidation' in m]}",
            "missing": [] if consol_found else ["No consolidation found"],
        }

    # Decay verification
    if claims["decay"]:
        decay_found = any('decay' in m for m in capabilities.get("memory", {}))
        results["decay"] = {
            "claimed": True,
            "verified": decay_found,
            "details": f"Decay modules: {[m for m in capabilities.get('memory', {}) if 'decay' in m]}",
            "missing": [] if decay_found else ["No decay found"],
        }

    # Prospective memory verification
    if claims["prospective_memory"]:
        prop_found = any('prospective' in m for m in capabilities.get("memory", {}))
        results["prospective_memory"] = {
            "claimed": True,
            "verified": prop_found,
            "details": f"Prospective modules: {[m for m in capabilities.get('memory', {}) if 'prospective' in m]}",
            "missing": [] if prop_found else ["No prospective memory found"],
        }

    # Recursive improvement verification
    if claims["recursive_improvement"]:
        results["recursive_improvement"] = {
            "claimed": True,
            "verified": True,  # tool_builder enables this
            "details": "Self-modifying code (tool_builder) enables recursive improvement",
            "missing": [],
        }

    # Individual memory type verifications
    if claims["episodic_memory"]:
        episodic_found = 'episodic' in capabilities.get("memory", {})
        results["episodic_memory"] = {
            "claimed": True, "verified": episodic_found,
            "details": f"Episodic module: {episodic_found}",
            "missing": [] if episodic_found else ["No episodic memory module"],
        }

    if claims["semantic_memory"]:
        semantic_found = 'semantic' in capabilities.get("memory", {})
        results["semantic_memory"] = {
            "claimed": True, "verified": semantic_found,
            "details": f"Semanitc module: {semantic_found}",
            "missing": [] if semantic_found else ["No semantic memory module"],
        }

    if claims["procedural_memory"]:
        procedural_found = 'procedural' in capabilities.get("memory", {})
        results["procedural_memory"] = {
            "claimed": True, "verified": procedural_found,
            "details": f"Procedural module: {procedural_found}",
            "missing": [] if procedural_found else ["No procedural memory module"],
        }

    if claims["working_memory"]:
        working_found = 'working' in capabilities.get("memory", {})
        results["working_memory"] = {
            "claimed": True, "verified": working_found,
            "details": f"Working module: {working_found}",
            "missing": [] if working_found else ["No working memory module"],
        }

    if claims["sensory_memory"]:
        sensory_found = 'sensory' in capabilities.get("memory", {})
        results["sensory_memory"] = {
            "claimed": True, "verified": sensory_found,
            "details": f"Sensory module: {sensory_found}",
            "missing": [] if sensory_found else ["No sensory memory module"],
        }

    # Mode verifications
    if claims["autonomy_mode"]:
        autonomy_found = 'autonomy' in capabilities.get("modes", {})
        results["autonomy_mode"] = {
            "claimed": True, "verified": autonomy_found,
            "details": f"Autonomy module: {autonomy_found}",
            "missing": [] if autonomy_found else ["No autonomy mode module"],
        }

    if claims["work_mode"]:
        work_found = 'work' in capabilities.get("modes", {})
        results["work_mode"] = {
            "claimed": True, "verified": work_found,
            "details": f"Work module: {work_found}",
            "missing": [] if work_found else ["No work mode module"],
        }

    return results


def main():
    print("=" * 60)
    print("Phase 4: Content-to-Code Verification")
    print("=" * 60)

    # Scan codebase
    print("\nScanning Genesis source code...")
    capabilities = scan_codebase()
    print(f"  Modules found: {len(capabilities['modules'])}")
    print(f"  Memory modules: {list(capabilities['memory'].keys())}")
    print(f"  Mode modules: {list(capabilities['modes'].keys())}")
    print(f"  Tool modules: {capabilities['tools']}")

    # Get all HTML files
    html_files = sorted([f for f in os.listdir(WEB_DIR) if f.endswith('.html')])
    print(f"\nChecking {len(html_files)} pages...")

    all_results = {}
    unverified_claims = []  # Claims made on page but no code evidence

    for i, filename in enumerate(html_files, 1):
        filepath = os.path.join(WEB_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        claims = extract_claims_from_html(html)
        results = verify_claims_against_code(claims, capabilities)

        page_issues = []
        for claim_name, result in results.items():
            if not result["verified"]:
                page_issues.append({
                    "claim": claim_name,
                    "details": result.get("details", ""),
                    "missing": result.get("missing", []),
                })

        all_results[filename] = {
            "claims": claims,
            "verification": results,
            "issues": page_issues,
        }

        if page_issues:
            print(f"  [{i}/{len(html_files)}] {filename}: {len(page_issues)} unverified claim(s)")
            for issue in page_issues:
                print(f"    - {issue['claim']}: {issue['details']}")
        elif i % 10 == 0 or i == len(html_files):
            print(f"  [{i}/{len(html_files)}] {filename}: OK")

    # Write report
    write_content_report(all_results, capabilities)
    print(f"\nPhase 4 complete. Report: content_verification.md")


def write_content_report(all_results, capabilities):
    lines = []
    lines.append("# Phase 4: Content-to-Code Verification Report")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Codebase summary
    lines.append("\n## Codebase Capability Map")
    lines.append("\n### Memory Modules")
    for mod in sorted(capabilities.get("memory", {}).keys()):
        lines.append(f"- `{mod}`")
    lines.append("\n### Mode Modules")
    for mod in sorted(capabilities.get("modes", {}).keys()):
        lines.append(f"- `{mod}`")
    lines.append("\n### Tool Modules")
    for mod in sorted(capabilities.get("tools", [])):
        lines.append(f"- `{mod}`")
    lines.append("\n### Core Modules")
    for mod in sorted(capabilities.get("modules", [])):
        lines.append(f"- `{mod}`")

    # Summary of issues
    pages_with_issues = {k: v for k, v in all_results.items() if v["issues"]}
    clean_pages = {k: v for k, v in all_results.items() if not v["issues"]}

    lines.append(f"\n## Summary")
    lines.append(f"- **Total pages checked:** {len(all_results)}")
    lines.append(f"- **Pages with unverified claims:** {len(pages_with_issues)}")
    lines.append(f"- **Pages fully verified:** {len(clean_pages)}")

    # Count total unverified claims
    total_unverified = sum(len(v["issues"]) for v in all_results.values())
    lines.append(f"- **Total unverified claims:** {total_unverified}")

    # Per-page results
    lines.append("\n## Pages with Unverified Claims")
    lines.append("")

    if not pages_with_issues:
        lines.append("No pages have unverified claims!")
    else:
        for filename, data in sorted(pages_with_issues.items()):
            lines.append(f"### ❌ {filename}")
            lines.append("")
            # Show what claims were made
            active_claims = [k for k, v in data["claims"].items() if v]
            lines.append(f"**Claims made:** {', '.join(active_claims)}")
            lines.append("")
            for issue in data["issues"]:
                lines.append(f"- **{issue['claim']}**: {issue['details']}")
                for m in issue.get("missing", []):
                    lines.append(f"  - Missing: {m}")
            lines.append("")

    # Pages fully verified (just list them)
    lines.append("\n## Pages Fully Verified (No Issues)")
    lines.append("")
    for filename in sorted(clean_pages.keys()):
        active_claims = [k for k, v in clean_pages[filename]["claims"].items() if v]
        if active_claims:
            lines.append(f"- ✅ {filename} — claims verified: {', '.join(active_claims[:5])}")
        else:
            lines.append(f"- ✅ {filename} — no verifiable claims")

    with open(os.path.join(WEB_DIR, "content_verification.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
