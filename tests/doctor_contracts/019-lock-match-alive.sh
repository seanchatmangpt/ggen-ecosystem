#!/usr/bin/env bash
set -eu
grep -Fq -- 'fresh --dry-run pack content_hash(es) match ggen.lock exactly' scripts/doctor.sh
