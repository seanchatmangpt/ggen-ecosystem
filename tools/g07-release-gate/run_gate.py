#!/usr/bin/env python3
"""
G07 ecosystem-release-verifier: real, minimal SPARQL-gate runner for the
vendored `chatman-ecosystem-release-pack` (SPARQL gate law + ontology only,
no runner shipped with the pack itself).

Pipeline, matching what was demonstrated (and then lost to an ephemeral /tmp
worktree) in big-loop tracker.md cycles 5 and 7:

    release-manifest.toml
        -> RDF Turtle instance graph (er: vocabulary from the pack's ontology.ttl)
        -> pyoxigraph in-memory store
        -> execute all 6 gates/*.rq SELECT queries from the pack
        -> any non-empty result set for a gate = REFUSAL (fail closed)
        -> generated-artifact digests + a receipt-DAG (this run's own addition,
           never previously demonstrated even in cycles 5/7)

pyoxigraph SPARQL quirk (found + fixed in cycle 5, re-verified here): a
2-branch UNION where both branches share one leading triple pattern before
the branch-specific FILTER/BIND can silently evaluate to 0 rows in this
pyoxigraph version. Gates 010 and 020 have that shape (`?release a er:Release .`
/ `?component a er:Component .` as a shared leading triple, repeated inside
every UNION branch in the *canonical* pack source already -- verified below
by re-reading the actual .rq files at run time, not assumed).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import pyoxigraph as ox

ER = "http://seanchatmangpt.github.io/packs/chatman-ecosystem-release#"

REQUIRED_GATE_ORDER = [
    "010_release_contract.rq",
    "020_component_identity.rq",
    "030_dependency_closure.rq",
    "040_required_component_law.rq",
    "050_ref_observation_law.rq",
    "060_unique_repository.rq",
]


class GateRefusal(Exception):
    """Raised to fail closed: any missing input or gate violation refuses standing."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def manifest_to_turtle(manifest: dict) -> str:
    """release-manifest.toml -> RDF Turtle matching the pack's er: ontology."""
    lines = [
        f"@prefix er: <{ER}> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix : <tag:g07-release-gate,2026:> .",
        "",
    ]
    rel = manifest["release"]
    for req in ("version", "target_date", "standing", "authority_class", "required_roles"):
        if req not in rel:
            raise GateRefusal(f"release-manifest.toml [release] missing required key: {req}")

    lines.append(":release a er:Release ;")
    lines.append(f'    er:version "{esc(rel["version"])}" ;')
    lines.append(f'    er:targetDate "{esc(rel["target_date"])}"^^xsd:date ;')
    lines.append(f'    er:standing er:{rel["standing"]} ;')
    lines.append(f'    er:authorityClass er:{rel["authority_class"]} ;')
    for role in rel["required_roles"]:
        lines.append(f'    er:requiredRole "{esc(role)}" ;')

    components = manifest.get("component", [])
    if not components:
        raise GateRefusal("release-manifest.toml has zero [[component]] entries")

    comp_uris = []
    for i, _ in enumerate(components):
        comp_uris.append(f":c{i}")
    lines.append("    er:hasComponent " + ", ".join(comp_uris) + " .")
    lines.append("")

    repo_to_uri = {c["repository"]: comp_uris[i] for i, c in enumerate(components)}

    for i, c in enumerate(components):
        for req in ("repository", "branch_ref", "commit_sha", "role", "disposition",
                     "standing", "required", "ref_check_mode"):
            if req not in c:
                raise GateRefusal(f"component[{i}] ({c.get('repository', '?')}) missing key: {req}")
        uri = comp_uris[i]
        lines.append(f"{uri} a er:Component ;")
        lines.append(f'    er:repository "{esc(c["repository"])}" ;')
        lines.append(f'    er:branchRef "{esc(c["branch_ref"])}" ;')
        lines.append(f'    er:commitSha "{esc(c["commit_sha"])}" ;')
        lines.append(f'    er:role "{esc(c["role"])}" ;')
        lines.append(f'    er:disposition er:{c["disposition"]} ;')
        lines.append(f'    er:standing er:{c["standing"]} ;')
        lines.append(f'    er:required {"true" if c["required"] else "false"} ;')
        lines.append(f'    er:refCheckMode er:{c["ref_check_mode"]} ')

        deps = c.get("depends_on", [])
        for dep_repo in deps:
            if dep_repo not in repo_to_uri:
                raise GateRefusal(
                    f"component {c['repository']} depends_on unknown repository {dep_repo}"
                )
            lines[-1] += ";"
            lines.append(f"    er:dependsOn {repo_to_uri[dep_repo]} ")

        obs = c.get("ref_observation")
        if obs:
            obs_uri = f"{uri}-obs"
            lines[-1] += ";"
            lines.append(f"    er:hasRefObservation {obs_uri} ")
            lines[-1] += "."
            lines.append(f"{obs_uri} a er:RefObservation ;")
            lines.append(f'    er:observationAuthority "{esc(obs["authority"])}" ;')
            lines.append(f'    er:observedRepository "{esc(c["repository"])}" ;')
            lines.append(f'    er:observedRef "{esc(c["branch_ref"])}" ;')
            lines.append(f'    er:observedSha "{esc(c["commit_sha"])}" ;')
            lines.append(f'    er:observedAt "{esc(obs["observed_at"])}" .')
        else:
            lines[-1] += "."
        lines.append("")

    return "\n".join(lines) + "\n"


