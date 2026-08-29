#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'doctor:' 'Justfile'
