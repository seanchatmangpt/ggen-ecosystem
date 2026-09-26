#!/usr/bin/env python3
"""Lock/crown admission court for ecosystem.lock.toml release and crown bumps.

Pure evaluation over already-present evidence (SELECT only, authority NONE):
it never fetches, publishes, or mutates. `load_inputs` gathers the subject
(lock text, .gitmodules, the sync workflow projection, its ontology source,
CHANGELOG, gitlinks and ancestry of an exact git revision); `evaluate` returns
typed violations. An empty list is admission; any entry is a refusal.

Every law here is crown-stable: `scripts/crown-submodules.py --apply` rewrites
every occurrence of an old pin in the lock and refreshes base_main_sha /
updated_at, and never edits workflows, ontology.ttl or CHANGELOG.md -- so a
lawful crown bump stays admitted while a hand-made release bump must keep the
workflow projection, its ontology source and the release record coherent.

Codes (each is a falsifier with a mutation case in
tests/lock_contracts/test_lock_crown_court.py):
  LOCK_UNPARSEABLE            lock text is not TOML
  PIN_SHAPE                   a pin is not a lowercase 40-hex commit id
  SUBMODULE_SET               lock [submodules] paths != .gitmodules paths
  SUBMODULE_DUPLICATE         two lock entries claim one path
  GITLINK_PIN                 gitlink at rev != lock [submodules] commit
  SECTION_PIN                 per-producer section sha != [submodules] commit
  WORKFLOW_DEFAULT_MISSING    sync workflow lacks ggen_container_tag/marketplace_sha defaults
  WORKFLOW_CONTAINER_TAG      workflow ggen_container_tag default != lock [container].tag
  PROJECTION_PARITY           workflow input defaults != ontology.ttl source defaults
  MARKETPLACE_DEFAULT_UNRECORDED  marketplace_sha default not cited in the release's CHANGELOG section
  RELEASE_IDENTITY            [container].tag != [ggen].release
  RELEASE_UNRECORDED          CHANGELOG has no section for [ggen].release
  CONTAINER_STANDING          standing outside vocabulary / ALIVE while republish pending /
                              republish pending without BLOCKED+failure / malformed digest
  BASE_NOT_ANCESTOR           base_main_sha is not an ancestor of the subject revision
  BASE_IS_SUBJECT             base_main_sha names the subject itself
  UPDATED_AT_SHAPE            updated_at is not YYYY-MM-DDTHH:MM:SSZ
  UPDATED_AT_STALE            updated_at precedes the base_main_sha commit
  UPDATED_AT_FUTURE           updated_at is later than the subject commit
"""
from __future__ import annotations

import argparse
import configparser
import datetime as dt
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

SHA40 = re.compile(r"[0-9a-f]{40}")
DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
UPDATED_AT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
STANDINGS = frozenset(
    {"UNKNOWN", "PARTIAL_ALIVE", "ALIVE", "BLOCKED", "BUILD_BROKEN", "UNSUPPORTED", "REFUSED"}
)
CLOCK_SLACK_SECONDS = 300
SYNC_WORKFLOW = ".github/workflows/ggen-ecosystem-sync.yml"

# (lock section, key, [submodules] commit key)
SECTION_PINS = (
    ("ggen", "commit_sha", "ggen_commit"),
    ("ggen_marketplace", "sha", "ggen_marketplace_commit"),
    ("pragprog_tps", "marketplace_sha", "ggen_marketplace_commit"),
    ("ggen_igniter", "sha", "ggen_igniter_commit"),
    ("beam4pm", "sha", "beam4pm_commit"),
    ("wasm4pm", "sha", "wasm4pm_commit"),
)

_INPUT_NAME = re.compile(r"^(\s+)([A-Za-z_][A-Za-z0-9_]*):\s*$")
_DEFAULT = re.compile(r"^\s+default:\s*(\S+)\s*$")


def workflow_defaults(text: str) -> list[tuple[str, str]]:
    """Ordered (input, default) pairs from a workflow_call/workflow_dispatch block.

    Indentation-scoped: a `default:` binds to the nearest enclosing input name
    with strictly smaller indentation. Works identically on the YAML file and
    on the YAML text embedded in ontology.ttl's gha:onBlock literal.
    """
    pairs: list[tuple[str, str]] = []
    current: tuple[int, str] | None = None
    for line in text.splitlines():
        name = _INPUT_NAME.match(line)
        if name:
            current = (len(name.group(1)), name.group(2))
            continue
        default = _DEFAULT.match(line)
        if default and current is not None:
            indent = len(line) - len(line.lstrip())
            if indent > current[0]:
                pairs.append((current[1], default.group(1).strip("\"'")))
    return pairs


