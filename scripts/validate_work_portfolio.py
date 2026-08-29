#!/usr/bin/env python3
"""Executable admission court for 50+100 manufacturing work portfolios."""
import argparse, glob, json, re, sys
from pathlib import Path

RULES = json.loads(r'''{"plan-id-format":{"key":"plan_id","good":"ws1-20260829-0800","standing":"REFUSED[PLAN_ID_FORMAT]"},"subject-exact-sha":{"key":"subject_sha","good":"5bcaee178cd9da5ba87ac99a8e8e968efa1e2cfb","standing":"REFUSED[SUBJECT_SHA_MUTABLE]"},"base-exact-sha":{"key":"base_sha","good":"5bcaee178cd9da5ba87ac99a8e8e968efa1e2cfb","standing":"REFUSED[BASE_SHA_MUTABLE]"},"head-exact-sha":{"key":"head_sha","good":"1111111111111111111111111111111111111111","standing":"REFUSED[HEAD_SHA_MUTABLE]"},"default-branch-bound":{"key":"default_branch","good":"main","standing":"REFUSED[DEFAULT_BRANCH_MISSING]"},"primary-minimum":{"key":"primary_count","good":50,"standing":"REFUSED[PRIMARY_UNDERFILLED]"},"reserve-minimum":{"key":"reserve_count","good":100,"standing":"REFUSED[RESERVE_UNDERFILLED]"},"work-key-uniqueness":{"key":"work_keys_unique","good":true,"standing":"REFUSED[DUPLICATE_WORK_KEY]"},"fingerprint-uniqueness":{"key":"fingerprints_unique","good":true,"standing":"REFUSED[DUPLICATE_FINGERPRINT]"},"acceptance-edge-uniqueness":{"key":"acceptance_edges_unique","good":true,"standing":"REFUSED[DUPLICATE_ACCEPTANCE_EDGE]"},"fingerprint-validity":{"key":"fingerprints_valid","good":true,"standing":"REFUSED[FINGERPRINT_MISMATCH]"},"dependencies-resolved":{"key":"dependencies_resolved","good":true,"standing":"REFUSED[UNKNOWN_DEPENDENCY]"},"dag-acyclic":{"key":"dag_acyclic","good":true,"standing":"REFUSED[DEPENDENCY_CYCLE]"},"primary-dependency-admission":{"key":"primary_dependencies_admitted","good":true,"standing":"REFUSED[PRIMARY_DEPENDENCY_UNADMITTED]"},"reserve-routes-defined":{"key":"reserve_routes_defined","good":true,"standing":"REFUSED[RESERVE_ROUTE_MISSING]"},"hypotheses-nonempty":{"key":"hypotheses_nonempty","good":true,"standing":"REFUSED[HYPOTHESIS_MISSING]"},"files-surfaces-nonempty":{"key":"files_surfaces_nonempty","good":true,"standing":"REFUSED[FILES_SURFACES_MISSING]"},"files-relative":{"key":"files_relative","good":true,"standing":"REFUSED[ABSOLUTE_SURFACE]"},"files-no-traversal":{"key":"files_no_traversal","good":true,"standing":"REFUSED[SURFACE_TRAVERSAL]"},"generated-surfaces-fenced":{"key":"generated_surfaces_excluded","good":true,"standing":"REFUSED[GENERATED_SURFACE_EDIT]"},"verifiers-nonempty":{"key":"verifiers_nonempty","good":true,"standing":"REFUSED[VERIFIER_MISSING]"},"falsifiers-nonempty":{"key":"falsifiers_nonempty","good":true,"standing":"REFUSED[FALSIFIER_MISSING]"},"rollbacks-nonempty":{"key":"rollbacks_nonempty","good":true,"standing":"REFUSED[ROLLBACK_MISSING]"},"next-routes-nonempty":{"key":"next_routes_nonempty","good":true,"standing":"REFUSED[NEXT_ROUTE_MISSING]"},"wip-limit":{"key":"max_wip_per_lane","good":3,"standing":"REFUSED[WIP_LIMIT_EXCEEDED]"},"active-lane-dedup":{"key":"active_collision_count","good":0,"standing":"REFUSED[ACTIVE_LANE_COLLISION]"},"immutable-source-refs":{"key":"mutable_ref_count","good":0,"standing":"REFUSED[MUTABLE_IDENTITY]"},"fresh-sha-binding":{"key":"stale_sha_count","good":0,"standing":"REFUSED[STALE_SHA]"},"authority-non-escalation":{"key":"authority_escalation_count","good":0,"standing":"REFUSED[AUTHORITY_ESCALATION]"},"brce-only-do":{"key":"unreceipted_do_route_count","good":0,"standing":"REFUSED[UNRECEIPTED_DO]"},"release-authority":{"key":"release_routes_authorized","good":true,"standing":"REFUSED[RELEASE_AUTHORITY]"},"deployment-authority":{"key":"deployment_routes_authorized","good":true,"standing":"REFUSED[DEPLOYMENT_AUTHORITY]"},"merge-exact-head":{"key":"merge_exact_head_guarded","good":true,"standing":"REFUSED[MERGE_HEAD_UNGUARDED]"},"message-authority":{"key":"message_routes_authorized","good":true,"standing":"REFUSED[MESSAGE_AUTHORITY]"},"permission-ceiling":{"key":"permission_escalation_count","good":0,"standing":"REFUSED[PERMISSION_ESCALATION]"},"receipt-secret-fence":{"key":"secret_field_count","good":0,"standing":"REFUSED[SECRET_IN_RECEIPT]"},"public-identity-fence":{"key":"private_identity_count","good":0,"standing":"REFUSED[PRIVATE_IDENTITY_DISCLOSURE]"},"receipt-subject-match":{"key":"receipt_subject_match","good":true,"standing":"REFUSED[RECEIPT_SUBJECT_MISMATCH]"},"replay-subject-match":{"key":"replay_subject_match","good":true,"standing":"REFUSED[REPLAY_SUBJECT_MISMATCH]"},"second-generation-identity":{"key":"second_generation_identical","good":true,"standing":"REFUSED[SECOND_GENERATION_DRIFT]"},"scenario-coverage":{"key":"scenario_coverage_complete","good":true,"standing":"REFUSED[SCENARIO_COVERAGE_GAP]"},"typed-failure-routes":{"key":"failure_routes_typed","good":true,"standing":"REFUSED[UNTYPED_FAILURE]"},"standing-vocabulary":{"key":"statuses_valid","good":true,"standing":"REFUSED[INVALID_STANDING]"},"commands-recorded":{"key":"commands_recorded","good":true,"standing":"REFUSED[COMMAND_EVIDENCE_MISSING]"},"exits-recorded":{"key":"exits_recorded","good":true,"standing":"REFUSED[EXIT_EVIDENCE_MISSING]"},"consequences-recorded":{"key":"consequences_recorded","good":true,"standing":"REFUSED[CONSEQUENCE_EVIDENCE_MISSING]"},"continuous-push":{"key":"push_continuous","good":true,"standing":"REFUSED[PUSH_RECEIPT_MISSING]"},"reversible-rollback":{"key":"rollback_reversible","good":true,"standing":"REFUSED[IRREVERSIBLE_ROLLBACK]"},"handoff-defined":{"key":"next_hour_handoff_defined","good":true,"standing":"REFUSED[HANDOFF_MISSING]"},"exact-head-verification":{"key":"exact_head_verified","good":true,"standing":"REFUSED[EXACT_HEAD_UNVERIFIED]"}}''')
CANONICAL = json.loads(r'''{"plan_id":"ws1-20260829-0800","subject_sha":"5bcaee178cd9da5ba87ac99a8e8e968efa1e2cfb","base_sha":"5bcaee178cd9da5ba87ac99a8e8e968efa1e2cfb","head_sha":"1111111111111111111111111111111111111111","default_branch":"main","primary_count":50,"reserve_count":100,"work_keys_unique":true,"fingerprints_unique":true,"acceptance_edges_unique":true,"fingerprints_valid":true,"dependencies_resolved":true,"dag_acyclic":true,"primary_dependencies_admitted":true,"reserve_routes_defined":true,"hypotheses_nonempty":true,"files_surfaces_nonempty":true,"files_relative":true,"files_no_traversal":true,"generated_surfaces_excluded":true,"verifiers_nonempty":true,"falsifiers_nonempty":true,"rollbacks_nonempty":true,"next_routes_nonempty":true,"max_wip_per_lane":3,"active_collision_count":0,"mutable_ref_count":0,"stale_sha_count":0,"authority_escalation_count":0,"unreceipted_do_route_count":0,"release_routes_authorized":true,"deployment_routes_authorized":true,"merge_exact_head_guarded":true,"message_routes_authorized":true,"permission_escalation_count":0,"secret_field_count":0,"private_identity_count":0,"receipt_subject_match":true,"replay_subject_match":true,"second_generation_identical":true,"scenario_coverage_complete":true,"failure_routes_typed":true,"statuses_valid":true,"commands_recorded":true,"exits_recorded":true,"consequences_recorded":true,"push_continuous":true,"rollback_reversible":true,"next_hour_handoff_defined":true,"exact_head_verified":true}''')
SHA40 = re.compile(r"^[0-9a-f]{40}$")
PLAN_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
FP16 = re.compile(r"^[0-9a-f]{16}$")

