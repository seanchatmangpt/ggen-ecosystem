#!/usr/bin/env bash
set -eu
grep -Fq -- 'matches ecosystem.lock.toml pin exactly' scripts/doctor.sh
