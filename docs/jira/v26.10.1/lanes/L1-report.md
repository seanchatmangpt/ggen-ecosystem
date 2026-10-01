# L1 report — lock core bump

- lane: L1
- branch: `release/v26.10.1` @ `19a2b1f1` (confirmed first action)
- files-written: `ecosystem.lock.toml` (11 lines changed, left UNSTAGED); this report
- scratch: `/tmp/v26101-lane1/` (asset downloads + shasum; nothing written inside the repo besides owned files)

## Decisions + rationale

1. **`[ggen].release` → `v26.9.28` (delegated decision, Option (a) executed).**
   Evidence: `gh release view v26.9.29 -R seanchatmangpt/ggen` → `release not found` (exit 1);
   `gh release list` shows `v26.9.28` tagged **Latest** (published 2026-09-29T02:21:02Z);
   `gh release view v26.10.0` → tag exists with `assets: []`. The pre-edit lock claimed
   `release = "v26.9.29"` — a release that does not exist on the forge. Both asset digests in the
   file were **recomputed by this lane** from fresh downloads and match the GitHub `.sha256`
   sidecars byte-for-byte (linux `47316dd0…`, aarch64 `d553c4bf…`), proving the file's digests were
   real v26.9.28 assets mislabeled as v26.9.29. Option (a) applied: `release = "v26.9.28"`,
   digests retained (now lane-verified), manufacture path stays executable.
   **Failed edge recorded: ggen tag `v26.10.0` (`82795cda`) exists but has no GitHub release/assets** —
   the next crown cannot point `[ggen].release` at v26.10.0 until a release is published.
2. **`base_main_sha` → `dc665a1e…`**: verified `git rev-parse dc665a1e…^{commit}` and
   `git rev-parse origin/main` both return exactly `dc665a1e93573949040900faa65b46af3a3ea6d9`
   (RESOLUTIONS seam confirmed, not just copied).
3. **`updated_at` → `2026-10-01T19:44:09Z`**: observed `date -u` wall clock at edit time (ISO-8601 Z).
4. **`[ggen_marketplace].latest_published_release{,_sha}` → `v26.9.30` / `80d429f1…`**: the file's
   v26.9.29/637b561c pair was stale (v26.9.29 marketplace release superseded);
   `gh release view -R seanchatmangpt/ggen-marketplace` → `v26.9.30` (published 2026-10-01T04:56:25Z);
   tag → commit resolved via `gh api repos/…/git/refs/tags/v26.9.30` → `80d429f13cc887f66855ba4029f6d83aa3a8098f`
   (lightweight commit tag). Note: `bf9eccb3…` (the pinned `sha`) describes `v26.9.30-6`, i.e. it is
   6 commits **after** this tag — consistent, not a conflict.
5. **`[ggen_igniter].version` → `26.9.30`**: observed `git -C vendor/ggen_igniter show 0abed8a3…:mix.exs`
   line 9 `version: "26.9.30"` (was stale `26.9.29`).
6. **`[beam4pm].version` → `26.9.30`**: observed `mix.exs` line 11 at `7bad16ab…` (was stale `26.9.28`).
7. **`[wasm4pm].version` → `26.9.30`**: two candidate files at `a7352d81…` disagree (`Cargo.toml` 26.9.30,
   `package.json` 26.9.28). Resolved by release-process evidence: wasm4pm's own release commit
   `cd08cc0e5` ("chore(release): v26.9.30 version bump") touches root `Cargo.toml`, not `package.json`
   — Cargo.toml is the release-managed version file; package.json lags. At the previous pin
   (`09c171b4…`) both files agreed (26.9.28), which is why the older value was ambiguous.
8. **`[wasm4pm].latest_published_release` → `v26.9.30`** (`gh release view -R seanchatmangpt/wasm4pm`;
   file had stale `v26.9.24`).
9. **`[container]`**: `tag` → `v26.10.1`, `standing = "BLOCKED"`, `requires_republish = true`,
   `failure` line rewritten to name v26.10.1 following the v26.9.25-crown precedent
   (commit `3b75fe27`, and the v26.9.29 refinement in `6dd3e732`): digest kept unchanged as
   historical-digest line ("digest below is historical evidence from the prior published image"),
   `observed_success_run/at/head_sha` kept unchanged as historical observation (run 35833887166).
   The lock file carried no inline comments, so no `# stale` comments were added (style-consistent).

## Verified unchanged (all at RESOLUTIONS targets, evidence run)

- `[ggen].commit_sha` `ff96f04e…` — `git -C vendor/ggen rev-parse ff96f04e8^{commit}` resolves.
- `[ggen_marketplace].sha` + `[pragprog_tps].marketplace_sha` `bf9eccb3…` — resolve in vendor; matches RESOLUTIONS.
- `[ggen_igniter].sha` `0abed8a3…`, `[beam4pm].sha` `7bad16ab…`, `[wasm4pm].sha` `a7352d81…`,
  `[submodules].{ggen,ggen_marketplace,autofde_lab,ggen_igniter,beam4pm,wasm4pm}_commit` — all six
  targets resolve via `git -C vendor/<v> rev-parse <sha>^{commit}`.
