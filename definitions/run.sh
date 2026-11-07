#!/usr/bin/env bash
# Runs every question in questions.txt, in 3 conditions, N times each, each in a fresh
# non-interactive Claude Code session that can only use the read-only `duck` MCP server.
# Usage: ./definitions/run.sh [N]     (default 3). Raw answers go to definitions/raw/.
set -u
N="${1:-3}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
CLAUDE_BIN="${CLAUDE_BIN:-$(ls -d "$HOME/Library/Application Support/Claude/claude-code/"*/*/claude.app/Contents/MacOS/claude 2>/dev/null | tail -1)}"
[ -x "$CLAUDE_BIN" ] || CLAUDE_BIN="claude"
MODEL="${MODEL:-claude-sonnet-5-5}"

for c in A B C; do rm -rf "/tmp/def$c"; mkdir -p "/tmp/def$c"; done
cp "$ROOT/demo.duckdb"      /tmp/defA/demo.duckdb
cp "$ROOT/demo.duckdb"      /tmp/defB/demo.duckdb
cp "$HERE/CLAUDE-B.md"      /tmp/defB/CLAUDE.md
cp "$ROOT/demo_view.duckdb" /tmp/defC/demo.duckdb
for c in A B C; do
  cat > "/tmp/def$c/mcp.json" <<JSON
{"mcpServers":{"duck":{"command":"uvx","args":["mcp-server-motherduck","--db-path","/tmp/def$c/demo.duckdb","--read-only"]}}}
JSON
done

mkdir -p "$HERE/raw"
i=0
while IFS= read -r q; do
  i=$((i+1))
  for c in A B C; do
    for n in $(seq 1 "$N"); do
      out="$HERE/raw/${c}_q${i}_${n}.txt"
      [ -s "$out" ] && continue   # resume: skip finished runs
      echo "cond $c  question $i  run $n"
      ( cd "/tmp/def$c" && "$CLAUDE_BIN" -p "$q" \
          --model "$MODEL" \
          --strict-mcp-config --mcp-config "/tmp/def$c/mcp.json" \
          --tools "" --allowedTools "mcp__duck" \
          --permission-mode dontAsk \
          --setting-sources project \
          --output-format text ) > "$out" 2> "$out.err" < /dev/null
    done
  done
done < "$HERE/questions.txt"
echo "Done. Now: python3 definitions/score.py"
