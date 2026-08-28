#!/usr/bin/env bash
# PR-010 crown test: run the fresh-consumer fixture against a real
# ggen-ecosystem container image.
#
# This script does NOT build, pull, or wait for any image itself. It takes
# an already-resolved image ref as its one argument and runs exactly the
# `docker run` invocation documented in
# tests/fixtures/fresh-consumer/README.md against the fixture directory.
#
# Usage:
#   tests/run-fresh-consumer.sh <image-ref>
#
# Example (once ecosystem.lock.toml's [container].digest is real):
#   tests/run-fresh-consumer.sh \
#     ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:<digest>
#
# Do NOT invoke this script against a real image from an automated agent
# session unless the image is confirmed to exist -- see this repo's
# orthogonal-swarm constraint on the Docker build subject.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <image-ref>" >&2
  exit 2
fi

IMAGE_REF="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURE_DIR="$SCRIPT_DIR/fixtures/fresh-consumer"

if [[ ! -f "$FIXTURE_DIR/ggen.toml" ]]; then
  echo "FAIL: fixture not found at $FIXTURE_DIR (expected ggen.toml)" >&2
  exit 1
fi

echo "== running fresh-consumer fixture against $IMAGE_REF =="
docker run --rm \
  -v "$FIXTURE_DIR:/workspace" \
  -w /workspace \
  "$IMAGE_REF" \
  ggen sync run

echo "== generated output =="
cat "$FIXTURE_DIR/out/hello.rs"

grep -q "shape=https://example.org/fresh-consumer#ThingShape" "$FIXTURE_DIR/out/hello.rs" \
  && echo "FRESH-CONSUMER CROWN TEST PASSED" \
  || { echo "FRESH-CONSUMER CROWN TEST FAILED: expected content missing from out/hello.rs" >&2; exit 1; }