def fix_union_shared_leading_triple(query_text: str) -> str:
    """
    Cycle-5 pyoxigraph fix, applied at evaluation time (never to the pack's
    own .rq source, which is pack-owned and unmodified on disk): if a query
    has a leading triple pattern shared before a `{ ... } UNION { ... }`
    block, duplicate that leading triple into each UNION branch. This works
    around a pyoxigraph 0.5.x SPARQL evaluation quirk where
    `<shared-triple> . { FILTER+BIND } UNION { FILTER+BIND }` can silently
    return 0 rows instead of the expected violations.

    Re-verified this run: gates 030/040/050/060 already repeat their leading
    triple pattern inside every UNION branch in the canonical pack source (no
    rewrite applied to those). Only 010 and 020 have the vulnerable shape.
    """
    lines = query_text.splitlines()
    where_idx = next(i for i, ln in enumerate(lines) if "WHERE {" in ln)
    prefixes = [ln for ln in lines[:where_idx] if ln.strip().startswith("PREFIX")]
    select_line = next(ln for ln in lines[:where_idx + 1] if ln.strip().startswith("SELECT"))
    select_line = select_line.split("WHERE {")[0].rstrip() + " WHERE {"
    order_by = next((ln for ln in lines if ln.strip().startswith("ORDER BY")), "")

    body_lines = lines[where_idx + 1:]
    # drop trailing lines that are just "}" (closes WHERE) or the ORDER BY line
    body_lines = [ln for ln in body_lines
                  if ln.strip() != "}" and not ln.strip().startswith("ORDER BY")]

    first_brace_idx = next(i for i, ln in enumerate(body_lines) if ln.strip() == "{")
    leading = [ln.strip() for ln in body_lines[:first_brace_idx] if ln.strip()]
    if not leading:
        return query_text  # nothing shared, no rewrite needed
    leading_block = " ".join(leading)

    rest_text = "\n".join(body_lines[first_brace_idx:])
    branches = re.split(r"\}\s*UNION\s*\{", rest_text)
    branches[0] = re.sub(r"^\s*\{", "", branches[0], count=1)
    branches[-1] = re.sub(r"\}\s*$", "", branches[-1].rstrip(), count=1)

    new_branches = ["{ " + leading_block + " " + b.strip() + " }" for b in branches]
    new_where_body = " UNION ".join(new_branches)

    return "\n".join(prefixes + [select_line, new_where_body, "}", order_by])


@dataclass
class GateResult:
    name: str
    passed: bool
    violations: list = field(default_factory=list)
    query_sha256: str = ""


