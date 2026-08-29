#!/usr/bin/env bash
set -eu
grep -Fq -- 'docker run --rm "$ref" ggen --version' scripts/doctor.sh
