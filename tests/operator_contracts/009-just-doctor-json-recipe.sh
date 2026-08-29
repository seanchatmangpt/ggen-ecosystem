#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'doctor-json:' 'Justfile'
