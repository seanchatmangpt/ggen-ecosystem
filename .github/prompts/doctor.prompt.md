---
description: Diagnose the current ggen-ecosystem exact head without mutating it.
---

Resolve the current exact HEAD and perform a read-only ecosystem diagnosis.

1. Read `AGENTS.md`, `docs/CURRENT-RELEASE-STANDING.md`, `ecosystem.lock.toml`, and the relevant receipt/certification sources.
2. Run `just doctor` if available, otherwise `bash scripts/doctor.sh`; also run `python3 scripts/github_dx_check.py --root .` for GitHub-native surfaces.
3. Run `just explain` and `just next` when they add information.
4. Distinguish observed execution, historical evidence, inference, and unsupported claims.
5. Return the narrowest high-information next transition and the exact standing supported by the evidence.

Do not repair, publish, merge, or edit generated projections during this prompt.
