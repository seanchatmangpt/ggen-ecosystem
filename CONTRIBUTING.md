# Contributing to ggen-ecosystem

This repository is a governed semantic software-manufacturing composition root rather than a conventional hand-coded application. Read `AGENTS.md`, `CLAUDE.md`, `docs/STANDING.md`, and `docs/CURRENT-RELEASE-STANDING.md` before changing authority-bearing, generated, or release surfaces.

## Choose the right entry point

Use `SUPPORT.md` and the GitHub issue chooser rather than a blank issue:

- open-ended architecture/design/ecosystem question → GitHub Discussions;
- reproducible defect → Bug Report;
- desired capability → Feature Request or Capability Gap;
- repeated contributor/operator friction → Developer Experience / QoL;
- missing/stale/contradictory docs → Documentation Gap;
- security vulnerability → private GitHub Security Advisory, never a public issue.

GitHub Discussions are currently enabled; use them for exploratory conversation that does not yet have a falsifiable issue/PR acceptance contract.

## Before you start

1. **Resolve the exact base.** Record the current `main` SHA before mutation. A branch name is a moving reference; evidence is bound to commits.
2. **Clone with submodules when the task needs the composed ecosystem.** `vendor/ggen`, `vendor/ggen-marketplace`, and `vendor/autofde-lab` are real gitlinks. Use `git clone --recurse-submodules ...` or `git submodule update --init --recursive`.
3. **Never hand-edit GGen-generated projections.** `.github/workflows/ggen-ecosystem-sync.yml` and `.github/workflows/ggen-ecosystem-container.yml` are manufactured consequences. Repair `ontology.ttl` or the admitted Marketplace producer/template and regenerate with the real GGen path.
4. **Use the operator surface.** `just --list` exposes the repository’s supported commands, including `doctor`, `github-dx`, `certify`, `chicago`, `dod`, `replay`, `falsify`, `bench`, and `stress`.
5. **Keep GitHub workflows least-privilege.** Every workflow must declare explicit permissions. Every external Action must be pinned to an exact 40-character commit SHA.
6. **Fence privileged PR events.** A `pull_request_target` workflow must never checkout or execute untrusted pull-request code.

## Development workflow

1. Create a purpose branch from the recorded exact `main` SHA.
2. Inspect the relevant semantic/control sources and run the cheapest read-only diagnostic before editing (`just doctor`, `just next`, `just explain`, or `just github-dx`).
3. Make the lawful source change. If it changes a generated consequence, execute the declared manufacturer and preserve the receipt/diff.
4. Run narrow falsifiers first, then the broader relevant court.
5. Before opening a PR, run `just github-dx`. Run `just doctor` / certification courts when standing or producer identity is affected, and `just chicago` when the container/manufacturing path is affected.
6. Open a PR using the repository template. Record exact base/head subjects, authority classification, real verification, standing, risk, and rollback.
7. Treat GitHub Actions as supplemental evidence. A green workflow does not promote a release or artifact beyond that workflow’s declared authority.

## Standing claims

Use only the repository vocabulary: `UNKNOWN`, `PARTIAL_ALIVE`, `ALIVE`, `BLOCKED`, `BUILD_BROKEN`, `UNSUPPORTED`, and typed `REFUSED`.

Inspection is not execution. Historical receipts are not current-head proof. A missing capability is `UNSUPPORTED`, not a reason to improvise a success claim.

## Commit and PR semantics

PR titles are mechanically checked and should use:

```text
type(optional-scope): concise summary
```

Accepted types include `feat`, `fix`, `docs`, `test`, `ci`, `chore`, `refactor`, `perf`, `build`, `revert`, `security`, and `dx`.

For multi-line local commit messages, prefer `git commit -F <message-file>` to avoid shell quoting corruption.

## GitHub-native DX

`docs/GITHUB-DX.md` is the capability map for Codespaces/devcontainers, issue forms, Discussions, CODEOWNERS, Dependabot, labeling, Dependency Review, CodeQL, repository hygiene, supply-chain attestations, release notes, citation metadata, and Copilot instructions/agents/prompts/setup.

Run:

```bash
just github-dx
```

before proposing GitHub workflow or collaboration changes. The court is read-only and fails closed on mutable Action refs, missing workflow permissions, unsafe `pull_request_target` patterns, incomplete issue/security routing, and other repository-native drift.
