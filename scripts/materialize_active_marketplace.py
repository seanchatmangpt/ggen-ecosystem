#!/usr/bin/env python3
"""Materialize the canonical active ggen Marketplace surface for runtime images.

The source checkout intentionally preserves the full legacy corpus. Runtime
consumers must not infer public capability identity from every directory under
packs/. This script projects marketplace.active.toml into an exact runtime
surface and refuses drift.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("REFUSED:PYTHON_3_11_REQUIRED") from exc


SCHEMA = "https://ggen.dev/marketplace/runtime-surface/v1"


class SurfaceError(ValueError):
    pass


def load_active(root: Path) -> tuple[str, tuple[str, ...]]:
    path = root / "marketplace.active.toml"
    if not path.is_file():
        raise SurfaceError(f"ACTIVE_SCOPE_MISSING:{path}")

    try:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise SurfaceError(f"ACTIVE_SCOPE_INVALID:{exc}") from exc

    active = document.get("active")
    if not isinstance(active, dict):
        raise SurfaceError("ACTIVE_SCOPE_INVALID:missing [active]")

    front_door = active.get("front_door")
    packs = active.get("packs")

    if not isinstance(front_door, str) or not front_door:
        raise SurfaceError("ACTIVE_SCOPE_INVALID:active.front_door")

    if (
        not isinstance(packs, list)
        or not packs
        or not all(isinstance(name, str) and name for name in packs)
    ):
        raise SurfaceError("ACTIVE_SCOPE_INVALID:active.packs")

    names = tuple(packs)
    if len(names) != len(set(names)):
        raise SurfaceError("ACTIVE_SCOPE_DUPLICATE:active.packs")
    if tuple(sorted(names)) != names:
        raise SurfaceError("ACTIVE_SCOPE_ORDER:active.packs")
    if front_door not in names:
        raise SurfaceError(f"ACTIVE_FRONT_DOOR_NOT_ADMITTED:{front_door}")

    return front_door, names


def direct_pack_dirs(root: Path) -> dict[str, Path]:
    packs_root = root / "packs"
    if not packs_root.is_dir():
        raise SurfaceError(f"PACKS_ROOT_MISSING:{packs_root}")
    return {
        child.name: child
        for child in packs_root.iterdir()
        if child.is_dir() and not child.name.startswith(".")
    }


def materialize(root: Path, prune: bool) -> dict[str, object]:
    front_door, active = load_active(root)
    active_set = set(active)
    before = direct_pack_dirs(root)

    missing = sorted(name for name in active if name not in before)
    if missing:
        raise SurfaceError("ACTIVE_PACK_MISSING:" + ",".join(missing))

    missing_manifest = sorted(
        name for name in active if not (before[name] / "pack.toml").is_file()
    )
    if missing_manifest:
        raise SurfaceError("ACTIVE_PACK_MANIFEST_MISSING:" + ",".join(missing_manifest))

    extras = sorted(set(before) - active_set)
    removed: list[str] = []

    if prune:
        for name in extras:
            shutil.rmtree(before[name])
            removed.append(name)

    after = direct_pack_dirs(root)
    visible = tuple(sorted(after))

    if visible != active:
        extra_after = sorted(set(visible) - active_set)
        missing_after = sorted(active_set - set(visible))
        detail = {
            "extra": extra_after,
            "missing": missing_after,
        }
        raise SurfaceError("RUNTIME_SURFACE_DRIFT:" + json.dumps(detail, sort_keys=True))

    return {
        "schema": SCHEMA,
        "front_door": front_door,
        "active_count": len(active),
        "active_packs": list(active),
        "source_pack_count": len(before),
        "removed_count": len(removed),
        "removed_packs": removed,
        "visible_pack_count": len(visible),
        "visible_packs": list(visible),
        "standing": "ALIVE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument(
        "--prune",
        action="store_true",
        help="delete non-active direct pack directories before exact-surface verification",
    )
    args = parser.parse_args()

    try:
        receipt = materialize(args.root, args.prune)
    except SurfaceError as exc:
        print(f"REFUSED:{exc}", file=sys.stderr)
        return 2

    json.dump(receipt, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
