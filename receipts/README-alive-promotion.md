# ALIVE promotion rule for v26.9.10

The committed `release-v26.9.10-container.json` remains historical release evidence. It MUST NOT be edited to claim `ALIVE` merely because a newer candidate passes CI.

A candidate earns exact-head `ALIVE` only when the `Real Chicago Consumer Matrix` workflow, on that exact candidate SHA, observes all of the following in one run:

1. recursive submodules checked out at the superproject-recorded commits;
2. immutable `v26.9.10` container digest pulled successfully;
3. network-isolated `ggen --version` from that digest equals `ggen 26.9.9`;
4. `tests/test_container_smoke.sh` exits zero against that exact immutable image;
5. `scripts/doctor.sh --json` reports every emitted gate `ALIVE`;
6. `scripts/dod_engine.py` binds its subject to the exact candidate SHA and reports `STATUS: ALIVE`;
7. the committed historical release receipt remains schema-valid;
8. mfact certification executes without weakening its `VERIFY` authority ceiling.

The workflow artifact is the replayable exact-head verification receipt. Historical release identity and exact-head qualification are deliberately separate subjects.
