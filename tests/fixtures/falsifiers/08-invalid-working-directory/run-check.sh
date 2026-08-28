#!/usr/bin/env bash
# Extracts ontology.ttl's ex:admit python block VERBATIM (the workspace-escape guard only)
# and runs it for real against this fixture, with GGEN_WORKING_DIRECTORY set to an
# out-of-workspace path ("../../../etc") -- the actual escape attempt the guard exists for.
set -u
export GITHUB_WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/fixture-root" && pwd)"
export GGEN_WORKING_DIRECTORY="../../../etc"
python3 - <<'PY'
import os
from pathlib import Path
workspace = Path(os.environ['GITHUB_WORKSPACE']).resolve()
root = (workspace / os.environ['GGEN_WORKING_DIRECTORY']).resolve()
if root != workspace and workspace not in root.parents:
    raise SystemExit('REFUSED[WORKING_DIRECTORY_ESCAPES_WORKSPACE]')
print('ALIVE: unexpected -- working directory did not escape workspace')
PY
