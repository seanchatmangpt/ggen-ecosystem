#!/usr/bin/env bash
# Canonical Chicago consumer qualification for ggen-ecosystem.
# This court may earn Chicago execution evidence only by running the real composed
# image against fresh consumer workspaces. No mocks, recorders, dry-runs, modeled
# gate states, fabricated receipts, or status-only substitutions are admitted.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/minimal-ggen-project"
SUBJECT_SHA="${CHICAGO_SUBJECT_SHA:-$(git -C "$REPO_ROOT" rev-parse HEAD)}"
IMAGE="ggen-ecosystem:chicago-${SUBJECT_SHA:0:12}"
EVIDENCE_PATH="${CHICAGO_EVIDENCE_PATH:-$REPO_ROOT/tests/.chicago-evidence.json}"

fail() {
  printf 'BUILD_BROKEN[CHICAGO]: %s\n' "$*" >&2
  exit 1
}

blocked() {
  printf 'BLOCKED[CHICAGO_RUNTIME]: %s\n' "$*" >&2
  exit 2
}

tree_digest() {
  local root="$1"
  local exclude_out="${2:-false}"
  python3 - "$root" "$exclude_out" <<'PY'
import hashlib
from pathlib import Path
import sys
root = Path(sys.argv[1])
exclude_out = sys.argv[2].lower() == "true"
# When excluding the manufactured surface (used by the "authoritative
# inputs must not mutate" checks), also exclude ggen's own real, expected
# runtime bookkeeping directories -- .ggen/keys/{signing,verifying}.key and
# .ggen-v2/receipt*.json are genuinely written by every real `ggen sync run`
# (see run_sync()'s own chmod-recovery step, which exists because
# .ggen/keys/* lands root-owned), not authoritative consumer input. This
# repo's own top-level .gitignore already treats both as generated, not
# tracked source.
excluded_dirs = {"out", ".ggen", ".ggen-v2"} if exclude_out else set()
h = hashlib.sha256()
for path in sorted(p for p in root.rglob("*") if p.is_file()):
    rel = path.relative_to(root).as_posix()
    if any(rel == d or rel.startswith(d + "/") for d in excluded_dirs):
        continue
    h.update(rel.encode())
    h.update(b"\0")
    h.update(path.read_bytes())
    h.update(b"\0")
print(h.hexdigest())
PY
}

run_sync() {
  local consumer="$1"
  local sync_status=0
  docker run --rm \
    -v "$consumer:/workspace" \
    -w /workspace \
    "$IMAGE" ggen sync run || sync_status=$?
  # The container runs as root by default, so files it writes (including
  # .ggen/keys/{signing,verifying}.key) can land root-owned and mode-restricted
  # on the bind mount. The host-side digest/cleanup steps run as the CI
  # runner's own (non-root) user and need real read/cleanup access to those
  # same files, so make the whole workspace world-readable/removable from
  # inside the same image right after the real write path runs -- do this
  # unconditionally (even on sync_status != 0) so a refused negative-path
  # run still leaves a cleanable workspace.
  docker run --rm \
    -v "$consumer:/workspace" \
    -w /workspace \
    "$IMAGE" chmod -R a+rwX /workspace
  # Return ggen's own exit code, not chmod's. Without this, a caller that
  # runs `set +e; run_sync ...; status=$?; set -e` (exactly what the
  # negative-consumer refusal check below does) captures chmod's exit
  # status instead -- chmod succeeds even when ggen genuinely refused,
  # silently turning a real refusal into an apparent, wrong success.
  return "$sync_status"
}

command -v git >/dev/null 2>&1 || blocked "git is unavailable"
command -v python3 >/dev/null 2>&1 || blocked "python3 is unavailable"
command -v docker >/dev/null 2>&1 || blocked "docker is unavailable"
docker info >/dev/null 2>&1 || blocked "docker daemon is unreachable"

ACTUAL_SHA="$(git -C "$REPO_ROOT" rev-parse HEAD)"
[[ "$ACTUAL_SHA" == "$SUBJECT_SHA" ]] || fail "exact subject mismatch expected=$SUBJECT_SHA actual=$ACTUAL_SHA"
[[ -f "$FIXTURE_DIR/ggen.toml" ]] || fail "consumer fixture missing ggen.toml"

if git -C "$REPO_ROOT" submodule status --recursive | grep -q '^-'; then
  fail "one or more required producer submodules are not materialized"
fi

echo "CHICAGO: build exact subject $SUBJECT_SHA"
docker build --load -t "$IMAGE" "$REPO_ROOT"

echo "CHICAGO: execute real composed binary"
VERSION_OUTPUT="$(docker run --rm "$IMAGE" ggen --version)"
[[ -n "$VERSION_OUTPUT" ]] || fail "ggen --version returned empty output"
docker run --rm "$IMAGE" test -d /opt/ggen-marketplace/packs

