# GitHub-native capability, DX, and QoL plane

This document is the capability map for repository-native GitHub affordances in `ggen-ecosystem`. It distinguishes **implemented repository surfaces** from **GitHub account/repository settings** that require separate administrative actuation. A file declaring a feature is not proof that a corresponding GitHub setting is enabled.

## Design law

GitHub is evidence transport, collaboration surface, package/release substrate, and authorized actuation interface. It is not semantic authority merely because a feature exists in the UI.

The repository keeps these boundaries explicit:

- semantic source / admission → ontology, `ggen.toml`, lock and certification contracts;
- manufacture → real GGen path and its declared producers;
- verification → repository courts, dependency review, CodeQL, mfact certification;
- GitHub UX → issue forms, PR templates, CODEOWNERS, labels, Dependabot, Copilot instructions/agents/prompts;
- DO → separately authorized merge, release, package publication, settings mutation, or deployment.

## Implemented repository-native surfaces

| Capability | Surface | DX/QoL effect | Authority |
|---|---|---|---|
| Review routing | `.github/CODEOWNERS` | deterministic reviewer discovery for semantic, generated, security, and release surfaces | review signal only |
| Support routing | `SUPPORT.md` + issue chooser | replaces ambiguous entry points with explicit bug/feature/DX/docs/capability/security routes | observation/intake |
| Bug and feature intake | existing issue forms | captures structured reproduction and desired behavior | observation/intake |
| Documentation intake | `.github/ISSUE_TEMPLATE/documentation.yml` | captures audience, exact stale/missing surface, desired consequence | observation/intake |
| DX/QoL intake | `.github/ISSUE_TEMPLATE/dx_qol.yml` | records end-to-end journey, repeated friction, measurable invariant and falsifier | observation/intake |
| Capability-gap intake | `.github/ISSUE_TEMPLATE/capability_gap.yml` | keeps `UNSUPPORTED` distinct from defects and forces exact evidence | observation/intake |
| PR evidence contract | `.github/PULL_REQUEST_TEMPLATE.md` | exact base/head, authority class, verification, standing, risk, rollback | review signal |
| PR title contract | `.github/workflows/pr-title.yml` | makes GitHub history/search/release-note semantics predictable | VERIFY |
| Path labels | `.github/labeler.yml` + `pr-labeler.yml` | automatically classifies PRs without checking out untrusted PR code | metadata write only |
| Dependency maintenance | `.github/dependabot.yml` | groups Action updates to reduce PR noise while keeping submodule identity movement separate | proposal only |
| Dependency vulnerability review | `.github/workflows/dependency-review.yml` | blocks newly introduced vulnerable dependency deltas | VERIFY |
| Code scanning | `.github/workflows/codeql.yml` | scans Python and GitHub Actions on PR/main and scheduled cadence | VERIFY / security events |
| Repository hygiene | `.github/workflows/repo-hygiene.yml` | one exact-head court for GitHub DX contracts, shell parse, lock and certification tests | VERIFY |
| Local DX court | `scripts/github_dx_check.py` | one command checks required surfaces, exact Action pins, permissions, PR-target fence and routing | VERIFY |
| Reusable bootstrap | `.github/actions/bootstrap-ecosystem/action.yml` | gives workflows/consumers a common exact-subject + courts bootstrap | CONSTRUCT/VERIFY; no push |
| Supply-chain attestation | `.github/workflows/supply-chain-attestation.yml` | reusable GitHub/Sigstore provenance for an already-known immutable subject | attestation write; registry push only when explicitly selected |
| Release-note configuration | `.github/release.yml` | categorizes GitHub-generated release notes | metadata configuration |
| Private vulnerability route | `SECURITY.md` + Security Advisory chooser link | keeps vulnerabilities out of public issues | intake |
| Conduct contract | `CODE_OF_CONDUCT.md` | sets evidence-centered collaboration expectations | governance prose |
| Copilot repository instructions | `.github/copilot-instructions.md` | gives coding agents the manufacturing/authority law by default | guidance only |
| Path-specific Copilot instructions | `.github/instructions/*.instructions.md` | applies generated-output, semantic-source, and certification rules at the edit surface | guidance only |
| Copilot custom agents | `.github/agents/*.agent.md` | specialized manufacturer, certifier, and DX roles with different authority expectations | candidate producer / verifier |
| Copilot prompt files | `.github/prompts/*.prompt.md` | reusable doctor, consumer-journey, and release-crown workflows | guidance only |
| Copilot Cloud Agent setup | `.github/workflows/copilot-setup-steps.yml` | primes exact checkout/submodules and read-only courts in the cloud agent environment | setup / VERIFY |

