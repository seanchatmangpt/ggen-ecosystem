#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURE="$ROOT/tests/fixtures/customer-gym"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

make_customer() {
  local target="$1"
  mkdir -p "$target/vendor/ggen-ecosystem" "$target/templates"
  cp "$FIXTURE/ggen.toml" "$target/ggen.toml"
  cp "$FIXTURE/ontology.ttl" "$target/ontology.ttl"

  # A real git submodule is physically contained inside the customer root.
  # Use git archive instead of a symlink so ggen's realpath containment court
  # sees exactly that topology while still binding the vendored bytes to the
  # exact checked-out producer HEAD.
  git -C "$ROOT" archive HEAD | tar -x -C "$target/vendor/ggen-ecosystem"
}

hash_outputs() {
  local target="$1"
  sha256sum \
    "$target/Cargo.toml" \
    "$target/src/main.rs" \
    "$target/src/gym_profile.rs" \
    "$target/gym/manifest.toml"
}

CUSTOMER="$WORK/customer"
make_customer "$CUSTOMER"

# 1. Manufacture a fresh downstream project through the vendored public wrapper.
"$CUSTOMER/vendor/ggen-ecosystem/bin/ggen-ecosystem" manufacture "$CUSTOMER"
for path in Cargo.toml src/main.rs src/gym_profile.rs gym/manifest.toml; do
  test -f "$CUSTOMER/$path"
done
test ! -d "$CUSTOMER/generated"

grep -F 'name = "acme-support-gym"' "$CUSTOMER/Cargo.toml"
grep -F 'pub const GYM_TITLE: &str = "Acme Support Gym";' "$CUSTOMER/src/gym_profile.rs"
grep -F 'Procedure { id: "inspect-ticket", title: "Inspect ticket", consequence: "READ" }' "$CUSTOMER/src/gym_profile.rs"
grep -F 'Procedure { id: "escalate-ticket", title: "Escalate ticket", consequence: "DO" }' "$CUSTOMER/src/gym_profile.rs"

# 2. Compile and execute the manufactured consequence against the real Rust toolchain.
cargo check --quiet --manifest-path "$CUSTOMER/Cargo.toml"
RUN_OUTPUT="$(cargo run --quiet --manifest-path "$CUSTOMER/Cargo.toml")"
grep -F 'acme-support-gym | Acme Support Gym' <<<"$RUN_OUTPUT"
grep -F 'procedures=2' <<<"$RUN_OUTPUT"
grep -F 'inspect-ticket|Inspect ticket|READ' <<<"$RUN_OUTPUT"
grep -F 'escalate-ticket|Escalate ticket|DO' <<<"$RUN_OUTPUT"

# 3. Prove deterministic replay: second manufacture must be byte-identical.
FIRST_HASHES="$(hash_outputs "$CUSTOMER")"
"$CUSTOMER/vendor/ggen-ecosystem/bin/ggen-ecosystem" manufacture "$CUSTOMER"
SECOND_HASHES="$(hash_outputs "$CUSTOMER")"
[[ "$FIRST_HASHES" = "$SECOND_HASHES" ]] || {
  echo 'BUILD_BROKEN[GYM_FACTORY_NON_IDEMPOTENT]' >&2
  diff -u <(printf '%s\n' "$FIRST_HASHES") <(printf '%s\n' "$SECOND_HASHES") || true
  exit 1
}
echo 'GYM_FACTORY_REPLAY_ALIVE'

# 4. Prove ontology sensitivity: change admitted intent and require a changed consequence.
python3 - "$CUSTOMER/ontology.ttl" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text()
old = 'dct:title "Escalate ticket"'
new = 'dct:title "Escalate customer ticket"'
if old not in text:
    raise SystemExit('fixture mutation anchor missing')
p.write_text(text.replace(old, new, 1))
PY
"$CUSTOMER/vendor/ggen-ecosystem/bin/ggen-ecosystem" manufacture "$CUSTOMER"
grep -F 'Procedure { id: "escalate-ticket", title: "Escalate customer ticket", consequence: "DO" }' "$CUSTOMER/src/gym_profile.rs"
THIRD_HASHES="$(hash_outputs "$CUSTOMER")"
[[ "$THIRD_HASHES" != "$SECOND_HASHES" ]] || {
  echo 'BUILD_BROKEN[ONTOLOGY_MUTATION_DID_NOT_CHANGE_ARTIFACT]' >&2
  exit 1
}
echo 'GYM_FACTORY_MUTATION_ALIVE'

# 5. Falsifier: an invalid customer ontology must be refused by SHACL admission.
BAD="$WORK/invalid-customer"
make_customer "$BAD"
python3 - "$BAD/ontology.ttl" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text()
needle = '    dct:identifier "acme-support-gym" ;\n'
if needle not in text:
    raise SystemExit('fixture refusal anchor missing')
p.write_text(text.replace(needle, '', 1))
PY
if "$BAD/vendor/ggen-ecosystem/bin/ggen-ecosystem" manufacture "$BAD"; then
  echo 'BUILD_BROKEN[INVALID_GYM_PROFILE_WAS_ADMITTED]' >&2
  exit 1
fi
echo 'GYM_FACTORY_SHACL_REFUSAL_ALIVE'

echo 'GYM_FACTORY_CHICAGO_ALIVE customer=acme-support-gym replay=deterministic mutation=sensitive invalid=refused vendor=in-root-exact-head'
