#!/usr/bin/env bash
set -eu
grep -Fq -- 'docker image inspect "$ref"' scripts/doctor.sh
