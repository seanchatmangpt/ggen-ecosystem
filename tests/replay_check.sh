#!/usr/bin/env bash
# replay_check.sh — PR-020 replay contract.
#
# Given a receipt JSON file matching docs/RECEIPT-SCHEMA.md, extract:
#   ecosystem.container_digest, subject.commit, execution.command
# then re-invoke that exact command against that exact container digest
# (docker run --rm <image>@<digest> <command>, mounting the subject commit's
# tree read from the local git history), and compare the new run's output
# digest against the receipt's recorded consequence.digest.
#
# It REFUSES rather than silently substituting a newer tag/HEAD when the
# exact digest is not locally resolvable (no docker pull is ever attempted).
#
# Usage:
#   tests/replay_check.sh [--dry-run] [--image-repo <repo>] <receipt.json>
#
# --dry-run   Print every extracted field and every command that WOULD be
#             run, then exit 0 before the actual `docker run` (or the local
#             digest-resolution check) executes. Safe to run with no docker
#             daemon, no container, and no real receipt.
# --image-repo <repo>
#             Override the container image repository (default: read from
#             [container].repository in ecosystem.lock.toml at repo root).
#
# Exit codes:
#   0  replay matched (consequence digest equal) OR --dry-run completed
#   1  replay ran but digests differed (REPLAY_MISMATCH)
#   2  usage error (bad args, file not found, receipt not valid JSON)
#   3  refused — typed REFUSED[<reason>] on stderr; see reasons below.
#
# Typed refusal reasons (all printed as REFUSED[<reason>] on stderr):
#   REPLAY_DIGEST_UNAVAILABLE   ecosystem.container_digest is not resolvable
#                               against a locally present image (no pull
#                               attempted — pinned-digest replay only).
#   REPLAY_COMMIT_UNAVAILABLE   subject.commit is not present in local git
#                               history (cannot materialize the exact tree).
#   REPLAY_SCHEMA_INVALID       receipt fails docs/RECEIPT-SCHEMA.md contract
#                               (delegates to scripts/verify-receipt.sh when
#                               present).
#   REPLAY_FIELD_MISSING        one of the three required fields could not be
#                               extracted from the receipt.
#
# This script never runs `docker build` or `docker push`, never rewrites
# ecosystem.lock.toml, and never falls back to `:latest`/HEAD when the exact
# digest or commit is unavailable — those are hard refusals, not fallbacks.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DRY_RUN=0
IMAGE_REPO_OVERRIDE=""
RECEIPT_PATH=""

usage() {
  echo "usage: $0 [--dry-run] [--image-repo <repo>] <receipt.json>" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --image-repo)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      IMAGE_REPO_OVERRIDE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "replay_check: unknown flag: $1" >&2
      usage
      exit 2
      ;;
    *)
      if [[ -n "$RECEIPT_PATH" ]]; then
        echo "replay_check: unexpected extra argument: $1" >&2
        usage
        exit 2
      fi
      RECEIPT_PATH="$1"
      shift
      ;;
  esac
done

if [[ -z "$RECEIPT_PATH" ]]; then
  usage
  exit 2
fi

if [[ ! -f "$RECEIPT_PATH" ]]; then
  echo "replay_check: receipt file not found: $RECEIPT_PATH" >&2
  exit 2
fi

refuse() {
  # $1 = reason token, $2 = human message
  echo "REFUSED[$1]: $2" >&2
  exit 3
}

echo "== replay_check: PR-020 replay contract =="
echo "receipt: $RECEIPT_PATH"

# --- Step 1: schema validation (delegate to verify-receipt.sh if present) ---
VERIFY_SCRIPT="$REPO_ROOT/scripts/verify-receipt.sh"
if [[ -x "$VERIFY_SCRIPT" ]]; then
  echo "-- validating receipt against docs/RECEIPT-SCHEMA.md via $VERIFY_SCRIPT"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "   [dry-run] would run: $VERIFY_SCRIPT $RECEIPT_PATH"
  fi
  if ! "$VERIFY_SCRIPT" "$RECEIPT_PATH"; then
    refuse "REPLAY_SCHEMA_INVALID" "receipt failed scripts/verify-receipt.sh validation: $RECEIPT_PATH"
  fi
