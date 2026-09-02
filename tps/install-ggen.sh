#!/usr/bin/env bash
set -euo pipefail

archive="$RUNNER_TEMP/ggen.tar.gz"
curl --fail --location --retry 3 --retry-all-errors \
  --proto '=https' --tlsv1.2 \
  -o "$archive" \
  https://github.com/seanchatmangpt/ggen/releases/download/v26.8.27/ggen-x86_64-unknown-linux-gnu.tar.gz
echo "ab442ced90a9836fd4eb07a5d61eb58293843cd515d864699fc0d0453444a035  $archive" | sha256sum --check --strict
mkdir -p "$RUNNER_TEMP/ggen"
tar -xzf "$archive" -C "$RUNNER_TEMP/ggen"
bin="$(find "$RUNNER_TEMP/ggen" -type f -name ggen -print -quit)"
test -n "$bin"
chmod +x "$bin"
echo "$(dirname "$bin")" >> "$GITHUB_PATH"
