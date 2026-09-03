# Justfile — Canonical Operator Surface for GGen Ecosystem TPS + DfCM Plant

# Default recipe: print help / recipes
default:
    @just --list

# Canonical Chicago qualification: real composed image, real write path, replay,
# independent second consumer, and real negative refusal. No dry-runs or modeled gates.
chicago:
    @bash tests/chicago_consumer.sh

# Attempt bounded closure toward ALIVE, executing only safe reversible repairs
alive:
    @python3 scripts/ecosystem_alive.py --apply-safe

# Pure observation of system state (never repairs)
doctor:
    @bash scripts/doctor.sh

# Structured machine-readable JSON sensor output
doctor-json:
    @bash scripts/doctor.sh --json

# Explain why current standing exists across all gates
explain:
    @python3 scripts/ecosystem_alive.py --explain

# Return highest-information lawful next transition
next:
    @python3 scripts/ecosystem_alive.py --next

# Render live exact-head Definition of Done
dod:
    @python3 scripts/dod_engine.py

# Execute current impact-selected verification pack
verify:
    @bash scripts/verify-provenance.sh

# Classify bounded GHCR/OCI observations without publishing or granting DO.
publication-evidence:
    @python3 tools/classify_container_publication.py --require-count 52

# Full publication-evidence self-test + exact 52-case conformance court.
publication-evidence-test:
    @python3 tools/classify_container_publication.py --self-test --require-count 52

# mfact-style certification court: bind producer pins, artifact authority,
# release evidence, Git lineage, and scoped standing without manufacturing ALIVE.
certify:
    @python3 scripts/certify_ecosystem.py --root .

# Adversarial unit court for certification promotion/refusal rules.
certify-test:
    @python3 -m unittest tests.test_mfact_certification -v

# Reproduce prior receipt evidence deterministically
replay:
    @bash tests/determinism_check.sh

# Run 25-case adversarial negative-path falsifier suite
falsify:
    @python3 scripts/chicago_falsifiers.py

# Show AutoFDE candidate closure plan without executing
plan:
    @python3 scripts/ecosystem_alive.py --json

# Expose the current gate / capability / dependency graph
graph:
    @cat ontology/gates.ttl 2>/dev/null || python3 scripts/ecosystem_alive.py --explain

# Real wall-clock timing benchmark of `ggen sync run --dry-run` (20 runs, min/max/mean/p50/p95).
# Benchmark evidence is performance-only and cannot earn Chicago standing.
bench:
    @bash scripts/benchmark.sh --runs 20

# Real concurrency stress test under --dry-run. Stress evidence is diagnostic and
# cannot earn Chicago standing because it does not execute the write consequence.
stress:
    @bash scripts/stress_test.sh --parallel 16

# --- act (local GitHub Actions parity) --------------------------------------
# GitHub Actions minutes are finite; these recipes run the real workflows
# locally via `act` instead. Machine-specific flags live here (not in
# .actrc, which has no override/merge mechanism) so the committed .actrc
# stays portable across Intel/Docker-Desktop machines. Defaults below match
# what was proven working on this machine (Colima, Apple Silicon).
act_arch := env_var_or_default("ACT_CONTAINER_ARCH", "linux/arm64")
# act's OWN connection to the Docker daemon comes from the standard
# DOCKER_HOST env var, which it does NOT infer from the active `docker
# context` (verified: with DOCKER_HOST unset, act defaulted to the stale
# /var/run/docker.sock symlink even though `docker context ls` shows
# `colima` active and that's where the pulled image actually lives).
export DOCKER_HOST := env_var_or_default("ACT_DAEMON_SOCKET", "unix://" + env_var_or_default("HOME", "") + "/.colima/default/docker.sock")
# `--container-daemon-socket` is a DIFFERENT thing: the socket bind-mounted
# INTO job containers for docker-in-docker steps. Bind-mounting Colima's real
# socket path directly fails under this VM backend ("mkdir .../docker.sock:
# operation not supported" — the macOS-side path isn't mountable as a source
# across the Lima VM boundary); /var/run/docker.sock works because that path
# is native to the VM's own root filesystem (matches the working invocation
# already recorded in docs/DEFINITION-OF-DONE.md).
act_container_socket := env_var_or_default("ACT_CONTAINER_DAEMON_SOCKET", "unix:///var/run/docker.sock")
act_flags := "--container-architecture " + act_arch + " --container-daemon-socket " + act_container_socket + " --secret-file .secrets"

# --bind (opt-in, NOT part of act_flags — see WARNING below): binds the real
# working directory into the job container instead of copying it. Needed
# ONLY by pr-governance.yml's Chicago consumer step, which does
# docker-outside-of-docker — a `docker run -v "$WORK_ROOT/consumer-a:
# /workspace" ...` issued FROM INSIDE the job container, talking to the HOST
# daemon over the bind-mounted socket. Under act's default copy-mode
# checkout, that scratch path only exists in the job container's own private
# overlay copy — invisible to the host daemon, which silently bind-mounts an
# EMPTY directory instead (observed real failure: "ggen.toml not found at
# /workspace/ggen.toml" even though the fixture was genuinely copied in
# moments earlier). No other job in this repo does this pattern, so no other
# recipe needs --bind — keep it scoped to act-governance only.
#
# WARNING, learned the hard way: --bind means `actions/checkout` runs
# DIRECTLY against this real working tree (not a disposable copy). A
# checkout step with `ref: <sha>` does a raw SHA checkout, which (a)
# discards every uncommitted change and untracked file exactly like a real
# `git checkout --force` + `git clean -fdx`, AND (b) detaches HEAD from
# whatever branch was checked out — pr-governance.yml's first --bind run did
# both: wiped every uncommitted edit in this repo (including this Justfile
# and .secrets) and detached HEAD, deleting the local
# repair/chicago-evidence-boundary-20260829 branch ref in the process
# (recovered only because origin/repair/chicago-evidence-boundary-20260829
# matched exactly — see git reflog / for-each-ref if this ever recurs).
# COMMIT real work before running act-governance. Never add --bind to the
# shared act_flags above.
act_flags_bind := act_flags + " --bind"

