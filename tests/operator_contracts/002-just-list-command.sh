#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @just --list' 'Justfile'
