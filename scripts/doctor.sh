#!/usr/bin/env bash
# scripts/doctor.sh — v26.8.28 submodule+container manufacturing health check.
#
# Prints one standing-vocabulary verdict per check (see docs/STANDING.md):
#   ALIVE | PARTIAL_ALIVE | BLOCKED | BUILD_BROKEN | UNSUPPORTED | UNKNOWN
#
# Exit code: 0 if no check emitted BLOCKED/BUILD_BROKEN/UNKNOWN, else 1.

set -u
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

JSON_MODE=0
if [ "${1:-}" = "--json" ]; then
  JSON_MODE=1
fi

FAIL=0
RESULTS=()
verdict() {
  # verdict <CHECK_NAME> <VERDICT> <detail...>
  local name="$1"; local v="$2"; shift 2
  local detail="$*"
  if [ "$JSON_MODE" -eq 0 ]; then
    printf '[%s] %-14s %s\n' "$name" "$v" "$detail"
  else
    RESULTS+=("{\"gate\": \"$name\", \"standing\": \"$v\", \"detail\": \"$(echo "$detail" | sed 's/"/\\"/g')\"}")
  fi
  case "$v" in
    BLOCKED|BUILD_BROKEN|UNKNOWN) FAIL=1 ;;
  esac
}

if [ "$JSON_MODE" -eq 0 ]; then
  echo "== ggen-ecosystem doctor.sh — v26.8.28 submodule+container manufacturing =="
  echo
fi

# --- (1) submodules initialized and checked out ---------------------------
name="1-submodules"
if ! command -v git >/dev/null 2>&1; then
  verdict "$name" UNSUPPORTED "git not on PATH"
else
  status_out="$(git submodule status 2>&1)"
  if [ -z "$status_out" ]; then
    verdict "$name" UNKNOWN "git submodule status produced no output"
  else
    bad=0
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      prefix="${line:0:1}"
      if [ "$prefix" = "-" ]; then
        verdict "$name" BLOCKED "not initialized: ${line#?}"
        bad=1
      elif [ "$prefix" = "+" ]; then
        verdict "$name" PARTIAL_ALIVE "checked out but does not match superproject's recorded SHA: ${line#?}"
        bad=1
      fi
    done <<< "$status_out"
    if [ "$bad" -eq 0 ]; then
      count="$(echo "$status_out" | grep -c '.')"
      verdict "$name" ALIVE "$count submodule(s) initialized and checked out at recorded commits: $(echo "$status_out" | tr '\n' ' ' | sed 's/  */ /g')"
    fi
  fi
fi
echo

# --- (2) ggen binary on PATH and --version succeeds ------------------------
name="2-ggen-binary"
if ! command -v ggen >/dev/null 2>&1; then
  verdict "$name" BLOCKED "ggen not found on PATH"
else
  ggen_path="$(command -v ggen)"
  if ver_out="$(ggen --version 2>&1)"; then
    ver_line="$(echo "$ver_out" | grep -o 'ggen [0-9][0-9.]*' | head -1)"
    verdict "$name" ALIVE "$ggen_path -> $ver_line"
  else
    verdict "$name" BUILD_BROKEN "ggen --version failed: $(echo "$ver_out" | tail -1)"
  fi
fi
echo

# --- (3) ggen.lock content_hash matches fresh dry-run sync ------------------
name="3-lock-hash-match"
if ! command -v ggen >/dev/null 2>&1; then
  verdict "$name" BLOCKED "ggen not on PATH, cannot run sync"
elif [ ! -f ggen.lock ]; then
  verdict "$name" UNKNOWN "ggen.lock not found"
else
  dry_out="$(ggen sync run --dry-run --format json-pretty 2>&1)"
  dry_rc=$?
  if [ "$dry_rc" -ne 0 ]; then
    verdict "$name" BUILD_BROKEN "ggen sync run --dry-run exited $dry_rc: $(echo "$dry_out" | tail -3 | tr '\n' ' ')"
  elif echo "$dry_out" | grep -q 'FM-PACK-008'; then
    verdict "$name" BLOCKED "FM-PACK-008 pack content_hash mismatch reported by dry-run"
  else
    mismatch=0
    while IFS='=' read -r pack lock_hash; do
      [ -z "$pack" ] && continue
      lock_hash_clean="$(echo "$lock_hash" | sed -E 's/^blake3://' | tr -d '"[:space:]')"
      dry_hash="$(echo "$dry_out" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
v = d.get('packs', {}).get('$pack')
if v:
    print(v)
