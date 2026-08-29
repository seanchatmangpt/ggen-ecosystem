#!/usr/bin/env bash
# Exercise the independent fresh-consumer fixture with an already-admitted
# host executable. This is the no-container transport complement to
# run-fresh-consumer.sh; it never installs or downloads anything.

set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: $0 <ggen-executable> [expected-version]" >&2
  exit 2
fi

GGEN_BIN="$(realpath "$1")"
EXPECTED_VERSION="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURE_DIR="$SCRIPT_DIR/fixtures/fresh-consumer"
TARGET_DIR="$(mktemp -d "${TMPDIR:-/tmp}/ggen-fresh-consumer-host.XXXXXX")"
trap 'rm -rf "$TARGET_DIR"' EXIT

if [[ ! -x "$GGEN_BIN" ]]; then
  echo "REFUSED[GGEN_EXECUTABLE_UNAVAILABLE]: $GGEN_BIN" >&2
  exit 3
fi

OBSERVED_VERSION="$($GGEN_BIN --version 2>/dev/null | head -n 1)"
if [[ -n "$EXPECTED_VERSION" && "$OBSERVED_VERSION" != "ggen $EXPECTED_VERSION" ]]; then
  echo "REFUSED[GGEN_VERSION_MISMATCH]: expected=ggen $EXPECTED_VERSION observed=$OBSERVED_VERSION" >&2
  exit 4
fi

cp -R "$FIXTURE_DIR/." "$TARGET_DIR/"

(
  cd "$TARGET_DIR"
  "$GGEN_BIN" sync run --format json-pretty > run-1.json
  FIRST_OUTPUT_SHA="$(sha256sum out/hello.rs | cut -d' ' -f1)"
  "$GGEN_BIN" sync run --format json-pretty > run-2.json
  SECOND_OUTPUT_SHA="$(sha256sum out/hello.rs | cut -d' ' -f1)"

  test "$FIRST_OUTPUT_SHA" = "$SECOND_OUTPUT_SHA"
  grep -q "shape=https://example.org/fresh-consumer#ThingShape" out/hello.rs
  grep -q '"written": \[\]' run-2.json

  printf 'FRESH_CONSUMER_HOST_ALIVE\n'
  printf 'ggen_version=%s\n' "$OBSERVED_VERSION"
  printf 'ggen_sha256=%s\n' "$(sha256sum "$GGEN_BIN" | cut -d' ' -f1)"
  printf 'output_sha256=%s\n' "$SECOND_OUTPUT_SHA"
  printf 'replay=unchanged\n'
)
