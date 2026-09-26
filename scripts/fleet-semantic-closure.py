#!/usr/bin/env python3
"""Fail-closed fleet semantic closure court.

Binds canonical capability ownership to exact producer subjects from
ecosystem.lock.toml. Emits a deterministic receipt; never grants authority.
"""
from __future__ import annotations
import argparse, hashlib, json, re, tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_TTL = {
    "fsc:FleetSemanticClosure", "fsc:Supplier", "fsc:Capability",
    "fsc:Consumer", "fsc:ClosureReceipt", "fsc:exactSubject",
    "fsc:canonicalOwner", "fsc:provides", "fsc:consumes",
    "fsc:authorityCeiling", "fsc:closureDigest", "fsc:replayDigest",
}

class Refusal(ValueError):
    pass

def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_digest(doc: object) -> str:
    return digest_bytes(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode())

def load_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)

def qualify(root: Path = ROOT) -> dict:
    manifest_path = root / "fleet.semantic.toml"
    lock_path = root / "ecosystem.lock.toml"
    if not manifest_path.is_file() or not lock_path.is_file():
        raise Refusal("REFUSED[MISSING_INPUT]")
    manifest = load_toml(manifest_path)
    lock = load_toml(lock_path)
    if manifest.get("version") != 1:
        raise Refusal("REFUSED[MANIFEST_VERSION]")
    if manifest.get("authority_ceiling") != "NONE":
        raise Refusal("REFUSED[AUTHORITY_WIDENING]")
    ontology_rel = manifest.get("ontology")
    if not isinstance(ontology_rel, str) or Path(ontology_rel).is_absolute() or ".." in Path(ontology_rel).parts:
        raise Refusal("REFUSED[ONTOLOGY_LOCATOR]")
    ontology_path = root / ontology_rel
    if not ontology_path.is_file():
        raise Refusal("REFUSED[ONTOLOGY_MISSING]")
    ttl = ontology_path.read_text()
    missing_terms = sorted(term for term in REQUIRED_TTL if term not in ttl)
    if missing_terms:
        raise Refusal("REFUSED[ONTOLOGY_TERM_MISSING]:" + ",".join(missing_terms))

    owners: dict[str, str] = {}
    suppliers = []
    for row in manifest.get("supplier", []):
        sid = row.get("id")
        section, key = row.get("lock_section"), row.get("lock_key")
        if not all(isinstance(x, str) and x for x in (sid, section, key)):
            raise Refusal("REFUSED[SUPPLIER_IDENTITY]")
        subject = lock.get(section, {}).get(key)
        if not isinstance(subject, str) or not SHA40.fullmatch(subject):
            raise Refusal(f"REFUSED[EXACT_SUBJECT]:{sid}")
        caps = row.get("capabilities")
        if not isinstance(caps, list) or not caps or any(not isinstance(c, str) or not c for c in caps):
            raise Refusal(f"REFUSED[CAPABILITY_SET]:{sid}")
        for cap in caps:
            prior = owners.setdefault(cap, sid)
            if prior != sid:
                raise Refusal(f"REFUSED[DUPLICATE_CANONICAL_OWNER]:{cap}:{prior}:{sid}")
        suppliers.append({"id": sid, "exact_subject": subject, "capabilities": sorted(caps)})

    if not suppliers:
        raise Refusal("REFUSED[NO_SUPPLIERS]")

    consumers = []
    used: set[str] = set()
    for row in manifest.get("consumer", []):
        cid, req, consequence = row.get("id"), row.get("requires"), row.get("consequence")
        if not isinstance(cid, str) or not cid or not isinstance(consequence, str) or not consequence:
            raise Refusal("REFUSED[CONSUMER_IDENTITY]")
        if not isinstance(req, list) or not req:
            raise Refusal(f"REFUSED[CONSUMER_REQUIREMENTS]:{cid}")
        unknown = sorted(set(req) - set(owners))
        if unknown:
            raise Refusal(f"REFUSED[UNOWNED_CAPABILITY]:{cid}:" + ",".join(unknown))
        used.update(req)
        consumers.append({
            "id": cid,
            "requires": sorted(req),
            "owners": {cap: owners[cap] for cap in sorted(req)},
            "consequence": consequence,
        })

    orphaned = sorted(set(owners) - used)
    if orphaned:
        raise Refusal("REFUSED[UNCONSUMED_CAPABILITY]:" + ",".join(orphaned))

    closure = {
        "schema": manifest["schema"],
        "authority": "NONE",
        "suppliers": sorted(suppliers, key=lambda x: x["id"]),
        "consumers": sorted(consumers, key=lambda x: x["id"]),
        "ontology_sha256": digest_bytes(ontology_path.read_bytes()),
        "manifest_sha256": digest_bytes(manifest_path.read_bytes()),
        "lock_sha256": digest_bytes(lock_path.read_bytes()),
    }
    closure_digest = canonical_digest(closure)
    receipt = {
        **closure,
        "closure_digest": closure_digest,
        "replay_digest": closure_digest,
        "standing": "ALIVE",
    }
    return receipt

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()
    try:
        receipt = qualify(args.root.resolve())
    except Refusal as exc:
        print(str(exc))
        return 2
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload)
    print(payload, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
