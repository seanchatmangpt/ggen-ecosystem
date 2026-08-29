#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'bootstrap_receipt = "receipts/bootstrap-ggen-ecosystem-sync.json"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-bootstrap-receipt-path'