def validate(observation):
    for edge, rule in RULES.items():
        value = observation.get(rule["key"])
        if edge == "plan-id-format":
            ok = isinstance(value, str) and bool(PLAN_ID.fullmatch(value))
        elif edge in {"subject-exact-sha", "base-exact-sha", "head-exact-sha"}:
            ok = isinstance(value, str) and bool(SHA40.fullmatch(value))
        elif edge == "primary-minimum":
            ok = isinstance(value, int) and value >= 50
        elif edge == "reserve-minimum":
            ok = isinstance(value, int) and value >= 100
        elif edge == "wip-limit":
            ok = isinstance(value, int) and 0 <= value <= 3
        else:
            ok = value == rule["good"]
        if not ok:
            return rule["standing"]
    return "ALIVE"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--fixtures", default="tests/fixtures/work-portfolio/*.json")
    ap.add_argument("--min-cases", type=int, default=1)
    args=ap.parse_args()
    paths=sorted(glob.glob(args.fixtures))
    if len(paths) < args.min_cases:
        print(f"REFUSED[CASE_CENSUS_UNDERFILLED]: {len(paths)} < {args.min_cases}", file=sys.stderr); return 1
    seen_ids=set(); seen_edges=set(); seen_fp=set()
    for path in paths:
        case=json.loads(Path(path).read_text())
        cid, edge, fp = case["id"], case["edge"], case["semantic_fingerprint"]
        if cid in seen_ids or edge in seen_edges or fp in seen_fp:
            print(f"REFUSED[DUPLICATE_CASE_IDENTITY]: {path}", file=sys.stderr); return 1
        seen_ids.add(cid); seen_edges.add(edge); seen_fp.add(fp)
        if edge not in RULES or not FP16.fullmatch(fp):
            print(f"REFUSED[MALFORMED_CASE_IDENTITY]: {path}", file=sys.stderr); return 1
        invalid=dict(CANONICAL); invalid.update(case["invalid"])
        control=dict(CANONICAL); control.update(case.get("control", {}))
        observed=validate(invalid); control_observed=validate(control)
        if observed != case["expected"] or control_observed != "ALIVE":
            print(f"BUILD_BROKEN[{cid}]: invalid={observed} expected={case['expected']} control={control_observed}", file=sys.stderr); return 1
    print(f"WORK_PORTFOLIO: ALIVE ({len(paths)} executable negative/control pairs)")
    return 0
if __name__ == "__main__":
    sys.exit(main())