- `[ggen].linux_x86_64_asset_sha256` / `aarch64_apple_darwin_asset_sha256` — recomputed via
  download + `shasum -a 256`, match sidecars and prior values.
- `[ggen_igniter].latest_published_release` `v26.8.27` — re-verified still latest.
- `[consumer_manufacture].release` `v26.8.27` — deliberately NOT bumped: not in RESOLUTIONS bump list;
  consistent with the frozen-generator-identity precedent (crown courts run frozen ggen v26.8.27).
- `observed_executable_sha256` `c44f9c56…` — left UNCHANGED per contract (no binary executed this lane);
  coherent with `release = v26.9.28` (evidence line cites run 36508964375, "binary reports ggen 26.9.28").
- `[catalog]` census fields (2026-08-28 era) — historical observation block, not a bump pin.

## Commands + exits (abridged, chronological)

| command | exit |
|---|---|
| `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 (`release/v26.10.1`, `19a2b1f1`) |
| `grep -nE 'v26\.|sha =|release =|version =|updated_at|base_main_sha|marketplace_sha' ecosystem.lock.toml` | 0 |
| `git rev-parse dc665a1e…^{commit}`; `git rev-parse origin/main` | 0 / 0 (both = dc665a1e) |
| `gh release view v26.9.28 -R seanchatmangpt/ggen --json assets` | 0 (11 assets) |
| `gh release view v26.9.29 -R seanchatmangpt/ggen` | 1 — `release not found` |
| `gh release view v26.10.0 -R seanchatmangpt/ggen` | 0 — `assets: []` |
| `gh release list -R seanchatmangpt/ggen --limit 8` | 0 (v26.9.28 = Latest) |
| `gh release download v26.9.28 … --pattern 'ggen-x86_64-unknown-linux-gnu.tar.gz*'` / `'ggen-aarch64-apple-darwin.tar.gz*'` → `/tmp/v26101-lane1/` | 0 / 0 |
| `shasum -a 256` both tarballs; `cat` both `.sha256` sidecars | 0 (all three digest sources agree) |
| `gh release view -R seanchatmangpt/ggen-marketplace` / `ggen_igniter` / `wasm4pm` | 0 (v26.9.30 / v26.8.27 / v26.9.30) |
| `gh api repos/seanchatmangpt/ggen-marketplace/git/refs/tags/v26.9.30` | 0 (commit `80d429f1…`) |
| `git -C vendor/<v> rev-parse <target>^{commit}` ×6 | 0 ×6 |
| `git -C vendor/ggen_igniter show 0abed8a3…:mix.exs | grep version:` | 0 (`"26.9.30"`) |
| `git -C vendor/beam4pm show 7bad16ab…:mix.exs | grep version:` | 0 (`"26.9.30"`) |
| `git -C vendor/wasm4pm {show a7352d81…:Cargo.toml, show a7352d81…:package.json, show cd08cc0e5 --stat}` | 0 (26.9.30 / 26.9.28 / release bump touches Cargo.toml) |
| `git status --porcelain ecosystem.lock.toml` (pre-edit) | empty — file was clean vs HEAD |
| `python3.11 -c "import tomllib;tomllib.load(open('ecosystem.lock.toml','rb'))"` | 0 (`TOML_OK dc665a1e v26.9.28 v26.10.1 26.9.30`) |
| `git diff --stat ecosystem.lock.toml` | 11 insertions, 11 deletions — intended lines only |
| `git status --porcelain ecosystem.lock.toml` (post-edit) | ` M` — modified, UNSTAGED (no `git add` run) |

Note: bare `python3 -c "import tomllib…"` fails on this host (`ModuleNotFoundError`, exit 1) — the
repo-standard `python3.11` was used for validation, as AGENTS.md prescribes.

## REFUSED / BLOCKED / UNKNOWN items

- **FAILED EDGE (recorded, no action):** ggen tag `v26.10.0` exists (`82795cda`) but has **no GitHub
  release and zero assets**; latest asset-bearing release is `v26.9.28`. `[ggen].release` therefore
  remains v26.9.28 until that release is published. This is the RESOLUTIONS-documented gap,
  confirmed by this lane's own `gh` observations, not assumed.
- **UNKNOWN (flagged, no change):** `observed_executable_sha256` (`c44f9c56…`) — field semantics bind
  to an executed binary; this lane did not execute ggen, so the value is retained as the v26.9.28-era
  observation. It is coherent with `release = v26.9.28` but has not been re-witnessed this session.
- **UNKNOWN (flagged, no change):** `[container].digest` (`sha256:6605878e…`) and `observed_success_*`
  describe the last published image (v26.9.22-era observation, run 35833887166); retained as
  historical evidence per crown precedent. Container standing for v26.10.1 = **BLOCKED** until the
  container workflow publishes and an independent pull verifies tag `v26.10.1`.
- **REFUSED_SEAM_CONFLICT: none.** Every RESOLUTIONS seam this lane checked matched observed evidence.
- No `git add/commit/checkout/branch/stash/push/submodule` commands were run. `vendor/*` read via
  read-only `git show/ls-tree/rev-parse/tag/log` only.
