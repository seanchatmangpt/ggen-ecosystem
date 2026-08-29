# Justfile — Canonical Operator Surface for GGen Ecosystem TPS + DfCM Plant

# Default recipe: print help / recipes
default:
    @just --list

# Canonical plant-wide qualification court (12 courts, 59+ real assertions, 0 mocks)
chicago:
    @tests/test_container_smoke.sh

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

# Real wall-clock timing benchmark of `ggen sync run --dry-run` (20 runs, min/max/mean/p50/p95)
bench:
    @bash scripts/benchmark.sh --runs 20

# Real concurrency stress test: N parallel `ggen sync run` processes, asserts identical
# graph_hash_hex across all of them and that ggen.lock stays untouched under --dry-run
stress:
    @bash scripts/stress_test.sh --parallel 16