def workflow_on_block(text: str) -> str:
    """The top-level `on:` mapping of a workflow file (up to the next top-level key)."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.fullmatch(r"(on|\"on\"|'on'):\s*", line):
            body = []
            for nxt in lines[i + 1:]:
                if nxt and not nxt[0].isspace() and not nxt.startswith("#"):
                    break
                body.append(nxt)
            return "\n".join(body)
    return ""


def ontology_on_block(text: str) -> str:
    """The gha:onBlock triple-quoted literal that ggen projects into the workflow `on:` block."""
    match = re.search(r'gha:onBlock\s+"""(.*?)"""', text, re.S)
    return match.group(1) if match else ""


def changelog_section(text: str, release: str) -> str | None:
    heading = re.compile(r"^## \[" + re.escape(release) + r"\]", re.M)
    match = heading.search(text)
    if not match:
        return None
    nxt = re.compile(r"^## \[", re.M).search(text, match.end())
    return text[match.end(): nxt.start() if nxt else len(text)]


def parse_utc(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def evaluate(inputs: dict) -> list[tuple[str, str]]:
    """Return typed violations; [] means admitted. Pure over `inputs`."""
    out: list[tuple[str, str]] = []
    try:
        lock = tomllib.loads(inputs["lock_text"])
    except tomllib.TOMLDecodeError as exc:
        return [("LOCK_UNPARSEABLE", str(exc))]

    subs = lock.get("submodules", {})
    lock_paths: dict[str, str] = {}
    for key, value in subs.items():
        if not key.endswith("_path"):
            continue
        stem = key[: -len("_path")]
        if value in lock_paths.values():
            out.append(("SUBMODULE_DUPLICATE", f"{value} claimed by {stem} and another entry"))
        lock_paths[stem] = value
    if set(lock_paths.values()) != set(inputs["gitmodules_paths"]):
        out.append((
            "SUBMODULE_SET",
            f"lock={sorted(set(lock_paths.values()))} gitmodules={sorted(inputs['gitmodules_paths'])}",
        ))

    for stem, path in sorted(lock_paths.items()):
        pin = subs.get(f"{stem}_commit")
        if not isinstance(pin, str) or not SHA40.fullmatch(pin):
            out.append(("PIN_SHAPE", f"[submodules].{stem}_commit={pin!r}"))
            continue
        observed = inputs["gitlinks"].get(path)
        if observed != pin:
            out.append(("GITLINK_PIN", f"{path}: gitlink={observed} lock={pin}"))

    for section, key, sub_key in SECTION_PINS:
        value = lock.get(section, {}).get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not SHA40.fullmatch(value):
            out.append(("PIN_SHAPE", f"[{section}].{key}={value!r}"))
        elif value != subs.get(sub_key):
            out.append(("SECTION_PIN", f"[{section}].{key}={value} [submodules].{sub_key}={subs.get(sub_key)}"))

    release = lock.get("ggen", {}).get("release")
    container = lock.get("container", {})
    tag = container.get("tag")
    if tag != release:
        out.append(("RELEASE_IDENTITY", f"[container].tag={tag} [ggen].release={release}"))
    section_text = changelog_section(inputs["changelog_text"], str(release))
    if section_text is None:
        out.append(("RELEASE_UNRECORDED", f"CHANGELOG.md has no '## [{release}]' section"))

    wf = workflow_defaults(workflow_on_block(inputs["workflow_text"]))
    onto = workflow_defaults(ontology_on_block(inputs["ontology_text"]))
    if wf != onto:
        out.append(("PROJECTION_PARITY", f"workflow={wf} ontology={onto}"))
    tags = [v for k, v in wf if k == "ggen_container_tag"]
    markets = [v for k, v in wf if k == "marketplace_sha"]
    if not tags or not markets:
        out.append(("WORKFLOW_DEFAULT_MISSING", f"ggen_container_tag={tags} marketplace_sha={markets}"))
    for value in tags:
        if value != tag:
            out.append(("WORKFLOW_CONTAINER_TAG", f"default={value} lock={tag}"))
    for value in markets:
        if not SHA40.fullmatch(value):
            out.append(("PIN_SHAPE", f"workflow marketplace_sha default={value!r}"))
        elif section_text is not None and value not in section_text:
            out.append(("MARKETPLACE_DEFAULT_UNRECORDED", f"{value} not cited in CHANGELOG [{release}]"))

    standing = container.get("standing")
    if standing not in STANDINGS:
        out.append(("CONTAINER_STANDING", f"standing={standing!r} outside vocabulary"))
    if container.get("requires_republish"):
        if standing != "BLOCKED" or not container.get("failure"):
            out.append(("CONTAINER_STANDING", "requires_republish without BLOCKED standing and typed failure"))
    elif standing == "ALIVE" and container.get("failure"):
        out.append(("CONTAINER_STANDING", "ALIVE while a failure is recorded"))
    digest = container.get("digest")
    if digest is not None and not DIGEST.fullmatch(str(digest)):
        out.append(("CONTAINER_STANDING", f"digest={digest!r} not sha256:<64 hex>"))

    base = lock.get("base_main_sha")
    if not isinstance(base, str) or not SHA40.fullmatch(base):
        out.append(("PIN_SHAPE", f"base_main_sha={base!r}"))
    else:
        if base == inputs["subject_sha"]:
            out.append(("BASE_IS_SUBJECT", base))
        elif not inputs["base_is_ancestor"]:
            out.append(("BASE_NOT_ANCESTOR", f"{base} is not an ancestor of {inputs['subject_sha']}"))

    updated = lock.get("updated_at")
    if not isinstance(updated, str) or not UPDATED_AT.fullmatch(updated):
        out.append(("UPDATED_AT_SHAPE", f"updated_at={updated!r}"))
    else:
        when = parse_utc(updated)
        slack = dt.timedelta(seconds=CLOCK_SLACK_SECONDS)
        base_time = inputs.get("base_commit_time")
        if base_time is not None and when + slack < base_time:
            out.append(("UPDATED_AT_STALE", f"{updated} precedes base commit {base_time.isoformat()}"))
        subject_time = inputs.get("subject_commit_time")
        if subject_time is not None and when - slack > subject_time:
            out.append(("UPDATED_AT_FUTURE", f"{updated} is after subject commit {subject_time.isoformat()}"))
    return out


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=check)


def load_inputs(root: Path, rev: str = "HEAD") -> dict:
    root = Path(root)
    parser = configparser.ConfigParser()
    parser.read_string((root / ".gitmodules").read_text())
    paths = [parser[s]["path"] for s in parser.sections() if s.startswith("submodule ")]
    subject = _git(root, "rev-parse", "--verify", f"{rev}^{{commit}}").stdout.strip()
    gitlinks: dict[str, str] = {}
    if paths:
        listing = _git(root, "ls-tree", subject, "--", *paths).stdout
        for line in listing.splitlines():
            meta, observed_path = line.split("\t", 1)
            mode, kind, sha = meta.split()
            if mode == "160000" and kind == "commit":
                gitlinks[observed_path] = sha
    lock_text = (root / "ecosystem.lock.toml").read_text()
    base = None
    try:
        base = tomllib.loads(lock_text).get("base_main_sha")
    except tomllib.TOMLDecodeError:
        pass
    base_is_ancestor = False
    base_time = None
    if isinstance(base, str) and SHA40.fullmatch(base):
        base_is_ancestor = _git(root, "merge-base", "--is-ancestor", base, subject, check=False).returncode == 0
        shown = _git(root, "show", "-s", "--format=%cI", base, check=False)
        if shown.returncode == 0:
            base_time = dt.datetime.fromisoformat(shown.stdout.strip())
    subject_time = dt.datetime.fromisoformat(_git(root, "show", "-s", "--format=%cI", subject).stdout.strip())
    return {
        "lock_text": lock_text,
        "gitmodules_paths": paths,
        "gitlinks": gitlinks,
        "workflow_text": (root / SYNC_WORKFLOW).read_text(),
        "ontology_text": (root / "ontology.ttl").read_text(),
        "changelog_text": (root / "CHANGELOG.md").read_text(),
        "subject_sha": subject,
        "base_is_ancestor": base_is_ancestor,
        "base_commit_time": base_time,
        "subject_commit_time": subject_time,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--rev", default="HEAD")
    args = ap.parse_args(argv)
    inputs = load_inputs(Path(args.root), args.rev)
    violations = evaluate(inputs)
    print(json.dumps({
        "schema": "https://ggen.dev/receipts/lock-crown-court/v1",
        "subject": inputs["subject_sha"],
        "authority": "NONE",
        "standing": "ALIVE" if not violations else "REFUSED",
        "violations": [{"code": c, "detail": d} for c, d in violations],
    }, indent=2, sort_keys=True))
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
