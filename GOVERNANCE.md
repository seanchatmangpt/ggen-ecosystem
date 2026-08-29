# Governance

This document defines who has decision-making authority over
`ggen-ecosystem`, how decisions actually get made today, and the real path
by which someone becomes a maintainer. It is written to match the current
size of the project, not to describe a structure that doesn't exist yet.

## Status: single-maintainer project

`ggen-ecosystem` currently has **one maintainer**: the individual listed in
[`.github/CODEOWNERS`](.github/CODEOWNERS) (`@seanchatmangpt`), who also
owns the repository. There is no steering committee, technical committee,
or maintainer vote today — stating otherwise would misrepresent the
project's actual bus factor to anyone deciding whether to depend on it or
contribute to it.

`.github/CODEOWNERS` is the single source of truth for who currently holds
maintainer authority. This document describes the *process*; it does not
duplicate the *roster* — if the two ever disagree, CODEOWNERS wins and this
file is stale and should be corrected.

## Roles

### Maintainer

A maintainer:

- Has merge access to `main` and is listed in `.github/CODEOWNERS`.
- Reviews and merges pull requests, following the workflow in
  [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Is responsible for the project's authority boundary (`SELECT` /
  `CONSTRUCT` / `DO`, see `AGENTS.md`) and for not letting generated
  projections (workflows, `generated/`) drift into hand-edited state.
- Enforces the [Code of Conduct](CODE_OF_CONDUCT.md) and triages security
  reports per [`SECURITY.md`](SECURITY.md).

### Contributor

Anyone who opens an issue, discussion, or pull request. No membership,
CLA, or pre-approval is required to contribute — see `CONTRIBUTING.md` for
the actual mechanics (branch from `main` at a resolved SHA, verify with
`just doctor` / `just chicago`, use the standing vocabulary in
`docs/STANDING.md` when making a claim about what now works).

There is currently no formal "member" tier between Contributor and
Maintainer. A track record of accepted, well-scoped contributions is what
the path to maintainer (below) is built from.

## Decision-making process

### Day-to-day changes (the normal case)

Ordinary changes — bug fixes, documentation, ontology edits, new packs,
CI/workflow regeneration — go through the pull request flow in
`CONTRIBUTING.md`. The maintainer reviews and merges. There is no
committee vote to wait on; a PR is decided by the maintainer applying the
same bar every reviewer here is asked to apply: does it verify for real
(`just doctor`, and `just chicago` for container/manufacturing-path
changes), and does it use the repo's typed standing vocabulary honestly
rather than smoothing a `BLOCKED`/`UNKNOWN` into a false `ALIVE`.

This is lazy-consensus in practice, not lazy-consensus in name: silence on
an open PR is not itself approval, and the maintainer's review is the gate.

### Changes to authority-boundary or admission semantics

Changes that touch the `SELECT`/`CONSTRUCT`/`DO` authority boundary, the
SHACL admission law (`admission/`), or what may be crowned `ALIVE`
(`docs/STANDING.md`) are held to a higher bar than a normal PR: they must
state explicitly what standing claim changes and why, and — where the
claim is about live execution rather than documentation — be backed by the
same receipted evidence chain the repo requires of any `ALIVE` claim
(exact lock identities, a real `ggen sync run`, `ggen receipt verify`,
deterministic replay). See `docs/STANDING.md` and `AGENTS.md` for the exact
chain. This applies to the maintainer's own changes too — the authority
boundary is not suspended for the person who wrote it.

### Branch protection (current real state)

`main` is not currently protected by a GitHub ruleset — see
[`docs/BRANCH-PROTECTION.md`](docs/BRANCH-PROTECTION.md) for why (an
in-flight automation cadence at the time it was drafted) and the exact
ruleset ready to apply (`.github/rulesets/main-branch-protection.json`).
Until that ruleset is applied, the maintainer can push directly to `main`;
the PR-based workflow in `CONTRIBUTING.md` is the enforced *practice*, not
yet an enforced *technical control*. This is stated here rather than
implied, because a governance document that omits it would overclaim the
project's actual controls.

## Becoming a maintainer

There is no committee to apply to, because there is no committee. The real
path, in order:

1. **Build a track record.** Multiple merged pull requests over time that
   needed little or no rework, spanning more than one area of the repo
   (ontology/admission, packs, CI/manufacturing, docs) — not a single
   large PR.
2. **Demonstrate the authority model, not just the diff.** Contributions
   that respect `SELECT`/`CONSTRUCT`/`DO` (`AGENTS.md`) and the standing
   vocabulary (`docs/STANDING.md`) without needing correction — e.g. never
   hand-editing a generated workflow, never claiming `ALIVE` without the
   receipt chain behind it.
