# L6 lane report — README pinned SHAs + standing line; CITATION.cff verify-only

- repo: /Users/sac/ggen-ecosystem, branch `release/v26.10.1` @ `19a2b1f1` (at dispatch; coordinator owns all git transitions)
- standing: **PARTIAL_ALIVE** — README resolved + bumped on the exact working-tree subject; the
  `(matches ecosystem.lock.toml and the vendor/* gitlink)` claims become true at coordinator
  integration (lock bump + crown), per contract.

## files-written

| file | action | staged |
|---|---|---|
| `README.md` | 3-way conflict resolved (both blocks), release-era references bumped to v26.10.1 | no (left unstaged per contract) |
| `CITATION.cff` | verify-only NO-OP — untouched | no |
| `docs/jira/v26.10.1/lanes/L6-report.md` | this report | no |

## decisions + rationale

1. **Conflict block 1 (standing callout) — merged both intents, then bumped.** Kept upstream's
   callout body (`BLOCKED[REQUIRES_REPUBLISH]` for the ecosystem release; "producer identities
   admitted below"; "historical container digests remain evidence for their own subjects only";
   DoD link) and the WIP's two standing corrections named by the contract: the crown note
   (`BLOCKED[AWAITING_PUBLISH]`, "authoritative live standing is `ecosystem.lock.toml [container]`")
   bumped v26.9.25 crown (2026-09-26) → v26.10.1 crown (2026-10-01), tag v26.9.25 → v26.10.1; and
   the callout's own release references v26.9.29 → v26.10.1. The WIP's `ALIVE`-era body (issue #146
   narrative) was superseded by upstream's newer standing text; the #146 fact survives in the
   preserved digest bullet below.