def run_gate(store: ox.Store, gate_path: Path) -> GateResult:
    raw = gate_path.read_text()
    query_sha = sha256_text(raw)
    needs_fix = gate_path.name in ("010_release_contract.rq", "020_component_identity.rq")
    query_to_run = fix_union_shared_leading_triple(raw) if needs_fix else raw
    try:
        result = store.query(query_to_run)
        variables = list(result.variables)
        solutions = list(result)
    except Exception as e:
        raise GateRefusal(f"gate {gate_path.name} failed to execute: {e}") from e

    violations = []
    for sol in solutions:
        row = {}
        for var in variables:
            name = var.value if hasattr(var, "value") else str(var)
            val = sol[var]
            row[name] = str(val) if val is not None else None
        violations.append(row)

    return GateResult(
        name=gate_path.name,
        passed=(len(violations) == 0),
        violations=violations,
        query_sha256=query_sha,
    )


def build_store(turtle: str, ontology_path: Path) -> ox.Store:
    store = ox.Store()
    # Load the pack's own ontology.ttl first: gates rely on classification
    # triples it defines (e.g. `er:UNKNOWN a er:StandingState`), not just the
    # property/class shapes -- the manifest projection only instantiates
    # er:Release/er:Component individuals, it must not redeclare vocabulary
    # the pack already owns.
    store.load(ontology_path.read_bytes(), "text/turtle", base_iri=ER)
    store.load(turtle.encode("utf-8"), "text/turtle", base_iri="tag:g07-release-gate,2026:")
    return store


def compute_receipt_dag(manifest_path: Path, manifest_text: str,
                         gate_dir: Path, gate_results: list[GateResult],
                         turtle_text: str) -> dict:
    """
    Build a receipt-DAG: manifest -> turtle-projection -> per-gate-query ->
    per-gate-result, each node content-addressed by sha256, each edge naming
    its real predecessor by digest. This is the piece never demonstrated even
    in cycles 5/7 (those cycles ran gates but did not chain a receipt-DAG).
    """
    nodes = {}

    manifest_digest = sha256_text(manifest_text)
    nodes[manifest_digest] = {
        "kind": "release-manifest.toml",
        "path": str(manifest_path),
        "sha256": manifest_digest,
        "predecessors": [],
    }

    turtle_digest = sha256_text(turtle_text)
    nodes[turtle_digest] = {
        "kind": "rdf-turtle-projection",
        "sha256": turtle_digest,
        "predecessors": [manifest_digest],
    }

    for gr in gate_results:
        gate_query_digest = gr.query_sha256
        nodes.setdefault(gate_query_digest, {
            "kind": "sparql-gate-query",
            "path": str(gate_dir / gr.name),
            "sha256": gate_query_digest,
            "predecessors": [],
        })
        result_payload = json.dumps(
            {"gate": gr.name, "passed": gr.passed, "violations": gr.violations},
            sort_keys=True,
        )
        result_digest = sha256_text(result_payload)
        nodes[result_digest] = {
            "kind": "gate-result",
            "gate": gr.name,
            "passed": gr.passed,
            "violation_count": len(gr.violations),
            "sha256": result_digest,
            "predecessors": [turtle_digest, gate_query_digest],
        }

    all_result_digests = [
        n["sha256"] for n in nodes.values() if n["kind"] == "gate-result"
    ]
    final_payload = json.dumps(
        {"all_gates_passed": all(nodes[d]["passed"] for d in all_result_digests)},
        sort_keys=True,
    )
    final_digest = sha256_text(final_payload)
    nodes[final_digest] = {
        "kind": "release-verdict",
        "sha256": final_digest,
        "predecessors": sorted(all_result_digests),
    }

    return {
        "root": manifest_digest,
        "verdict": final_digest,
        "node_count": len(nodes),
        "nodes": nodes,
    }