act-list:
    act -l {{act_flags}}

# Dry-run parse every real workflow individually (fast, no containers started).
# ggen-ecosystem-sync.yml is workflow_call-only (no push/pull_request/
# workflow_dispatch trigger), so it needs its own event name or act reports
# "Could not find any stages to run" against the default push event.
act-validate:
    #!/usr/bin/env bash
    set -euo pipefail
    for f in .github/workflows/*.yml; do
      echo "== act -n: $f =="
      if [[ "$(basename "$f")" == "ggen-ecosystem-sync.yml" ]]; then
        act workflow_call -n -W "$f" {{act_flags}}
      else
        act -n -W "$f" {{act_flags}}
      fi
    done

act-codeql:
    act push -W .github/workflows/codeql.yml -j analyze-python {{act_flags}}

act-work-portfolio:
    act pull_request -W .github/workflows/work-portfolio-court.yml -j court {{act_flags}}

act-publication-evidence:
    act pull_request -W .github/workflows/publication-evidence-court.yml -j court {{act_flags}}

act-mfact:
    act pull_request -W .github/workflows/mfact-certification.yml -j certify {{act_flags}}

# Needs a crafted event (real base/head SHA pair) for the exact-head git-diff
# check to be meaningful — see .act-events/pr-governance.json (gitignored,
# created by the act-governance-event recipe from real repo history).
act-governance-event:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p .act-events
    head="$(git rev-parse HEAD)"
    base="$(git rev-parse HEAD~3)"
    cat > .act-events/pr-governance.json <<JSON
    {
      "pull_request": {
        "number": 0,
        "base": {"sha": "$base"},
        "head": {"sha": "$head"}
      }
    }
    JSON
    echo "wrote .act-events/pr-governance.json (base=$base head=$head)"

act-governance: act-governance-event
    #!/usr/bin/env bash
    set -euo pipefail
    if ! git diff --quiet || ! git diff --cached --quiet; then
      echo "REFUSED: uncommitted changes present. act-governance uses --bind," >&2
      echo "and pr-governance.yml's checkout step resets this real working tree" >&2
      echo "to the current ref -- commit or stash first (see act_flags_bind's" >&2
      echo "WARNING comment above for exactly what this destroyed once already)." >&2
      exit 1
    fi
    branch="$(git branch --show-current)"
    if [[ -z "$branch" ]]; then
      echo "REFUSED: already in detached HEAD -- reattach to a real branch first" >&2
      echo "(git checkout -B <branch-name>) so this recipe knows what to restore." >&2
      exit 1
    fi
    status=0
    act pull_request -W .github/workflows/pr-governance.yml -j source-authority -e .act-events/pr-governance.json {{act_flags_bind}} || status=$?
    # actions/checkout's `ref: <sha>` step ALWAYS detaches HEAD under --bind
    # (it does a raw SHA checkout), even on a clean tree with no data at
    # risk -- reattach unconditionally so this repo is never left detached
    # after a normal recipe run.
    current="$(git branch --show-current)"
    if [[ -z "$current" ]]; then
      git checkout -B "$branch"
      echo "reattached HEAD to $branch after --bind checkout detached it"
    fi
    exit "$status"

# The generated sync workflow is workflow_call-only; invoke it directly with
# that event name. Never hand-edit this file (see .github/copilot-instructions.md)
# — its one upload-artifact step is an accepted, documented act-only failure
# (Node18/WebCrypto "crypto is not defined"), everything before it is real coverage.
#
# marketplace_sha MUST be passed explicitly, matching the current
# vendor/ggen-marketplace submodule pin (`git submodule status
# vendor/ggen-marketplace`, also recorded in ecosystem.lock.toml) -- the
# workflow's own default input value is a stale snapshot from whenever this
# generated file was last regenerated, and the real-CI callers of this
# reusable workflow (e.g. a release pipeline) always pass the current value
# explicitly rather than relying on that default.
act-sync:
    #!/usr/bin/env bash
    set -euo pipefail
    marketplace_sha="$(git submodule status vendor/ggen-marketplace | awk '{print substr($1,1,40)}' | tr -d '+- ')"
    act workflow_call -W .github/workflows/ggen-ecosystem-sync.yml \
      --input "marketplace_sha=$marketplace_sha" \
      {{act_flags}}

# Dry-run only by default.
act-container-dryrun:
    act -n -W .github/workflows/ggen-ecosystem-container.yml {{act_flags}}

# Real local build (build-only, push:false/load:true under ACT — see the
# workflow's own act-guarded steps). Never pushes to ghcr.io. Uses
# workflow_dispatch (its actual dispatchable trigger) rather than `push`,
# since act's synthetic push event ref wouldn't match this workflow's
# `tags: v[0-9]+.[0-9]+.[0-9]+` filter.
act-container:
    act workflow_dispatch -W .github/workflows/ggen-ecosystem-container.yml --input image_tag=act-local {{act_flags}}

act-all: act-list act-validate act-codeql act-work-portfolio act-publication-evidence act-mfact act-governance act-sync
