#!/usr/bin/env python3
"""Execute a ggen-manufactured supply-chain evidence court.

Authority lives in manufacturing/supply-chain/ontology.ttl plus the pinned
supply-chain-evidence marketplace pack. This runtime is deliberately generic:
it builds the observed bundle, applies declarative mutations, and interprets
the generated assertion DSL. Refusal codes are data, not handwritten branches.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
import tomllib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
COURT = ROOT / "manufacturing/supply-chain/generated/supply-chain-evidence-cases.json"


def head_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def load_lock() -> dict[str, Any]:
    return tomllib.loads((ROOT / "ecosystem.lock.toml").read_text(encoding="utf-8"))


def base_bundle(lock: dict[str, Any], head: str) -> dict[str, Any]:
    image = lock["container"]["repository"]
    tag = lock["container"]["tag"]
    digest = lock["container"]["digest"].removeprefix("sha256:")
    ggen = lock["ggen"]["commit_sha"]
    market = lock["ggen_marketplace"]["sha"]
    autofde = lock["submodules"]["autofde_lab_commit"]
    subject = f"{image}@sha256:{digest}"
    return {
        "provenance": {
            "_type": "https://in-toto.io/Statement/v1",
            "subject": [{"name": subject, "digest": {"sha256": digest}}],
            "predicateType": "https://slsa.dev/provenance/v1",
            "predicate": {
                "buildDefinition": {
                    "buildType": "https://github.com/Attestations/GitHubActionsWorkflow@v1",
                    "externalParameters": {"source": {
                        "uri": "git+https://github.com/seanchatmangpt/ggen-ecosystem",
                        "digest": {"gitCommit": head},
                    }},
                    "internalParameters": {
                        "workflow": f".github/workflows/ggen-ecosystem-container.yml@{head}"
                    },
                    "resolvedDependencies": [
                        {"uri": "git+https://github.com/seanchatmangpt/ggen", "digest": {"gitCommit": ggen}},
                        {"uri": "git+https://github.com/seanchatmangpt/ggen-marketplace", "digest": {"gitCommit": market}},
                        {"uri": "git+https://github.com/seanchatmangpt/autofde-lab", "digest": {"gitCommit": autofde}},
                    ],
                },
                "runDetails": {
                    "builder": {"id": "https://github.com/actions/runner/github-hosted"},
                    "metadata": {
                        "invocationId": "https://github.com/seanchatmangpt/ggen-ecosystem/actions/runs/33244628216",
                        "startedOn": "2026-08-29T09:04:33Z",
                        "finishedOn": "2026-08-29T10:04:33Z",
                    },
                },
            },
        },
        "spdx": {
            "spdxVersion": "SPDX-2.3", "dataLicense": "CC0-1.0", "SPDXID": "SPDXRef-DOCUMENT",
            "name": "ggen-ecosystem-v26.8.28",
            "documentNamespace": f"https://github.com/seanchatmangpt/ggen-ecosystem/sbom/{head}",
            "creationInfo": {"created": "2026-08-29T10:04:33Z", "creators": ["Tool: ggen-ecosystem-supply-chain-court"]},
            "packages": [
                {"name": "ggen-ecosystem", "SPDXID": "SPDXRef-Package-ggen-ecosystem", "versionInfo": tag,
                 "downloadLocation": "NOASSERTION", "filesAnalyzed": False, "licenseConcluded": "NOASSERTION",
                 "licenseDeclared": "NOASSERTION", "supplier": "Organization: seanchatmangpt",
                 "checksums": [{"algorithm": "SHA256", "checksumValue": digest}]},
                {"name": "ggen", "SPDXID": "SPDXRef-Package-ggen", "versionInfo": ggen},
                {"name": "ggen-marketplace", "SPDXID": "SPDXRef-Package-marketplace", "versionInfo": market},
                {"name": "autofde-lab", "SPDXID": "SPDXRef-Package-autofde", "versionInfo": autofde},
            ],
            "relationships": [
                {"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES", "relatedSpdxElement": "SPDXRef-Package-ggen-ecosystem"},
                {"spdxElementId": "SPDXRef-Package-ggen-ecosystem", "relationshipType": "CONTAINS", "relatedSpdxElement": "SPDXRef-Package-ggen"},
                {"spdxElementId": "SPDXRef-Package-ggen-ecosystem", "relationshipType": "CONTAINS", "relatedSpdxElement": "SPDXRef-Package-marketplace"},
                {"spdxElementId": "SPDXRef-Package-ggen-ecosystem", "relationshipType": "CONTAINS", "relatedSpdxElement": "SPDXRef-Package-autofde"},
            ],
        },
        "cyclonedx": {
            "bomFormat": "CycloneDX", "specVersion": "1.6",
            "serialNumber": "urn:uuid:4d7b42d2-93d9-4f76-a121-72dd7f6f08aa", "version": 1,
            "metadata": {"timestamp": "2026-08-29T10:04:33Z", "component": {
                "type": "container", "bom-ref": subject, "name": "ggen-ecosystem", "version": tag,
                "hashes": [{"alg": "SHA-256", "content": digest}],
            }},
            "components": [
                {"type": "application", "bom-ref": f"ggen@{ggen}", "name": "ggen", "version": ggen},
                {"type": "data", "bom-ref": f"ggen-marketplace@{market}", "name": "ggen-marketplace", "version": market},
                {"type": "application", "bom-ref": f"autofde-lab@{autofde}", "name": "autofde-lab", "version": autofde},
            ],
            "dependencies": [{"ref": subject, "dependsOn": [f"ggen@{ggen}", f"ggen-marketplace@{market}", f"autofde-lab@{autofde}"]}],
        },
    }


_MISSING = object()


def at(root: Any, path: str) -> Any:
    if path.startswith("$"):
        return _MISSING
    node = root
    for part in path.split("."):
        try:
            node = node[int(part)] if isinstance(node, list) else node[part]
        except (KeyError, IndexError, TypeError, ValueError):
            return _MISSING
    return node


def context(lock: dict[str, Any], head: str) -> dict[str, str]:
    digest = lock["container"]["digest"].removeprefix("sha256:")
    return {
        "$head": head, "$digest": digest, "$tag": lock["container"]["tag"],
        "$subject": f'{lock["container"]["repository"]}@sha256:{digest}',
        "$ggen": lock["ggen"]["commit_sha"], "$market": lock["ggen_marketplace"]["sha"],
        "$autofde": lock["submodules"]["autofde_lab_commit"],
    }


def resolve(value: Any, ctx: dict[str, str]) -> Any:
    if isinstance(value, str):
        if value in ctx:
            return ctx[value]
        for key, replacement in ctx.items():
            value = value.replace(key, replacement)
        return value
    if isinstance(value, list):
        return [resolve(v, ctx) for v in value]
    if isinstance(value, dict):
        return {k: resolve(v, ctx) for k, v in value.items()}
    return value


def walk(node: Any):
    if isinstance(node, dict):
        for k, v in node.items():
            yield k, v
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def evaluate(bundle: dict[str, Any], assertion: dict[str, Any], ctx: dict[str, str]) -> bool:
    op = assertion["op"]
    path = assertion.get("path", "")
    value = resolve(assertion.get("value"), ctx)
    actual = at(bundle, path) if path else _MISSING
    if op == "always": return True
    if op == "eq": return actual is not _MISSING and actual == value
    if op == "len_eq": return actual is not _MISSING and hasattr(actual, "__len__") and len(actual) == value
    if op == "len_ge": return actual is not _MISSING and hasattr(actual, "__len__") and len(actual) >= value
    if op == "keys_eq": return isinstance(actual, dict) and set(actual) == set(value)
    if op == "regex": return isinstance(actual, str) and re.fullmatch(str(value), actual) is not None
    if op == "starts_with": return isinstance(actual, str) and actual.startswith(str(value))
    if op == "ends_with": return isinstance(actual, str) and actual.endswith(str(value))
    if op == "contains": return isinstance(actual, str) and str(value) in actual
    if op == "datetime": return parse_time(actual) is not None
    if op == "time_order":
        start, finish = parse_time(at(bundle, assertion["start"])), parse_time(at(bundle, assertion["finish"]))
        return start is not None and finish is not None and finish >= start
    if op == "int_ge": return isinstance(actual, int) and actual >= int(value)
    if op == "find_exists":
        return isinstance(actual, list) and any(isinstance(x, dict) and x.get(assertion["key"]) == value for x in actual)
    if op == "find_eq":
        if not isinstance(actual, list): return False
        for item in actual:
            if isinstance(item, dict) and item.get(assertion["key"]) == assertion["match"]:
                return item.get(assertion["field"], _MISSING) == value
        return False
    if op == "nested_any":
        if not isinstance(actual, list): return False
        target = next((x for x in actual if isinstance(x, dict) and x.get(assertion["key"]) == assertion["match"]), None)
        if not isinstance(target, dict) or not isinstance(target.get(assertion["field"]), list): return False
        wanted = resolve(assertion["where"], ctx)
        return any(isinstance(x, dict) and all(x.get(k) == v for k, v in wanted.items()) for x in target[assertion["field"]])
    if op == "nested_any_simple":
        if not isinstance(actual, list): return False
        wanted = resolve(assertion["where"], ctx)
        return any(isinstance(x, dict) and all(x.get(k) == v for k, v in wanted.items()) for x in actual)
    if op == "contains_map": return isinstance(actual, list) and resolve(assertion["value"], ctx) in actual
    if op == "set_eq": return isinstance(actual, list) and set(actual) == set(resolve(assertion["value"], ctx))
    if op == "all_equal":
        vals = [ctx[p] if p.startswith("$") else at(bundle, p) for p in assertion["paths"]]
        return _MISSING not in vals and len(set(vals)) == 1
    if op == "no_value_regex":
        rx = re.compile(str(value), re.I)
        return not any(isinstance(v, str) and rx.search(v) for _, v in walk(bundle))
    if op == "no_secret_values":
        rx = re.compile(assertion["key_regex"], re.I)
        return not any(rx.search(str(k)) and v not in (None, "", [], {}) for k, v in walk(bundle))
    raise ValueError(f"unknown assertion op: {op}")


def mutate(root: Any, mutation: dict[str, Any]) -> None:
    if not mutation: return
    parts = mutation["path"].split(".")
    node = root
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    leaf = parts[-1]
    if mutation.get("op", "set") == "delete":
        if isinstance(node, list): del node[int(leaf)]
        else: node.pop(leaf, None)
    else:
        if isinstance(node, list): node[int(leaf)] = copy.deepcopy(mutation.get("value"))
        else: node[leaf] = copy.deepcopy(mutation.get("value"))


def load_court() -> list[dict[str, Any]]:
    doc = json.loads(COURT.read_text(encoding="utf-8"))
    if doc.get("schema") != "ggen.supply-chain-evidence.court/v1": raise ValueError("REFUSED[COURT_SCHEMA]")
    cases = doc.get("cases")
    if not isinstance(cases, list) or len(cases) != 80: raise ValueError("REFUSED[COURT_CARDINALITY]")
    ordinals = [c.get("ordinal") for c in cases]
    if ordinals != sorted(ordinals) or len(set(ordinals)) != len(ordinals): raise ValueError("REFUSED[COURT_ORDER]")
    return cases


def run_case(case: dict[str, Any], all_cases: list[dict[str, Any]], lock: dict[str, Any], head: str) -> tuple[bool, str]:
    bundle = base_bundle(lock, head)
    mutate(bundle, case["mutation"])
    ctx = context(lock, head)
    failed = sorted(c["expected"] for c in all_cases if c["expected"] != "ALIVE" and not evaluate(bundle, c["assertion"], ctx))
    expected = case["expected"]
    ok = (not failed) if expected == "ALIVE" else expected in failed
    return ok, f"{'ALIVE' if ok else 'BUILD_BROKEN'} {case['case_id']} expected={expected} observed={failed or ['ALIVE']}"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("case_ids", nargs="*")
    args = ap.parse_args(argv[1:])
    cases = load_court()
    if args.case_ids:
        wanted = set(args.case_ids)
        cases_to_run = [c for c in cases if c["case_id"] in wanted]
        if len(cases_to_run) != len(wanted):
            print("UNKNOWN[CASE_ID]", file=sys.stderr); return 2
    else:
        cases_to_run = cases
    lock, head = load_lock(), head_sha()
    failed = 0
    for case in cases_to_run:
        try:
            ok, line = run_case(case, cases, lock, head)
        except Exception as exc:
            ok, line = False, f"BUILD_BROKEN {case.get('case_id','?')}: {type(exc).__name__}: {exc}"
        print(line)
        failed += not ok
    print(f"checked={len(cases_to_run)} passed={len(cases_to_run)-failed} failed={failed} subject={head} authority=ggen")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
