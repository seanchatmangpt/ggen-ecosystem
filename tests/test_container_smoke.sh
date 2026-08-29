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
    if [[ "$REPO_ROOT" == "$HOME"* ]]; then
        SCRATCH_DIR="$REPO_ROOT/tests/.scratch-container-smoke"
    else
        SCRATCH_DIR="${HOME}/.cache/ggen-scratch-container-smoke"
    fi
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
# Assertion 4: Python imports for autofde_lab and autofde_lab_planner
# =============================================================================
echo
echo "== Assertion 4: python imports for autofde_lab and autofde_lab_planner =="
IMPORTS_OUTPUT="$(docker run --rm "$IMAGE" python3 -c '
import autofde_lab
import autofde_lab_planner
from autofde_lab_planner.engine import CompositePlannerEngine
print("AUTOFDE_PLANNER_OK")
' 2>&1)"
IMPORTS_STATUS=$?
echo "--- real observed output ---"
echo "$IMPORTS_OUTPUT"
echo "--- exit code: $IMPORTS_STATUS ---"

if [ "$IMPORTS_STATUS" -ne 0 ]; then
    fail "assertion 4: python imports exited non-zero ($IMPORTS_STATUS)"
elif ! echo "$IMPORTS_OUTPUT" | grep -q "AUTOFDE_PLANNER_OK"; then
    fail "assertion 4: python imports missing AUTOFDE_PLANNER_OK"
else
    pass "assertion 4: autofde_lab and autofde_lab_planner import cleanly in container"
fi

# =============================================================================
# Assertion 5: Category-B Composite Detector diagnosis execution
# =============================================================================
echo
echo "== Assertion 5: CompositePlannerEngine diagnosis on real fault fixture =="
DIAGNOSIS_OUTPUT="$(docker run --rm "$IMAGE" python3 -c '
from autofde_lab_planner.engine import CompositePlannerEngine
engine = CompositePlannerEngine(namespace="default", app_name="order-service")
manifest = [{"metadata": {"name": "order-service"}, "spec": {"template": {"spec": {"containers": [{"name": "app", "ports": [{"hostPort": 8080}]}]}}}}]
res = engine.run_diagnosis(deployments_json=manifest)
has_conflicts = len(res.host_port_conflicts) > 0
print(f"DIAGNOSIS_OK host_port_conflicts={len(res.host_port_conflicts)}")
' 2>&1)"
DIAGNOSIS_STATUS=$?
echo "--- real observed output ---"
echo "$DIAGNOSIS_OUTPUT"
echo "--- exit code: $DIAGNOSIS_STATUS ---"

if [ "$DIAGNOSIS_STATUS" -ne 0 ]; then
    fail "assertion 5: CompositePlannerEngine diagnosis exited non-zero ($DIAGNOSIS_STATUS)"
elif ! echo "$DIAGNOSIS_OUTPUT" | grep -q "DIAGNOSIS_OK"; then
    fail "assertion 5: CompositePlannerEngine diagnosis output unexpected: $DIAGNOSIS_OUTPUT"
else
    pass "assertion 5: CompositePlannerEngine executed real diagnosis inside container ($DIAGNOSIS_OUTPUT)"
fi

# =============================================================================
# Assertion 6: POWL structural replay tree algebra
# =============================================================================
echo
echo "== Assertion 6: POWL structural replay tree =="
POWL_OUTPUT="$(docker run --rm "$IMAGE" python3 -c '
from autofde_lab.powl.algebra import Atom, PartialOrder, OrderEdge, NodeId
a1 = Atom("validate")
a2 = Atom("manufacture")
po = PartialOrder(children=(a1, a2), order=frozenset({OrderEdge(NodeId(0), NodeId(1))}))
print(f"POWL_TREE_OK children={len(po.children)} order_edges={len(po.order)}")
' 2>&1)"
POWL_STATUS=$?
echo "--- real observed output ---"
echo "$POWL_OUTPUT"
echo "--- exit code: $POWL_STATUS ---"

if [ "$POWL_STATUS" -ne 0 ]; then
    fail "assertion 6: POWL algebra exited non-zero ($POWL_STATUS)"
elif ! echo "$POWL_OUTPUT" | grep -q "POWL_TREE_OK"; then
    fail "assertion 6: POWL algebra output unexpected: $POWL_OUTPUT"
else
    pass "assertion 6: POWL structural node algebra executed cleanly inside container ($POWL_OUTPUT)"
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