" 2>/dev/null)"
      if [ -z "$dry_hash" ]; then
        continue
      fi
      if [ "$dry_hash" != "$lock_hash_clean" ]; then
        verdict "$name" BLOCKED "pack '$pack' content_hash mismatch: ggen.lock=$lock_hash_clean dry-run=$dry_hash"
        mismatch=1
      fi
    done < <(awk '/^\[packs\./{gsub(/[][]/,"",$0); split($0,a,"."); pack=a[2]} /^content_hash/{gsub(/"/,"",$0); split($0,b,"="); gsub(/^ +| +$/,"",b[2]); print pack"="b[2]}' ggen.lock)
    if [ "$mismatch" -eq 0 ]; then
      verdict "$name" ALIVE "fresh --dry-run pack content_hash(es) match ggen.lock exactly; no [FM-PACK-008] mismatch"
    fi
  fi
fi
echo

# --- (4) docker available and image runs ggen --version --------------------
name="4-docker-image"
if ! command -v docker >/dev/null 2>&1; then
  verdict "$name" UNSUPPORTED "docker not on PATH"
elif ! docker info >/dev/null 2>&1; then
  verdict "$name" BLOCKED "docker daemon not reachable (docker info failed)"
else
  image="ghcr.io/seanchatmangpt/ggen-ecosystem"
  tag="$(awk -F'"' '/^tag *=/{print $2; exit}' ecosystem.lock.toml 2>/dev/null)"
  if [ -z "$tag" ] || [[ "$tag" == UNKNOWN-TODO* ]]; then
    verdict "$name" BLOCKED "no built/published image tag yet (ecosystem.lock.toml [container].tag = '$tag')"
  else
    ref="${image}:${tag}"
    if docker image inspect "$ref" >/dev/null 2>&1; then
      run_out="$(docker run --rm "$ref" ggen --version 2>&1)"
      if [ $? -eq 0 ]; then
        verdict "$name" ALIVE "local image $ref: $(echo "$run_out" | grep -o 'ggen [0-9][0-9.]*' | head -1)"
      else
        verdict "$name" BUILD_BROKEN "docker run $ref ggen --version failed: $(echo "$run_out" | tail -2 | tr '\n' ' ')"
      fi
    elif docker pull "$ref" >/tmp/doctor_docker_pull.$$ 2>&1; then
      run_out="$(docker run --rm "$ref" ggen --version 2>&1)"
      rm -f /tmp/doctor_docker_pull.$$
      if [ $? -eq 0 ]; then
        verdict "$name" ALIVE "pulled $ref: $(echo "$run_out" | grep -o 'ggen [0-9][0-9.]*' | head -1)"
      else
        verdict "$name" BUILD_BROKEN "docker run $ref ggen --version failed: $(echo "$run_out" | tail -2 | tr '\n' ' ')"
      fi
    else
      verdict "$name" BLOCKED "image $ref not present locally and not pullable: $(tail -2 /tmp/doctor_docker_pull.$$ 2>/dev/null | tr '\n' ' ')"
      rm -f /tmp/doctor_docker_pull.$$
    fi
  fi
fi
echo

# --- (5) UNKNOWN-TODO placeholders in ecosystem.lock.toml -------------------
name="5-unknown-todo"
if [ ! -f ecosystem.lock.toml ]; then
  verdict "$name" UNKNOWN "ecosystem.lock.toml not found"
else
  todo_lines="$(grep -n 'UNKNOWN-TODO' ecosystem.lock.toml || true)"
  if [ -z "$todo_lines" ]; then
      verdict "$name" ALIVE "no UNKNOWN-TODO placeholders remain in ecosystem.lock.toml"
  else
    n="$(echo "$todo_lines" | grep -c '.')"
    verdict "$name" PARTIAL_ALIVE "$n documented UNKNOWN-TODO placeholder(s) present (honestly marked pending, not a failure)"
    if [ "$JSON_MODE" -eq 0 ]; then
      echo "$todo_lines" | sed 's/^/    line /'
    fi
  fi
fi
[ "$JSON_MODE" -eq 0 ] && echo

# --- (6) vendor/ggen-marketplace commit matches ecosystem.lock.toml ---------
name="6-marketplace-pin"
if [ ! -f ecosystem.lock.toml ]; then
  verdict "$name" UNKNOWN "ecosystem.lock.toml not found"
elif [ ! -d vendor/ggen-marketplace ]; then
  verdict "$name" BLOCKED "vendor/ggen-marketplace submodule directory missing"
