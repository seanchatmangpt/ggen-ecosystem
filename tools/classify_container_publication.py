#!/usr/bin/env python3
"""Classify container-publication evidence without performing publication.

This verifier is intentionally stdlib-only and read-only.  It converts bounded
observations into the repository standing vocabulary; it never logs in, pushes,
changes package visibility, or grants DO authority.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
SECRET = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|\"auth\"\s*:\s*\"[A-Za-z0-9+/=]{8,}\")")


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


def verify_case(path: Path) -> bool:
    try:
        case = json.loads(path.read_text(encoding="utf-8"))
        actual = classify(case["evidence"])
        expected = case["expected"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"{path}: malformed case: {exc}", file=sys.stderr)
        return False
    ok = actual == expected
    print(f"{path.name}: {'PASS' if ok else 'FAIL'} {actual['standing']}[{actual['reason']}]")
    if not ok:
        print(f"expected={expected!r} actual={actual!r}", file=sys.stderr)
    return ok


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
    args = parser.parse_args()
    if args.self_test and not self_test():
        print("publication classifier self-test failed", file=sys.stderr)
        return 1
    paths = args.paths
    if not paths and not args.self_test:
        paths = sorted(Path("tests/publication-evidence/cases").glob("*.json"))
    if not paths:
        print("publication classifier self-test passed")
        return 0
    passed = sum(verify_case(path) for path in paths)
    print(f"checked={len(paths)} passed={passed} failed={len(paths) - passed}")
    return 0 if passed == len(paths) else 1


if __name__ == "__main__":
    raise SystemExit(main())
