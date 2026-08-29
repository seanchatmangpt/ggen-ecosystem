#!/usr/bin/env python3
"""mfact-style fail-closed certification for the ggen ecosystem."""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, tomllib
from pathlib import Path
from typing import Any

SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
VERSION_RE = re.compile(r"^v[0-9][0-9A-Za-z.+-]*$")
STANDING_RE = re.compile(r"^(UNKNOWN|PARTIAL_ALIVE|ALIVE|BLOCKED|BUILD_BROKEN|UNSUPPORTED|REFUSED)(\[[^\]]+\])?$")
PLACEHOLDERS = {"", "unknown", "unknown-todo", "todo", "tbd", "placeholder", "fixme", "xxx"}

def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def base_standing(value: str) -> str:
    return value.split("[", 1)[0]

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()

def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)

def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors = []
    if contract.get("schema_version") != 1:
        errors.append("REFUSED[MFACT_CONTRACT_SCHEMA]")
    if not SHA1_RE.fullmatch(str(contract.get("source_sha", ""))):
        errors.append("REFUSED[MFACT_SOURCE_SHA]")
    if contract.get("authority_ceiling") != "VERIFY":
        errors.append("REFUSED[MFACT_AUTHORITY_CEILING]")
    if contract.get("policy", {}).get("historical_evidence_ceiling") != "PARTIAL_ALIVE":
        errors.append("REFUSED[MFACT_HISTORICAL_CEILING]")
    return errors

def validate_lock(lock: dict[str, Any]) -> list[str]:
    errors = []
    ggen = lock.get("ggen", {})
    market = lock.get("ggen_marketplace", {})
    subs = lock.get("submodules", {})
    container = lock.get("container", {})
    release = str(ggen.get("release", ""))
    ggen_sha = str(ggen.get("commit_sha", ""))
    market_sha = str(market.get("sha", ""))
    sub_ggen = str(subs.get("ggen_commit", ""))
    sub_market = str(subs.get("ggen_marketplace_commit", ""))
    repo = str(container.get("repository", ""))
    tag = str(container.get("tag", ""))
    digest = str(container.get("digest", ""))
    if not VERSION_RE.fullmatch(release): errors.append("REFUSED[GGEN_RELEASE_IDENTITY]")
    if not SHA1_RE.fullmatch(ggen_sha): errors.append("REFUSED[GGEN_COMMIT_IDENTITY]")
    if not SHA1_RE.fullmatch(market_sha): errors.append("REFUSED[MARKETPLACE_COMMIT_IDENTITY]")
    if ggen_sha != sub_ggen: errors.append("REFUSED[GGEN_SUBMODULE_PIN_DRIFT]")
    if market_sha != sub_market: errors.append("REFUSED[MARKETPLACE_SUBMODULE_PIN_DRIFT]")
    if repo != "ghcr.io/seanchatmangpt/ggen-ecosystem": errors.append("REFUSED[CONTAINER_REPOSITORY_IDENTITY]")
    if tag != release: errors.append("REFUSED[CONTAINER_RELEASE_TAG_DRIFT]")
    if not SHA256_RE.fullmatch(digest): errors.append("REFUSED[IMMUTABLE_CONTAINER_DIGEST_REQUIRED]")
    for label, value in {
        "ggen.release": release, "ggen.commit_sha": ggen_sha, "ggen_marketplace.sha": market_sha,
        "container.repository": repo, "container.tag": tag, "container.digest": digest,
    }.items():
        if value.strip().lower() in PLACEHOLDERS or "unknown-todo" in value.lower():
            errors.append(f"REFUSED[PLACEHOLDER_LOAD_BEARING_IDENTITY]:{label}")
    return errors