else
  echo "-- scripts/verify-receipt.sh not found or not executable; skipping schema pre-check" >&2
  echo "   (falling back to raw JSON parse only)" >&2
fi

if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$RECEIPT_PATH" 2>/dev/null; then
  echo "replay_check: receipt is not valid JSON: $RECEIPT_PATH" >&2
  exit 2
fi

# --- Step 2: extract the three required fields (stdlib json only) ---
extract() {
  python3 - "$RECEIPT_PATH" "$1" <<'PY'
import json
import sys

path, dotted = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)

node = data
for part in dotted.split("."):
    if not isinstance(node, dict) or part not in node:
        sys.exit(1)
    node = node[part]

if node is None:
    sys.exit(1)

print(node)
PY
}

CONTAINER_DIGEST="$(extract "ecosystem.container_digest" || true)"
SUBJECT_COMMIT="$(extract "subject.commit" || true)"
EXEC_COMMAND="$(extract "execution.command" || true)"
RECORDED_CONSEQUENCE_DIGEST="$(extract "consequence.digest" || true)"

if [[ -z "$CONTAINER_DIGEST" || -z "$SUBJECT_COMMIT" || -z "$EXEC_COMMAND" || -z "$RECORDED_CONSEQUENCE_DIGEST" ]]; then
  refuse "REPLAY_FIELD_MISSING" "one or more of ecosystem.container_digest, subject.commit, execution.command, consequence.digest missing from $RECEIPT_PATH"
fi

echo "-- extracted fields"
echo "   ecosystem.container_digest = $CONTAINER_DIGEST"
echo "   subject.commit             = $SUBJECT_COMMIT"
echo "   execution.command          = $EXEC_COMMAND"
echo "   consequence.digest (recorded) = $RECORDED_CONSEQUENCE_DIGEST"

# --- Step 3: resolve the image repository (never mutates ecosystem.lock.toml) ---
LOCK_FILE="$REPO_ROOT/ecosystem.lock.toml"
if [[ -n "$IMAGE_REPO_OVERRIDE" ]]; then
  IMAGE_REPO="$IMAGE_REPO_OVERRIDE"
elif [[ -f "$LOCK_FILE" ]]; then
  IMAGE_REPO="$(python3 - "$LOCK_FILE" <<'PY'
import sys
try:
    import tomllib
except ImportError:
    tomllib = None

path = sys.argv[1]
if tomllib is not None:
    with open(path, "rb") as fh:
        data = tomllib.load(fh)
    print(data.get("container", {}).get("repository", ""))
else:
    # minimal fallback parse: find `repository = "..."` under [container]
    in_container = False
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if s == "[container]":
                in_container = True
                continue
            if s.startswith("[") and in_container:
                break
            if in_container and s.startswith("repository"):
                print(s.split("=", 1)[1].strip().strip('"'))
                break
PY
)"
else
  IMAGE_REPO=""
fi

if [[ -z "$IMAGE_REPO" ]]; then
  refuse "REPLAY_FIELD_MISSING" "could not resolve container image repository (no --image-repo given and [container].repository missing/unreadable in $LOCK_FILE)"
fi

IMAGE_REF="${IMAGE_REPO}@${CONTAINER_DIGEST}"
echo "-- resolved image ref: $IMAGE_REF (repository from: ${IMAGE_REPO_OVERRIDE:+--image-repo flag}${IMAGE_REPO_OVERRIDE:-$LOCK_FILE})"

# --- Step 4: local-only digest resolution (never pulls) ---
echo "-- checking local digest resolvability (no pull will be attempted)"
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "   [dry-run] would run: docker image inspect --format '{{.Id}}' \"$IMAGE_REF\""
  echo "   [dry-run] on failure this REFUSES as REFUSED[REPLAY_DIGEST_UNAVAILABLE] (no fallback to :latest/HEAD)"
