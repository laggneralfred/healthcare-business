#!/usr/bin/env bash

set -euo pipefail

SPRINT_NUMBER="${1:-}"
MESSAGE="${2:-}"
REMOTE="${3:-origin}"

if [[ -z "${SPRINT_NUMBER}" || -z "${MESSAGE}" ]]; then
    echo "Usage: bash scripts/sprint-freeze-tag.sh <sprint-number> <message> [remote]" >&2
    exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: sprint-freeze-tag.sh must be run inside a git repository." >&2
    exit 1
fi

TAG_NAME="sprint-${SPRINT_NUMBER}-freeze"

echo "Creating annotated tag ${TAG_NAME}"
git tag -a "${TAG_NAME}" -m "${MESSAGE}"

echo "Pushing HEAD to ${REMOTE}"
git push "${REMOTE}" HEAD

echo "Pushing tag ${TAG_NAME} to ${REMOTE}"
git push "${REMOTE}" "${TAG_NAME}"

echo "Sprint freeze push complete for ${TAG_NAME}"
