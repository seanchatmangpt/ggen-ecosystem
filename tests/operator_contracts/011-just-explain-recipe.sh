#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'explain:' 'Justfile'
