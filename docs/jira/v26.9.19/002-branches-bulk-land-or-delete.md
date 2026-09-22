# ggen-ecosystem: triage 36 PR-less unmerged remote branches

- Standing: OPEN
- Created: 2026-09-19 (v26.9.19 gh survey wave)
- Source: origin branches not merged into `main` with no open PR
- Evidence: `git branch -r --no-merged origin/main`: automation/crown-33602384909 automation/ws1-20260829-0002-alive-engine-v1 automation/ws5-ggen-sync-20260828-1348 automation/ws5-ggen-sync-50 chore/autofde-lab-pin-sync claude/ecosystem-docker-setup-4cfe41 claude/ultracode-branch-merge-amiyd7 demo/ggen-feature-proof-v26.9.1 docs/add-changelog docs/capture-v26.9.15-review-and-crown-receipt docs/fix-replay-staleness docs/fix-transport-staleness docs/governance-md docs/third-party-licenses feat/autonomics-4th-safe-action feat/closure-kernel-20260908 feat/cosign-keyless-signing feat/full-github-ecosystem-closure feat/github-dx-qol-max feat/github-dx-qol-max-v2 feat/github-max-dx-qol-20260829 feat/trivy-container-scan fix/certify-tests-init fix/container-lock-stale-blocked-standing fix/dod-reconcile-doctor-count fix/ggen-toml-stale-marketplace-sha-comment fix/launch-ready-customer-path fix/mfact-certification-historical-drift fix/pragprog-tps-hardcoded-marketplace-sha fix/scripts-lint plan/v26.9.1-jira preserve/detached-test-fixes-20260917 repair/publication-evidence-contract-v2 repair/publication-evidence-current-main validate/github-docker-main-v1 worktree-wf_eed2124b-93b-1

## Work to complete
- Triage each branch: land (open a PR) or delete (`git push origin --delete <branch>`). Work in batches; record decisions in History.

## Acceptance
- `git branch -r --no-merged origin/main` is empty after `git fetch --prune`.

## History
- 2026-09-19 | OPEN | survey found 36 PR-less branches | full list above | triage pending
