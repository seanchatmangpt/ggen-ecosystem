# GitHub Copilot instructions

Treat this repository as a governed software-manufacturing composition root, not a conventional hand-coded application.

Read `AGENTS.md`, `CLAUDE.md`, `docs/STANDING.md`, and `docs/CURRENT-RELEASE-STANDING.md` before making standing, release, or generated-artifact claims.

## Non-negotiable boundaries

- Ontology/admission/profile sources outrank generated projections.
- `.github/workflows/ggen-ecosystem-sync.yml` and `.github/workflows/ggen-ecosystem-container.yml` are GGen-manufactured projections. Do not hand-edit them as a final solution; repair their semantic source/template and regenerate through the declared GGen path.
- `SELECT`, `CONSTRUCT`, `VERIFY`, and `DO` are separate authorities. A diagnostic, review, workflow definition, or model output never implies actuation authority.
- Historical evidence cannot certify a newer exact head. Resolve the current SHA and bind claims to it.
- Use only the standing vocabulary documented by the repository and preserve typed failures.
- External GitHub Actions must be pinned to exact 40-character commit SHAs. New workflows must declare explicit least-privilege permissions.
- Never combine `pull_request_target` with checkout or execution of untrusted pull-request code.

## Preferred workflow

1. Resolve the exact subject and read the relevant semantic/control sources.
2. Run the cheapest read-only diagnostics (`just doctor`, `just next`, `just explain`, `just github-dx`) before proposing mutation.
3. Make the smallest semantic input change that preserves the requested option space; do not patch generated consequences directly.
4. Run narrow falsifiers first, then the broader relevant court.
5. Report exact commands, exact SHAs, observed evidence, and scoped standing.

For GitHub-native DX changes, run `python3 scripts/github_dx_check.py --root .` and keep workflow permissions/pins mechanically valid.
