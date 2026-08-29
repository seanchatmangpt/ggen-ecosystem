#!/usr/bin/env bash
# scripts/benchmark.sh — real, executable timing benchmarks for the ggen sync
# manufacturing pipeline. No mocking: every number below is measured from a
# real `ggen sync run` invocation against this repo's real ontology.ttl/
# ggen.toml, timed with the shell's own `time` builtin (wall-clock, real
# process spawn included). Outputs JSON to stdout; human summary to stderr.
#
# Usage: scripts/benchmark.sh [--runs N] [--json-out FILE]

set -euo pipefail

RUNS=20
JSON_OUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --runs) RUNS="$2"; shift 2 ;;
    --json-out) JSON_OUT="$2"; shift 2 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "== ggen-ecosystem benchmark: $RUNS runs of \`ggen sync run --dry-run\` ==" >&2

times_ms=()
for i in $(seq 1 "$RUNS"); do
  start=$(python3 -c 'import time; print(time.time_ns())')
  ggen sync run --dry-run --format quiet >/dev/null 2>&1
  end=$(python3 -c 'import time; print(time.time_ns())')
  ms=$(( (end - start) / 1000000 ))
  times_ms+=("$ms")
done

# Compute min/max/mean/p50/p95 in pure python (no bc/awk float assumptions).
python3 - "${times_ms[@]}" <<'PYEOF' > "${JSON_OUT:-/dev/stdout}"
import json
import sys

times = sorted(int(x) for x in sys.argv[1:])
n = len(times)

def pct(p):
    idx = min(n - 1, int(round(p * (n - 1))))
    return times[idx]

result = {
    "benchmark": "ggen_sync_run_dry_run_wall_clock_ms",
    "runs": n,
    "min_ms": times[0],
    "max_ms": times[-1],
    "mean_ms": round(sum(times) / n, 2),
    "p50_ms": pct(0.50),
    "p95_ms": pct(0.95),
    "raw_ms": times,
}
print(json.dumps(result, indent=2))
PYEOF

echo "== done ==" >&2
