#!/bin/bash
# SessionStart hook for ggen-ecosystem (Claude Code on the web only).
#
# Prepares the environment for the repo's Docker-based verification path
# (`make image`, `just chicago`, tests/test_container_smoke.sh,
# scripts/doctor.sh gates 4/11) and for the `just`/`make` recipes documented
# in CLAUDE.md and README.md:
#
#   1. Vendored git submodules (vendor/ggen, vendor/ggen-marketplace,
#      vendor/autofde-lab, vendor/beam4pm, vendor/ggen_igniter) -- a plain
#      clone does not populate them, and almost everything below depends on
#      them being checked out (Dockerfile COPY steps, ggen sync run,
#      doctor.sh gate 1).
#   2. The `just` command runner -- not preinstalled in this sandbox image;
#      CLAUDE.md: "Prefer just recipes for anything beyond basic setup."
#   3. A reachable Docker daemon -- not running by default here (see below).
#
# Remote (Claude Code on the web) only: a local checkout already has its own
# Docker Desktop/Engine and a submodule tree populated by the developer's own
# workflow, so this hook is a deliberate no-op outside the remote sandbox.
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

log() { echo "[session-start] $*"; }

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}" || exit 0

# --- 1. vendored submodules -------------------------------------------------
# Idempotent: a no-op when everything is already checked out at the recorded
# SHA (scripts/doctor.sh gate 1 reports the same thing as ALIVE/BLOCKED).
log "initializing git submodules..."
if git submodule update --init --recursive; then
  log "submodules OK"
else
  log "WARNING: git submodule update --init --recursive failed (see above) -- vendor/* may be incomplete"
fi

# --- 2. `just` command runner ------------------------------------------------
if command -v just >/dev/null 2>&1; then
  log "just already present: $(just --version)"
else
  log "installing just..."
  if apt-get install -y just >/dev/null 2>&1 || (apt-get update >/dev/null 2>&1 && apt-get install -y just >/dev/null 2>&1); then
    log "just installed: $(just --version)"
  else
    log "WARNING: could not install just -- Justfile recipes will be unavailable; Makefile targets still work"
  fi
fi

# --- 3. Docker daemon ---------------------------------------------------------
# Real, observed root cause (not guessed): this sandbox's container drops
# CAP_SYS_RESOURCE from the bounding set (`capsh --print` shows
# "Current IAB: !cap_sys_resource"). The distro's own /etc/init.d/docker
# unconditionally runs `ulimit -Hn 524288` before starting dockerd, which
# needs exactly that capability to raise a hard limit -- so
# `service docker start` fails closed with "Operation not permitted" before
# dockerd ever runs, and docker info reports "no such file or directory" on
# /var/run/docker.sock forever after. Confirmed by reproducing both the
# init-script failure and the working fallback by hand before writing this.
#
# Fix: try the normal path first (works unmodified in sandboxes that keep
# CAP_SYS_RESOURCE); fall back to invoking dockerd directly, which needs no
# ulimit change beyond this container's own default (already 20000 open
# files -- ample for local image builds/runs).
if docker info >/dev/null 2>&1; then
  log "docker daemon already running"
else
  log "starting docker daemon..."
  service docker start >/tmp/session-start-dockerd-init.log 2>&1

  if ! docker info >/dev/null 2>&1; then
    log "service docker start did not bring the daemon up (see /tmp/session-start-dockerd-init.log) -- starting dockerd directly"
    mkdir -p /var/log
    nohup dockerd --pidfile /var/run/docker-manual.pid >/var/log/dockerd-manual.log 2>&1 &
    disown

    for _ in $(seq 1 30); do
      docker info >/dev/null 2>&1 && break
      sleep 1
    done
  fi

  if docker info >/dev/null 2>&1; then
    log "docker daemon is up ($(docker version --format '{{.Server.Version}}' 2>/dev/null))"
  else
    log "WARNING: docker daemon still not reachable after both start attempts -- Docker-dependent commands will report BLOCKED (see /var/log/dockerd-manual.log)"
  fi
fi

log "done"
exit 0
