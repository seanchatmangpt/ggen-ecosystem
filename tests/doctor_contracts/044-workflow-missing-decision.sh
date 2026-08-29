#!/usr/bin/env bash
set -eu
# Real, evidence-driven update 2026-08-29: doctor.sh's row-9 handling of a
# workflow absent from ggen's dry-run decisions changed from an
# unconditional BLOCKED ("not present in dry-run decisions") to a real
# fix distinguishing "not ontology-managed" (informational) from actual
# content drift (still BLOCKED) -- see scripts/doctor.sh's own comment
# there for the false-positive this fixed (mfact-certification.yml).
# This fingerprint now tracks the new real phrase.
grep -Fq -- 'informational, not drift' scripts/doctor.sh
