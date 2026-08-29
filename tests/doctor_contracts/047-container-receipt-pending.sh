#!/usr/bin/env bash
set -eu
grep -Fq -- 'container build not yet completed by the authoritative build owner' scripts/doctor.sh
