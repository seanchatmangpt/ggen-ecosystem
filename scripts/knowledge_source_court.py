#!/usr/bin/env python3
"""Court for eco:knowledgeSource edges in ecosystem.ttl.

Executes the existing ws4/ws1 SPARQL queries against the live graph, then
adjudicates every knowledgeSource object:

  (a) resolves to a dcterms:description annotation node;
  (b) resolves to a real sibling checkout at the canonical ~/ path
      (explicit checked-in mapping below);
  (c) annotation-referenced pack/test paths exist in the sibling repos.

Exit 0 (PASS or DEGRADED) when no real inconsistency. Exit 1 on:
  - a knowledgeSource eco:ggen-ecosystem edge without a dcterms:description
    annotation on its object, or
  - an annotation-referenced path (REPO_ARTIFACTS) missing while its repo
    checkout is present.

Missing sibling repos are not errors: they produce BLOCKED:<repo> skips and a
DEGRADED summary (exit 0), so the court degrades on machines without the
sibling checkouts rather than failing.

--self-check runs the sabotage twin (a graph with one knowledgeSource edge
deleted must FAIL the court) and a determinism check (two runs, identical
stdout).
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import DCTERMS

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "ecosystem.ttl"
ECO = "https://ggen.dev/ecosystem#"

# Explicit, checked-in mapping: graph node name -> canonical sibling checkout
# (~/<name>). Derived from the dcterms:identifier convention
# "seanchatmangpt/<repo>" on the root node and the one-canonical-checkout-per-
# repo convention at ~/<repo>.
REPO_ROOTS: dict[str, Path] = {
    name: Path.home() / name
    for name in (
        "ggen-marketplace",
        "affidavit",
        "graphlaw",
        "insa",
        "mfact",
        "castle",
        "unibit",
    )
}

# Explicit, checked-in mapping: graph node name -> repo-relative artifact paths
# referenced by that node's dcterms:description / skos:note annotations. Each
# entry is asserted to exist ONLY when the repo checkout itself is present
# (otherwise the check is a BLOCKED:<repo> skip).
REPO_ARTIFACTS: dict[str, tuple[str, ...]] = {
    "ggen-marketplace": (
        "packs/refusal-vocabulary-pack",
        "packs/insa-law-pack",
    ),
    "mfact": (
        "procint/ProcInt.lean",
        "procint/AxiomAudit.lean",
        "procint/ProcInt/StrataStore.lean",
    ),
    "castle": (
        "docs/qme-1-reference.md",
        "crates/castle-ggen-rdf",
    ),
    "unibit": (
        "crates/unibit-kernel/tests",
    ),
    # ggen-marketplace packs consumed by affidavit/graphlaw/insa seams live
    # under ggen-marketplace (already checked above).
    "affidavit": (),
    "graphlaw": (),
    "insa": (),
}

QUERIES: tuple[Path, ...] = (
    ROOT / "queries/ws4-root-composition/10-knowledge-source.rq",
    ROOT / "queries/ws4-root-composition/48-root-has-single-knowledge-source.rq",
    ROOT / "queries/ws1-repository-contracts/13-knowledgesource-property.rq",
)

# The admitted knowledgeSource edge set (2026-10-13 wave). The court refuses a
# graph whose edge set differs — missing or extra — so edge deletion cannot
# silently pass.
EXPECTED_EDGES: frozenset[str] = frozenset(
    {"ggen-marketplace", "affidavit", "graphlaw", "insa", "mfact", "castle", "unibit"}
)


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def knowledge_sources(g: Graph) -> list[str]:
    from rdflib import URIRef

    subj = URIRef(ECO + "ggen-ecosystem")
    return sorted(str(o).split("#")[-1] for o in g.objects(subj, URIRef(ECO + "knowledgeSource")))


def run_queries(g: Graph) -> list[tuple[str, bool]]:
    """Execute the existing query files (no duplicated query text)."""
    results = []
    for qpath in QUERIES:
        qtext = qpath.read_text(encoding="utf-8")
        ask = g.query(qtext).askAnswer
        results.append((qpath.name, bool(ask)))
    return results


def adjudicate(graph_path: Path) -> tuple[int, list[str]]:
    """Return (exit_code, report_lines)."""
    lines: list[str] = []
    g = load_graph(graph_path)
    edges = knowledge_sources(g)
    lines.append(f"edges: {len(edges)} knowledgeSource objects on eco:ggen-ecosystem")

    edge_set = set(edges)
    if edge_set != set(EXPECTED_EDGES):
        missing = sorted(set(EXPECTED_EDGES) - edge_set)
        extra = sorted(edge_set - set(EXPECTED_EDGES))
        lines.append(f"RESULT: FAIL (edge set drift; missing={missing} extra={extra})")
        return 1, lines

    # Query-layer execution (existing query files, re-executed not copied).
    for name, passed in run_queries(g):
        lines.append(f"query {name}: {'ASK true' if passed else 'ASK false'}")

    errors: list[str] = []
    missing_repos: list[str] = []
    resolved: list[str] = []

    from rdflib import URIRef as _URIRef

    for name in edges:
        node = _URIRef(ECO + name)
        descs = list(g.objects(node, DCTERMS.description))
        if not descs:
            errors.append(f"REFUSED[EDGE_WITHOUT_ANNOTATION] {name}")
            continue
        repo = REPO_ROOTS.get(name)
        if repo is None:
            errors.append(f"REFUSED[UNKNOWN_KNOWLEDGE_SOURCE] {name}")
            continue
        if not repo.is_dir():
            missing_repos.append(name)
            lines.append(f"BLOCKED:{name} repo checkout absent at {repo} — artifact checks skipped")
            continue
        resolved.append(name)
        artifact_errors = []
        for rel in REPO_ARTIFACTS.get(name, ()):
            p = repo / rel
            if not p.exists():
                artifact_errors.append(rel)
        if artifact_errors:
            for rel in artifact_errors:
                errors.append(f"REFUSED[ANNOTATION_PATH_MISSING] {name}: {rel}")
            lines.append(f"FAIL {name}: annotation paths missing at {repo}: {artifact_errors}")
        else:
            n = len(REPO_ARTIFACTS.get(name, ()))
            lines.append(f"PASS {name}: annotation present; repo present at {repo}; {n} artifact path(s) verified")

    # DEGRADED if any repo absent; FAIL on errors; PASS otherwise.
    if errors:
        for e in errors:
            lines.append(e)
        lines.append(f"RESULT: FAIL ({len(errors)} inconsistency(ies), {len(resolved)}/{len(edges)} repos resolved)")
        return 1, lines
    if missing_repos:
        lines.append(
            "RESULT: DEGRADED (" + ", ".join(f"BLOCKED:{r}" for r in missing_repos)
            + f"); {len(resolved)}/{len(edges)} sibling repos resolved"
        )
        return 0, lines
    lines.append(f"RESULT: PASS ({len(resolved)}/{len(edges)} sibling repos resolved)")
    return 0, lines


SABOTAGE_OLD = (
    "eco:knowledgeSource eco:ggen-marketplace, eco:affidavit, eco:graphlaw, "
    "eco:insa, eco:mfact, eco:castle, eco:unibit ."
)
SABOTAGE_NEW = (
    "eco:knowledgeSource eco:ggen-marketplace, eco:affidavit, eco:graphlaw, "
    "eco:mfact, eco:castle, eco:unibit ."
)


def sabotage_twin(dest: Path) -> Path:
    """Write a copy of ecosystem.ttl with one knowledgeSource edge deleted."""
    text = GRAPH.read_text(encoding="utf-8")
    if SABOTAGE_OLD not in text:
        raise SystemExit("sabotage anchor not found in ecosystem.ttl")
    dest.write_text(text.replace(SABOTAGE_OLD, SABOTAGE_NEW), encoding="utf-8")
    return dest


def self_check() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        twin = sabotage_twin(tmp / "sabotaged.ttl")
        code, lines = adjudicate(twin)
        if code != 1:
            print("SELF-CHECK FAIL: sabotage twin (edge deleted) did not FAIL the court", file=sys.stderr)
            return 1
        print(f"SELF-CHECK sabotage twin: correctly FAILed ({len(lines)} report lines)")

    runs = []
    for _ in range(2):
        code, lines = adjudicate(GRAPH)
        runs.append((code, "\n".join(lines)))
    if runs[0] != runs[1]:
        print("SELF-CHECK FAIL: two runs produced different output", file=sys.stderr)
        return 1
    print(f"SELF-CHECK determinism: two runs identical (exit {runs[0][0]})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true", help="run sabotage twin + determinism checks")
    args = parser.parse_args(argv)

    if args.self_check:
        return self_check()

    code, lines = adjudicate(GRAPH)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
