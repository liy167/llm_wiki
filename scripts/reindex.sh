#!/usr/bin/env bash
set -euo pipefail

# Rebuild wiki/index.md skeleton if needed.
# This script is optional on Windows; run with Git Bash or WSL.

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INDEX="$ROOT/wiki/index.md"

cat > "$INDEX" <<'EOF'
# Knowledge Base Index

## sources

Per-source summary pages created from raw materials.

| Article | Summary | Updated |
|---------|---------|---------|

## concepts

Reusable concepts, methods, and patterns.

| Article | Summary | Updated |
|---------|---------|---------|

## entities

People, tools, organizations, and papers.

| Article | Summary | Updated |
|---------|---------|---------|

## synthesis

Cross-source synthesis pages and archived conclusions.

| Article | Summary | Updated |
|---------|---------|---------|
EOF

echo "Rebuilt wiki/index.md"
