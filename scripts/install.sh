#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install.sh --target codex|claude|agents [--dest PATH] [--force] [--dry-run]

Targets:
  codex   Install under ${CODEX_HOME:-$HOME/.codex}/skills by default.
  claude  Install under $HOME/.claude/skills by default.
  agents  Install under $PWD/.agents/skills by default.

--dest PATH overrides the parent skills directory. The Skill is copied to
PATH/analyze-paper.
EOF
}

target=""
destination=""
force=0
dry_run=0

while (($#)); do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { echo "Missing value for --target" >&2; exit 2; }
      target="$2"
      shift 2
      ;;
    --dest)
      [[ $# -ge 2 ]] || { echo "Missing value for --dest" >&2; exit 2; }
      destination="$2"
      shift 2
      ;;
    --force)
      force=1
      shift
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "$target" ]] || { echo "--target is required" >&2; usage >&2; exit 2; }

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/analyze-paper"
[[ -f "$source_dir/SKILL.md" ]] || {
  echo "Canonical Skill not found: $source_dir" >&2
  exit 1
}

if [[ -z "$destination" ]]; then
  case "$target" in
    codex)
      destination="${CODEX_HOME:-$HOME/.codex}/skills"
      ;;
    claude)
      destination="$HOME/.claude/skills"
      ;;
    agents)
      destination="$PWD/.agents/skills"
      ;;
    *)
      echo "Unsupported target: $target" >&2
      exit 2
      ;;
  esac
elif [[ "$target" != "codex" && "$target" != "claude" && "$target" != "agents" ]]; then
  echo "Unsupported target: $target" >&2
  exit 2
fi

install_path="${destination%/}/analyze-paper"

if [[ -e "$install_path" && "$force" -ne 1 ]]; then
  echo "Refusing to replace existing installation: $install_path" >&2
  echo "Re-run with --force to replace it." >&2
  exit 1
fi

if [[ "$dry_run" -eq 1 ]]; then
  printf 'Would install %s to %s for target %s\n' "$source_dir" "$install_path" "$target"
  exit 0
fi

mkdir -p "$destination"
stage_dir="$(mktemp -d "${destination%/}/.analyze-paper.XXXXXX")"
trap 'rm -rf "$stage_dir"' EXIT
cp -R "$source_dir" "$stage_dir/analyze-paper"

if [[ -e "$install_path" ]]; then
  rm -rf "$install_path"
fi
mv "$stage_dir/analyze-paper" "$install_path"

printf 'Installed analyze-paper to %s\n' "$install_path"