else
  if ! docker image inspect --format '{{.Id}}' "$IMAGE_REF" >/dev/null 2>&1; then
    refuse "REPLAY_DIGEST_UNAVAILABLE" "image digest not locally resolvable: $IMAGE_REF (refusing rather than pulling or substituting a newer tag/HEAD)"
  fi
fi

# --- Step 5: materialize the subject commit's exact tree ---
WORKTREE_DIR=""
cleanup() {
  if [[ -n "$WORKTREE_DIR" && -d "$WORKTREE_DIR" ]]; then
    git -C "$REPO_ROOT" worktree remove --force "$WORKTREE_DIR" >/dev/null 2>&1 || rm -rf "$WORKTREE_DIR"
  fi
}
trap cleanup EXIT

echo "-- checking subject commit is present in local git history"
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "   [dry-run] would run: git -C \"$REPO_ROOT\" cat-file -e \"${SUBJECT_COMMIT}^{commit}\""
  echo "   [dry-run] on failure this REFUSES as REFUSED[REPLAY_COMMIT_UNAVAILABLE]"
  WORKTREE_DIR="/tmp/replay-check-<mktemp>"
  echo "   [dry-run] would run: git -C \"$REPO_ROOT\" worktree add --detach \"$WORKTREE_DIR\" \"$SUBJECT_COMMIT\""
else
  if ! git -C "$REPO_ROOT" cat-file -e "${SUBJECT_COMMIT}^{commit}" 2>/dev/null; then
    refuse "REPLAY_COMMIT_UNAVAILABLE" "subject.commit not present in local git history: $SUBJECT_COMMIT (refusing rather than replaying against a different tree)"
  fi
  WORKTREE_DIR="$(mktemp -d /tmp/replay-check-XXXXXX)"
  rmdir "$WORKTREE_DIR"
  git -C "$REPO_ROOT" worktree add --detach "$WORKTREE_DIR" "$SUBJECT_COMMIT" >/dev/null
fi

# --- Step 6: re-invoke the exact command against the exact digest ---
OUTPUT_FILE=""
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "-- [dry-run] would run:"
  echo "     docker run --rm -v \"$WORKTREE_DIR:/workspace\" -w /workspace \"$IMAGE_REF\" $EXEC_COMMAND"
  echo "-- [dry-run] would then sha256-hash the command's captured stdout and compare it against"
  echo "   the recorded consequence.digest ($RECORDED_CONSEQUENCE_DIGEST)."
  echo "-- [dry-run] STOPPING before the actual docker run (per --dry-run contract). Exiting 0."
  exit 0
fi

OUTPUT_FILE="$(mktemp /tmp/replay-check-output-XXXXXX)"
echo "-- running: docker run --rm -v \"$WORKTREE_DIR:/workspace\" -w /workspace \"$IMAGE_REF\" $EXEC_COMMAND"
# shellcheck disable=SC2086
if ! docker run --rm -v "$WORKTREE_DIR:/workspace" -w /workspace "$IMAGE_REF" $EXEC_COMMAND >"$OUTPUT_FILE" 2>&1; then
  echo "replay_check: replayed command exited non-zero (output captured in $OUTPUT_FILE)" >&2
  exit 1
fi

NEW_DIGEST_RAW="$(shasum -a 256 "$OUTPUT_FILE" | awk '{print $1}')"
NEW_DIGEST="sha256:${NEW_DIGEST_RAW}"

# Normalize recorded digest for comparison (accept bare hex or sha256:-prefixed).
RECORDED_NORMALIZED="$RECORDED_CONSEQUENCE_DIGEST"
if [[ "$RECORDED_NORMALIZED" != sha256:* ]]; then
  RECORDED_NORMALIZED="sha256:${RECORDED_NORMALIZED}"
fi

echo "-- replay consequence digest: $NEW_DIGEST"
echo "-- recorded consequence digest: $RECORDED_NORMALIZED"

if [[ "$NEW_DIGEST" == "$RECORDED_NORMALIZED" ]]; then
  echo "== REPLAY MATCH: consequence digest identical =="
  exit 0
else
  echo "REPLAY_MISMATCH: replayed digest $NEW_DIGEST != recorded digest $RECORDED_NORMALIZED" >&2
  exit 1
fi
