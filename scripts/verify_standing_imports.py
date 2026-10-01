#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, tomllib
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_CASES = {
    "allow_without_certificate","pdp_mixup","spiffe_wrong_trust_domain",
    "principal_substitution","effect_digest_substitution","jwt_replay",
    "federation_as_authority","pagination_mutation",
    "unknown_metadata_extension","allocation_plus_allow",
}

def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

def observed_git_head(root: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, default=Path("contracts/standing-imports/v26.9.30.json"))
    p.add_argument("--marketplace-root", type=Path, required=True)
    p.add_argument("--output", type=Path)
    a=p.parse_args()
    doc=json.loads(a.manifest.read_text(encoding="utf-8"))
    refusals=[]
    donors=doc.get("donors",[])
    if len(donors)!=5: refusals.append("DONOR_CARDINALITY")
    ids=[d.get("id") for d in donors]
    if "google/A2A" in ids or "a2aproject/A2A" not in ids: refusals.append("DONOR_IDENTITY_DRIFT")
    for d in donors:
        if d.get("required_standing")!="ADMITTED": refusals.append("OWNER_STANDING_UNADMITTED:"+str(d.get("id")))
        if d.get("identity_class")=="git_commit":
            if not SHA40.fullmatch(str(d.get("commit_sha",""))): refusals.append("IMPORT_IDENTITY_UNBOUND:"+str(d.get("id")))
            if not d.get("provenance_source"): refusals.append("IMPORT_PROVENANCE_UNBOUND:"+str(d.get("id")))
        elif d.get("identity_class")=="standards_artifact":
            for key in ("publisher","artifact_id","stable_uri","finality_evidence"):
                if not d.get(key): refusals.append("IMPORT_IDENTITY_UNBOUND:"+str(d.get("id"))+":"+key)
        else:
            refusals.append("UNKNOWN_IDENTITY_CLASS:"+str(d.get("id")))
    if doc["law"].get("technical_conformance_implies_authority") is not False: refusals.append("AUTHORITY_ESCALATION")
    if doc["law"].get("donor_presence_implies_runtime_authority") is not False: refusals.append("RUNTIME_PROMOTION")
    if doc["law"].get("imported_do_authority")!="forbidden": refusals.append("IMPORTED_DO_AUTHORITY")

    pack=doc["marketplace_absorption_pack"]
    observed_marketplace_sha=observed_git_head(a.marketplace_root)
    if observed_marketplace_sha is None:
        refusals.append("MARKETPLACE_SUBJECT_UNOBSERVABLE")
    elif observed_marketplace_sha != pack["commit_sha"]:
        refusals.append("MARKETPLACE_SUBJECT_SUBSTITUTION")
    root=a.marketplace_root / pack["path"]
    source=tomllib.loads((root/"source-lock.toml").read_text(encoding="utf-8"))
    courts=tomllib.loads((root/"qualification/courts.toml").read_text(encoding="utf-8"))
    if source["spiffe"].get("commit_sha")!="f97c46dfd0ff0d4e412cce5c73846a9ca32a99a2": refusals.append("SPIFFE_IDENTITY_DRIFT")
    if source["authzen"].get("stable_uri")!="https://openid.net/specs/authorization-api-1_0.html": refusals.append("AUTHZEN_IDENTITY_DRIFT")
    declared=set(courts.get("cases",[]))
    present={p.stem for p in (root/"qualification").glob("*.json")}
    if declared!=REQUIRED_CASES or not REQUIRED_CASES.issubset(present): refusals.append("QUALIFICATION_COURT_GAP")

    yaml_paths=[
      Path("contracts/standing-imports/v26.9.30.yaml"),
      Path("contracts/standing-imports/v26.9.30.projections.yaml"),
      Path("contracts/standing-imports/v26.9.30.identities.yaml"),
    ]
    if any("google/A2A" in p.read_text(encoding="utf-8") for p in yaml_paths): refusals.append("DONOR_IDENTITY_DRIFT")

    receipt={
      "schema":"standing-import-verification-receipt/v1",
      "standing":"ALIVE" if not refusals else "REFUSED",
      "subject":doc["subject"],
      "manifest_digest":digest(a.manifest),
      "marketplace_pack":pack,\n      "observed_marketplace_sha":observed_marketplace_sha,
      "qualified_donors":ids if not refusals else [],
      "refusals":sorted(set(refusals)),
      "authority":"NONE",
      "imported_do_authority":"forbidden",
    }
    rendered=json.dumps(receipt,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(rendered,encoding="utf-8")
    print(rendered,end="")
    return 0 if not refusals else 2
if __name__=="__main__":
    raise SystemExit(main())
