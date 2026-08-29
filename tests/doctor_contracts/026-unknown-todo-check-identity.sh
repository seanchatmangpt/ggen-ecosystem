#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="5-unknown-todo"' scripts/doctor.sh
