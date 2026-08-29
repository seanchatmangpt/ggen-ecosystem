#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="9-workflow-drift"' scripts/doctor.sh
