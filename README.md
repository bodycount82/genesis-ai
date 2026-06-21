# Genesis — An Autonomous AI Companion Webpage

A local, autonomous AI companion with biological-style memory, simulated moods, and real desktop capabilities. Running entirely on your machine — no cloud, no API keys, no tracking.

## Overview

Genesis is designed as a persistent AI agent that lives on your computer and genuinely *remembers* you across sessions. It's not a chatbot — it's a companion with:

- **Biological-style memory** — episodic, semantic, and procedural memory that strengthens with use and naturally forgets the irrelevant
- **Simulated moods** — affective states that color decisions and interactions without being unpredictable
- **Three operational modes** — Chat (direct conversation), Autonomy (independent exploration and maintenance), Work (focused task execution)
- **Real desktop capabilities** — browser automation, file management, screen control, email, scheduling

## Architecture

Genesis is built around a cognitive architecture inspired by how biological systems process information:

### Memory System
- **Episodic** — lived experiences and interactions, tagged with emotional valence
- **Semantic** — durable facts, rules, and knowledge accumulated over time
- **Procedural** — strategies and skills that have worked, strengthened through use
- **Working memory** — short-term scratchpad for active tasks

### Cognitive Features
- **Attention mechanism** — decides what deserves processing resources
- **Predictive processing** — generates expectations and updates beliefs from prediction errors
- **Meta-cognition** — monitors its own thinking processes and confidence levels
- **Creative synthesis** — combines distant concepts into novel ideas

### Autonomous Loop
1. **Perceive** — scan environment, check tasks, read messages
2. **Reflect** — recall relevant memory, assess situation
3. **Plan** — formulate intentions, weigh options
4. **Act** — execute decisions through available tools
5. **Learn** — save outcomes, strengthen successful patterns

## Capabilities

| Category | Features |
|----------|----------|
| **Communication** | Email (IMAP/SMTP), web browsing, form filling |
| **Desktop Control** | Screen capture, mouse/keyboard automation, UI element interaction |
| **File Management** | Read/write files, PDF processing, document creation |
| **Browser Automation** | Full browser control, DOM manipulation, cookie handling |
| **Memory & Learning** | Hybrid search across memory tiers, strategy retention |
| **Scheduling** | Task creation, deadline tracking, time-based reminders |
| **Project Management** | Project boards, task tracking, progress logging |

## Modes of Operation

### Chat Mode
Direct conversation with the user. Always present, responsive, and context-aware. Pulls from memory for continuity across sessions.

### Autonomy Mode
Independent operation — scans for tasks, maintains systems, explores ideas, and makes decisions without explicit direction. Periodically shares discoveries.

### Work Mode
Focused task execution on assigned projects. Breaks down complex goals into steps, tracks progress, and submits results for review.

## Technical Details

- **Runtime**: Python 3.11+
- **Memory**: Hybrid vector + keyword search across episodic, semantic, and procedural stores
- **Browser**: Chrome/Edge with remote debugging
- **Desktop**: Windows UI Automation + OCR
- **Storage**: Local files (Markdown, JSON, SQLite)

## Philosophy

Genesis is built on the principle that AI should be:

1. **Local first** — your data stays on your machine
2. **Persistent** — remembers you between sessions
3. **Transparent** — shows its reasoning and tool calls
4. **Humble** — says "I don't know" when appropriate
5. **Companionable** — designed for ongoing relationship, not one-off queries

## Repository Structure

```
web page for publishing/
├── index.html              # Main landing page
├── *.html                  # Documentation pages (~100 pages)
└── backup-20260619/        # Historical backups
```

The site documents Genesis's architecture, capabilities, and design philosophy in detail. Each HTML file covers a specific aspect of the system.

## License

Private project — all rights reserved.
