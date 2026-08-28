# Required Falsifiers — Fixtures

Falsifier fixtures for each admission-refusal case named in
`docs/PRD-ARD-v26.8.28.md` Section 34 ("Required Falsifiers"). Each subdirectory is a
minimal, self-contained fixture (a copy of `ecosystem.lock.toml` with one field
deliberately wrong, a synthetic status line, or a directory missing an expected file) plus
a `run-check.sh` that executes the real local check logic against it, where one exists.

**Nothing here touches the real `vendor/` submodules or the real `ecosystem.lock.toml`.**
Every fixture is a standalone copy under this directory. Where a check needs to compare
against real state (e.g. the actual `vendor/ggen`/`vendor/ggen-marketplace` HEAD), it reads
that state read-only via `git rev-parse`/`git ls-files` — it never writes to `vendor/`.

Run all runnable checks:

```bash
for d in tests/fixtures/falsifiers/*/run-check.sh; do echo "== $d =="; "$d"; echo; done
```

## Table

| # | Falsifier | Fixture | Real check exercised | Expected typed output | Result |
|---|-----------|---------|----------------------|------------------------|--------|
| 1 | Wrong GGen commit | `01-wrong-ggen-commit/ecosystem.lock.toml` (`ggen_commit` set to `0000…dead`) | Adapted from `scripts/doctor.sh` check-7 (`7-gitlink-exact`)/check-6 pattern: compare recorded `[submodules].ggen_commit` against real (untouched) `vendor/ggen` `HEAD` via `git rev-parse` | `REFUSED[GGEN_SUBMODULE_DRIFT]:<actual>:<recorded>` | **Confirmed** — ran for real, fired exactly as expected |
| 2 | Wrong marketplace commit | `02-wrong-marketplace-commit/ecosystem.lock.toml` (`ggen_marketplace_commit` set to `1111…feed`) | `scripts/doctor.sh` check-6 (`6-marketplace-pin`) logic, pointed at the fixture lock file, compared against the real (untouched) `vendor/ggen-marketplace` `HEAD` | `REFUSED[MARKETPLACE_SUBMODULE_DRIFT]:<actual>:<recorded>` | **Confirmed** — ran for real, fired exactly as expected |
| 3 | Dirty/mismatched gitlink | `03-dirty-mismatched-gitlink/submodule-status.txt` (synthetic `git submodule status` output: one `-` not-initialized line, one `+` mismatched line) | `scripts/doctor.sh` check-1 (`1-submodules`) prefix-parsing loop, run verbatim against the synthetic status text (real `vendor/` left untouched per the no-touch-vendor constraint) | `REFUSED[SUBMODULE_NOT_INITIALIZED]:…` and `REFUSED[SUBMODULE_GITLINK_MISMATCH]:…` | **Confirmed** — ran for real, fired exactly as expected |
| 4 | Missing marketplace | `04-missing-marketplace/fixture-root/` (has `ecosystem.lock.toml`, deliberately no `vendor/ggen-marketplace/` directory) | `scripts/doctor.sh` check-6 directory-existence guard, run against the fixture root | `REFUSED[MARKETPLACE_SUBMODULE_MISSING]:vendor/ggen-marketplace` | **Confirmed** — ran for real, fired exactly as expected |
| 5 | Missing python runtime marker | `05-missing-python-runtime-marker/Dockerfile.fragment` (illustrative final-stage COPY omitting `python3`) | None — this is a container-internal fact (Section 16/18.2's `python3` runtime, used by `ex:admit`/`ex:evidence`'s inline `python3` blocks) that only a running image can confirm, and no image may be built/run here (orthogonal-swarm Docker constraint) | `REFUSED[CONTAINER_PYTHON_RUNTIME_MISSING]` (not yet implemented anywhere) | **UNSUPPORTED** — honest gap, not exercised |
| 6 | Missing GGen executable marker | `06-missing-ggen-executable-marker/run-check.sh` | Host-level analog of `scripts/doctor.sh` check-2 (`2-ggen-binary`), run with `PATH=/usr/bin:/bin` so `command -v ggen` fails the same way it would if the image's final stage omitted the `ggen` binary | `REFUSED[GGEN_EXECUTABLE_NOT_FOUND]:PATH=/usr/bin:/bin` | **Confirmed** (host-level analog) — ran for real; the container-internal marker itself is **UNSUPPORTED** (no image to probe) |
| 7 | Wrong image digest format | `07-wrong-image-digest-format/ecosystem.lock.toml` (`[container].digest = "not-a-real-digest-12345"`, fails `^sha256:[0-9a-f]{64}$`) | None — `scripts/doctor.sh` checks 4/11 test image *presence*, not digest *format*; no format validator exists in `ontology.ttl`'s `ex:admit`/`ex:evidence` either | `REFUSED[INVALID_IMAGE_DIGEST_FORMAT]` (not yet implemented anywhere) | **UNSUPPORTED** — honest gap, not exercised (no new checker invented, per task scope) |
| 8 | Invalid working directory | `08-invalid-working-directory/fixture-root/` + `run-check.sh` (`GGEN_WORKING_DIRECTORY=../../../etc`) | `ontology.ttl`'s `ex:admit` step's inline python workspace-escape guard, extracted **verbatim** and run for real against the fixture | `REFUSED[WORKING_DIRECTORY_ESCAPES_WORKSPACE]` | **Confirmed** — ran for real, fired exactly as expected |
| 9 | Generated artifact drift | `09-generated-artifact-drift/ggen-ecosystem-sync.yml.tampered` (a copy of the real generated workflow file with one appended line) | `scripts/doctor.sh` check-9 (`9-workflow-drift`) mechanism: diff a tampered copy of a `ggen`-generated file against the real committed file | `REFUSED[GENERATED_ARTIFACT_DRIFT]:ggen-ecosystem-sync.yml (fixture differs from committed generated file)` | **Confirmed** — ran for real, fired exactly as expected |
| 10 | Missing receipt | `10-missing-receipt/fixture-root/receipts/` (empty directory) | `scripts/doctor.sh` check-10 (`10-container-receipt`) `find` query, pointed at the empty fixture `receipts/` | `REFUSED[RECEIPT_MISSING]:v26.8.28 container receipt not found under receipts/` | **Confirmed** — ran for real, fired exactly as expected |

## Summary

- **8 of 10** falsifiers have a real local check (either an existing `scripts/doctor.sh`
  check adapted to point at the fixture, or `ontology.ttl`'s `ex:admit` inline python guard
  extracted verbatim) and were **actually run** against their fixture, producing the exact
  typed refusal expected.
- **2 of 10** (missing python runtime marker in the image, wrong image digest format) are
  honestly marked **UNSUPPORTED**: both require either a running container (blocked by the
  orthogonal-swarm Docker constraint on this task) or a format-validation check that does
  not exist yet anywhere in this repo. These are real gaps for a future gate
  (`scripts/doctor.sh` check-12/13 candidates), not silently assumed covered.

## See Also

- `docs/PRD-ARD-v26.8.28.md` Section 34 (Required Falsifiers), Section 22 (Admission
  Architecture), Section 17 (Container Identity)
- `scripts/doctor.sh` — the standing health-check script whose check logic several fixtures
  adapt
- `ontology.ttl`'s `ex:admit`/`ex:evidence` steps — the real admission/evidence-binding
  inline shell+python this repo's CI actually runs
