#!/usr/bin/env bash
# scripts/stress_test.sh — real concurrency stress test for the ggen sync
# pipeline. Runs N real `ggen sync run --dry-run` processes in parallel
# against this repo's real ontology.ttl/ggen.toml and asserts every one
# produces the IDENTICAL graph_hash_hex -- a real determinism-under-
# concurrency falsifier, not a mocked assertion. Also asserts none crash
# (non-zero exit) and none corrupt ggen.lock (read-only under --dry-run,
# verified by hashing it before/after).
#
# Usage: scripts/stress_test.sh [--parallel N]

set -euo pipefail

PARALLEL=16
while [[ $# -gt 0 ]]; do
  case "$1" in
    --parallel) PARALLEL="$2"; shift 2 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SCRATCH="$REPO_ROOT/.stress-scratch"
mkdir -p "$SCRATCH"
rm -f "$SCRATCH"/run-*.json "$SCRATCH"/run-*.exit

LOCK_HASH_BEFORE=$(shasum -a 256 ggen.lock | awk '{print $1}')

echo "== stress test: $PARALLEL concurrent \`ggen sync run --dry-run\` processes ==" >&2

pids=()
for i in $(seq 1 "$PARALLEL"); do
  (
    ggen sync run --dry-run --format json-pretty > "$SCRATCH/run-$i.json" 2>"$SCRATCH/run-$i.stderr"
    echo $? > "$SCRATCH/run-$i.exit"
  ) &
  pids+=("$!")
done

fail=0
for pid in "${pids[@]}"; do
  wait "$pid" || fail=1
done

LOCK_HASH_AFTER=$(shasum -a 256 ggen.lock | awk '{print $1}')

set +e
python3 - "$PARALLEL" "$SCRATCH" "$LOCK_HASH_BEFORE" "$LOCK_HASH_AFTER" <<'PYEOF'
import json
import sys
from pathlib import Path

n = int(sys.argv[1])
scratch = Path(sys.argv[2])
lock_before, lock_after = sys.argv[3], sys.argv[4]

exit_codes = {}
graph_hashes = {}
crashed = []
for i in range(1, n + 1):
    exit_file = scratch / f"run-{i}.exit"
    json_file = scratch / f"run-{i}.json"
    code = int(exit_file.read_text().strip()) if exit_file.exists() else -1
    exit_codes[i] = code
    if code != 0:
        crashed.append(i)
        continue
    try:
        data = json.loads(json_file.read_text())
        graph_hashes[i] = data.get("graph_hash_hex")
    except Exception as e:
        crashed.append(i)

unique_hashes = set(graph_hashes.values())
result = {
    "stress_test": "concurrent_ggen_sync_run_dry_run",
    "parallelism": n,
    "crashed_runs": crashed,
    "all_exit_zero": len(crashed) == 0,
    "unique_graph_hashes_observed": len(unique_hashes),
    "graph_hash_consistent": len(unique_hashes) == 1,
    "graph_hash_hex": next(iter(unique_hashes)) if len(unique_hashes) == 1 else sorted(unique_hashes),
    "ggen_lock_untouched_by_dry_run": lock_before == lock_after,
    "PASS": (len(crashed) == 0) and (len(unique_hashes) == 1) and (lock_before == lock_after),
}
print(json.dumps(result, indent=2))
if not result["PASS"]:
    sys.exit(1)
PYEOF
STATUS=$?
set -e

rm -rf "$SCRATCH"
exit $STATUS