2. **Conflict block 2 (pins list + frontier intake) — merged both intents.** Kept upstream's
   structure verbatim where values conform: intro sentence, GGen published-release detail lines
   (v26.9.28 @ `ff96f04e…` = the RESOLUTIONS ggen target, so unchanged; archive/build-output
   SHA-256 lines kept as published-release artifact evidence), Marketplace pack line, "digest
   retained in lock is historical evidence" bullet (bumped v26.9.29 → v26.10.1), and the entire
   Seven-day frontier intake section (4 paragraphs, byte-identical). Adopted the WIP's flat
   `Marketplace commit:` / `AutoFDE Lab commit:` line formats (contract: "phrase exactly as the
   existing lines do") and kept the WIP's Historical composed-container digest bullet verbatim
   (the contract-named container-digest line rewrite).
3. **All six producer pins set to RESOLUTIONS crown targets.** Contract named three arrows (ggen,
   Marketplace, AutoFDE); the other three current-pin lines (Igniter, Beam4PM, WASM4PM) carried
   v26.9.29-era crowns that are neither new pinned values nor explicitly historical, so the
   contract's 40-hex gate forced them to the RESOLUTIONS targets as well:
   ggen `ff96f04e8c7b851e5cca53f3faf5ce1d5f43ce6e` (unchanged), ggen-marketplace
   `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2`, autofde-lab `71de04a60db723764fab5afe042b42937b471e0e`,
   ggen_igniter `0abed8a35db68c18bba6982b266dd7546c162d1c`, beam4pm
   `7bad16ab4c20d0eeb90adca1c90a6f3f4d5900dc`, wasm4pm `a7352d818dbcaa15909833f13ac367dc5950a7a9`.
   Superseded v26.9.29-era values (`637b561c…`, `cb82395d…`, `d42a5af9…`, `4c5eed22…`,
   `aa98261d…`, `2ec870ef…`) were removed from current-pin positions only; they remain reachable
   at `git show HEAD:README.md` and in the v26.9.29-era release docs.
4. **Source versions observed, never guessed** (RESOLUTIONS-prescribed method, executed read-only
   against the fetched target SHAs; all six targets verified locally present via
   `git cat-file -t`, exit 0): ggen_igniter `26.9.30` (`mix.exs` line 9 @ `0abed8a3`),
   beam4pm `26.9.30` (`mix.exs` line 11 @ `7bad16ab`), wasm4pm `26.9.30` (`Cargo.toml` @
   `a7352d81`). Old-crown cross-check (beam4pm @ `aa98261d` `mix.exs` = `26.9.28`) confirmed
   `mix.exs` is the file the pre-existing "source version" claims referred to.
5. **wasm4pm dual-version skew recorded, not silently pruned:** at `a7352d81`, `Cargo.toml`
   reads `26.9.30` but npm `package.json` reads `26.9.28`. The README line cites `26.9.30` (per
   `Cargo.toml`) and states the `package.json` skew inline; see UNKNOWN items.
6. **Dropped cut-specific release-observation claims** ("latest observed published GitHub Release
   remains `v26.8.27`" / `v26.9.24`; "no matching `v26.9.28` tag was observed at this release
   cut"; upstream's "Marketplace published release: `v26.9.29` at `637b561c…`; rolling crown
   `cb82395d…`"): not re-observable in this lane (no network release observation authorized);
   release-observation evidence is L2's dossier scope. Listed under UNKNOWN.

## 40-hex residue inventory (`grep -nE '[0-9a-f]{40}' README.md`, post-edit)

| line | value | class |
|---|---|---|
| 66 | `ff96f04e…` | new pinned value (ggen) |
| 69 | `47316dd0…` (64-hex) | explicitly historical: ggen v26.9.28 release-archive SHA-256 |
| 71 | `c44f9c56…` (64-hex) | explicitly historical: release-run build-output SHA-256 (run 36508964375) |
| 73 | `bf9eccb3…` | new pinned value (ggen-marketplace) |
| 74 | `71de04a6…` | new pinned value (autofde-lab) |
| 76 | `0abed8a3…` | new pinned value (ggen_igniter) |
| 78 | `7bad16ab…` | new pinned value (beam4pm) |
| 80 | `a7352d81…` | new pinned value (wasm4pm) |
| 88 | `b9e17023…` (64-hex) | explicitly historical: composed-container digest ("not currently admitted as pullable") |
| 92 | `50c9172b…` | explicitly historical: pinned observation subject of the dated 2026-09-23..09-30 seven-day intake window (upstream content, not a producer pin) |
| 130 | `dcd363b5…` | explicitly historical: bootstrap provenance (section self-labels "historical evidence") |
| 134–136 | `0455db2b…`, `e03c5da8…`, `27500c76…` (64-hex) | explicitly historical: bootstrap artifact/workflow/graph digests |

Gate result: every remaining hex value is a new pinned value or explicitly historical. Zero
conflict markers (`grep -c '<<<<<<<'` = 0; `>>>>>>` = 0; `^=======$` = 0). Remaining `v26.9.x`
strings are only the historical era-label "v26.9.22-era digest" and the still-current fact
"GGen published release: `v26.9.28`" (RESOLUTIONS: latest asset-bearing ggen release).

## CITATION.cff (verify-only)

`grep -nE 'version|date-released' CITATION.cff` → sole match `1:cff-version: 1.2.0` (exit 0).
No `version:` field, no `date-released:` field → **NO-OP recorded**; file left byte-identical
and unstaged, per contract.

## commands + exits (evidence log)

```
git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD   # release/v26.10.1 / 19a2b1f1 — exit 0
git show archive/pre-v26.10.1-dirty-20261001:README.md > /tmp/v26101-lane6/README.wip.md   # exit 0
git show HEAD:README.md > /tmp/v26101-lane6/README.head.md                                 # exit 0
diff README.head.md README.wip.md                                               # exit 1 (expected: files differ)
cat CITATION.cff; grep -nE 'version|date-released' CITATION.cff                 # exit 0 (1 match only)
for 6 vendors: git -C vendor/<v> rev-parse -q --verify HEAD                     # exit 0 each
git -C vendor/{ggen_igniter,beam4pm,wasm4pm,ggen-marketplace,autofde-lab,ggen} \
    cat-file -t <RESOLUTIONS target>                                            # exit 0 all six (commit)
git -C vendor/ggen_igniter show 0abed8a3…:mix.exs | grep -m1 '^version'         # exit 1 (indented key)
git -C vendor/ggen_igniter show 0abed8a3…:mix.exs | grep -nE 'version'          # exit 0 → line 9: version: "26.9.30"
git -C vendor/beam4pm show 7bad16ab…:mix.exs | grep -nE 'version:'              # exit 0 → line 11: version: "26.9.30"
git -C vendor/wasm4pm ls-tree --name-only a7352d81… | grep -iE 'mix.exs|Cargo.toml|package.json|…'  # exit 0 → Cargo.toml, package.json
git -C vendor/wasm4pm show a7352d81…:Cargo.toml | grep -m1 '^version'           # exit 0 → 26.9.30
git -C vendor/wasm4pm show a7352d81…:package.json | grep -m1 '"version"'        # exit 0 → 26.9.28
git -C vendor/wasm4pm show 2ec870ef…:Cargo.toml | grep -m1 '^version'           # exit 0 → 26.9.28 (old-crown cross-check)
git -C vendor/wasm4pm show 2ec870ef…:package.json | grep -m1 '"version"'        # exit 0 → 26.9.28
git -C vendor/beam4pm show aa98261d…:mix.exs | grep -nE 'version:'              # exit 0 → 26.9.28 (old-crown cross-check)
Edit README.md (block 1) / Edit README.md (block 2)                             # applied
grep -c '<<<<<<<' README.md                                                     # 0
grep -c '>>>>>>>' README.md                                                     # 0
grep -c '^=======$' README.md                                                   # 0
grep -nE '[0-9a-f]{40}' README.md                                               # exit 0 (inventory above)
grep -n 'v26\.9\.2[0-9]' README.md                                              # exit 0 (2 lawful residues)
git status --porcelain README.md CITATION.cff docs/jira/v26.10.1/lanes/         # M README.md; ?? lanes/ — exit 0
```

## REFUSED / BLOCKED / UNKNOWN items

- **REFUSED_SEAM_CONFLICT: none.** All locally observed evidence agreed with the pinned seams;
  no seam altered.
- **UNKNOWN — wasm4pm canonical version file:** `Cargo.toml` `26.9.30` vs `package.json`
  `26.9.28` at crown target `a7352d81`. README cites Cargo.toml and states the skew inline;
  canonical-file determination left to L1 (lock `[wasm4pm].version`) / L2 (dossier).
- **UNKNOWN — latest published GitHub releases** for ggen_igniter / beam4pm / wasm4pm /
  ggen-marketplace not re-observed by this lane (no release-observation authority); the dropped
  observation claims are L2 dossier scope.
- **Deferred truth (by design, per contract):** the `(matches ecosystem.lock.toml and the
  vendor/* gitlink)` parentheticals and "(also the current `vendor/ggen` gitlink)" are statements
  of the pin this release sets; they become observed fact only at coordinator integration
  (lock bump + `crown-submodules.py --apply`), not at lane time.
