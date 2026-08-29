#!/usr/bin/env bash
set -euo pipefail
# fingerprint: job-build-and-push
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
# Updated 2026-08-29: real, evidence-driven restructure (commits 3c8b4109,
# ca21ca9d, 1a2d7b35) replaced the single `build-and-push:` job with three
# native per-architecture jobs after a real QEMU-based single-job attempt
# hit its own 120-minute timeout (run 33244628216). Checks the real
# current job set instead of the retired single-job name.
grep -Fq 'build-amd64:' .github/workflows/ggen-ecosystem-container.yml
grep -Fq 'build-arm64:' .github/workflows/ggen-ecosystem-container.yml
grep -Fq 'merge-manifest:' .github/workflows/ggen-ecosystem-container.yml
