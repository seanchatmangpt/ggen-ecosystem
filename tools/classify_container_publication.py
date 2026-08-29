#!/usr/bin/env python3
"""Classify container-publication evidence without performing publication.

This verifier is intentionally stdlib-only and read-only. It converts bounded
observations into the repository standing vocabulary; it never logs in, pushes,
changes package visibility, or grants DO authority.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
CASE_ID = re.compile(r"PUB-[0-9]{3}")
REASON = re.compile(r"[A-Z][A-Z0-9_]+")
SECRET = re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|"auth"\s*:\s*"[A-Za-z0-9+/=]{8,}")')
STANDINGS = {"UNKNOWN", "PARTIAL_ALIVE", "ALIVE", "BLOCKED", "BUILD_BROKEN", "UNSUPPORTED", "REFUSED"}
REQUIRED_CASE_KEYS = {
    "schema", "id", "title", "hypothesis", "acceptance_edge", "evidence",
    "expected", "observed_source", "authority_ceiling", "falsifier",
    "semantic_fingerprint",
}


def verdict(standing: str, reason: str) -> dict[str, str]:
    return {"standing": standing, "reason": reason}


def classify(evidence: list[str]) -> dict[str, str]:
    text = "\n".join(str(item) for item in evidence)
    low = text.lower()

    # Safety and identity refusals precede availability classifications.
    if SECRET.search(text):
        return verdict("REFUSED", "SECRET_EXPOSURE")
    refusals = (
        ("do_without_brce", "UNAUTHORIZED_DO"),
        ("package ownership collision", "OWNERSHIP_COLLISION"),
        ("stale base sha", "STALE_SHA"),
        ("source sha drift", "SOURCE_SHA_DRIFT"),
        ("marketplace sha drift", "MARKETPLACE_SHA_DRIFT"),
        ("producer sha drift", "PRODUCER_SHA_DRIFT"),
        ("platform digest collision", "PLATFORM_DIGEST_COLLISION"),
        ("expected digest mismatch", "DIGEST_MISMATCH"),
        ("replay consequence mismatch", "REPLAY_MISMATCH"),
        ("receipt schema invalid", "RECEIPT_INVALID"),
        ("invalid manifest json", "MALFORMED_MANIFEST"),
        ("manifest list missing linux/", "PARTIAL_MANIFEST"),
    )
    for marker, reason in refusals:
        if marker in low:
            return verdict("REFUSED", reason)
    if "application/vnd.oci.image.manifest.v1+json" in low:
        return verdict("REFUSED", "NOT_OCI_INDEX")
    if "permission_denied: write_package" in low:
        return verdict("REFUSED", "PACKAGE_WRITE_PERMISSION")

    raw_digests = re.findall(r"sha256:[A-Za-z0-9]+", text)
    if raw_digests and any(not DIGEST.fullmatch(item) for item in raw_digests):
        return verdict("REFUSED", "DIGEST_FORMAT")
    if "published " in low and "@sha256:" not in low:
        return verdict("REFUSED", "MUTABLE_IDENTITY")
    if "pushed no digest" in low:
        return verdict("REFUSED", "MUTABLE_IDENTITY")

    blockers = (
        (("unauthorized: authentication required", "token expired", "insufficient_scope", "denied requested access to resource"), "REGISTRY_AUTH"),
        (("toomanyrequests", "rate limit"), "REGISTRY_RATE_LIMIT"),
        (("could not resolve host", "no such host"), "REGISTRY_DNS"),
        (("i/o timeout", "context deadline exceeded"), "REGISTRY_TIMEOUT"),
        (("connection refused",), "REGISTRY_TRANSPORT"),
        (("x509 certificate", "tls handshake"), "REGISTRY_TLS"),
        (("manifest unknown",), "MANIFEST_UNKNOWN"),
    )
    for markers, reason in blockers:
        if any(marker in low for marker in markers):
            return verdict("BLOCKED", reason)

    broken = (
        (("no space left on device",), "DISK_EXHAUSTED"),
        (("out of memory", "killed process"), "OUT_OF_MEMORY"),
        (("dockerfile parse error",), "DOCKERFILE"),
        (("cargo build failed", "exit code 101"), "TOOLCHAIN"),
        (("vendor/ggen does not exist",), "SUBMODULE_MISSING"),
    )
    for markers, reason in broken:
        if any(marker in low for marker in markers):
            return verdict("BUILD_BROKEN", reason)
    if "no match for platform" in low or "windows/amd64 unsupported" in low:
        return verdict("UNSUPPORTED", "PLATFORM")

    if "amd64 consumer failed" in low:
        return verdict("PARTIAL_ALIVE", "AMD64_CONSUMER_FAILED")
    if "arm64 consumer failed" in low:
        return verdict("PARTIAL_ALIVE", "ARM64_CONSUMER_FAILED")

    amd_push = "pushed linux/amd64 @sha256:" in low
    arm_push = "pushed linux/arm64 @sha256:" in low
    index = "oci index @sha256:" in low
    amd_consumer = "consumer linux/amd64 exit 0" in low
    arm_consumer = "consumer linux/arm64 exit 0" in low
    replay = "replay match" in low

    if amd_push and arm_push and index and amd_consumer and arm_consumer and replay:
        return verdict("ALIVE", "MULTIARCH_PUBLISHED")
    if amd_push and arm_push and index and amd_consumer and arm_consumer:
        return verdict("PARTIAL_ALIVE", "REPLAY_PENDING")
    if amd_push and arm_push and index:
        return verdict("PARTIAL_ALIVE", "CONSUMER_PENDING")
    if amd_push and arm_push:
        return verdict("PARTIAL_ALIVE", "MANIFEST_PENDING")
    if amd_push:
        return verdict("PARTIAL_ALIVE", "AMD64_ONLY")
    if arm_push:
        return verdict("PARTIAL_ALIVE", "ARM64_ONLY")
    return verdict("UNKNOWN", "INSUFFICIENT_EVIDENCE")


def validate_case_envelope(case: Any) -> list[str]:
    """Validate the executable subset of publication-evidence-case.schema.json."""
    errors: list[str] = []
    if not isinstance(case, dict):
        return ["case must be an object"]
    keys = set(case)
    missing = REQUIRED_CASE_KEYS - keys
    extra = keys - REQUIRED_CASE_KEYS
    if missing:
        errors.append("missing keys: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("unexpected keys: " + ", ".join(sorted(extra)))
    if case.get("schema") != "ggen-ecosystem/publication-evidence-case/v1":
        errors.append("schema must equal ggen-ecosystem/publication-evidence-case/v1")
    if not isinstance(case.get("id"), str) or CASE_ID.fullmatch(case["id"]) is None:
        errors.append("id must match PUB-[0-9]{3}")
    for key in ("title", "hypothesis", "observed_source", "falsifier", "semantic_fingerprint"):
        if not isinstance(case.get(key), str) or not case[key]:
            errors.append(f"{key} must be a non-empty string")
    edge = case.get("acceptance_edge")
    if not isinstance(edge, str) or not edge.startswith("publication."):
        errors.append("acceptance_edge must start with publication.")
    evidence = case.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item for item in evidence):
        errors.append("evidence must be a non-empty array of non-empty strings")
    expected = case.get("expected")
    if not isinstance(expected, dict) or set(expected) != {"standing", "reason"}:
        errors.append("expected must contain exactly standing and reason")
    else:
        if expected.get("standing") not in STANDINGS:
            errors.append("expected.standing is outside repository vocabulary")
        reason = expected.get("reason")
        if not isinstance(reason, str) or REASON.fullmatch(reason) is None:
            errors.append("expected.reason must be an uppercase typed reason")
    if case.get("authority_ceiling") != "VERIFY":
        errors.append("authority_ceiling must equal VERIFY")
    return errors


def load_case(path: Path) -> dict[str, Any] | None:
    try:
        case = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"{path}: malformed JSON: {exc}", file=sys.stderr)
        return None
    errors = validate_case_envelope(case)
    if errors:
        print(f"{path}: invalid case envelope: {'; '.join(errors)}", file=sys.stderr)
        return None
    return case


def verify_case(path: Path) -> tuple[bool, dict[str, Any] | None]:
    case = load_case(path)
    if case is None:
        return False, None
    actual = classify(case["evidence"])
    expected = case["expected"]
    ok = actual == expected
    print(f"{path.name}: {'PASS' if ok else 'FAIL'} {actual['standing']}[{actual['reason']}]")
    if not ok:
        print(f"expected={expected!r} actual={actual!r}", file=sys.stderr)
    return ok, case


def self_test() -> bool:
    checks = [
        (["permission_denied: write_package"], verdict("REFUSED", "PACKAGE_WRITE_PERMISSION")),
        (["pushed linux/amd64 @sha256:" + "a" * 64], verdict("PARTIAL_ALIVE", "AMD64_ONLY")),
        (["manifest unknown"], verdict("BLOCKED", "MANIFEST_UNKNOWN")),
        (["do_without_brce"], verdict("REFUSED", "UNAUTHORIZED_DO")),
        (["nothing observed"], verdict("UNKNOWN", "INSUFFICIENT_EVIDENCE")),
    ]
    return all(classify(evidence) == expected for evidence, expected in checks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--require-count", type=int, default=None)
    args = parser.parse_args()
    if args.self_test and not self_test():
        print("publication classifier self-test failed", file=sys.stderr)
        return 1
    paths = args.paths
    if not paths:
        paths = sorted(Path("tests/publication-evidence/cases").glob("*.json"))
    if args.require_count is not None and len(paths) != args.require_count:
        print(f"fixture count mismatch: expected={args.require_count} actual={len(paths)}", file=sys.stderr)
        return 1
    if not paths:
        print("no publication-evidence fixtures found", file=sys.stderr)
        return 1

    passed = 0
    seen_ids: set[str] = set()
    seen_fingerprints: set[str] = set()
    uniqueness_ok = True
    for path in paths:
        ok, case = verify_case(path)
        passed += int(ok)
        if case is None:
            continue
        case_id = case["id"]
        fingerprint = case["semantic_fingerprint"]
        if case_id in seen_ids:
            print(f"{path}: duplicate id {case_id}", file=sys.stderr)
            uniqueness_ok = False
        if fingerprint in seen_fingerprints:
            print(f"{path}: duplicate semantic_fingerprint {fingerprint}", file=sys.stderr)
            uniqueness_ok = False
        seen_ids.add(case_id)
        seen_fingerprints.add(fingerprint)

    failed = len(paths) - passed
    print(f"checked={len(paths)} passed={passed} failed={failed} unique={uniqueness_ok}")
    return 0 if failed == 0 and uniqueness_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
