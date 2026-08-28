# Missing python runtime marker — UNSUPPORTED (gap)

The composed container (Section 16, Dockerfile) is expected to carry a working `python3`
runtime (used by `ex:admit` and `ex:evidence`'s inline `python3 - <<'PY'` blocks in
`ontology.ttl`, which run *inside* the composed image per Section 18.2). No local script
in this repo (`scripts/doctor.sh`, `ontology.ttl`) currently asserts "the built image has a
`python3` marker/binary at a known path" independent of actually running a container.

Per the orthogonal-swarm constraint on this task, no container may be built or run here to
manufacture and probe a real fixture image, so this falsifier cannot be exercised for real
right now.

**Fixture**: a placeholder Dockerfile-fragment showing what a broken multi-stage COPY would
look like (final stage missing `python3`) — see `Dockerfile.fragment` in this directory. It
is illustrative only; it is not run against a real build.

**Expected typed refusal (not yet implemented anywhere)**: something like
`REFUSED[CONTAINER_PYTHON_RUNTIME_MISSING]`, which `scripts/doctor.sh` could add as a new
check-12 that runs `docker run --rm <image> python3 --version` once an image tag is real
(today `ecosystem.lock.toml [container].tag = "UNKNOWN-TODO-not-yet-built"`, so check-11 in
doctor.sh already reports `BLOCKED[IMAGE_NOT_YET_BUILT]` upstream of this check ever running).

**Verdict for this falsifier**: `UNSUPPORTED` — honestly a gap, not a false pass.
