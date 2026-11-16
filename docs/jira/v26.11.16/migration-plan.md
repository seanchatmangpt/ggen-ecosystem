# ggen-ecosystem migration plan v26.11.16

Standing: UNVERIFIED

## Identity
- Path: /Users/sac/ggen-ecosystem
- Remote: https://github.com/seanchatmangpt/ggen-ecosystem
- Branch: main@ab2a8504 (tracks origin/main)
- Last commit: 2026-10-13 | commits: 4229 | size: 8991 MB
- Languages/build: composition root — Justfile, Makefile, Dockerfile, ggen.toml,
  ecosystem.lock.toml, ontology.ttl; six git submodules under vendor/; CLAUDE.md present
- Nested repos (submodules, catalogued here only): vendor/autofde-lab@71de04a6,
  vendor/beam4pm@c3017e42, vendor/ggen@ff96f04e8, vendor/ggen-marketplace@bf9eccb34,
  vendor/ggen_igniter@0abed8a, vendor/wasm4pm@a7352d818

## Observed state
- Dirty 0 / untracked 0 — clean tree
- ahead 0 / behind 0; stash count: 3603 (census); unpushed local branches: 12 — e.g.
  archive/pre-v26.10.1-dirty-20261001 (preservation ref), chore/autofde-lab-pin-sync
  (ahead 3, behind 231 of origin/main), several branches whose upstream is `gone`
- vendor/ = 4.2 GB (submodule checkouts, likely with their own target/ dirs); generated/ 16 KB
- Submodules: 6, all initialised (see Identity)

## What it is
Canonical governed composition root for the ggen ecosystem: owns identity, composition,
admission, closure, qualification, transport and release standing; ggen and ggen-marketplace are
vendored as real git submodules and built into a published container.

## Classification
ACTIVE — census value stands.

## Migration risk
MEDIUM — the root is clean and pushed, but 3603 stashes and the 12 local branches (notably the
archive/pre-v26.10.1-dirty preservation ref and chore/autofde-lab-pin-sync +3) would be lost.
The 4.2 GB vendor/ tree may contain unpushed submodule work — check each.

## Recommended action
CLONE-FRESH (after branch/submodule triage)
1. `cd /Users/sac/ggen-ecosystem && git push origin archive/pre-v26.10.1-dirty-20261001 \
   chore/autofde-lab-pin-sync` — preserve the two meaningful local refs.
2. `git branch -vv | grep ': gone'` — delete branches whose upstream is gone (already merged).
3. DECISION: 3603 stashes — treat as noise; optionally
   `git bundle create /Volumes/archive/ggen-ecosystem-refs.bundle --all` before discarding.
4. `git submodule foreach 'git status --porcelain | head; git log --oneline @{u}.. 2>/dev/null'`
   — list dirty/unpushed work inside the six vendor/ checkouts; push each from its own repo.
5. `git submodule foreach 'rm -rf target _build node_modules deps'` — not needed if cloning
   fresh, but do it if the directory must be copied.
6. On new machine: `git clone --recurse-submodules \
   https://github.com/seanchatmangpt/ggen-ecosystem`.

## First commands on the new machine
- `just check` (or `make check`) per Justfile; `git submodule status` to confirm pins
  (stated, not run)

## See Also
- ../v26.10.1/
- /Users/sac/docs/jira/v26.11.16/README.md
