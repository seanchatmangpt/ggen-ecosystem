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
bin_dir="$(dirname "$bin")"

# GITHUB_PATH is applied only to subsequent workflow steps. Several TPS/Chicago
# courts intentionally install and execute ggen in the same shell, so bind the
# verified binary into the runner's existing PATH immediately as well.
if [ -w /usr/local/bin ]; then
  install -m 0755 "$bin" /usr/local/bin/ggen
elif command -v sudo >/dev/null 2>&1; then
  sudo install -m 0755 "$bin" /usr/local/bin/ggen
fi

echo "$bin_dir" >> "$GITHUB_PATH"

if command -v ggen >/dev/null 2>&1; then
  ggen --version >/dev/null 2>&1 || ggen --help >/dev/null
  echo "GGEN_INSTALL_ALIVE $(command -v ggen)"
else
  echo "GGEN_INSTALL_BLOCKED[NOT_ON_CURRENT_PATH]:$bin" >&2
  exit 1
fi
