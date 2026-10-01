#!/usr/bin/env python3
"""Executable prior-art court for provenance imports.

PROV relations carry evidence/provenance semantics only.  They never imply
runtime authorization, semantic equivalence, truth, or consequential DO.
Input is a JSON import manifest. Exit non-zero on authority promotion.
"""
import json, sys

ALLOWED_CEILINGS = {"NONE", "EVIDENCE_ONLY", "EVIDENCE_VALIDATION_ONLY", "VERIFY"}
FORBIDDEN_IMPLICATIONS = {
    "prov:wasDerivedFrom": {"semantic_equivalence", "authorization", "do_authority"},
    "prov:wasAttributedTo": {"authorization", "do_authority"},
    "prov:wasAssociatedWith": {"authorization", "do_authority"},
    "prov:used": {"authorization", "do_authority"},
    "prov:wasGeneratedBy": {"authorization", "do_authority"},
}

def validate(doc):
    errors = []
    donor = doc.get("donor", {})
    if donor.get("standard") != "W3C PROV-O":
        errors.append("PROV_DONOR_UNBOUND")
    if not donor.get("version") or not donor.get("source"):
        errors.append("PROV_IDENTITY_INCOMPLETE")
    ceiling = doc.get("runtime_authority_ceiling")
    if ceiling not in ALLOWED_CEILINGS:
        errors.append("PROV_AUTHORITY_CEILING_INVALID")
    if doc.get("imported_do_authority") not in (False, "forbidden", "FORBIDDEN"):
        errors.append("PROV_AUTHORITY_PROMOTION")
    for mapping in doc.get("mappings", []):
        relation = mapping.get("prov_relation")
        claims = set(mapping.get("implies", []))
        bad = claims & FORBIDDEN_IMPLICATIONS.get(relation, set())
        if bad:
            errors.append("PROV_RELATION_OVERCLAIM:" + relation + ":" + ",".join(sorted(bad)))
    return sorted(set(errors))

def main():
    doc = json.load(sys.stdin)
    errors = validate(doc)
    receipt = {
        "court": "prov-import-authority-v1",
        "status": "ALIVE" if not errors else "REFUSED",
        "errors": errors,
        "authority": "NONE",
        "imported_do_authority": "forbidden",
    }
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0 if not errors else 2

if __name__ == "__main__":
    raise SystemExit(main())