# Keep scratch under the checked-out tree so Docker Desktop/Colima mounts behave
# consistently with hosted Linux runners. Cleanup is unconditional.
WORK_ROOT="$REPO_ROOT/tests/.scratch-chicago-${RANDOM}-${RANDOM}"
rm -rf "$WORK_ROOT"
mkdir -p "$WORK_ROOT/consumer-a" "$WORK_ROOT/consumer-b" "$WORK_ROOT/consumer-negative"
trap 'rm -rf "$WORK_ROOT"' EXIT
cp -R "$FIXTURE_DIR/." "$WORK_ROOT/consumer-a/"
cp -R "$FIXTURE_DIR/." "$WORK_ROOT/consumer-b/"
cp -R "$FIXTURE_DIR/." "$WORK_ROOT/consumer-negative/"

INPUT_A_BEFORE="$(tree_digest "$WORK_ROOT/consumer-a" true)"
INPUT_B_BEFORE="$(tree_digest "$WORK_ROOT/consumer-b" true)"

# Consumer A: real write path.
echo "CHICAGO: consumer A real ggen sync run"
run_sync "$WORK_ROOT/consumer-a"
[[ -f "$WORK_ROOT/consumer-a/out/hello.rs" ]] || fail "consumer A did not manufacture out/hello.rs"
grep -q 'shape=https://example.org/shapes#ThingShape' "$WORK_ROOT/consumer-a/out/hello.rs" || fail "consumer A output content mismatch"
OUTPUT_A_FIRST="$(tree_digest "$WORK_ROOT/consumer-a/out" false)"
INPUT_A_AFTER="$(tree_digest "$WORK_ROOT/consumer-a" true)"
[[ "$INPUT_A_BEFORE" == "$INPUT_A_AFTER" ]] || fail "consumer A authoritative inputs mutated during manufacture"

# Replay: execute the real write path again and require identical output.
echo "CHICAGO: consumer A deterministic replay"
run_sync "$WORK_ROOT/consumer-a"
OUTPUT_A_REPLAY="$(tree_digest "$WORK_ROOT/consumer-a/out" false)"
[[ "$OUTPUT_A_FIRST" == "$OUTPUT_A_REPLAY" ]] || fail "consumer A replay digest drifted"

# Independent consumer B: no shared generated state.
echo "CHICAGO: consumer B independent real ggen sync run"
run_sync "$WORK_ROOT/consumer-b"
[[ -f "$WORK_ROOT/consumer-b/out/hello.rs" ]] || fail "consumer B did not manufacture out/hello.rs"
OUTPUT_B="$(tree_digest "$WORK_ROOT/consumer-b/out" false)"
INPUT_B_AFTER="$(tree_digest "$WORK_ROOT/consumer-b" true)"
[[ "$INPUT_B_BEFORE" == "$INPUT_B_AFTER" ]] || fail "consumer B authoritative inputs mutated during manufacture"
[[ "$OUTPUT_A_FIRST" == "$OUTPUT_B" ]] || fail "independent consumers produced different output digests"

# Negative consumer: exercise the real parser/config admission boundary. Missing
# ggen.toml must refuse with a nonzero exit and must not manufacture output.
echo "CHICAGO: negative consumer real refusal"
mv "$WORK_ROOT/consumer-negative/ggen.toml" "$WORK_ROOT/consumer-negative/ggen.toml.disabled"
set +e
NEGATIVE_OUTPUT="$(run_sync "$WORK_ROOT/consumer-negative" 2>&1)"
NEGATIVE_EXIT=$?
set -e
[[ "$NEGATIVE_EXIT" -ne 0 ]] || fail "negative consumer unexpectedly succeeded without ggen.toml"
[[ ! -e "$WORK_ROOT/consumer-negative/out/hello.rs" ]] || fail "negative consumer manufactured output despite refusal"

mkdir -p "$(dirname "$EVIDENCE_PATH")"
python3 - "$EVIDENCE_PATH" "$SUBJECT_SHA" "$VERSION_OUTPUT" "$OUTPUT_A_FIRST" "$OUTPUT_A_REPLAY" "$OUTPUT_B" "$NEGATIVE_EXIT" <<'PY'
import json
from pathlib import Path
import sys
path = Path(sys.argv[1])
evidence = {
    "schema": "ggen-ecosystem/chicago-evidence-v1",
    "subject_sha": sys.argv[2],
    "ggen_version_output": sys.argv[3],
    "executed": {
        "docker_build": True,
        "consumer_a_sync_run": True,
        "consumer_a_replay_sync_run": True,
        "consumer_b_sync_run": True,
        "negative_consumer_sync_run": True,
    },
    "dry_run": False,
    "consumer_a_output_sha256": sys.argv[4],
    "consumer_a_replay_sha256": sys.argv[5],
    "consumer_b_output_sha256": sys.argv[6],
    "negative_exit": int(sys.argv[7]),
}
path.write_text(json.dumps(evidence, sort_keys=True, indent=2) + "\n")
print(json.dumps(evidence, sort_keys=True))
PY

printf '%s\n' "$NEGATIVE_OUTPUT" | tail -20 || true
printf 'ALIVE[CHICAGO_CONSUMER]: subject=%s output=%s negative_exit=%s evidence=%s\n' \
  "$SUBJECT_SHA" "$OUTPUT_A_FIRST" "$NEGATIVE_EXIT" "$EVIDENCE_PATH"
