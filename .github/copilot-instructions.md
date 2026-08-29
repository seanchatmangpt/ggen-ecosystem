# GitHub Copilot repository instructions

Treat this repository as the canonical composition root of the ggen ecosystem.

- Read `AGENTS.md` before proposing changes.
- Ontology, admission, lock, and marketplace-pack inputs outrank generated projections.
- Never hand-edit `.github/workflows/ggen-ecosystem-sync.yml`, `generated/`, `consumer/`, or `.ggen-v2/`; repair the semantic source and regenerate through the documented GGen rail.
- Keep SELECT, CONSTRUCT, and DO separate. Hooks manufacture intents only; they do not actuate.
- Use only the standing vocabulary in `AGENTS.md`, including typed `REFUSED[...]` results.
- Preserve exact repository/ref/SHA identity in verification evidence.
- Prefer `just doctor` for orientation, then the narrowest relevant verifier, and `just certify-test` for certification-contract changes.
- Do not weaken tests, bypass admission, fabricate receipts, or treat GitHub status metadata as execution proof.
- GitHub Actions should use least-privilege `permissions`, bounded `timeout-minutes`, concurrency cancellation where safe, and `persist-credentials: false` for read-only checkout jobs.