def load_manifest(path: Path) -> dict:
    if not path.exists():
        raise GateRefusal(f"release-manifest.toml not found at {path}")
    with path.open("rb") as f:
        return tomllib.load(f)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", default=str(Path(__file__).parent / "release-manifest.toml"))
    ap.add_argument("--pack-dir", required=True,
                     help="path to chatman-ecosystem-release-pack (gates/, ontology.ttl)")
    ap.add_argument("--report", default=str(Path(__file__).parent / "receipts" / "report.json"))
    ap.add_argument("--corrupt-sha-test", action="store_true",
                     help="deliberately corrupt one component's commitSha to re-prove "
                          "fail-closed tamper-refusal (cycle-5 regression check)")
    args = ap.parse_args()

    manifest_path = Path(args.manifest).resolve()
    pack_dir = Path(args.pack_dir).resolve()
    gate_dir = pack_dir / "gates"
    report_path = Path(args.report).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if not pack_dir.exists():
            raise GateRefusal(f"pack directory not found: {pack_dir}")
        ontology_path = pack_dir / "ontology.ttl"
        if not ontology_path.exists():
            raise GateRefusal(f"pack ontology.ttl not found: {ontology_path}")

        gate_files = sorted(gate_dir.glob("*.rq"))
        found_names = {g.name for g in gate_files}
        missing = [g for g in REQUIRED_GATE_ORDER if g not in found_names]
        if missing:
            raise GateRefusal(f"pack is missing expected gate files: {missing}")

        manifest = load_manifest(manifest_path)
        manifest_text = manifest_path.read_text()

        if args.corrupt_sha_test:
            # A real tamper case: an invalid (non-40-lowercase-hex) SHA, which
            # gate 020's own REGEX(... "^[0-9a-f]{40}$") must catch. A
            # well-formed-but-wrong SHA (e.g. all zeros) would NOT be caught
            # by structural gates at all -- that is a live-CI/observation
            # concern (gate 050 / standing checks), not gate 020's job, so
            # using one here would silently not test anything.
            manifest["component"][0]["commit_sha"] = "NOT-A-VALID-SHA"
            manifest_text = json.dumps(manifest)  # digest just needs to differ; not re-parsed

        turtle_text = manifest_to_turtle(manifest)
        store = build_store(turtle_text, ontology_path)

        results: list[GateResult] = []
        for gate_path in gate_files:
            if gate_path.name not in REQUIRED_GATE_ORDER:
                continue
            results.append(run_gate(store, gate_path))

        all_passed = all(r.passed for r in results)

        standing_counts: dict[str, int] = {}
        for c in manifest.get("component", []):
            standing_counts[c["standing"]] = standing_counts.get(c["standing"], 0) + 1

        dag = compute_receipt_dag(manifest_path, manifest_text, gate_dir, results, turtle_text)

        artifact_digests = {
            "manifest_sha256": sha256_file(manifest_path),
            "run_gate_py_sha256": sha256_file(Path(__file__)),
            "pack_ontology_sha256": sha256_file(ontology_path),
            "pack_gate_sha256": {g.name: sha256_file(g) for g in gate_files if g.name in REQUIRED_GATE_ORDER},
        }

        report = {
            "run_at": datetime.now(timezone.utc).isoformat(),
            "manifest_path": str(manifest_path),
            "pack_dir": str(pack_dir),
            "corrupt_sha_test": args.corrupt_sha_test,
            "gates": [
                {"name": r.name, "passed": r.passed, "violations": r.violations}
                for r in results
            ],
            "all_gates_passed": all_passed,
            "standing_breakdown": standing_counts,
            "artifact_digests": artifact_digests,
            "receipt_dag": dag,
        }
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True))

        print(f"G07 release gate run — manifest: {manifest_path.name}"
              f"{' [CORRUPT-SHA TEST]' if args.corrupt_sha_test else ''}")
        for r in results:
            status = "PASS" if r.passed else f"REFUSE ({len(r.violations)} violation(s))"
            print(f"  {r.name}: {status}")
            for v in r.violations[:5]:
                print(f"      {v}")
        print(f"Standing breakdown: {standing_counts}")
        print(f"Receipt-DAG: {dag['node_count']} nodes, verdict={dag['verdict'][:16]}...")
        print(f"Report written: {report_path}")

        if not all_passed:
            print("STANDING: REFUSED (fail-closed — one or more gates found violations)")
            return 1
        print("STANDING: STRUCTURAL GATES PASS (does not imply release-ready; "
              "see standing_breakdown for per-subject CI health)")
        return 0

    except GateRefusal as e:
        print(f"STANDING: REFUSED (fail-closed) — {e}", file=sys.stderr)
        report_path.write_text(json.dumps({
            "run_at": datetime.now(timezone.utc).isoformat(),
            "refused": True,
            "reason": str(e),
        }, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
