#!/usr/bin/env bash
# tests/determinism_check.sh — PR-012 determinism proof.
#
# Proves: `ggen sync run --dry-run` against the same unchanged inputs
# (ontology.ttl / ggen.toml) produces a byte-identical `graph_hash_hex`
# across two consecutive runs from a clean state.
#
# Uses the HOST's installed `ggen` binary (~/.local/bin/ggen per
# scripts/doctor.sh check 2). Does NOT touch Docker, does NOT build or
# push any image, does NOT alter vendor/ggen* gitlinks or
# ecosystem.lock.toml.
#
# Remediation for a stale ggen.lock is per README.md / Makefile's `sync`
# target: "removes any stale ggen.lock, then runs `ggen sync run
# --dry-run`" — a dry-run does not itself write ggen.lock, but we still
# start from a clean slate the same way `make sync` does, since a stale
# lock is documented as the thing to clear before trusting a dry-run.
#
# Exit code: 0 if both runs' graph_hash_hex match, 1 otherwise.

set -u
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== tests/determinism_check.sh — PR-012 determinism proof =="
echo

if ! command -v ggen >/dev/null 2>&1; then
  echo "BLOCKED: ggen not found on PATH" >&2
  exit 1
fi

if [ ! -f ontology.ttl ] || [ ! -f ggen.toml ]; then
  echo "BLOCKED: ontology.ttl or ggen.toml not found in $(pwd)" >&2
  exit 1
fi

# --- clean state: remove any stale ggen.lock (documented remediation, ---
# --- same as `make sync`'s `rm -f ggen.lock` before a dry-run/run) -------
if [ -f ggen.lock ]; then
  echo "removing stale ggen.lock before determinism check (per README.md/Makefile 'sync' remediation)"
  rm -f ggen.lock
fi

extract_hash() {
  # stdin is the raw stdout of `ggen sync run --dry-run --format json-pretty`.
  # ggen emits the JSON summary followed by a trailing tracing INFO log line
  # on stdout, so parse only the first balanced top-level JSON object rather
  # than the whole stream.
  python3 -c "
import sys, json
raw = sys.stdin.read()
decoder = json.JSONDecoder()
try:
    d, _ = decoder.raw_decode(raw)
except Exception as e:
    print('PARSE_ERROR:' + str(e), file=sys.stderr)
    sys.exit(1)
h = d.get('graph_hash_hex')
if h is None:
    print('MISSING_FIELD graph_hash_hex', file=sys.stderr)
    sys.exit(1)
print(h)
"
}

echo "--- run 1: ggen sync run --dry-run --format json-pretty ---"
run1_stdout="$(mktemp)"
run1_stderr="$(mktemp)"
ggen sync run --dry-run --format json-pretty >"$run1_stdout" 2>"$run1_stderr"
run1_rc=$?
if [ "$run1_rc" -ne 0 ]; then
  echo "BLOCKED: run 1 exited $run1_rc" >&2
  tail -20 "$run1_stderr" >&2
  exit 1
fi
run1_hash="$(extract_hash < "$run1_stdout")"
if [ -z "$run1_hash" ]; then
  echo "BLOCKED: could not extract graph_hash_hex from run 1 output" >&2
  tail -40 "$run1_stdout" >&2
  exit 1
fi
echo "run 1 graph_hash_hex: $run1_hash"
echo

echo "--- run 2: ggen sync run --dry-run --format json-pretty ---"
run2_stdout="$(mktemp)"
run2_stderr="$(mktemp)"
ggen sync run --dry-run --format json-pretty >"$run2_stdout" 2>"$run2_stderr"
run2_rc=$?
if [ "$run2_rc" -ne 0 ]; then
  echo "BLOCKED: run 2 exited $run2_rc" >&2
  tail -20 "$run2_stderr" >&2
  exit 1
fi
run2_hash="$(extract_hash < "$run2_stdout")"
if [ -z "$run2_hash" ]; then
  echo "BLOCKED: could not extract graph_hash_hex from run 2 output" >&2
  tail -40 "$run2_stdout" >&2
  exit 1
fi
echo "run 2 graph_hash_hex: $run2_hash"
echo

rm -f "$run1_stdout" "$run1_stderr" "$run2_stdout" "$run2_stderr"

if [ "$run1_hash" = "$run2_hash" ]; then
  echo "PASS: graph_hash_hex is byte-identical across both dry-run invocations"
  echo "  run1: $run1_hash"
  echo "  run2: $run2_hash"
  exit 0
else
  echo "FAIL: graph_hash_hex differs between runs" >&2
  echo "  run1: $run1_hash" >&2
  echo "  run2: $run2_hash" >&2
  exit 1
fi
