#!/usr/bin/env bash
set -euo pipefail
# fingerprint: login-v3-pin
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'docker/login-action@74a5d142397b4f367a81961eba4e8cd7edddf772' .github/workflows/ggen-ecosystem-container.yml
