#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'default:' 'Justfile'
