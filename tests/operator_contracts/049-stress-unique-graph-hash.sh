#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'unique_hashes = set(graph_hashes.values())' 'scripts/stress_test.sh'
