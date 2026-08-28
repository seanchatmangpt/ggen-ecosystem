#!/usr/bin/env bash
# verify-receipt.sh — validate a v26.8.28 release receipt JSON file against the
# contract defined in docs/RECEIPT-SCHEMA.md.
#
# Usage: scripts/verify-receipt.sh <path/to/receipt.json>
# Exit 0 = valid. Exit 1 = invalid (message on stderr naming the field/rule).
# Exit 2 = usage error (missing arg, file not found, not valid JSON).
#
# Implementation note: the actual validation logic lives in an embedded Python3
# block (stdlib json only, no third-party deps) so this stays a single
# executable file with no separate script to keep in sync.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <receipt.json>" >&2
  exit 2
fi

receipt_path="$1"

if [[ ! -f "$receipt_path" ]]; then
  echo "verify-receipt: file not found: $receipt_path" >&2
  exit 2
fi

python3 - "$receipt_path" <<'PY'
import json
import re
import sys

path = sys.argv[1]

try:
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
except OSError as exc:
    print(f"verify-receipt: cannot read {path}: {exc}", file=sys.stderr)
    sys.exit(2)

try:
    doc = json.loads(raw)
except json.JSONDecodeError as exc:
    print(f"verify-receipt: {path} is not valid JSON: {exc}", file=sys.stderr)
    sys.exit(2)

errors = []

SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^(sha256:)?[0-9a-f]{64}$")
STANDING_BASE_RE = re.compile(
    r"^(UNKNOWN|PARTIAL_ALIVE|ALIVE|BLOCKED|BUILD_BROKEN|UNSUPPORTED|REFUSED)"
    r"(\[[^\]]+\])?$"
)
PLACEHOLDER_VALUES = {"unknown-todo", "todo", "tbd", "placeholder", "fixme", "xxx", ""}

MANDATORY_STRING_FIELDS = [
    "subject.repository",
    "subject.commit",
    "ecosystem.version",
    "ecosystem.ggen_commit",
    "ecosystem.marketplace_commit",
    "ecosystem.container_digest",
    "admission.result",
    "execution.command",
    "consequence.digest",
    "verification.doctor",
    "verification.chicago",
    "verification.dod",
    "standing",
]

MANDATORY_INT_FIELDS = [
    "execution.exit_code",
]

SHA1_FIELDS = [
    "subject.commit",
    "ecosystem.ggen_commit",
    "ecosystem.marketplace_commit",
]

SHA256_FIELDS = [
    "ecosystem.container_digest",
    "consequence.digest",
]

STANDING_FIELDS = [
    "standing",
    "verification.doctor",
    "verification.chicago",
    "verification.dod",
]


def get_path(doc, dotted):
    node = doc
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None, False
        node = node[part]
    return node, True


# Rule 2: mandatory fields present
for field in MANDATORY_STRING_FIELDS:
    value, present = get_path(doc, field)
    if not present or value is None:
        errors.append(f"missing mandatory field: {field}")
    elif not isinstance(value, str) or value == "":
        errors.append(f"field {field} must be a non-empty string, got: {value!r}")

for field in MANDATORY_INT_FIELDS:
    value, present = get_path(doc, field)
    if not present or value is None:
        errors.append(f"missing mandatory field: {field}")
    elif isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"field {field} must be an integer, got: {value!r}")

# Rule 3/4: format checks (only if present and a string, to avoid duplicate noise)
for field in SHA1_FIELDS:
    value, present = get_path(doc, field)
    if present and isinstance(value, str) and value:
        if not SHA1_RE.match(value):
            errors.append(
                f"field {field} must be a 40-char lowercase hex git SHA, got: {value!r}"
            )

for field in SHA256_FIELDS:
    value, present = get_path(doc, field)
    if present and isinstance(value, str) and value:
        if not SHA256_RE.match(value):
            errors.append(
                f"field {field} must match sha256 hex format "
                f"(optional 'sha256:' + 64 lowercase hex chars), got: {value!r}"
            )

# optional patch_sha256, format-checked only if present
value, present = get_path(doc, "patch_sha256")
if present and isinstance(value, str) and value:
    if not SHA256_RE.match(value):
        errors.append(
            f"field patch_sha256 must match sha256 hex format, got: {value!r}"
        )

# Rule 6: standing vocabulary
for field in STANDING_FIELDS:
    value, present = get_path(doc, field)
    if present and isinstance(value, str) and value:
        if not STANDING_BASE_RE.match(value):
            errors.append(
                f"field {field} has invalid standing value: {value!r} "
                f"(must be one of UNKNOWN/PARTIAL_ALIVE/ALIVE/BLOCKED/BUILD_BROKEN/"
                f"UNSUPPORTED/REFUSED, optionally with a bracketed reason)"
            )

# Rule 5: admission.result is ADMITTED or REFUSED[...]
value, present = get_path(doc, "admission.result")
if present and isinstance(value, str) and value:
    if not re.match(r"^(ADMITTED|REFUSED(\[[^\]]+\])?)$", value):
        errors.append(
            f"field admission.result must be ADMITTED or REFUSED[reason], got: {value!r}"
        )

# Rule 7: no placeholder values when standing == ALIVE
top_standing, top_present = get_path(doc, "standing")
if top_present and top_standing == "ALIVE":
    for field in MANDATORY_STRING_FIELDS:
        value, present = get_path(doc, field)
        if present and isinstance(value, str) and value.strip().lower() in PLACEHOLDER_VALUES:
            errors.append(
                f"standing=ALIVE but field {field} is a placeholder value: {value!r}"
            )

if errors:
    print(f"verify-receipt: INVALID — {path}", file=sys.stderr)
    for err in errors:
        print(f"  - {err}", file=sys.stderr)
    sys.exit(1)

print(f"verify-receipt: VALID — {path}")
sys.exit(0)
PY
