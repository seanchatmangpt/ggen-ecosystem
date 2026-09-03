#!/usr/bin/env python3
"""Execute independent consumer projects through the real GGen CLI.

Scenario modules are production plugins: each supplies an RDF graph and SPARQL
query, and this command manufactures the project twice, checks byte identity,
and emits an execution receipt.  No fake GGen boundary exists in this tool.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


@dataclasses.dataclass(frozen=True)
class Scenario:
    name: str
    query: str
    minimum_rows: int = 1
    inline_query: bool = False


ONTOLOGY = '''@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <https://example.org/chicago-consumer#> .

ex:ThingShape a sh:NodeShape ; sh:targetClass ex:Thing ; rdfs:label "Thing Shape"@en ;
  sh:property [ sh:path ex:name ; sh:datatype xsd:string ; sh:minCount 1 ; sh:maxCount 1 ] .
ex:OtherShape a sh:NodeShape ; sh:targetClass ex:Other ; rdfs:label "Other Shape"@en ;
  sh:property [ sh:path ex:name ; sh:datatype xsd:string ; sh:minCount 1 ] .
ex:a a ex:Thing ; ex:name "Alpha" ; ex:rank 1 ; ex:enabled true ;
  ex:amount "12.50"^^xsd:decimal ; ex:when "2026-08-29"^^xsd:date .
ex:b a ex:Thing ; ex:name "Beta" ; ex:rank 2 ; ex:enabled false ;
  ex:amount "7.25"^^xsd:decimal ; ex:when "2026-08-30"^^xsd:date .
ex:c a ex:Other ; ex:name "Gamma" ; ex:rank 3 ; ex:enabled true ;
  ex:amount "4.00"^^xsd:decimal ; ex:when "2026-08-31"^^xsd:date .
'''


def load_scenarios() -> dict[str, Scenario]:
    root = Path(__file__).with_name("chicago_scenarios")
    found: dict[str, Scenario] = {}
    for path in sorted(root.glob("scenario_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if not spec or not spec.loader:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        scenario = module.SCENARIO
        if scenario.name in found:
            raise RuntimeError(f"duplicate scenario: {scenario.name}")
        found[scenario.name] = scenario
    return found


def execute(ggen: Path, scenario: Scenario) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix=f"ggen-chicago-{scenario.name}-") as raw:
        root = Path(raw)
        (root / "queries").mkdir()
        (root / "templates").mkdir()
        (root / "ontology.ttl").write_text(ONTOLOGY)
        (root / "queries" / "extract.rq").write_text(scenario.query.strip() + "\n")
        (root / "templates" / "output.tera").write_text(
            f"scenario={scenario.name}\n" +
            "{% for row in sparql_results %}value={{ row.value }}\n{% endfor %}"
        )
        query_source = (
            "query = { inline = " + json.dumps(scenario.query.strip()) + " }"
            if scenario.inline_query else
            'query = { file = "queries/extract.rq" }'
        )
        (root / "ggen.toml").write_text(f'''[project]
name = "chicago-{scenario.name}"
version = "0.1.0"
description = "Real Chicago consumer matrix scenario"
authors = ["ggen-ecosystem"]
license = "MIT"

[ontology]
source = "ontology.ttl"
standard_only = false

[generation]
output_dir = "."

[[generation.rules]]
name = "{scenario.name}"
{query_source}
template = {{ file = "templates/output.tera" }}
output_file = "out/result.txt"
mode = "Overwrite"
''')
        runs = []
        digests = []
        for generation in (1, 2):
            proc = subprocess.run(
                [str(ggen), "sync", "run", "--format", "json-pretty"],
                cwd=root, text=True, capture_output=True,
            )
            runs.append({"generation": generation, "exit_code": proc.returncode,
                         "stdout": proc.stdout, "stderr": proc.stderr})
            if proc.returncode:
                raise RuntimeError(f"{scenario.name}: generation {generation} exit={proc.returncode}\n{proc.stderr}")
            output = root / "out" / "result.txt"
            if not output.is_file():
                raise RuntimeError(f"{scenario.name}: output missing")
            payload = output.read_bytes()
            if payload.count(b"value=") < scenario.minimum_rows:
                raise RuntimeError(f"{scenario.name}: expected at least {scenario.minimum_rows} rows")
            digests.append(hashlib.sha256(payload).hexdigest())
        if digests[0] != digests[1]:
            raise RuntimeError(f"{scenario.name}: second-generation drift")
        return {"scenario": scenario.name, "standing": "ALIVE", "command": "ggen sync run --format json-pretty",
                "exit_codes": [r["exit_code"] for r in runs], "output_sha256": digests[1],
                "second_generation_identity": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ggen", required=True, type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scenario")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    ggen = args.ggen.resolve()
    if not ggen.is_file() or not ggen.stat().st_mode & 0o111:
        raise SystemExit(f"REFUSED[GGEN_EXECUTABLE_UNAVAILABLE]:{ggen}")
    scenarios = load_scenarios()
    selected = list(scenarios.values()) if args.all else [scenarios[args.scenario]]
    receipts = [execute(ggen, scenario) for scenario in selected]
    if args.json:
        print(json.dumps({"standing": "ALIVE", "scenario_count": len(receipts), "receipts": receipts}, indent=2, sort_keys=True))
    else:
        for receipt in receipts:
            print(f"CHICAGO_ALIVE {receipt['scenario']} {receipt['output_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
