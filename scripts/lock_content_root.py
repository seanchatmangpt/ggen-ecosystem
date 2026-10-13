#!/usr/bin/env python3
"""Lock content root (C18 hermetic pins, L91).

Computes a deterministic content root over the pin surfaces of
ecosystem.lock.toml. Each pin identity (repo + path + pin value) is
canonicalized to sorted "key=value" lines and hashed; the sorted digest
concatenation is hashed again to fold a single root.

Determinism: two runs are byte-identical regardless of key order in the TOML.

Usage:
  python3 scripts/lock_content_root.py [--lock PATH] [--out PATH] [--head-sha SHA]
  python3 scripts/lock_content_root.py --check [--root-file PATH]

Output JSON: {"pins": {path: digest}, "root": ..., "lock_head_sha": ...}
--check recomputes the root and compares against the committed .lock-root
golden file; exit 1 naming the diverging pins on mismatch.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover
    tomllib = None

DEFAULT_LOCK = Path(__file__).resolve().parents[1] / "ecosystem.lock.toml"

# Pin surfaces: section -> key holding the pin path (identity) and the key(s)
# holding the pin value. Submodules are path/commit pairs; other sections pin
# an artifact by their sha/digest fields.
PIN_SURFACES = {
    "submodules": None,  # pairs x_path / x_commit
    "ggen": ("commit_sha",),
    "ggen_marketplace": ("sha",),
    "ggen_igniter": ("sha",),
    "beam4pm": ("sha",),
    "wasm4pm": ("sha",),
    "container": ("digest", "observed_success_head_sha"),
}


def _canon(lines: list[str]) -> str:
    return "\n".join(sorted(lines))


def _digest(identity: str, value: str) -> str:
    h = hashlib.sha256()
    h.update(identity.encode("utf-8"))
    h.update(b"\x00")
    h.update(_canon(["repo=ggen-ecosystem", f"path={identity}", f"value={value}"]).encode("utf-8"))
    return h.hexdigest()


def extract_pins(lock: dict) -> dict[str, str]:
    """Return {pin_path: pin_value} from a parsed lock table."""
    pins: dict[str, str] = {}
    subs = lock.get("submodules", {})
    for k in sorted(subs):
        if k.endswith("_path"):
            commit_key = k[: -len("_path")] + "_commit"
            if commit_key in subs:
                pins[subs[k]] = subs[commit_key]
    for section, keys in PIN_SURFACES.items():
        if section == "submodules" or section not in lock:
            continue
        tbl = lock[section]
        for key in keys:
            if key in tbl:
                pins[f"{section}/{key}"] = str(tbl[key])
    return pins


def fold_root(pin_digests: dict[str, str]) -> str:
    """Fold sorted pin digests into a single content root."""
    concat = "".join(pin_digests[p] for p in sorted(pin_digests))
    return hashlib.sha256(concat.encode("utf-8")).hexdigest()


def compute_root(lock_path: Path = DEFAULT_LOCK, head_sha: str | None = None) -> dict:
    if tomllib is None:
        raise SystemExit("python 3.11+ required (tomllib)")
    lock_path = Path(lock_path)
    raw = lock_path.read_bytes()
    lock = tomllib.loads(raw.decode("utf-8"))
    pins = extract_pins(lock)
    if not pins:
        raise SystemExit(f"no pins found in {lock_path}")
    digests = {p: _digest(p, v) for p, v in pins.items()}
    resolved_head = head_sha or lock.get("base_main_sha")
    if not resolved_head:
        raise SystemExit("no head sha available (pass --head-sha)")
    return {
        "pins": digests,
        "root": fold_root(digests),
        "lock_head_sha": resolved_head,
    }


def _write(result: dict, out: Path | None) -> None:
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if out:
        out.write_text(text)
    else:
        sys.stdout.write(text)


def main(argv: list[str]) -> int:
    args = list(argv)
    lock_path = DEFAULT_LOCK
    out = None
    head_sha = None
    check = False
    root_file = Path(__file__).resolve().parents[1] / ".lock-root"
    it = iter(args)
    for a in it:
        if a == "--lock":
            lock_path = Path(next(it))
        elif a == "--out":
            out = Path(next(it))
        elif a == "--head-sha":
            head_sha = next(it)
        elif a == "--check":
            check = True
        elif a == "--root-file":
            root_file = Path(next(it))
        else:
            raise SystemExit(f"unknown argument {a!r}")
    result = compute_root(lock_path, head_sha)
    if not check:
        _write(result, out)
        return 0
    if not root_file.exists():
        print(f"REFUSED[LOCK_ROOT_MISSING]: {root_file} does not exist", file=sys.stderr)
        return 1
    expected = json.loads(root_file.read_text())
    root_file_path = expected.get("path", ".lock-root")
    drift = sorted(
        p
        for p in sorted(set(result["pins"]) | set(expected.get("pins", {})))
        if result["pins"].get(p) != expected.get("pins", {}).get(p)
    )
    if expected.get("root") != result["root"] or drift:
        print(f"REFUSED[LOCK_ROOT_DIVERGED]: root {root_file_path}", file=sys.stderr)
        print(f"  expected root: {expected.get('root')}", file=sys.stderr)
        print(f"  observed root: {result['root']}", file=sys.stderr)
        for p in drift:
            print(
                f"  pin {p}: expected {expected.get('pins', {}).get(p)} "
                f"observed {result['pins'].get(p)}",
                file=sys.stderr,
            )
        return 1
    print(f"ALIVE: lock content root matches {root_file_path} ({result['root']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
