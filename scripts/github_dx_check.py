#!/usr/bin/env python3
"""Fail-closed, read-only checks for the repository's GitHub-native DX surface."""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

PINNED_ACTION_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?@[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)

REQUIRED = [
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/documentation.yml",
    ".github/ISSUE_TEMPLATE/dx_qol.yml",
    ".github/ISSUE_TEMPLATE/capability_gap.yml",
    ".github/dependabot.yml",
    ".github/labeler.yml",
    ".github/release.yml",
    ".github/copilot-instructions.md",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/pr-labeler.yml",
    ".github/workflows/pr-title.yml",
    ".github/workflows/repo-hygiene.yml",
    ".github/workflows/copilot-setup-steps.yml",
    ".github/workflows/supply-chain-attestation.yml",
    "SECURITY.md",
    "SUPPORT.md",
    "CODE_OF_CONDUCT.md",
]


def record(checks: list[dict[str, object]], name: str, ok: bool, detail: str) -> None:
    checks.append({"name": name, "ok": ok, "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    checks: list[dict[str, object]] = []

    missing = [path for path in REQUIRED if not (root / path).is_file()]
    record(checks, "github_required_surfaces", not missing, "missing=" + ",".join(missing) if missing else f"{len(REQUIRED)} required surfaces present")

    # Parse all TOML contracts with the Python standard library.
    toml_failures: list[str] = []
    for path in sorted(root.rglob("*.toml")):
        if ".git" in path.parts or "vendor" in path.parts:
            continue
        try:
            with path.open("rb") as handle:
                tomllib.load(handle)
        except Exception as exc:  # noqa: BLE001 - diagnostic court must report the exact parser failure
            toml_failures.append(f"{path.relative_to(root)}:{exc}")
    record(checks, "toml_parse", not toml_failures, "; ".join(toml_failures) if toml_failures else "all non-vendored TOML parsed")

    workflow_files = sorted((root / ".github/workflows").glob("*.y*ml")) if (root / ".github/workflows").is_dir() else []
    action_files = sorted((root / ".github/actions").rglob("*.y*ml")) if (root / ".github/actions").is_dir() else []
    unpinned: list[str] = []
    permissionless: list[str] = []
    unsafe_pr_target: list[str] = []
    tabbed_yaml: list[str] = []

    for path in workflow_files + action_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        if "\t" in text:
            tabbed_yaml.append(rel)
        for ref in USES_RE.findall(text):
            if ref.startswith("./") or ref.startswith("docker://"):
                continue
            if not PINNED_ACTION_RE.fullmatch(ref):
                unpinned.append(f"{rel}:{ref}")
        if path in workflow_files and "permissions:" not in text:
            permissionless.append(rel)
        if path in workflow_files and re.search(r"^\s*pull_request_target\s*:", text, re.MULTILINE):
            if "actions/checkout@" in text or re.search(r"^\s*run\s*:\s*", text, re.MULTILINE):
                unsafe_pr_target.append(rel)

    record(checks, "actions_exact_sha_pins", not unpinned, "; ".join(unpinned) if unpinned else "all external uses refs are exact 40-char SHAs")
    record(checks, "workflow_permissions_explicit", not permissionless, ",".join(permissionless) if permissionless else "all workflows declare permissions")
    record(checks, "pull_request_target_fence", not unsafe_pr_target, ",".join(unsafe_pr_target) if unsafe_pr_target else "no pull_request_target workflow executes untrusted PR code")
    record(checks, "yaml_no_tabs", not tabbed_yaml, ",".join(tabbed_yaml) if tabbed_yaml else "workflow/action YAML contains no tab indentation")

    issue_config = root / ".github/ISSUE_TEMPLATE/config.yml"
    issue_text = issue_config.read_text(encoding="utf-8") if issue_config.is_file() else ""
    record(checks, "issue_chooser_no_disabled_discussions_link", "/discussions" not in issue_text, "no Discussions dead-end" if "/discussions" not in issue_text else "disabled Discussions URL remains")

    codeowners = root / ".github/CODEOWNERS"
    owner_text = codeowners.read_text(encoding="utf-8") if codeowners.is_file() else ""
    record(checks, "codeowners_default_route", "* @seanchatmangpt" in owner_text, "default review owner present" if "* @seanchatmangpt" in owner_text else "default owner missing")

    generated = [root / ".github/workflows/ggen-ecosystem-sync.yml", root / ".github/workflows/ggen-ecosystem-container.yml"]
    record(checks, "generated_workflow_projection_fence", all(path.is_file() for path in generated), "canonical GGen workflow projections present")

    ok = all(bool(item["ok"]) for item in checks)
    result = {
        "schema": "https://ggen.dev/diagnostics/github-dx/v1",
        "standing": "ALIVE[GITHUB_DX_CONTRACTS]" if ok else "BUILD_BROKEN[GITHUB_DX_CONTRACTS]",
        "checks": checks,
        "summary": {"passed": sum(1 for item in checks if item["ok"]), "total": len(checks)},
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in checks:
            print(f"{'PASS' if item['ok'] else 'FAIL'} {item['name']}: {item['detail']}")
        print(f"{result['standing']} — {result['summary']['passed']}/{result['summary']['total']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
