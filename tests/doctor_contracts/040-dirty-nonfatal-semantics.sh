#!/usr/bin/env bash
set -eu
grep -Fq -- 'dirty untracked/modified content in a submodule working tree is NOT necessarily fatal' scripts/doctor.sh
