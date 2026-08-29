#!/usr/bin/env bash
set -eu
grep -Fq -- 'docker pull "$ref"' scripts/doctor.sh
