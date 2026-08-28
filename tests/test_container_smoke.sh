#!/usr/bin/env bash
# Chicago-style (no mocks) smoke test for the composed ggen-ecosystem Docker image.
#
# Every assertion below runs a REAL `docker run` against the REAL built image and
# checks REAL observed stdout/exit codes/files -- there is no stubbed or assumed
# output anywhere in this script. If docker itself is unavailable, this script
# reports BLOCKED (exit 2) rather than faking a pass.
#
# Usage: bash tests/test_container_smoke.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="ggen-ecosystem:test"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/minimal-ggen-project"

PASS_COUNT=0
FAIL_COUNT=0

pass() { echo "PASS: $1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { echo "FAIL: $1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }

# --- BLOCKED check: docker itself must be real and reachable ---------------
if ! command -v docker >/dev/null 2>&1; then
    echo "BLOCKED: docker is not installed / not on PATH -- cannot run any real assertion."
    exit 2
fi
if ! docker info >/dev/null 2>&1; then
    echo "BLOCKED: docker daemon is not reachable (docker info failed) -- cannot run any real assertion."
    exit 2
fi

# --- ensure the real image exists, building it for real if not -------------
if docker images -q "$IMAGE" | grep -q .; then
    echo "== image $IMAGE already present, reusing it =="
else
    echo "== image $IMAGE not found, building for real (this can take several minutes) =="
    # --load is required: modern docker CLI defaults to the buildx driver, whose build output
    # otherwise stays in the builder's own cache and never reaches `docker images`/`docker run`
    # (confirmed the hard way: a build reporting exit 0 without --load still left "Unable to
    # find image" on the very next `docker run`).
    if ! docker build --load -t "$IMAGE" "$REPO_ROOT"; then
        echo "BLOCKED: real 'docker build -t $IMAGE $REPO_ROOT' failed -- cannot run any real assertion."
        exit 2
    fi
fi

# =============================================================================
# Assertion 1: `ggen --version` prints a real, non-empty version string
# matching a pattern like '26.'
# =============================================================================
echo
echo "== Assertion 1: ggen --version =="
VERSION_OUTPUT="$(docker run --rm "$IMAGE" ggen --version 2>&1)"
VERSION_STATUS=$?
echo "--- real observed output ---"
echo "$VERSION_OUTPUT"
echo "--- exit code: $VERSION_STATUS ---"

if [ "$VERSION_STATUS" -ne 0 ]; then
    fail "assertion 1: 'ggen --version' exited non-zero ($VERSION_STATUS)"
elif [ -z "$VERSION_OUTPUT" ]; then
    fail "assertion 1: 'ggen --version' produced empty output"
elif ! echo "$VERSION_OUTPUT" | grep -Eq '[0-9]+\.[0-9]+'; then
    fail "assertion 1: 'ggen --version' output did not match a version pattern (N.N): '$VERSION_OUTPUT'"
else
    pass "assertion 1: ggen --version printed real version string: '$VERSION_OUTPUT'"
fi

# =============================================================================
# Assertion 2: `ls /opt/ggen-marketplace/packs` lists real pack directories,
# non-empty, containing 'github-actions-pack'
# =============================================================================
echo
echo "== Assertion 2: ls /opt/ggen-marketplace/packs =="
PACKS_OUTPUT="$(docker run --rm "$IMAGE" ls /opt/ggen-marketplace/packs 2>&1)"
PACKS_STATUS=$?
echo "--- real observed output ---"
echo "$PACKS_OUTPUT"
echo "--- exit code: $PACKS_STATUS ---"

if [ "$PACKS_STATUS" -ne 0 ]; then
    fail "assertion 2: 'ls /opt/ggen-marketplace/packs' exited non-zero ($PACKS_STATUS)"
elif [ -z "$PACKS_OUTPUT" ]; then
    fail "assertion 2: 'ls /opt/ggen-marketplace/packs' produced empty output"
elif ! echo "$PACKS_OUTPUT" | grep -q "github-actions-pack"; then
    fail "assertion 2: 'github-actions-pack' not found in real pack listing: '$PACKS_OUTPUT'"
else
    pass "assertion 2: /opt/ggen-marketplace/packs lists real packs including github-actions-pack"
fi

# =============================================================================
# Assertion 3: mount the real minimal fixture, run `ggen sync run` inside the
# container, and assert the real expected output file was actually written
# with real expected content.
# =============================================================================
echo
echo "== Assertion 3: ggen sync run against mounted fixture =="

if [ ! -f "$FIXTURE_DIR/ggen.toml" ]; then
    fail "assertion 3: fixture missing at $FIXTURE_DIR/ggen.toml"
else
    # Use a scratch copy of the fixture so repeated runs are idempotent and we
    # never leave generated output files inside the checked-in fixture dir.
    #
    # Scratch dir MUST live under the repo tree, not system mktemp -d
    # (/var/folders/... or /private/tmp on macOS): confirmed the hard way that
    # colima (this machine's docker host) has `mounts: []` configured, so only
    # paths already visible to the VM (this repo, under $HOME) bind-mount real
    # content into a container -- a /var/folders scratch dir bind-mounts as an
    # EMPTY directory with no error, which silently produced a false
    # [FM-CONFIG-001] "ggen.toml not found" here on the first real run.
    SCRATCH_DIR="$REPO_ROOT/tests/.scratch-container-smoke"
    rm -rf "$SCRATCH_DIR"
    mkdir -p "$SCRATCH_DIR"
    cp -R "$FIXTURE_DIR/." "$SCRATCH_DIR/"
    rm -rf "$SCRATCH_DIR/out"

    SYNC_OUTPUT="$(docker run --rm \
        -v "$SCRATCH_DIR:/workspace" \
        -w /workspace \
        "$IMAGE" ggen sync run 2>&1)"
    SYNC_STATUS=$?
    echo "--- real observed output ---"
    echo "$SYNC_OUTPUT"
    echo "--- exit code: $SYNC_STATUS ---"

    OUT_FILE="$SCRATCH_DIR/out/hello.rs"

    if [ "$SYNC_STATUS" -ne 0 ]; then
        fail "assertion 3: 'ggen sync run' exited non-zero ($SYNC_STATUS)"
    elif [ ! -f "$OUT_FILE" ]; then
        fail "assertion 3: expected output file not written: $OUT_FILE"
    else
        echo "--- real generated file: $OUT_FILE ---"
        GENERATED_CONTENT="$(cat "$OUT_FILE")"
        echo "$GENERATED_CONTENT"
        if echo "$GENERATED_CONTENT" | grep -q "shape=https://example.org/shapes#ThingShape"; then
            pass "assertion 3: ggen sync run wrote real expected content to out/hello.rs"
        else
            fail "assertion 3: out/hello.rs written but missing expected content (shape=...ThingShape)"
        fi
    fi

    rm -rf "$SCRATCH_DIR"
fi

# =============================================================================
# Summary
# =============================================================================
echo
echo "== SUMMARY: $PASS_COUNT passed, $FAIL_COUNT failed =="

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi
exit 0