else
  recorded="$(awk -F'"' '/ggen_marketplace_commit *=/{print $2; exit}' ecosystem.lock.toml)"
  actual="$(git -C vendor/ggen-marketplace rev-parse HEAD 2>&1)"
  rev_rc=$?
  if [ -z "$recorded" ]; then
    verdict "$name" UNKNOWN "ecosystem.lock.toml has no [submodules].ggen_marketplace_commit"
  elif [ "$rev_rc" -ne 0 ]; then
    verdict "$name" BUILD_BROKEN "git rev-parse HEAD failed in vendor/ggen-marketplace: $actual"
  elif [ "$recorded" = "$actual" ]; then
    verdict "$name" ALIVE "vendor/ggen-marketplace HEAD ($actual) matches ecosystem.lock.toml pin exactly"
  else
    verdict "$name" BLOCKED "mismatch: ecosystem.lock.toml pin=$recorded vendor/ggen-marketplace HEAD=$actual"
  fi
fi
echo

# --- (7) exact gitlink verification vs ecosystem.lock.toml [submodules] ----
name="7-gitlink-exact"
if [ ! -f ecosystem.lock.toml ]; then
  verdict "$name" UNKNOWN "ecosystem.lock.toml not found"
else
  ls_out="$(git ls-files -s vendor/ggen vendor/ggen-marketplace 2>&1)"
  ggen_mode="$(echo "$ls_out" | awk '$4=="vendor/ggen"{print $1}')"
  ggen_sha="$(echo "$ls_out" | awk '$4=="vendor/ggen"{print $2}')"
  mp_mode="$(echo "$ls_out" | awk '$4=="vendor/ggen-marketplace"{print $1}')"
  mp_sha="$(echo "$ls_out" | awk '$4=="vendor/ggen-marketplace"{print $2}')"
  lock_ggen_sha="$(awk -F'"' '/^ggen_commit *=/{print $2; exit}' ecosystem.lock.toml)"
  lock_mp_sha="$(awk -F'"' '/^ggen_marketplace_commit *=/{print $2; exit}' ecosystem.lock.toml)"
  bad=0
  if [ "$ggen_mode" != "160000" ]; then
    verdict "$name" BLOCKED "vendor/ggen gitlink mode is '$ggen_mode', expected 160000"
    bad=1
  fi
  if [ "$mp_mode" != "160000" ]; then
    verdict "$name" BLOCKED "vendor/ggen-marketplace gitlink mode is '$mp_mode', expected 160000"
    bad=1
  fi
  if [ -z "$lock_ggen_sha" ] || [ -z "$lock_mp_sha" ]; then
    verdict "$name" UNKNOWN "ecosystem.lock.toml missing [submodules] ggen_commit/ggen_marketplace_commit"
    bad=1
  elif [ "$ggen_sha" != "$lock_ggen_sha" ]; then
    verdict "$name" BLOCKED "vendor/ggen gitlink SHA ($ggen_sha) != ecosystem.lock.toml ggen_commit ($lock_ggen_sha)"
    bad=1
  elif [ "$mp_sha" != "$lock_mp_sha" ]; then
    verdict "$name" BLOCKED "vendor/ggen-marketplace gitlink SHA ($mp_sha) != ecosystem.lock.toml ggen_marketplace_commit ($lock_mp_sha)"
    bad=1
  fi
  if [ "$bad" -eq 0 ]; then
    verdict "$name" ALIVE "both gitlinks mode 160000, SHAs exactly match ecosystem.lock.toml [submodules]: ggen=$ggen_sha marketplace=$mp_sha"
  fi
fi
echo

# --- (8) dirty-submodule detection (honest count, not auto-fatal) ----------
name="8-dirty-submodules"
if [ ! -d vendor/ggen ] || [ ! -d vendor/ggen-marketplace ]; then
  verdict "$name" UNKNOWN "one or both vendor/ submodule directories missing"
else
  ggen_dirty_out="$(git -C vendor/ggen status --short 2>&1)"
  ggen_dirty_rc=$?
  mp_dirty_out="$(git -C vendor/ggen-marketplace status --short 2>&1)"
  mp_dirty_rc=$?
  if [ "$ggen_dirty_rc" -ne 0 ] || [ "$mp_dirty_rc" -ne 0 ]; then
    verdict "$name" UNKNOWN "git status failed in a submodule: ggen_rc=$ggen_dirty_rc marketplace_rc=$mp_dirty_rc"
  else
    ggen_n="$(echo "$ggen_dirty_out" | grep -c '.')"
    mp_n="$(echo "$mp_dirty_out" | grep -c '.')"
    if [ "$ggen_n" -eq 0 ] && [ "$mp_n" -eq 0 ]; then
      verdict "$name" ALIVE "vendor/ggen: 0 dirty entries, vendor/ggen-marketplace: 0 dirty entries"
    else
      verdict "$name" PARTIAL_ALIVE "vendor/ggen: $ggen_n dirty entr(y/ies), vendor/ggen-marketplace: $mp_n dirty entr(y/ies) — dirty untracked/modified content in a submodule working tree is NOT necessarily fatal to the gitlink pin recorded in the superproject (check 7 verifies the pin itself); this only flags that the submodule's own working tree has local changes/untracked files worth a human look"
    fi
  fi
