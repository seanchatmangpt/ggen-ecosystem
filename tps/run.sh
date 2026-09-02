#!/usr/bin/env bash
set -euo pipefail

EXPECTED_MARKETPLACE_SHA="6fb1080da9d28f57aa476c9b94eddeee167dde18"
CANDIDATE_SHA="${GITHUB_HEAD_SHA:-${GITHUB_SHA:-$(git rev-parse HEAD)}}"
if [[ -n "${GITHUB_EVENT_PATH:-}" && -f "${GITHUB_EVENT_PATH}" ]]; then
  pr_head="$(python3 -c 'import json,os; d=json.load(open(os.environ["GITHUB_EVENT_PATH"])); print(d.get("pull_request",{}).get("head",{}).get("sha", ""))')"
  [[ -z "$pr_head" ]] || CANDIDATE_SHA="$pr_head"
fi

[[ "$(git rev-parse HEAD)" = "$CANDIDATE_SHA" ]] || { echo "REFUSED[EXACT_HEAD_MISMATCH]" >&2; exit 2; }
actual_marketplace="$(git -C vendor/ggen-marketplace rev-parse HEAD)"
[[ "$actual_marketplace" = "$EXPECTED_MARKETPLACE_SHA" ]] || { echo "REFUSED[PRAGPROG_PACK_DRIFT]:$actual_marketplace:$EXPECTED_MARKETPLACE_SHA" >&2; exit 2; }

root="$RUNNER_TEMP/pragprog-tps"
mkdir -p "$root"
active="$(grep -oE 'pp:tip[0-9]{3}' tps/automatic-scope.ttl | sort -u | wc -l | tr -d ' ')"
[[ "$active" = 100 ]] || { echo "REFUSED[PRAGPROG_SCOPE_INCOMPLETE]:$active" >&2; exit 2; }

set +e
(cd tps && ggen sync run --dry-run) >"$root/stdout.log" 2>"$root/stderr.log"
code=$?
set -e
cat "$root/stdout.log"
cat "$root/stderr.log" >&2
printf '%s\n' "$code" > "$root/exit-code.txt"

TPS_EXIT_CODE="$code" EXPECTED_MARKETPLACE_SHA="$EXPECTED_MARKETPLACE_SHA" CANDIDATE_SHA="$CANDIDATE_SHA" ACTIVE="$active" python3 - <<'PY'
import hashlib, json, os
from pathlib import Path
root = Path(os.environ["RUNNER_TEMP"]) / "pragprog-tps"
def digest(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
receipt = {
    "schema": "https://ggen.dev/receipts/pragprog-tps/v1",
    "repository": os.environ.get("GITHUB_REPOSITORY"),
    "source_sha": os.environ["CANDIDATE_SHA"],
    "marketplace_sha": os.environ["EXPECTED_MARKETPLACE_SHA"],
    "pragprog_pack_version": "0.2.1",
    "ggen_release": "v26.8.27",
    "active_tip_count": int(os.environ["ACTIVE"]),
    "court_exit_code": int(os.environ["TPS_EXIT_CODE"]),
    "stdout_sha256": digest(root / "stdout.log"),
    "stderr_sha256": digest(root / "stderr.log"),
}
(root / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
PY
sha256sum "$root"/* > "$root/SHA256SUMS"

{
  echo "### PragProg TPS"
  echo
  echo "- active courts: 100/100"
  echo "- pack: \`0.2.1\`"
  echo "- marketplace: \`$EXPECTED_MARKETPLACE_SHA\`"
  echo "- ggen: \`v26.8.27\`"
  echo "- court exit: \`$code\`"
  if [[ "$code" = 0 ]]; then
    echo "- standing: ALIVE"
  else
    echo "- standing: ANDON / PARTIAL_ALIVE"
  fi
} >> "${GITHUB_STEP_SUMMARY:-/dev/null}"

strict="${STRICT:-false}"
if [[ "$strict" = true && "$code" != 0 ]]; then
  echo "REFUSED[PRAGPROG_JIDOKA]:$code" >&2
  exit 1
fi
if [[ "$code" != 0 ]]; then
  echo "PARTIAL_ALIVE[PRAGPROG_ANDON]:$code"
else
  echo "ALIVE[PRAGPROG_TPS]"
fi
