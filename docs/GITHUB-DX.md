# GitHub-native capability, DX, and QoL plane

This document maps repository-native GitHub affordances in `ggen-ecosystem` and distinguishes them from repository/account settings that require separate administrative actuation. A checked-in file is never, by itself, proof that the matching GitHub setting is enabled.

## Design law

GitHub is evidence transport, collaboration surface, package/release substrate, agent environment, and authorized actuation interface. It is not semantic authority merely because a feature exists in the UI.

The repository keeps these boundaries explicit:

- semantic source / admission → ontology, `ggen.toml`, lock and certification contracts;
- manufacture → real GGen path and its declared producers;
- verification → repository courts, capability probes, CodeQL, mfact certification;
- GitHub UX → issue forms, Discussions, PR templates, CODEOWNERS, labels, Dependabot, Codespaces/devcontainer, citation metadata, Copilot instructions/agents/prompts;
- DO → separately authorized merge, release, package publication, settings mutation, or deployment.

## Implemented repository-native surfaces

| Capability | Surface | DX/QoL effect | Authority |
|---|---|---|---|
| Codespaces / cloud dev bootstrap | `.devcontainer/devcontainer.json` | gives GitHub-hosted development a declared environment instead of tribal setup knowledge | environment setup |
| Review routing | `.github/CODEOWNERS` | deterministic reviewer discovery for semantic, generated, security, and release surfaces | review signal only |
| Support routing | `SUPPORT.md` + issue chooser | separates exploratory Discussion, bugs, features, DX, docs, capability gaps, release standing, and private security reports | observation/intake |
| Incident intake | `.github/ISSUE_TEMPLATE/incident.yml` | captures production/release incidents as a distinct workflow | observation/intake |
| Documentation intake | `.github/ISSUE_TEMPLATE/documentation.yml` | captures audience, exact stale/missing surface, and desired consequence | observation/intake |
| DX/QoL intake | `.github/ISSUE_TEMPLATE/dx_qol.yml` | records end-to-end journey, repeated friction, measurable invariant, and falsifier | observation/intake |
| Capability-gap intake | `.github/ISSUE_TEMPLATE/capability_gap.yml` | keeps `UNSUPPORTED` distinct from a defect and forces exact evidence | observation/intake |
| PR evidence contract | `.github/PULL_REQUEST_TEMPLATE.md` | exact base/head, authority class, verification, standing, risk, and rollback | review signal |
| PR authority court | `.github/workflows/pr-governance.yml` | parses control surfaces and refuses direct generated-workflow edits without source authority | VERIFY |
| PR title contract | `.github/workflows/pr-title.yml` | makes GitHub history/search/release-note semantics predictable | VERIFY |
| Path labels | `.github/labeler.yml` + `pr-labeler.yml` | automatically classifies PRs without checking out untrusted PR code | metadata write only |
| Dependency maintenance | `.github/dependabot.yml` | groups Action updates to reduce PR noise while keeping submodule identity movement separate | proposal only |
| Dependency Review capability | `.github/workflows/dependency-review.yml` | probes GitHub Dependency Graph; enforces vulnerability-delta review only when the repository capability exists | VERIFY / typed `UNSUPPORTED` sensor |
| Code scanning | `.github/workflows/codeql.yml` | scans Python and GitHub Actions on PR/main plus scheduled cadence | VERIFY / security events |
| Repository hygiene | `.github/workflows/repo-hygiene.yml` | exact-head court for GitHub contracts, shell parse, lock correspondence, and certification tests | VERIFY |
| Local DX court | `scripts/github_dx_check.py` | one command checks required surfaces, exact Action pins, permissions, PR-target fencing, and issue/security routing | VERIFY |
| Reusable bootstrap | `.github/actions/bootstrap-ecosystem/action.yml` | common exact-subject/submodule/court bootstrap for workflows and consumers | CONSTRUCT/VERIFY; no push |
| Supply-chain attestation | `.github/workflows/supply-chain-attestation.yml` | reusable GitHub/Sigstore provenance for an already-known immutable subject | attestation write; registry push only when explicitly selected |
| Release-note configuration | `.github/release.yml` | categorizes GitHub-generated release notes | metadata configuration |
| Citation metadata | `CITATION.cff` | exposes a GitHub-native citation surface for research/reuse | metadata |
| Private vulnerability route | `SECURITY.md` + Security Advisory chooser | keeps vulnerabilities out of public issues | intake |
| Conduct contract | `CODE_OF_CONDUCT.md` | sets collaboration expectations | governance prose |
| Copilot repository instructions | `.github/copilot-instructions.md` | gives coding agents manufacturing/authority law by default | guidance only |
| Path-specific Copilot instructions | `.github/instructions/*.instructions.md` | applies generated-output, semantic-source, and certification rules at edit time | guidance only |
| Copilot custom agents | `.github/agents/*.agent.md` | specialized Manufacturer, Certifier, and GitHub DX roles | candidate producer / verifier |
| Copilot prompt files | `.github/prompts/*.prompt.md` | reusable Doctor, Consumer Journey, and Release Crown workflows | guidance only |
| Copilot Cloud Agent setup | `.github/workflows/copilot-setup-steps.yml` | primes exact checkout/submodules and read-only courts in the cloud agent environment | setup / VERIFY |

