#!/usr/bin/env python3
"""Court for the ecosystem node's declaration predicates in ecosystem.ttl.

Adjudicates the four predicate families on eco:ggen-ecosystem that were
previously declarations with no executable check:

  owns           -> each object must be a declared skos:Concept
  defaultProfile -> object must be a declared eco:Profile, prov:Plan node
  maximalProfile -> object must be a declared eco:Profile, prov:Plan node
  manufacturedBy -> object must resolve to a node in the graph

The exact object sets are pinned (closed sets pinned from the live graph on
2026-10-13); the court refuses a graph whose sets differ — missing or extra —
so edge deletion, addition, or retargeting cannot silently pass.

The court loads ecosystem.ttl PLUS the ontology files that declare the
referenced objects (ontology/profiles.ttl, ontology/repositories.ttl): a
declaration edge on the ecosystem node is only checkable against the union
graph where its objects carry their declarations.

Exit 0 (PASS) when every family matches its pinned set and every object
resolves. Exit 1 on any drift or unresolvable object.

--self-check runs delete-edge sabotage twins (one per predicate family — a
twin with one edge deleted must FAIL the court) and a determinism check
(two runs, identical output).
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS, PROV

ROOT = Path(__file__).resolve().parents[1]
ECO = "https://ggen.dev/ecosystem#"
ECO_NODE = URIRef(ECO + "ggen-ecosystem")

# Union-graph sources: ecosystem.ttl carries the declaration edges; the
# ontology files carry the object-side declarations the cross-checks resolve
# against.
SOURCES: tuple[Path, ...] = (
    ROOT / "ecosystem.ttl",
    ROOT / "ontology/profiles.ttl",
    ROOT / "ontology/repositories.ttl",
)

# Closed sets pinned from the live graph (2026-10-13 wave). The court refuses
# any drift: missing or extra objects in any family.
EXPECTED: dict[str, frozenset[str]] = {
    "owns": frozenset(
        {"Composition", "Admission", "Closure", "Qualification", "Transport", "Standing"}
    ),
    "defaultProfile": frozenset({"cloud-session"}),
    "maximalProfile": frozenset({"everything"}),
    "manufacturedBy": frozenset({"ggen"}),
}

# Local-name resolvers per family: how an object must be declared in the
# union graph. Each entry is a predicate taking (graph, node) -> bool.
RESOLVERS: dict[str, str] = {
    "owns": "concept",        # must be a declared skos:Concept
    "defaultProfile": "profile",  # must be a declared eco:Profile, prov:Plan
    "maximalProfile": "profile",
    "manufacturedBy": "node",     # must resolve to a node in the graph
}


def load_graph(paths: tuple[Path, ...] = SOURCES) -> Graph:
    g = Graph()
    for p in paths:
        g.parse(p, format="turtle")
    return g


def objects_of(g: Graph, predicate: str) -> set[str]:
    return {
        str(o).split("#")[-1]
        for o in g.objects(ECO_NODE, URIRef(ECO + predicate))
    }


def is_concept(g: Graph, node: URIRef) -> bool:
    return (node, RDF.type, SKOS.Concept) in g


def is_profile(g: Graph, node: URIRef) -> bool:
    return (node, RDF.type, URIRef(ECO + "Profile")) in g and (
        node,
        RDF.type,
        PROV.Plan,
    ) in g


def resolves(g: Graph, node: URIRef) -> bool:
    return len(list(g.predicate_objects(node))) > 0


CHECKS: dict[str, callable] = {
    "concept": is_concept,
    "profile": is_profile,
    "node": resolves,
}


def adjudicate(graph_sources: tuple[Path, ...] = SOURCES) -> tuple[int, list[str]]:
    """Return (exit_code, report_lines)."""
    lines: list[str] = []
    g = load_graph(graph_sources)

    errors: list[str] = []
    ok: list[str] = []

    for family, expected in EXPECTED.items():
        actual = objects_of(g, family)
        resolver = CHECKS[RESOLVERS[family]]

        # Closed-set drift check.
        if actual != set(expected):
            missing = sorted(set(expected) - actual)
            extra = sorted(actual - set(expected))
            errors.append(
                f"REFUSED[SET_DRIFT] {family}: missing={missing} extra={extra}"
            )
            lines.append(f"FAIL {family}: set drift (missing={missing} extra={extra})")
            continue

        # Per-object declaration cross-check.
        family_errors = []
        for name in sorted(actual):
            node = URIRef(ECO + name)
            if not resolver(g, node):
                family_errors.append(name)
        if family_errors:
            for name in family_errors:
                errors.append(f"REFUSED[UNDECLARED_OBJECT] {family}: {name}")
            lines.append(
                f"FAIL {family}: objects not declared per family contract: {family_errors}"
            )
        else:
            n = len(actual)
            lines.append(f"PASS {family}: {n} object(s) pinned and declared ({', '.join(sorted(actual))})")

    if errors:
        for e in errors:
            lines.append(e)
        lines.append(
            f"RESULT: FAIL ({len(errors)} inconsistency(ies) across {len(EXPECTED)} predicate families)"
        )
        return 1, lines
    lines.append(f"RESULT: PASS (all {len(EXPECTED)} predicate families pinned and resolved)")
    return 0, lines


# --- sabotage twins: one edge deleted per predicate family -------------------

ANCHOR_TO_DELETED: dict[str, tuple[str, str]] = {
    "owns": (
        "eco:owns eco:Composition, eco:Admission, eco:Closure, eco:Qualification, eco:Transport, eco:Standing ;",
        "eco:owns eco:Composition, eco:Admission, eco:Closure, eco:Qualification, eco:Transport ;",
    ),
    "defaultProfile": (
        "eco:defaultProfile eco:cloud-session ;",
        "a dcat:Dataset, prov:Entity ;",
    ),
    "maximalProfile": (
        "eco:maximalProfile eco:everything ;",
        "a dcat:Dataset, prov:Entity ;",
    ),
    "manufacturedBy": (
        "eco:manufacturedBy eco:ggen",
        "",
    ),
}


def sabotage_twin(family: str, dest: Path) -> Path:
    """Write a copy of the sources with one edge of `family` deleted."""
    text = SOURCES[0].read_text(encoding="utf-8")
    anchor, replacement = ANCHOR_TO_DELETED[family]
    if anchor not in text:
        raise SystemExit(f"sabotage anchor not found for {family} in ecosystem.ttl")

    if family == "owns":
        new_text = text.replace(anchor, replacement)
    else:
        # Single-object families: delete the predicate line entirely. In the
        # current block every deleted line ends with " ;" (knowledgeSource is
        # the block-final " ." line), so termination stays valid.
        key = anchor.rstrip(" ;.\n")
        kept = [ln for ln in text.splitlines(keepends=True) if key not in ln]
        new_text = "".join(kept)
    dest.write_text(new_text, encoding="utf-8")
    return dest


def self_check() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for family in EXPECTED:
            twin = sabotage_twin(family, tmp / f"sabotaged-{family}.ttl")
            code, lines = adjudicate()
            # twin writes to tmp but adjudicate re-reads SOURCES; adjudicate
            # against the twin by loading twin in place of ecosystem.ttl.
            sources = (twin, *SOURCES[1:])
            code, lines = adjudicate(sources)
            if code != 1:
                print(
                    f"SELF-CHECK FAIL: sabotage twin ({family} edge deleted) did not FAIL the court",
                    file=sys.stderr,
                )
                failures += 1
            else:
                print(f"SELF-CHECK sabotage twin [{family}]: correctly FAILed ({len(lines)} report lines)")

    runs = []
    for _ in range(2):
        runs.append(adjudicate())
    if runs[0] != runs[1]:
        print("SELF-CHECK FAIL: two runs produced different output", file=sys.stderr)
        failures += 1
    else:
        print(f"SELF-CHECK determinism: two runs identical (exit {runs[0][0]})")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true", help="run sabotage twins + determinism checks")
    args = parser.parse_args(argv)

    if args.self_check:
        return self_check()

    code, lines = adjudicate()
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