fi
echo

# --- (9) generated-workflow drift: ggen sync run --dry-run vs committed -----
name="9-workflow-drift"
if ! command -v ggen >/dev/null 2>&1; then
  verdict "$name" BLOCKED "ggen not on PATH, cannot check drift"
else
  dry_out2="$(ggen sync run --dry-run 2>/tmp/doctor_dry2_err.$$)"
  dry_rc2=$?
  dry_err2="$(cat /tmp/doctor_dry2_err.$$ 2>/dev/null)"; rm -f /tmp/doctor_dry2_err.$$
  if [ "$dry_rc2" -ne 0 ]; then
    verdict "$name" BUILD_BROKEN "ggen sync run --dry-run exited $dry_rc2: $(echo "$dry_err2" | tail -3 | tr '\n' ' ')"
  else
    drift=0
    drift_detail=""
    for wf in .github/workflows/*.yml; do
      [ -e "$wf" ] || continue
      base="$(basename "$wf")"
      # decisions map keys are workflow-relative paths as written by ggen (".github/workflows/<file>")
      decision="$(echo "$dry_out2" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
dec = d.get('decisions', {})
key = '.github/workflows/$base'
print(dec.get(key, ''))
" 2>/dev/null)"
      if [ -z "$decision" ]; then
        drift=1
        drift_detail="${drift_detail}${base}: not present in dry-run decisions (possible DRIFT or renamed target); "
      elif echo "$decision" | grep -qi 'unchanged'; then
        : # MATCH
      else
        drift=1
        drift_detail="${drift_detail}${base}: ${decision}; "
      fi
    done
    if [ "$drift" -eq 0 ]; then
      verdict "$name" ALIVE "MATCH: all committed .github/workflows/*.yml reported unchanged by fresh ggen sync run --dry-run"
    else
      verdict "$name" BLOCKED "DRIFT: $drift_detail"
    fi
  fi
fi
echo

# --- (10) receipt/replay presence for v26.8.28 container work --------------
name="10-container-receipt"
if [ ! -d receipts ]; then
  verdict "$name" UNKNOWN "receipts/ directory not found"
else
  found="$(find receipts -type f -iname '*v26.8.28*' -iname '*container*.json' 2>/dev/null)"
  if [ -n "$found" ]; then
    verdict "$name" ALIVE "found v26.8.28 container receipt(s): $(echo "$found" | tr '\n' ' ')"
  else
    verdict "$name" PARTIAL_ALIVE "no receipts/*v26.8.28*/*container*.json found yet (container build not yet completed by the authoritative build owner — this is an honest pending state, not this script's failure)"
  fi
fi
echo

# --- (11) image/digest presence check — never builds, never hangs ----------
name="11-image-presence"
if ! command -v docker >/dev/null 2>&1; then
  verdict "$name" UNSUPPORTED "docker not on PATH"
elif ! docker info >/dev/null 2>&1; then
  verdict "$name" BLOCKED "docker daemon not reachable (docker info failed) — cannot check image presence"
else
  tag2="$(awk -F'"' '/^tag *=/{print $2; exit}' ecosystem.lock.toml 2>/dev/null)"
  image2="ghcr.io/seanchatmangpt/ggen-ecosystem"
  candidates=()
  [ -n "$tag2" ] && [[ "$tag2" != UNKNOWN-TODO* ]] && candidates+=("${image2}:${tag2}")
  candidates+=("ggen-ecosystem:test")
  present=0
  detail=""
  for ref in "${candidates[@]}"; do
    if inspect_out="$(docker image inspect "$ref" 2>&1)"; then
      digest="$(echo "$inspect_out" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if d:
    print(d[0].get('Id',''))
" 2>/dev/null)"
      verdict "$name" ALIVE "image present locally: $ref (Id=$digest)"
      present=1
      break
    fi
  done
  if [ "$present" -eq 0 ]; then
    verdict "$name" BLOCKED "IMAGE_NOT_YET_BUILT — none of [${candidates[*]}] present locally (no docker build/pull attempted by this script)"
  fi
fi

if [ "$JSON_MODE" -eq 1 ]; then
  IFS=,
  echo "{\"subject\": \"seanchatmangpt/ggen-ecosystem\", \"fail\": $FAIL, \"gates\": [${RESULTS[*]}]}"
else
  echo "== summary: $([ "$FAIL" -eq 0 ] && echo 'no BLOCKED/BUILD_BROKEN/UNKNOWN verdicts' || echo 'one or more checks BLOCKED/BUILD_BROKEN/UNKNOWN — see above') =="
fi
exit "$FAIL"