## Hosted evidence from PR #159

The capability plane is being falsified on GitHub-hosted runners rather than accepted from YAML inspection alone.

Observed on the PR exact-head lineage during implementation:

- Repository Hygiene passed its real GitHub-hosted run.
- PR Governance passed after replacing the concurrently introduced mutable `actions/checkout@v4` reference with an exact commit pin and expanding the generated-projection fence to both ecosystem-generated workflows.
- PR Title passed against the actual PR title.
- CodeQL successfully initialized and analyzed GitHub Actions; Python analysis also completed successfully on the preceding exact head before final documentation reconciliation.
- Copilot Setup Steps successfully checked out recursive ecosystem submodules and ran the repository courts on the preceding exact head before final documentation reconciliation.
- Dependency Review first failed with GitHub's explicit `Dependency review is not supported on this repository` response. The workflow now probes the Dependency Graph API first: when unavailable it records `UNSUPPORTED[DEPENDENCY_GRAPH_DISABLED]` and skips the vulnerability-delta action; when available, the real Dependency Review action remains a hard gate.

Every final-head workflow must still complete successfully after the last commit; earlier runs remain historical evidence, not final-head proof.

## Security invariants

Every new or modified third-party GitHub Action is pinned to an exact 40-character commit SHA. `scripts/github_dx_check.py` mechanically rejects mutable Action refs.

Every workflow declares an explicit `permissions` block. The supply-chain attestation workflow starts at `permissions: {}` and grants only per-job permissions required by the selected path.

`pull_request_target` is used only for trusted-base path labeling. That workflow does not checkout or execute pull-request code. The DX court rejects any `pull_request_target` workflow that combines the trigger with checkout or a `run:` step.

Dependency Review and CodeQL are independent security sensors. Neither may promote release standing merely because its workflow passes.

## Copilot / agent ergonomics

The repository exposes one global instruction set plus narrower path-specific contracts:

- generated workflow reviews repair source and regenerate rather than patch output;
- semantic/control files preserve admission and exact identity correspondence;
- certification remains VERIFY-only.

Custom agents make role separation explicit: the Manufacturer may edit lawful semantic surfaces, the Certifier is intentionally read-only, and the DX Specialist optimizes GitHub journeys without granting itself release authority.

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

## Live GitHub settings / externally actuated capabilities

These states are observed separately from checked-in repository files. They can change independently and must be re-read before relying on them.

| Capability | Latest observed state in this implementation | Boundary |
|---|---|---|
| Discussions | **enabled** after a concurrent settings change during this run | issue chooser now exposes Discussions for exploratory design questions |
| Repository topics | **populated** (`code-generation`, `container`, `devops`, `dfcm`, `ggen`, `github-actions`, `rdf`, `semantic-web`, `shacl`) | discoverability metadata; not semantic admission |
| Dependency Graph | **disabled / unavailable to Dependency Review** in the real PR run | requires repository security-analysis setting; workflow records typed `UNSUPPORTED` until enabled |
| Repository rulesets / branch protection | no rulesets observed at the earlier census | current connector exposes ruleset reads but not create/update authority |
| Auto-merge | disabled | repository setting; current connector does not expose repository-settings mutation |
| Update branch button | disabled | repository setting; current connector does not expose repository-settings mutation |
| GitHub Pages | not established by this change | requires a Pages/deployment decision; not needed for the manufacturing rail |
| Secret scanning / push protection | not asserted | security-setting state was not exposed as a writable/verified control in this session |
| Dependabot security updates / alerts | not asserted | settings-level state is distinct from checked-in Dependabot version-update configuration |
| Required status checks | not asserted | select only after workflow names are stable and an authorized ruleset/branch-protection write surface exists |
| Codespaces prebuilds | not asserted | `.devcontainer` provides the environment contract; prebuild enablement is a separate settings actuation |

The absence of a settings mutation is not a reason to encode a fake equivalent in workflow YAML. Preserve the option until an authorized administrative surface is available.

## Deliberate exclusions

An automatic stale/close workflow is intentionally not installed. In this repository, inactivity is not sufficient evidence that work is obsolete, and automatic closure conflicts with the factory's learning/innovation and backlog-completion model. GitHub-native capability maximalism means maximizing **lawful useful options**, not enabling every Marketplace Action indiscriminately.

No workflow automatically merges Dependabot, submodule, generated-workflow, or release changes. Those changes can alter producer identity or standing and require exact-subject verification.

## Acceptance

The checked-in GitHub plane is coherent when `scripts/github_dx_check.py` passes on the exact head and all applicable PR-triggered workflows complete successfully on that same head. This proves repository-native contracts are internally coherent. It does **not** prove settings-only features are enabled, and it does not promote the independently governed release/capsule standing.
