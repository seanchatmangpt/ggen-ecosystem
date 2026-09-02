#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURE="$ROOT/tests/fixtures/operator-redundancy"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

make_project() {
  local target="$1"
  mkdir -p "$target/vendor/ggen-ecosystem" "$target/templates"
  cp "$FIXTURE/ggen.toml" "$target/ggen.toml"
  cp "$FIXTURE/ontology.ttl" "$target/ontology.ttl"
  git -C "$ROOT" archive HEAD | tar -x -C "$target/vendor/ggen-ecosystem"
}

manufacture() {
  local target="$1"
  "$target/vendor/ggen-ecosystem/bin/ggen-ecosystem" manufacture "$target"
}

GOOD="$WORK/good"
make_project "$GOOD"

# 1. Prove the admitted operating model has no runtime human dependency while
# retaining an explicit constitutional human boundary.
manufacture "$GOOD"
test -f "$GOOD/redundancy/receipt.toml"
test ! -d "$GOOD/generated"
grep -F 'status = "ALIVE"' "$GOOD/redundancy/receipt.toml"
grep -F 'policy = "named-human-free-runtime"' "$GOOD/redundancy/receipt.toml"
grep -F 'id = "operate-portfolio"' "$GOOD/redundancy/receipt.toml"
grep -F 'runtime_requires_human = false' "$GOOD/redundancy/receipt.toml"
grep -F 'id = "need-missing-adapter"' "$GOOD/redundancy/receipt.toml"
grep -F 'child_workflow = "manufacture-missing-adapter"' "$GOOD/redundancy/receipt.toml"
grep -F 'resume_workflow = "operate-portfolio"' "$GOOD/redundancy/receipt.toml"
grep -F 'id = "change-authority-constitution"' "$GOOD/redundancy/receipt.toml"
grep -F 'principal = "constitutional-principal"' "$GOOD/redundancy/receipt.toml"

# 2. Deterministic replay: unchanged admitted intent produces byte-identical evidence.
FIRST="$(sha256sum "$GOOD/redundancy/receipt.toml")"
manufacture "$GOOD"
SECOND="$(sha256sum "$GOOD/redundancy/receipt.toml")"
[[ "$FIRST" = "$SECOND" ]] || {
  echo 'BUILD_BROKEN[OPERATOR_REDUNDANCY_NON_IDEMPOTENT]' >&2
  exit 1
}
echo 'OPERATOR_REDUNDANCY_REPLAY_ALIVE'

# 3. Intent sensitivity: changing the operational policy title must regenerate evidence.
python3 - "$GOOD/ontology.ttl" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text()
old = 'dct:title "Observe, select, actuate, verify, and replan the work portfolio"'
new = 'dct:title "Observe, select, actuate, verify, recover, and replan the work portfolio"'
if old not in text:
    raise SystemExit('operator redundancy mutation anchor missing')
p.write_text(text.replace(old, new, 1))
PY
manufacture "$GOOD"
grep -F 'title = "Observe, select, actuate, verify, recover, and replan the work portfolio"' "$GOOD/redundancy/receipt.toml"
THIRD="$(sha256sum "$GOOD/redundancy/receipt.toml")"
[[ "$THIRD" != "$SECOND" ]] || {
  echo 'BUILD_BROKEN[OPERATOR_REDUNDANCY_MUTATION_NOT_PROJECTED]' >&2
  exit 1
}
echo 'OPERATOR_REDUNDANCY_MUTATION_ALIVE'

# 4. Falsifier: an operational workflow requiring a human at runtime must be refused.
BAD_HUMAN="$WORK/bad-human"
make_project "$BAD_HUMAN"
python3 - "$BAD_HUMAN/ontology.ttl" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text()
old = '    orx:runtimeRequiresHuman false ;\n'
new = '    orx:runtimeRequiresHuman true ;\n'
if old not in text:
    raise SystemExit('runtime-human falsifier anchor missing')
p.write_text(text.replace(old, new, 1))
PY
if manufacture "$BAD_HUMAN"; then
  echo 'BUILD_BROKEN[RUNTIME_HUMAN_DEPENDENCY_WAS_ADMITTED]' >&2
  exit 1
fi
echo 'OPERATOR_REDUNDANCY_RUNTIME_HUMAN_REFUSAL_ALIVE'

# 5. Falsifier: a missing capability that ends without a child manufacture path
# is valid Turtle but invalid operational architecture.
BAD_CAPABILITY="$WORK/bad-capability"
make_project "$BAD_CAPABILITY"
python3 - "$BAD_CAPABILITY/ontology.ttl" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text()
old = '    orx:forWorkflow ex:OperatePortfolio ;\n    orx:handledByChildWorkflow ex:ManufactureMissingAdapter .\n'
new = '    orx:forWorkflow ex:OperatePortfolio .\n'
if old not in text:
    raise SystemExit('missing-capability falsifier anchor missing')
p.write_text(text.replace(old, new, 1))
PY
if manufacture "$BAD_CAPABILITY"; then
  echo 'BUILD_BROKEN[HUMAN_ESCALATION_CAPABILITY_GAP_WAS_ADMITTED]' >&2
  exit 1
fi
echo 'OPERATOR_REDUNDANCY_CAPABILITY_REFUSAL_ALIVE'

echo 'OPERATOR_REDUNDANCY_CHICAGO_ALIVE operational=named-human-free constitutional=human-admitted missing-capability=manufacture-verify-receipt-resume vendor=in-root-exact-head'
