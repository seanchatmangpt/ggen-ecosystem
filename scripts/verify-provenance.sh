#!/usr/bin/env bash
# scripts/verify-provenance.sh — real identity-consistency check across the repo's
# lock/manifest files. NEVER touches Docker (no docker build/push/run/inspect).
#
# Checks, each printing one standing-vocabulary verdict (see docs/STANDING.md):
#   1. ggen commit identity:        [ggen].commit_sha == [submodules].ggen_commit
#                                    == real `git -C vendor/ggen rev-parse HEAD`
#   2. marketplace commit identity: [ggen_marketplace].sha == [submodules].ggen_marketplace_commit
#                                    == real `git -C vendor/ggen-marketplace rev-parse HEAD`
#   3. ggen.toml pack path exists as a real directory under vendor/ggen-marketplace
#   4. UNKNOWN-TODO placeholders classified: honestly-still-pending vs
#      release-blocker-if-still-present-at-crown, per docs/DEFINITION-OF-DONE.md
#   5. [container].digest format check (sha256:[0-9a-f]{64}) IF set to a real value
#      (placeholder is skipped, not checked; no registry fetch, format only)
#   6. every generated file (.github/workflows/*.yml) matches what a fresh
#      `ggen sync run --dry-run` would produce (complements scripts/doctor.sh's
#      check #3, which only covers pack content_hash, not the workflow files
#      themselves — this check is not a duplicate)
#
# This script never runs `docker build`, `docker push`, touches the Dockerfile,
# alters vendor/ggen or vendor/ggen-marketplace's checked-out commit, or changes
# ecosystem.lock.toml's [container] tag/digest. Read-only with respect to those.
#
# Exit code: 0 if no check emits BLOCKED/BUILD_BROKEN/UNKNOWN, else 1.

set -u
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 1

FAIL=0
verdict() {
  # verdict <CHECK_NAME> <VERDICT> <detail...>
  local name="$1"; local v="$2"; shift 2
  printf '[%s] %-14s %s\n' "$name" "$v" "$*"
  case "$v" in
    BLOCKED|BUILD_BROKEN|UNKNOWN) FAIL=1 ;;
  esac
}

LOCK=ecosystem.lock.toml
MANIFEST=ggen.toml
DOD=docs/DEFINITION-OF-DONE.md

echo "== ggen-ecosystem verify-provenance.sh — identity/manifest drift (no Docker) =="
echo