3. **Be asked, or ask.** The existing maintainer proposes adding a new
   maintainer (or a contributor asks directly). This is a judgment call by
   the current maintainer(s), not a vote, for as long as there is exactly
   one maintainer — see "What changes when a second maintainer exists"
   below for what happens once that stops being true.
4. **Grant.** The change is two concrete, auditable actions: adding the
   person's GitHub handle to `.github/CODEOWNERS`, and granting them write
   access to the repository. Both are visible in the repo's own history —
   there is no private or undocumented promotion path.

There is no fixed contribution count or tenure requirement, because a
project this size does not have enough history to calibrate one honestly.
The criteria above are qualitative and applied by the current
maintainer(s); if that ever proves to need more structure (a formal
nomination + objection window, for instance), that change belongs in this
document, following the amendment process below.

### What changes when a second maintainer exists

The moment a second maintainer is added, single-person judgment calls stop
being sufficient for two categories of decision, and this document must be
amended (not silently reinterpreted) to say so explicitly:

- **Adding or removing a maintainer** moves from "the maintainer decides"
  to requiring agreement among the existing maintainers (a simple rule
  such as "no standing objection within a stated window" is sufficient at
  small scale — this document does not pre-commit to a specific voting
  threshold before there is a second maintainer to negotiate it with).
- **Authority-boundary and admission-law changes** (the higher bar above)
  move from single-maintainer sign-off to requiring at least one other
  maintainer's review, since the entire point of that boundary is that it
  isn't self-certified by whoever is changing it.

This section exists so that growth in maintainership isn't blocked on
inventing a governance model from scratch under time pressure — the shape
is decided now, while it's cheap, even though it isn't load-bearing yet.

## Maintainer responsibilities

A maintainer is expected to:

- Respond to security reports per the timeline in `SECURITY.md`.
- Keep `CODEOWNERS`, this document, and the actual repository state
  (who has write access) consistent with each other.
- Not hand-edit generated files (`.github/workflows/*.yml`, `generated/`)
  — fix the ontology/pack source and regenerate, per `CLAUDE.md` and
  `AGENTS.md`.
- Enforce the Code of Conduct, including on their own conduct.

## Stepping down and succession

A maintainer may step down at any time by saying so in an issue or
discussion and removing themselves from `.github/CODEOWNERS`. There is
currently no other maintainer to hand the project to automatically — this
is the honest bus-factor consequence of a single-maintainer project, and
is named here rather than left implicit. A contributor who wants to see
this risk reduced should read "Becoming a maintainer" above; that is the
actual mechanism for reducing it, not a promise made in this document on
the current maintainer's behalf.

## Conflict resolution

With one maintainer, there is no peer to escalate a disagreement to inside
the project; the maintainer's decision on a PR or issue is final. A
contributor who disagrees can:

- Make the technical case in the PR/issue thread, citing the repo's own
  standing vocabulary and verification commands rather than opinion — the
  same evidentiary bar the maintainer is expected to apply to themself.
- Open a [Discussion](https://github.com/seanchatmangpt/ggen-ecosystem/discussions)
  if the disagreement is about direction rather than a specific change.
- Fork. The [MIT license](LICENSE) exists precisely so this is always a
  real option, not a theoretical one.

Reports about a maintainer's conduct specifically (as opposed to a
technical disagreement) follow the enforcement path in
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), which routes to GitHub Security
Advisories when contacting the maintainer directly isn't appropriate.

## Changes to this document

Changes to `GOVERNANCE.md` go through the same pull request process as any
other change (`CONTRIBUTING.md`). Given the current single-maintainer
state, the maintainer approves changes to their own governance the same
way they approve any other PR — there is no separate ratification body.
Once a second maintainer exists, changes to this document fall under the
"authority-boundary" review bar above (at least one other maintainer's
review), since governance changes are exactly the kind of self-certifying
edit that bar exists to prevent.

## Related documents

- [`CODEOWNERS`](.github/CODEOWNERS) — the current maintainer roster
  (source of truth; this document must not contradict it).
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — the actual contribution workflow
  and verification commands referenced throughout this document.
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — behavioral standards and
  enforcement.
- [`SECURITY.md`](SECURITY.md) — vulnerability reporting and response
  timeline.
- [`SUPPORT.md`](SUPPORT.md) — where to file issues versus discussions.
- [`AGENTS.md`](AGENTS.md) — the authority boundary (`SELECT`/`CONSTRUCT`/
  `DO`) that governs what any contributor, including the maintainer, may
  claim or automate.
- [`docs/STANDING.md`](docs/STANDING.md) — the standing vocabulary and
  evidence chain referenced in "Decision-making process" above.
- [`docs/BRANCH-PROTECTION.md`](docs/BRANCH-PROTECTION.md) — the current,
  real state of `main`'s technical protection.

---

Last updated: 2026-08-29.
