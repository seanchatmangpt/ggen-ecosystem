# v26.9.18 Wave Plan — RFC-GPACK-001 implementation (15-agent fan-out)

Operator instruction: "launch 15 agents to implement all of this work and then
tag v26.9.17". `v26.9.17` is already tagged+published (2026-09-18T03:51Z,
container `sha256:9c6a5c36…`, receipt in repo) — the tag will NOT move. This
wave implements the RFC's unimplemented half (its §85/§86/§87 migration ladders
+ the §94 spec pack + Appendix C/D corpora) and lands as **v26.9.18**.

## Baselines (verified 2026-09-18T04:xxZ)

- `ggen` origin/main == pin `ad3a7e661` (RFC inspected subject)
- `ggen_igniter` origin/main == pin `15305cea`
- `ggen-marketplace` origin/main == pin `800b8c6c5`
- Concurrency: rider STOPPED (operator cut, log run 1620/FINAL); ad-hoc wave
  15 ≤ 16 heavyweight flash ceiling — lawful, sole load.

## Wave layout (15 tickets, disjoint paths per repo)

| # | Repo | Ticket | Deliverable (RFC anchor) |
|---|---|---|---|
| 01 | marketplace | T01 | `ggen-pack-spec-pack` scaffold: pack.toml + gp: vocabulary ontology + core gates (§94, App. B, §10) |
| 02 | marketplace | T02 | valid corpus under spec-pack `qualification/positive/` (App. D valid/*, §91 hello-pack verbatim) |
| 03 | marketplace | T03 | invalid corpus + refusal assertions under `qualification/negative/` (App. D invalid/*, App. C codes) |
| 04 | marketplace | T04 | cross-engine vectors `vectors/` (App. D cross-engine/*, §23/§24 canonical bindings) |
| 05 | marketplace | T05 | catalog projection increment (#87): pack-owned class/lifecycle for spec-pack family |
| 06 | ggen | T06 | `queries/` discovery ≠ `gates/` refusal (§13/§14, D1) |
| 07 | ggen | T07 | `.tera` discovery + explicit renderer identity (§17–§22, D2) |
| 08 | ggen | T08 | portable SHA-256 PackDigest, `ggen-pack-v1` algorithm (§37/§38/§39) |
| 09 | ggen | T09 | consumer alias ≠ canonical name in receipts (§9) |
| 10 | ggen | T10 | portable receipt envelope v1 (§54/§55) |
| 11 | ggen | T11 | semantic-only Core packs admitted (§73) |
| 12 | igniter | T12 | gates = refusal falsifiers, queries = render inputs (§14, D1) |
| 13 | igniter | T13 | pack.toml consumed + identity correspondence (§7/§8, D3) |
| 14 | igniter | T14 | canonical RDF binding normalization (§23/§24, D6) |
| 15 | igniter | T15 | portable receipt envelope + recursive `.tera` discovery (§55, §20) |

Cross-engine crown (App. E) is wave 2 — needs both engines' increments green
first. Bounded honestly here; not silently pruned.

## Integration law (coordinator-only)

- Worktrees: `~/wt-v26918/<repo>-NN-<slug>/`, branch `gpack/<repo>-NN-<slug>`.
- Agents: commit only, never push, never leave their worktree.
- Coordinator: review diff → run repo-scope tests → push branch → PR → merge.
  Serialized per repo; ONE --no-ff merge per integration pass; red → reset +
  BLOCKED + ticket reopened.
- 20-min worktree silence = dead agent → reap, top up at half pace.
- After repos merge: ecosystem advances pins/lock → certify/bench/sync →
  PR → tag `v26.9.18` → container → closure receipt.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T04:10Z | PARTIAL_ALIVE | (tickets uncommitted, this tree) | rider stopped verified; 3 producer mains == pins verified; worktrees + 15 tickets next | dispatch → integrate → release v26.9.18 |
