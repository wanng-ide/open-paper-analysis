#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
installer="$repo_root/scripts/install.sh"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

bash "$installer" --target codex --dest "$tmp_dir/codex" --dry-run |
  grep -F "$tmp_dir/codex/analyze-paper" >/dev/null

bash "$installer" --target codex --dest "$tmp_dir/codex"
test -f "$tmp_dir/codex/analyze-paper/SKILL.md"

if bash "$installer" --target codex --dest "$tmp_dir/codex" >/dev/null 2>&1; then
  echo "Installer replaced an existing Skill without --force" >&2
  exit 1
fi

bash "$installer" --target codex --dest "$tmp_dir/codex" --force
bash "$installer" --target claude --dest "$tmp_dir/claude"
bash "$installer" --target agents --dest "$tmp_dir/agents"

for target in codex claude agents; do
  test -f "$tmp_dir/$target/analyze-paper/SKILL.md"
  test -f "$tmp_dir/$target/analyze-paper/references/quality-standard.md"
done

echo "Installer tests passed"
