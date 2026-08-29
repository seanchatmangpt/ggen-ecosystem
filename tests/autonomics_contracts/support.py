"""Isolated loader for the BRCE autonomics module.

The production module imports the real gymact package.  These contracts replace
only that import boundary with recording value objects; subprocess execution is
still refused unless an individual test explicitly supplies a recorder.
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Value:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Ledger:
    instances = []

    def __init__(self, path):
        self.path = path
        self.items = []
        type(self).instances.append(self)

    def append(self, receipt):
        self.items.append(receipt)


def load_module(*, admitted=True):
    gymact = types.ModuleType("gymact")
    for name in (
        "ActionDefinition", "ExpectedEffect", "VerificationStrategy",
        "AuthorityRequirement", "SubjectRef", "PreparedAction",
        "ExecutionGrant",
    ):
        setattr(gymact, name, type(name, (Value,), {}))
    class Receipt(Value):
        def __init__(self, **kwargs):
            super().__init__(receipt_id="contract-receipt", **kwargs)
    gymact.Receipt = Receipt
    gymact.VerificationKind = types.SimpleNamespace(PROCESS_CONFORMANCE="PROCESS_CONFORMANCE")
    gymact.IdempotencyClass = types.SimpleNamespace(IDEMPOTENT="IDEMPOTENT")
    gymact.ReversalClass = types.SimpleNamespace(REVERSIBLE="REVERSIBLE")
    gymact.Standing = types.SimpleNamespace(PARTIAL_ALIVE="PARTIAL_ALIVE", ALIVE="ALIVE", BLOCKED="BLOCKED")
    gymact.Operation = types.SimpleNamespace(ACT="ACT")
    gymact.SQLiteReceiptLedger = Ledger
    gymact.admit_execution = lambda *args, **kwargs: Value(admitted=admitted)
    sys.modules["gymact"] = gymact
    spec = importlib.util.spec_from_file_location("autonomics_gymact_contract_subject", ROOT / "scripts" / "autonomics_gymact.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