def validate_release_receipt(receipt: dict[str, Any], lock: dict[str, Any]) -> list[str]:
    errors = []
    subject = receipt.get("subject", {})
    ecosystem = receipt.get("ecosystem", {})
    admission = receipt.get("admission", {})
    execution = receipt.get("execution", {})
    verification = receipt.get("verification", {})
    standing = str(receipt.get("standing", ""))
    if subject.get("repository") != "seanchatmangpt/ggen-ecosystem": errors.append("REFUSED[RECEIPT_REPOSITORY_IDENTITY]")
    if not SHA1_RE.fullmatch(str(subject.get("commit", ""))): errors.append("REFUSED[RECEIPT_SUBJECT_IDENTITY]")
    if ecosystem.get("version") != lock.get("ggen", {}).get("release"): errors.append("REFUSED[RECEIPT_RELEASE_DRIFT]")
    if ecosystem.get("ggen_commit") != lock.get("ggen", {}).get("commit_sha"): errors.append("REFUSED[RECEIPT_GGEN_DRIFT]")
    if ecosystem.get("marketplace_commit") != lock.get("ggen_marketplace", {}).get("sha"): errors.append("REFUSED[RECEIPT_MARKETPLACE_DRIFT]")
    if ecosystem.get("container_digest") != lock.get("container", {}).get("digest"): errors.append("REFUSED[RECEIPT_CONTAINER_DRIFT]")
    if admission.get("result") != "ADMITTED": errors.append("REFUSED[RELEASE_NOT_ADMITTED]")
    if execution.get("exit_code") != 0: errors.append("BUILD_BROKEN[RELEASE_EXECUTION_NONZERO]")
    if not STANDING_RE.fullmatch(standing): errors.append("REFUSED[RECEIPT_STANDING_VOCABULARY]")
    for key in ("doctor", "chicago", "dod"):
        if not STANDING_RE.fullmatch(str(verification.get(key, ""))):
            errors.append(f"REFUSED[RECEIPT_{key.upper()}_STANDING]")
    return errors

def validate_ledger(root: Path, ledger: dict[str, Any]):
    errors, observed = [], []
    artifacts = ledger.get("artifact", [])
    if not isinstance(artifacts, list) or not artifacts:
        return ["REFUSED[MFACT_ARTIFACT_LEDGER_EMPTY]"], observed
    allowed = {"source","projection","constructor","control","evidence","historical_evidence","documentation","verifier"}
    seen = set()
    for entry in artifacts:
        path_text, kind = str(entry.get("path","")), str(entry.get("kind",""))
        if not path_text or path_text in seen:
            errors.append(f"REFUSED[MFACT_ARTIFACT_IDENTITY]:{path_text}")
            continue
        seen.add(path_text)
        if kind not in allowed: errors.append(f"REFUSED[MFACT_ARTIFACT_KIND]:{path_text}:{kind}")
        if kind == "projection" and bool(entry.get("standing_authority")):
            errors.append(f"REFUSED[GENERATED_PROJECTION_STANDING_AUTHORITY]:{path_text}")
        path = root / path_text
        if not path.is_file():
            errors.append(f"REFUSED[MFACT_ARTIFACT_MISSING]:{path_text}")
            continue
        source = entry.get("source")
        if source and not (root / str(source)).is_file():
            errors.append(f"REFUSED[MFACT_ARTIFACT_SOURCE_MISSING]:{path_text}:{source}")
        observed.append({
            "path": path_text, "kind": kind, "producer": entry.get("producer"),
            "standing_authority": bool(entry.get("standing_authority")),
            "load_bearing": bool(entry.get("load_bearing")), "sha256": sha256_file(path),
        })
    return errors, observed

def git_lineage(root: Path, receipt_subject: str, load_bearing_paths: list[str]) -> dict[str, Any]:
    result = {"available": False, "head": None, "receipt_subject_ancestor": None, "load_bearing_changed": None, "changed_paths": []}
    try:
        head = git(root, "rev-parse", "HEAD").stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return result
    result["available"], result["head"] = bool(SHA1_RE.fullmatch(head)), head
    if not result["available"]: return result
    ancestor = git(root, "merge-base", "--is-ancestor", receipt_subject, head, check=False)
    result["receipt_subject_ancestor"] = ancestor.returncode == 0
    if ancestor.returncode != 0: return result
    changed = git(root, "diff", "--name-only", receipt_subject, head, "--", *load_bearing_paths, check=False)
    if changed.returncode != 0: return result
    paths = [x for x in changed.stdout.splitlines() if x]
    result["changed_paths"], result["load_bearing_changed"] = paths, bool(paths)
    return result

def classify_standing(receipt_standing: str, *, git_available: bool, current_head: str|None, receipt_subject: str, receipt_subject_ancestor: bool|None, load_bearing_changed: bool|None):
    receipt_base = base_standing(receipt_standing)
    if receipt_base in {"REFUSED","BUILD_BROKEN","BLOCKED","UNSUPPORTED"}:
        return receipt_standing, ["release receipt itself does not carry positive standing"]
    if not git_available:
        return "UNKNOWN[GIT_LINEAGE_UNOBSERVED]", ["git lineage unavailable"]
    if receipt_subject_ancestor is not True:
        return "REFUSED[RECEIPT_SUBJECT_NOT_ANCESTOR]", ["release receipt subject is not an ancestor of current subject"]
    if current_head == receipt_subject and receipt_base == "ALIVE":
        return "ALIVE", ["exact release subject and ALIVE release receipt"]
    reasons = []
    if current_head != receipt_subject: reasons.append("release evidence is historical relative to current HEAD")
    if load_bearing_changed: reasons.append("load-bearing manufacturing paths changed after release receipt")
    if receipt_base == "PARTIAL_ALIVE": reasons.append("release receipt itself is PARTIAL_ALIVE")
    return "PARTIAL_ALIVE[BOUNDED_CERTIFICATION]", reasons or ["exact-head ALIVE requirements are not met"]

