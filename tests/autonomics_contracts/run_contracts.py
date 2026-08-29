#!/usr/bin/env python3
"""Run autonomics contracts with the Python standard library only."""
from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


class MonkeyPatch:
    def __init__(self):
        self.undo = []

    def setattr(self, obj, name, value):
        old = getattr(obj, name)
        self.undo.append((obj, name, old))
        setattr(obj, name, value)

    def restore(self):
        for obj, name, old in reversed(self.undo):
            setattr(obj, name, old)


def main() -> int:
    failures = []
    paths = sorted(HERE.glob("test_*.py"))
    for path in paths:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            tests = [value for name, value in vars(module).items() if name.startswith("test_") and callable(value)]
            assert len(tests) == 1, f"expected one court, found {len(tests)}"
            test = tests[0]
            patch = MonkeyPatch()
            try:
                if len(inspect.signature(test).parameters) == 1:
                    test(patch)
                else:
                    test()
            finally:
                patch.restore()
            print(f"PASS {path.name}")
        except Exception as exc:
            failures.append((path.name, exc))
            print(f"FAIL {path.name}: {exc}", file=sys.stderr)
    print(f"RESULT {len(paths) - len(failures)}/{len(paths)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
