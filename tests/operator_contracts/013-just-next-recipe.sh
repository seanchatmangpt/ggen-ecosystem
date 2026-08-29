#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'next:' 'Justfile'
