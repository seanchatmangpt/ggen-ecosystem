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
# --bind: bind the real working directory into the job container instead of
# copying it. Required for correctness whenever a step does
# docker-outside-of-docker (bind-mounts a path it just wrote into a SIBLING
# container via the host daemon, e.g. tests/chicago_consumer.sh's
# `docker run -v "$WORK_ROOT/consumer-a:/workspace" ...`) — under copy mode,
# that path only exists inside this job container's private overlay copy,
# invisible to the host daemon, which silently bind-mounts an empty
# directory instead (observed real failure: "ggen.toml not found at
# /workspace/ggen.toml" even though the fixture was genuinely copied in).
#
# WARNING: --bind means `actions/checkout` operates DIRECTLY on this real
# working tree (not a disposable copy) — a checkout step that resets to a
# ref will discard uncommitted changes and untracked files exactly like a
# real `git checkout --force` + `git clean -fdx` would. Commit (or stash)
# real work before running any --bind recipe below. (Learned the hard way:
# act-governance's first --bind run wiped every uncommitted edit in this
# repo, including .secrets, because pr-governance.yml's checkout step resets
# to `github.sha` == current HEAD.)
act_flags := "--bind --container-architecture " + act_arch + " --container-daemon-socket " + act_container_socket + " --secret-file .secrets"

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
    act pull_request -W .github/workflows/pr-governance.yml -j source-authority -e .act-events/pr-governance.json {{act_flags}}

# The generated sync workflow is workflow_call-only; invoke it directly with
# that event name. Never hand-edit this file (see .github/copilot-instructions.md)
# — its one upload-artifact step is an accepted, documented act-only failure
# (Node18/WebCrypto "crypto is not defined"), everything before it is real coverage.
act-sync:
    act workflow_call -W .github/workflows/ggen-ecosystem-sync.yml {{act_flags}}

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
