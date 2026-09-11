# ALIVE promotion rule for v26.9.10

The committed `release-v26.9.10-container.json` remains historical release evidence. It MUST NOT be edited to claim `ALIVE` merely because a newer candidate passes CI.

A candidate earns exact-head `ALIVE` only when the `Real Chicago Consumer Matrix` workflow, on that exact candidate SHA, observes all of the following in one run:

1. recursive top-level submodules checked out at the superproject-recorded commits;
2. immutable `v26.9.10` release digest independently pulled and its network-isolated `ggen --version` observed as `ggen 26.9.9`;
3. a composed container built from the exact candidate SHA;
4. the candidate image proves AutoFDE's admitted `wrapt.lru_cache` runtime dependency;
5. `tests/test_container_smoke.sh` exits zero against that exact candidate image;
6. `scripts/doctor.sh --json` reports every emitted gate `ALIVE`;
7. `scripts/dod_engine.py` binds its subject to the exact candidate SHA and reports `STATUS: ALIVE`;
8. the historical release receipt remains schema-valid and mfact executes without weakening its `VERIFY` authority ceiling.

Historical immutable-release identity and exact-head qualification are deliberately separate subjects. Exact-head workflow execution is the replayable evidence; it does not rewrite the historical release receipt or grant publication/merge authority.
