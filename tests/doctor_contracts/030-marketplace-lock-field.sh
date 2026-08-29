#!/usr/bin/env bash
set -eu
grep -Fq -- 'ggen_marketplace_commit' scripts/doctor.sh
