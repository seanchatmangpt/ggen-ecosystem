#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'graph:' 'Justfile'
