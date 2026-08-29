#!/usr/bin/env bash
set -eu
grep -Fq -- 'content_hash' scripts/doctor.sh
