#!/usr/bin/env bash
set -euo pipefail
# fingerprint: buildpush-v6-pin
grep -Fq 'docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8' .github/workflows/ggen-ecosystem-container.yml
