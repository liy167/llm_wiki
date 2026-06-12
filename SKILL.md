---
name: llm-wiki-copilot
description: "Use when ingesting raw sources, querying compiled wiki pages, and linting wiki quality in this repository."
---

# LLM Wiki Skill (Local Adaptation)

This repository follows a Karpathy-style LLM-Wiki workflow adapted for VS Code + Copilot.

## Operations

### Ingest
- Read newly added files under raw/
- Create or update wiki/sources/ pages
- Update related wiki/concepts/, wiki/entities/, and wiki/synthesis/
- Refresh wiki/index.md and append wiki/log.md

### Query
- Read wiki/index.md first
- Read relevant pages and answer with citations
- Optional archive to outputs/query.md or wiki/synthesis/

### Lint
- Validate index consistency and internal markdown links
- Validate required folder/file structure
- Output report to outputs/lint.md

## Invariants
- raw/ is immutable by default
- wiki/log.md is append-only
- wiki/index.md is the first navigation entry
