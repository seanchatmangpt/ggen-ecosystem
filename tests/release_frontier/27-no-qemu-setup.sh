#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-qemu-setup
! grep -Fq 'docker/setup-qemu-action@' .github/workflows/ggen-ecosystem-container.yml