## Security invariants

Every new third-party GitHub Action is pinned to an exact 40-character commit SHA. `scripts/github_dx_check.py` mechanically rejects mutable Action refs.

Every workflow declares an explicit `permissions` block. The supply-chain attestation workflow starts at `permissions: {}` and grants only per-job permissions required by the selected path.

`pull_request_target` is used only for trusted-base path labeling. That workflow does not checkout or execute pull-request code. The DX court rejects any `pull_request_target` workflow that combines the trigger with checkout or a `run:` step.

Dependency Review and CodeQL are independent security sensors. Neither may promote release standing merely because its workflow passes.

## Copilot / agent ergonomics

The repository exposes one global instruction set plus narrower path-specific contracts:

- generated workflow reviews must repair source and regenerate rather than patch output;
- semantic/control files preserve admission and exact identity correspondence;
- certification remains VERIFY-only.

Custom agents make the role separation visible to the developer: the manufacturer may edit lawful semantic surfaces, the certifier is intentionally read-only, and the DX specialist optimizes GitHub journeys without granting itself release authority.

Prompt files provide reproducible reusable tasks instead of relying on remembered chat phrasing:

- `doctor.prompt.md` — exact-head read-only diagnosis;
- `consumer-journey.prompt.md` — stranger-path/customer-journey evaluation;
- `release-crown.prompt.md` — exact publication → fresh pull → sync → receipt → replay → certification chain.

## Operator surface

Run:

```bash
just github-dx
just github-dx-json
```

or directly:

```bash
python3 scripts/github_dx_check.py --root .
python3 scripts/github_dx_check.py --root . --json
```

The court is read-only. A failure names the GitHub contract that drifted; it does not repair or publish anything.

## Settings-only / external GitHub capabilities

These capabilities are useful but are **not represented as enabled merely by repository files**. They require GitHub repository/account administration or another actuation surface and must be observed after actuation before being claimed active.

| Capability | Observed state during this implementation | Why not silently changed here |
|---|---|---|
| Repository rulesets / branch protection | no rulesets observed | current connector exposes ruleset reads but not create/update authority |
| Discussions | disabled | repository setting; issue chooser was corrected so it no longer sends users to a dead URL |
| Auto-merge | disabled | repository setting; current connector does not expose repository-settings mutation |
| Update branch button | disabled | repository setting; current connector does not expose repository-settings mutation |
| GitHub Pages | not established by this change | requires a deployment/pages configuration decision; not needed for the manufacturing rail |
| Secret scanning / push protection | not asserted | security-setting state was not exposed as a writable/verified control in this session |
| Dependabot security updates / alerts | not asserted | settings-level state is distinct from the checked-in Dependabot version-update configuration |
| Required status checks | not asserted | should be selected only after exact workflow names are stable and a ruleset/branch-protection write surface exists |

The absence of a settings mutation is not a reason to encode a fake equivalent in workflow YAML. Preserve the option until the authorized administrative surface is available.

## Deliberate exclusions

An automatic stale/close workflow is intentionally not installed. In this repository, inactivity is not sufficient evidence that work is obsolete, and automatic closure would conflict with the factory's learning/innovation and backlog-completion model. GitHub-native capability maximalism means maximizing **lawful useful options**, not enabling every Marketplace Action indiscriminately.

No workflow automatically merges Dependabot, submodule, generated-workflow, or release changes. Those changes can alter producer identity or standing and require exact-subject verification.

## Acceptance

The repository-native GitHub plane is coherent when `scripts/github_dx_check.py` passes on the exact head and all PR-triggered workflows that apply to the change complete successfully. That proves the checked-in capability contracts are internally consistent. It does **not** prove settings-only features are enabled or that the currently blocked GHCR release crown has been restored.