# --- helper: pull a "key = "value"" scalar from a [section] in a TOML file, first match after the section header
toml_scalar() {
  # toml_scalar <file> <section> <key>
  awk -v sect="[$2]" -v key="$3" '
    $0 == sect { insect=1; next }
    /^\[/ { insect=0 }
    insect && $0 ~ ("^" key " *=") {
      line=$0
      sub("^" key " *= *", "", line)
      gsub(/^"|"$/, "", line)
      gsub(/^ +| +$/, "", line)
      print line
      exit
    }
  ' "$1"
}

# --- (1) ggen commit triple-equality: [ggen].commit_sha == [submodules].ggen_commit == real vendor/ggen HEAD
name="1-ggen-commit-identity"
if [ ! -f "$LOCK" ]; then
  verdict "$name" UNKNOWN "$LOCK not found"
elif [ ! -d vendor/ggen ]; then
  verdict "$name" BLOCKED "vendor/ggen submodule directory missing"
else
  lock_commit="$(toml_scalar "$LOCK" ggen commit_sha)"
  sub_commit="$(toml_scalar "$LOCK" submodules ggen_commit)"
  real_commit="$(git -C vendor/ggen rev-parse HEAD 2>&1)"
  rev_rc=$?
  if [ -z "$lock_commit" ] || [ -z "$sub_commit" ]; then
    verdict "$name" UNKNOWN "missing [ggen].commit_sha or [submodules].ggen_commit in $LOCK (got commit_sha='$lock_commit' ggen_commit='$sub_commit')"
  elif [ "$rev_rc" -ne 0 ]; then
    verdict "$name" BUILD_BROKEN "git rev-parse HEAD failed in vendor/ggen: $real_commit"
  elif [ "$lock_commit" = "$sub_commit" ] && [ "$sub_commit" = "$real_commit" ]; then
    verdict "$name" ALIVE "[ggen].commit_sha == [submodules].ggen_commit == vendor/ggen HEAD, all $real_commit"
  else
    verdict "$name" BLOCKED "mismatch: [ggen].commit_sha=$lock_commit [submodules].ggen_commit=$sub_commit vendor/ggen HEAD=$real_commit"
  fi
fi
echo

# --- (2) marketplace commit triple-equality: [ggen_marketplace].sha == [submodules].ggen_marketplace_commit == real vendor/ggen-marketplace HEAD
name="2-marketplace-commit-identity"
if [ ! -f "$LOCK" ]; then
  verdict "$name" UNKNOWN "$LOCK not found"
elif [ ! -d vendor/ggen-marketplace ]; then
  verdict "$name" BLOCKED "vendor/ggen-marketplace submodule directory missing"
else
  lock_sha="$(toml_scalar "$LOCK" ggen_marketplace sha)"
  sub_commit="$(toml_scalar "$LOCK" submodules ggen_marketplace_commit)"
  real_commit="$(git -C vendor/ggen-marketplace rev-parse HEAD 2>&1)"
  rev_rc=$?
  if [ -z "$lock_sha" ] || [ -z "$sub_commit" ]; then
    verdict "$name" UNKNOWN "missing [ggen_marketplace].sha or [submodules].ggen_marketplace_commit in $LOCK (got sha='$lock_sha' ggen_marketplace_commit='$sub_commit')"
  elif [ "$rev_rc" -ne 0 ]; then
    verdict "$name" BUILD_BROKEN "git rev-parse HEAD failed in vendor/ggen-marketplace: $real_commit"
  elif [ "$lock_sha" = "$sub_commit" ] && [ "$sub_commit" = "$real_commit" ]; then
    verdict "$name" ALIVE "[ggen_marketplace].sha == [submodules].ggen_marketplace_commit == vendor/ggen-marketplace HEAD, all $real_commit"
  else
    verdict "$name" BLOCKED "mismatch: [ggen_marketplace].sha=$lock_sha [submodules].ggen_marketplace_commit=$sub_commit vendor/ggen-marketplace HEAD=$real_commit"
  fi
fi
echo

# --- (2b) autofde-lab commit identity: [submodules].autofde_lab_commit == real vendor/autofde-lab HEAD
name="2b-autofde-lab-commit-identity"
if [ ! -f "$LOCK" ]; then
  verdict "$name" UNKNOWN "$LOCK not found"
elif [ ! -d vendor/autofde-lab ]; then
  verdict "$name" BLOCKED "vendor/autofde-lab submodule directory missing"
else
  sub_commit="$(toml_scalar "$LOCK" submodules autofde_lab_commit)"
  real_commit="$(git -C vendor/autofde-lab rev-parse HEAD 2>&1)"
  rev_rc=$?
  if [ -z "$sub_commit" ]; then
    verdict "$name" UNKNOWN "missing [submodules].autofde_lab_commit in $LOCK"
  elif [ "$rev_rc" -ne 0 ]; then
    verdict "$name" BUILD_BROKEN "git rev-parse HEAD failed in vendor/autofde-lab: $real_commit"
  elif [ "$sub_commit" = "$real_commit" ]; then
    verdict "$name" ALIVE "[submodules].autofde_lab_commit == vendor/autofde-lab HEAD ($real_commit)"
  else
    verdict "$name" BLOCKED "mismatch: [submodules].autofde_lab_commit=$sub_commit vendor/autofde-lab HEAD=$real_commit"
  fi
fi
echo

# --- (3) ggen.toml pack path resolves to a real existing directory under vendor/ggen-marketplace
name="3-pack-path-exists"
if [ ! -f "$MANIFEST" ]; then
  verdict "$name" UNKNOWN "$MANIFEST not found"
else
  # Extract every `path = "..."` line inside the [packs] table.
  pack_lines="$(awk '
    /^\[packs\]/ { insect=1; next }
    /^\[/ { insect=0 }
    insect && /path *=/ {
      name=$0; sub(/ *=.*/, "", name); gsub(/^[ \t]+|[ \t]+$/, "", name)
      val=$0; sub(/^[^=]*= */, "", val); gsub(/[{}"]/, "", val)
      # val may look like: github-actions = { path = "vendor/..." }
      print $0
    }
  ' "$MANIFEST")"
  paths="$(grep -vE '^[[:space:]]*#' "$MANIFEST" | grep -oE 'path *= *"[^"]+"' | sed -E 's/path *= *"([^"]+)"/\1/')"
  if [ -z "$paths" ]; then
    verdict "$name" UNKNOWN "no [packs.*] path = \"...\" entries found in $MANIFEST"
  else
    bad=0
    checked=0
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      checked=$((checked + 1))
      case "$p" in
        vendor/ggen-marketplace/*) ;;
        *)
          verdict "$name" BLOCKED "pack path '$p' does not live under vendor/ggen-marketplace"
          bad=1
          continue
          ;;
      esac
      if [ ! -d "$p" ]; then
        verdict "$name" BLOCKED "pack path '$p' does not exist as a directory"
        bad=1
      fi
    done <<< "$paths"
    if [ "$bad" -eq 0 ]; then
      verdict "$name" ALIVE "$checked pack path(s) in $MANIFEST all resolve to real directories under vendor/ggen-marketplace"
    fi
  fi
fi
echo

# --- (4) UNKNOWN-TODO placeholders, classified against docs/DEFINITION-OF-DONE.md
name="4-unknown-todo-classified"
if [ ! -f "$LOCK" ]; then
  verdict "$name" UNKNOWN "$LOCK not found"
else
  todo_lines="$(grep -n 'UNKNOWN-TODO' "$LOCK" || true)"
  if [ -z "$todo_lines" ]; then
    verdict "$name" ALIVE "no UNKNOWN-TODO placeholders remain in $LOCK"
  else
    # Fields the ggen.toml comment / DoD PR-001/PR-009 explicitly documents as
    # historical/no-longer-load-bearing once the container path replaced binary
    # release consumption. Everything else in [container] (tag/digest) is the
    # PR-009 crown-chain field: honest-pending now, but a real release blocker
    # if still UNKNOWN-TODO at crown/release time (see DoD PR-001, PR-009, PR-014).
    n="$(echo "$todo_lines" | grep -c '.')"
    dod_note=""
    if [ -f "$DOD" ]; then
      dod_note=" (cross-referenced against $DOD)"
    else
      verdict "$name" UNKNOWN "$DOD not found — cannot cross-reference which UNKNOWN-TODOs are honestly-pending vs release-blocking"
    fi
    blocker=0
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      case "$line" in
        *linux_x86_64_asset_sha256*|*observed_executable_sha256*)
          echo "    HONEST-NON-BLOCKING (historical, superseded by [container] path per DoD PR-001): ${line}"
          ;;
        *"tag ="*|*"digest ="*)
          echo "    HONEST-PENDING-NOW / CROWN-BLOCKER-IF-STILL-UNKNOWN-AT-RELEASE (DoD PR-009): ${line}"
          ;;
        *)
          echo "    UNCLASSIFIED — new UNKNOWN-TODO not covered by known DoD rows, treat as a potential blocker: ${line}"
          blocker=1
          ;;
      esac
    done <<< "$todo_lines"
    if [ "$blocker" -eq 1 ]; then
      verdict "$name" BLOCKED "$n UNKNOWN-TODO placeholder(s) present in $LOCK, at least one unclassified against $DOD$dod_note"
    else
      verdict "$name" PARTIAL_ALIVE "$n UNKNOWN-TODO placeholder(s) present in $LOCK, all classified as honestly-pending per $DOD$dod_note"
    fi
  fi
fi
echo

# --- (5) [container].digest format check (sha256:[0-9a-f]{64}) — format only, no registry fetch
name="5-container-digest-format"
if [ ! -f "$LOCK" ]; then
  verdict "$name" UNKNOWN "$LOCK not found"
else
  digest="$(toml_scalar "$LOCK" container digest)"
  if [ -z "$digest" ]; then
    verdict "$name" UNKNOWN "no [container].digest field found in $LOCK"
  elif [[ "$digest" == UNKNOWN-TODO* ]]; then
    verdict "$name" PARTIAL_ALIVE "[container].digest is still the honest placeholder ('$digest'); not built/pushed yet, format check skipped (not a failure)"
  elif [[ "$digest" =~ ^sha256:[0-9a-f]{64}$ ]]; then
    verdict "$name" ALIVE "[container].digest matches sha256:[0-9a-f]{64}: $digest"
  else
    verdict "$name" BLOCKED "[container].digest set to a non-placeholder value that does NOT match sha256:[0-9a-f]{64}: '$digest'"
  fi
fi
echo

# --- (6) generated .github/workflows/*.yml match a fresh `ggen sync run --dry-run`
# Complements scripts/doctor.sh check #3 (which only diffs [packs.*] content_hash
# against ggen.lock) — this check instead inspects the dry-run's own "skipped:
# unchanged: content identical" / "written" verdict for the workflow files
# themselves, which doctor.sh does not do. No docker involved; this is `ggen
# sync run --dry-run`, a read-only planning pass over already-checked-out
# vendor/ggen and vendor/ggen-marketplace sources.
name="6-workflow-drift"
WORKFLOWS=(".github/workflows/ggen-ecosystem-sync.yml" ".github/workflows/ggen-ecosystem-container.yml")
if ! command -v ggen >/dev/null 2>&1; then
  verdict "$name" BLOCKED "ggen not on PATH, cannot run dry-run sync"
else
  missing=0
  for f in "${WORKFLOWS[@]}"; do
    [ -f "$f" ] || { verdict "$name" BLOCKED "expected generated file missing: $f"; missing=1; }
  done
  if [ "$missing" -eq 0 ]; then
    dry_out="$(ggen sync run --dry-run --format json-pretty 2>&1)"
    dry_rc=$?
    if [ "$dry_rc" -ne 0 ]; then
      verdict "$name" BUILD_BROKEN "ggen sync run --dry-run exited $dry_rc: $(echo "$dry_out" | tail -3 | tr '\n' ' ')"
    else
      json_only="$(echo "$dry_out" | sed -n '/^{/,/^}/p')"
      drift=0
      for f in "${WORKFLOWS[@]}"; do
        if echo "$json_only" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(2)
f = '$f'
written = [w[0] if isinstance(w, list) else w for w in d.get('written', [])]
decisions = d.get('decisions', {})
if f in written:
    sys.exit(1)
dec = decisions.get(f, '')
if 'unchanged' in dec:
    sys.exit(0)
sys.exit(3)
" 2>/dev/null; then
          : # unchanged, no drift
        else
          rc=$?
          if [ "$rc" -eq 1 ]; then
            echo "    DRIFT: $f would be (re)written by a fresh ggen sync run — on-disk file does not match ontology-generated content"
          else
            echo "    UNKNOWN: $f not mentioned as 'written' or 'unchanged' in dry-run output (decision unclear)"
          fi
          drift=1
        fi
      done
      if [ "$drift" -eq 0 ]; then
        verdict "$name" ALIVE "fresh --dry-run reports all ${#WORKFLOWS[@]} generated workflow file(s) unchanged: content identical to on-disk"
      else
        verdict "$name" BLOCKED "one or more generated workflow files drifted from what --dry-run would (re)generate — see DRIFT lines above"
      fi
    fi
  fi
fi
echo

echo "== summary: $([ "$FAIL" -eq 0 ] && echo 'no BLOCKED/BUILD_BROKEN/UNKNOWN verdicts' || echo 'one or more checks BLOCKED/BUILD_BROKEN/UNKNOWN — see above') =="
exit "$FAIL"