def certify(root: Path, contract_path: Path):
    contract = load_toml(contract_path)
    lock_path = root / str(contract["lockfile"])
    ledger_path = root / str(contract["artifact_ledger"])
    receipt_path = root / str(contract["release_receipt"])
    errors = validate_contract(contract)
    for path, label in ((lock_path,"LOCKFILE"),(ledger_path,"ARTIFACT_LEDGER"),(receipt_path,"RELEASE_RECEIPT")):
        if not path.is_file(): errors.append(f"REFUSED[MFACT_{label}_MISSING]:{path.relative_to(root)}")
    lock = load_toml(lock_path) if lock_path.is_file() else {}
    ledger = load_toml(ledger_path) if ledger_path.is_file() else {}
    release = load_json(receipt_path) if receipt_path.is_file() else {}
    if lock: errors.extend(validate_lock(lock))
    observed = []
    if ledger:
        ledger_errors, observed = validate_ledger(root, ledger); errors.extend(ledger_errors)
    if release and lock: errors.extend(validate_release_receipt(release, lock))
    subject_commit = str(release.get("subject", {}).get("commit", ""))
    load_paths = list(contract.get("subject", {}).get("load_bearing_paths", []))
    lineage = git_lineage(root, subject_commit, load_paths) if SHA1_RE.fullmatch(subject_commit) else {"available":False,"head":None,"receipt_subject_ancestor":None,"load_bearing_changed":None,"changed_paths":[]}
    if lineage.get("available") and lineage.get("receipt_subject_ancestor") is False:
        errors.append("REFUSED[RECEIPT_SUBJECT_NOT_ANCESTOR]")
    if errors:
        standing, reasons, code = "REFUSED[MFACT_CERTIFICATION_INCONSISTENT_EVIDENCE]", sorted(set(errors)), 1
    else:
        standing, reasons = classify_standing(
            str(release.get("standing","UNKNOWN")), git_available=bool(lineage.get("available")),
            current_head=lineage.get("head"), receipt_subject=subject_commit,
            receipt_subject_ancestor=lineage.get("receipt_subject_ancestor"),
            load_bearing_changed=lineage.get("load_bearing_changed"),
        ); code = 0
    payload = {
        "schema":"https://ggen.dev/receipts/mfact-certification/v1",
        "certification":{"name":contract.get("name"),"source_repository":contract.get("source_repository"),"source_sha":contract.get("source_sha"),"authority_ceiling":contract.get("authority_ceiling")},
        "subject":{"repository":"seanchatmangpt/ggen-ecosystem","head":lineage.get("head"),"release_receipt_subject":subject_commit or None,"receipt_subject_ancestor":lineage.get("receipt_subject_ancestor"),"load_bearing_changed":lineage.get("load_bearing_changed"),"changed_load_bearing_paths":lineage.get("changed_paths",[])},
        "producer_identity":{"ggen_release":lock.get("ggen",{}).get("release") if lock else None,"ggen_commit":lock.get("ggen",{}).get("commit_sha") if lock else None,"marketplace_commit":lock.get("ggen_marketplace",{}).get("sha") if lock else None,"container":lock.get("container",{}).get("repository") if lock else None,"container_digest":lock.get("container",{}).get("digest") if lock else None},
        "release_evidence":{"path":str(receipt_path.relative_to(root)),"standing":release.get("standing") if release else None,"execution_exit_code":release.get("execution",{}).get("exit_code") if release else None,"admission":release.get("admission",{}).get("result") if release else None},
        "artifacts":observed,"standing":standing,"reasons":reasons,"errors":sorted(set(errors)),
    }
    return code, payload

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--contract", default="certification/mfact.toml")
    parser.add_argument("--receipt")
    parser.add_argument("--require-alive", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    code, payload = certify(root, (root / args.contract).resolve())
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        p = Path(args.receipt); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if args.require_alive and payload["standing"] != "ALIVE":
        print(f"certify-ecosystem: required ALIVE, observed {payload['standing']}", file=sys.stderr)
        return 1
    return code

if __name__ == "__main__":
    raise SystemExit(main())
