#!/usr/bin/env bash
set -eu
grep -Fq -- "grep -n 'UNKNOWN-TODO' ecosystem.lock.toml" scripts/doctor.sh
