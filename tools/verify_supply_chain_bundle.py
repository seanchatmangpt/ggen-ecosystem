#!/usr/bin/env python3
"""Verify an exact-identity SLSA + SPDX + CycloneDX release evidence bundle.

This court validates evidence structure and cross-format identity only. It does
not claim that an OCI subject exists, that a signature was observed, or that a
release is ALIVE.
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
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
UUID = re.compile(r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
PLACEHOLDER = re.compile(r"UNKNOWN|TODO|PLACEHOLDER|EXAMPLE", re.I)
SECRET_KEY = re.compile(r"token|password|secret|private[_-]?key", re.I)

def head_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

def iso(value: Any) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

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
                    "externalParameters": {
                        "source": {
                            "uri": "git+https://github.com/seanchatmangpt/ggen-ecosystem",
                            "digest": {"gitCommit": head},
                        }
                    },
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
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": "ggen-ecosystem-v26.8.28",
            "documentNamespace": f"https://github.com/seanchatmangpt/ggen-ecosystem/sbom/{head}",
            "creationInfo": {
                "created": "2026-08-29T10:04:33Z",
                "creators": ["Tool: ggen-ecosystem-supply-chain-court"],
            },
            "packages": [
                {
                    "name": "ggen-ecosystem",
                    "SPDXID": "SPDXRef-Package-ggen-ecosystem",
                    "versionInfo": tag,
                    "downloadLocation": "NOASSERTION",
                    "filesAnalyzed": False,
                    "licenseConcluded": "NOASSERTION",
                    "licenseDeclared": "NOASSERTION",
                    "supplier": "Organization: seanchatmangpt",
                    "checksums": [{"algorithm": "SHA256", "checksumValue": digest}],
                    "externalRefs": [{"referenceCategory": "PACKAGE-MANAGER", "referenceType": "purl", "referenceLocator": f"pkg:oci/ggen-ecosystem@{tag}?repository_url=ghcr.io/seanchatmangpt"}],
                },
                {"name": "ggen", "SPDXID": "SPDXRef-Package-ggen", "versionInfo": ggen, "downloadLocation": "git+https://github.com/seanchatmangpt/ggen", "filesAnalyzed": False, "licenseConcluded": "NOASSERTION", "licenseDeclared": "NOASSERTION"},
                {"name": "ggen-marketplace", "SPDXID": "SPDXRef-Package-marketplace", "versionInfo": market, "downloadLocation": "git+https://github.com/seanchatmangpt/ggen-marketplace", "filesAnalyzed": False, "licenseConcluded": "NOASSERTION", "licenseDeclared": "NOASSERTION"},
                {"name": "autofde-lab", "SPDXID": "SPDXRef-Package-autofde", "versionInfo": autofde, "downloadLocation": "git+https://github.com/seanchatmangpt/autofde-lab", "filesAnalyzed": False, "licenseConcluded": "NOASSERTION", "licenseDeclared": "NOASSERTION"},
            ],
            "relationships": [
                {"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES", "relatedSpdxElement": "SPDXRef-Package-ggen-ecosystem"},
                {"spdxElementId": "SPDXRef-Package-ggen-ecosystem", "relationshipType": "CONTAINS", "relatedSpdxElement": "SPDXRef-Package-ggen"},
                {"spdxElementId": "SPDXRef-Package-ggen-ecosystem", "relationshipType": "CONTAINS", "relatedSpdxElement": "SPDXRef-Package-marketplace"},
                {"spdxElementId": "SPDXRef-Package-ggen-ecosystem", "relationshipType": "CONTAINS", "relatedSpdxElement": "SPDXRef-Package-autofde"},
            ],
        },
        "cyclonedx": {
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "serialNumber": "urn:uuid:4d7b42d2-93d9-4f76-a121-72dd7f6f08aa",
            "version": 1,
            "metadata": {
                "timestamp": "2026-08-29T10:04:33Z",
                "component": {
                    "type": "container",
                    "bom-ref": subject,
                    "name": "ggen-ecosystem",
                    "version": tag,
                    "hashes": [{"alg": "SHA-256", "content": digest}],
                },
            },
            "components": [
                {"type": "application", "bom-ref": f"ggen@{ggen}", "name": "ggen", "version": ggen},
                {"type": "data", "bom-ref": f"ggen-marketplace@{market}", "name": "ggen-marketplace", "version": market},
                {"type": "application", "bom-ref": f"autofde-lab@{autofde}", "name": "autofde-lab", "version": autofde},
            ],
            "dependencies": [
                {"ref": subject, "dependsOn": [f"ggen@{ggen}", f"ggen-marketplace@{market}", f"autofde-lab@{autofde}"]}
            ],
        },
    }

def walk(node: Any):
    if isinstance(node, dict):
        for key, value in node.items():
            yield key, value
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)

def validate(bundle: dict[str, Any], lock: dict[str, Any], head: str) -> list[str]:
    errors: list[str] = []
    image = lock["container"]["repository"]
    tag = lock["container"]["tag"]
    digest = lock["container"]["digest"].removeprefix("sha256:")
    ggen = lock["ggen"]["commit_sha"]
    market = lock["ggen_marketplace"]["sha"]
    autofde = lock["submodules"]["autofde_lab_commit"]
    exact_subject = f"{image}@sha256:{digest}"

    p = bundle.get("provenance", {})
    subjects = p.get("subject", [])
    if p.get("_type") != "https://in-toto.io/Statement/v1": errors.append("REFUSED[PROV_TYPE]")
    if not isinstance(subjects, list) or len(subjects) != 1: errors.append("REFUSED[PROV_SUBJECT_COUNT]")
    subject = subjects[0] if isinstance(subjects, list) and subjects else {}
    if subject.get("name") != exact_subject: errors.append("REFUSED[PROV_SUBJECT_NAME]")
    sd = subject.get("digest", {})
    if set(sd) != {"sha256"}: errors.append("REFUSED[PROV_SUBJECT_DIGEST_ALGORITHM]")
    if not HEX64.fullmatch(str(sd.get("sha256", ""))): errors.append("REFUSED[PROV_SUBJECT_DIGEST_SHAPE]")
    if sd.get("sha256") != digest: errors.append("REFUSED[PROV_SUBJECT_DIGEST_DRIFT]")
    if p.get("predicateType") != "https://slsa.dev/provenance/v1": errors.append("REFUSED[PROV_PREDICATE_TYPE]")
    pred = p.get("predicate", {})
    bd = pred.get("buildDefinition", {})
    if bd.get("buildType") != "https://github.com/Attestations/GitHubActionsWorkflow@v1": errors.append("REFUSED[PROV_BUILD_TYPE]")
    source = bd.get("externalParameters", {}).get("source", {})
    if source.get("uri") != "git+https://github.com/seanchatmangpt/ggen-ecosystem": errors.append("REFUSED[PROV_SOURCE_URI]")
    if source.get("digest", {}).get("gitCommit") != head: errors.append("REFUSED[PROV_SOURCE_DIGEST]")
    workflow = bd.get("internalParameters", {}).get("workflow", "")
    if not isinstance(workflow, str) or not workflow.endswith(f"@{head}"): errors.append("REFUSED[PROV_WORKFLOW_REF_MUTABLE]")
    materials = bd.get("resolvedDependencies", [])
    material_map = {m.get("uri"): m.get("digest", {}).get("gitCommit") for m in materials if isinstance(m, dict)}
    if material_map.get("git+https://github.com/seanchatmangpt/ggen") != ggen: errors.append("REFUSED[PROV_GGEN_MATERIAL]")
    if material_map.get("git+https://github.com/seanchatmangpt/ggen-marketplace") != market: errors.append("REFUSED[PROV_MARKETPLACE_MATERIAL]")
    if material_map.get("git+https://github.com/seanchatmangpt/autofde-lab") != autofde: errors.append("REFUSED[PROV_AUTOFDE_MATERIAL]")
    rd = pred.get("runDetails", {})
    if rd.get("builder", {}).get("id") != "https://github.com/actions/runner/github-hosted": errors.append("REFUSED[PROV_BUILDER_ID]")
    meta = rd.get("metadata", {})
    if not str(meta.get("invocationId", "")).startswith("https://github.com/seanchatmangpt/ggen-ecosystem/actions/runs/"): errors.append("REFUSED[PROV_INVOCATION_ID]")
    started, finished = iso(meta.get("startedOn")), iso(meta.get("finishedOn"))
    if started is None: errors.append("REFUSED[PROV_STARTED_ON]")
    if finished is None: errors.append("REFUSED[PROV_FINISHED_ON]")
    if started and finished and finished < started: errors.append("REFUSED[PROV_TIME_ORDER]")

    s = bundle.get("spdx", {})
    if s.get("spdxVersion") != "SPDX-2.3": errors.append("REFUSED[SPDX_VERSION]")
    if s.get("dataLicense") != "CC0-1.0": errors.append("REFUSED[SPDX_DATA_LICENSE]")
    if s.get("SPDXID") != "SPDXRef-DOCUMENT": errors.append("REFUSED[SPDX_DOCUMENT_ID]")
    if not str(s.get("documentNamespace", "")).startswith("https://"): errors.append("REFUSED[SPDX_NAMESPACE]")
    ci = s.get("creationInfo", {})
    if not ci.get("creators"): errors.append("REFUSED[SPDX_CREATOR]")
    if iso(ci.get("created")) is None: errors.append("REFUSED[SPDX_CREATED]")
    packages = s.get("packages", [])
    pkgs = {x.get("SPDXID"): x for x in packages if isinstance(x, dict)}
    root = pkgs.get("SPDXRef-Package-ggen-ecosystem")
    if root is None: errors.append("REFUSED[SPDX_ROOT_PACKAGE]")
    else:
        if root.get("versionInfo") != tag: errors.append("REFUSED[SPDX_ROOT_VERSION]")
        checks = root.get("checksums", [])
        if not any(c.get("algorithm") == "SHA256" and c.get("checksumValue") == digest for c in checks if isinstance(c, dict)): errors.append("REFUSED[SPDX_ROOT_CHECKSUM]")
    rels = s.get("relationships", [])
    relset = {(x.get("spdxElementId"), x.get("relationshipType"), x.get("relatedSpdxElement")) for x in rels if isinstance(x, dict)}
    if ("SPDXRef-DOCUMENT", "DESCRIBES", "SPDXRef-Package-ggen-ecosystem") not in relset: errors.append("REFUSED[SPDX_DESCRIBES]")
    for sid, reason in [("SPDXRef-Package-ggen","SPDX_GGEN_PACKAGE"),("SPDXRef-Package-marketplace","SPDX_MARKETPLACE_PACKAGE"),("SPDXRef-Package-autofde","SPDX_AUTOFDE_PACKAGE")]:
        if sid not in pkgs: errors.append(f"REFUSED[{reason}]")

    c = bundle.get("cyclonedx", {})
    if c.get("bomFormat") != "CycloneDX": errors.append("REFUSED[CDX_FORMAT]")
    if c.get("specVersion") != "1.6": errors.append("REFUSED[CDX_SPEC_VERSION]")
    if not UUID.fullmatch(str(c.get("serialNumber", ""))): errors.append("REFUSED[CDX_SERIAL]")
    if not isinstance(c.get("version"), int) or c.get("version", 0) < 1: errors.append("REFUSED[CDX_VERSION]")
    cm = c.get("metadata", {})
    if iso(cm.get("timestamp")) is None: errors.append("REFUSED[CDX_TIMESTAMP]")
    cr = cm.get("component", {})
    if cr.get("type") != "container": errors.append("REFUSED[CDX_ROOT_TYPE]")
    if cr.get("name") != "ggen-ecosystem": errors.append("REFUSED[CDX_ROOT_NAME]")
    if cr.get("version") != tag: errors.append("REFUSED[CDX_ROOT_VERSION]")
    if cr.get("bom-ref") != exact_subject: errors.append("REFUSED[CDX_ROOT_REF]")
    if not any(h.get("alg") == "SHA-256" and h.get("content") == digest for h in cr.get("hashes", []) if isinstance(h, dict)): errors.append("REFUSED[CDX_ROOT_HASH]")
    comps = {x.get("name"): x for x in c.get("components", []) if isinstance(x, dict)}
    if comps.get("ggen", {}).get("version") != ggen: errors.append("REFUSED[CDX_GGEN_COMPONENT]")
    if comps.get("ggen-marketplace", {}).get("version") != market: errors.append("REFUSED[CDX_MARKETPLACE_COMPONENT]")
    if comps.get("autofde-lab", {}).get("version") != autofde: errors.append("REFUSED[CDX_AUTOFDE_COMPONENT]")
    deps = {x.get("ref"): set(x.get("dependsOn", [])) for x in c.get("dependencies", []) if isinstance(x, dict)}
    wanted = {f"ggen@{ggen}", f"ggen-marketplace@{market}", f"autofde-lab@{autofde}"}
    if deps.get(exact_subject) != wanted: errors.append("REFUSED[CDX_DEPENDENCY_CLOSURE]")

    spdx_hash = root.get("checksums", [{}])[0].get("checksumValue") if root else None
    cdx_hash = cr.get("hashes", [{}])[0].get("content") if cr else None
    if len({sd.get("sha256"), spdx_hash, cdx_hash}) != 1: errors.append("REFUSED[CROSS_FORMAT_DIGEST]")
    if len({tag, root.get("versionInfo") if root else None, cr.get("version")}) != 1: errors.append("REFUSED[CROSS_FORMAT_VERSION]")
    for key, value in walk(bundle):
        if isinstance(value, str) and PLACEHOLDER.search(value): errors.append("REFUSED[PLACEHOLDER_VALUE]"); break
    if "@sha256:" not in str(subject.get("name", "")): errors.append("REFUSED[MUTABLE_SUBJECT_IDENTITY]")
    for key, value in walk(bundle):
        if SECRET_KEY.search(str(key)) and value not in (None, "", [], {}): errors.append("REFUSED[SECRET_LEAK]"); break
    return sorted(set(errors))

def mutate(root: Any, mutation: dict[str, Any]) -> None:
    if not mutation:
        return
    parts = mutation["path"].split(".")
    node = root
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    leaf = parts[-1]
    if mutation.get("op", "set") == "delete":
        if isinstance(node, list): del node[int(leaf)]
        else: node.pop(leaf, None)
    else:
        if isinstance(node, list): node[int(leaf)] = mutation.get("value")
        else: node[leaf] = mutation.get("value")

def run_case(path: pathlib.Path, lock: dict[str, Any], head: str) -> tuple[bool, str]:
    case = json.loads(path.read_text(encoding="utf-8"))
    bundle = base_bundle(lock, head)
    mutate(bundle, case.get("mutation", {}))
    errors = validate(bundle, lock, head)
    expected = case["expected"]
    ok = (not errors) if expected == "ALIVE" else expected in errors
    return ok, f"{'ALIVE' if ok else 'BUILD_BROKEN'} {case['case_id']} expected={expected} observed={errors or ['ALIVE']}"

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="*", type=pathlib.Path)
    args = ap.parse_args(argv[1:])
    paths = args.cases or sorted((ROOT / "tests/supply-chain-bundle/cases").glob("*.json"))
    if not paths:
        print("UNKNOWN[NO_SUPPLY_CHAIN_CASES]", file=sys.stderr)
        return 2
    lock, head = load_lock(), head_sha()
    failed = 0
    for path in paths:
        try:
            ok, line = run_case(path, lock, head)
        except Exception as exc:
            ok, line = False, f"BUILD_BROKEN {path}: {type(exc).__name__}: {exc}"
        print(line)
        failed += not ok
    print(f"checked={len(paths)} passed={len(paths)-failed} failed={failed} subject={head}")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
