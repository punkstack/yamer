#!/usr/bin/env bash
# scripts/worktree.sh — helper for running parallel agents on isolated branches
#
# Usage:
#   ./scripts/worktree.sh new <role> <slug>     Create a worktree for an agent
#   ./scripts/worktree.sh list                  List active worktrees
#   ./scripts/worktree.sh merge <slug>          Squash-merge a branch back to main
#   ./scripts/worktree.sh prune                 Remove finished worktrees

set -euo pipefail

WORKTREES_DIR="agent-worktrees"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"

cmd="${1:-help}"

case "$cmd" in
  new)
    role="${2:?Usage: worktree.sh new <role> <slug>}"
    slug="${3:?Usage: worktree.sh new <role> <slug>}"
    branch="agent/${role}/${slug}"
    path="${WORKTREES_DIR}/${role}-${slug}"

    mkdir -p "$WORKTREES_DIR"
    git fetch origin "$DEFAULT_BRANCH" 2>/dev/null || true
    git worktree add -b "$branch" "$path" "$DEFAULT_BRANCH"

    echo ""
    echo "✓ Worktree created"
    echo "  Path:   $path"
    echo "  Branch: $branch"
    echo ""
    echo "Agent should cd into $path and work there."
    ;;

  list)
    git worktree list
    ;;

  merge)
    slug="${2:?Usage: worktree.sh merge <slug>}"
    # Find the worktree by slug (matches any role)
    match=$(git worktree list --porcelain | awk -v s="$slug" '/^worktree/ && $2 ~ s {print $2}' | head -1)
    if [ -z "$match" ]; then
      echo "✗ No worktree found matching slug: $slug" >&2
      exit 1
    fi
    branch=$(git -C "$match" rev-parse --abbrev-ref HEAD)

    echo "Merging $branch into $DEFAULT_BRANCH (squash)..."
    git checkout "$DEFAULT_BRANCH"
    git merge --squash "$branch"
    echo ""
    echo "Squash staged. Review with: git diff --staged"
    echo "Then commit: git commit -m \"merge: ${branch}\""
    echo "Then prune: ./scripts/worktree.sh prune"
    ;;

  prune)
    # Remove worktrees whose branches are merged into main
    git worktree list --porcelain | awk '/^worktree/ {print $2}' | while read -r wt; do
      [ "$wt" = "$(git rev-parse --show-toplevel)" ] && continue
      br=$(git -C "$wt" rev-parse --abbrev-ref HEAD)
      if git merge-base --is-ancestor "$br" "$DEFAULT_BRANCH" 2>/dev/null; then
        echo "Pruning merged worktree: $wt ($br)"
        git worktree remove "$wt"
        git branch -D "$br" 2>/dev/null || true
      fi
    done
    git worktree prune
    ;;

  help|*)
    cat <<EOF
worktree.sh — parallel agent dev helper

Commands:
  new <role> <slug>     Create a worktree for an agent
                          role:  backend | frontend | qa
                          slug:  short identifier for the task
                          example: ./scripts/worktree.sh new backend invoice-api
  list                  Show active worktrees
  merge <slug>          Squash-merge that worktree's branch back to main
  prune                 Remove worktrees whose branches are already merged
  help                  This message

Layout it creates:
  agent-worktrees/
    backend-invoice-api/    (branch: agent/backend/invoice-api)
    frontend-invoice-ui/    (branch: agent/frontend/invoice-ui)

When to use:
  Two or more agents writing code at the same time on independent files.
  Sequential or read-only work — don't bother, work on main.
EOF
    ;;
esac
