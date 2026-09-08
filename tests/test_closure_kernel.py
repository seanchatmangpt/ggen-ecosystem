import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from closure_kernel import (  # noqa: E402
    ChildState,
    ClosureRequest,
    DeadEdge,
    DecisionKind,
    EvidenceGap,
    RefusalCode,
    Standing,
    plan_closure,
)


class ClosureKernelContractTests(unittest.TestCase):
    def kinds(self, plan):
        return {d.kind for d in plan.decisions}

    def test_alive_requires_exact_execution_verification_and_receipt(self):
        partial = plan_closure(ClosureRequest(subject_id="repo@sha", exact_subject_verified=True, receipt_present=True))
        self.assertEqual(Standing.PARTIAL_ALIVE, partial.standing)
        self.assertIn(DecisionKind.VERIFY_EXACT_SUBJECT, self.kinds(partial))
        alive = plan_closure(ClosureRequest(subject_id="repo@sha", exact_subject_executed=True, exact_subject_verified=True, receipt_present=True))
        self.assertEqual(Standing.ALIVE, alive.standing); self.assertIn(DecisionKind.CLOSE, self.kinds(alive)); self.assertFalse(alive.actuated)

    def test_same_failed_hypothesis_gets_at_most_one_retry(self):
        first = plan_closure(ClosureRequest(subject_id="workflow@sha", dead_edges=(DeadEdge("ci", "same-hypothesis", same_hypothesis_failures=1),)))
        repeated = plan_closure(ClosureRequest(subject_id="workflow@sha", dead_edges=(DeadEdge("ci", "same-hypothesis", same_hypothesis_failures=2),)))
        self.assertIn(DecisionKind.RETRY_ONCE, self.kinds(first)); self.assertNotIn(DecisionKind.RETRY_ONCE, self.kinds(repeated)); self.assertIn(DecisionKind.REPAIR_DEMAND, self.kinds(repeated))

    def test_new_hypothesis_reopens_dead_edge(self):
        old = plan_closure(ClosureRequest(subject_id="workflow@sha", dead_edges=(DeadEdge("ci", "hypothesis-a", same_hypothesis_failures=3),)))
        new = plan_closure(ClosureRequest(subject_id="workflow@sha", dead_edges=(DeadEdge("ci", "hypothesis-b", same_hypothesis_failures=1),)))
        self.assertIn(DecisionKind.REPAIR_DEMAND, self.kinds(old)); self.assertIn(DecisionKind.RETRY_ONCE, self.kinds(new))

    def test_missing_capability_manufactures_child_instead_of_asking_operator(self):
        plan = plan_closure(ClosureRequest(subject_id="parent", missing_capabilities=("receipt-replay",)))
        self.assertIn(DecisionKind.CHILD_MANUFACTURE, self.kinds(plan)); self.assertTrue(any(d.target == "receipt-replay" for d in plan.decisions))

    def test_child_resumes_parent_only_with_verification_and_receipt_pair(self):
        not_ready = plan_closure(ClosureRequest(subject_id="parent", child_states=(ChildState("child", verified_exact_subject=True),)))
        ready = plan_closure(ClosureRequest(subject_id="parent", child_states=(ChildState("child", True, True),)))
        self.assertNotIn(DecisionKind.RESUME_PARENT, self.kinds(not_ready)); self.assertIn(DecisionKind.RESUME_PARENT, self.kinds(ready))

    def test_ready_child_is_not_remanufactured(self):
        plan = plan_closure(ClosureRequest(subject_id="parent", missing_capabilities=("child",), child_states=(ChildState("child", True, True),)))
        child_kinds = {d.kind for d in plan.decisions if d.target == "child"}
        self.assertIn(DecisionKind.RESUME_PARENT, child_kinds); self.assertNotIn(DecisionKind.CHILD_MANUFACTURE, child_kinds)

    def test_blocked_edge_is_topology_and_preserves_alternatives(self):
        plan = plan_closure(ClosureRequest(subject_id="provider-selection", dead_edges=(DeadEdge("provider-a", "availability", blocked=True, alternate_candidate_count=2),)))
        self.assertEqual(Standing.PARTIAL_ALIVE, plan.standing); self.assertEqual(("provider-a:alternate:1", "provider-a:alternate:2"), plan.preserved_candidates)

    def test_no_alternative_block_is_blocked_not_refused(self):
        plan = plan_closure(ClosureRequest(subject_id="provider-selection", dead_edges=(DeadEdge("only-provider", "availability", blocked=True),)))
        self.assertEqual(Standing.BLOCKED, plan.standing)

    def test_unsupported_without_alternative_is_unsupported_not_blocked(self):
        plan = plan_closure(ClosureRequest(subject_id="provider-selection", dead_edges=(DeadEdge("only-provider", "capability", unsupported=True),)))
        self.assertEqual(Standing.UNSUPPORTED, plan.standing); self.assertNotEqual(Standing.BLOCKED, plan.standing)

    def test_repeated_failed_edge_without_alternative_is_build_broken(self):
        plan = plan_closure(ClosureRequest(subject_id="workflow@sha", dead_edges=(DeadEdge("ci", "same", same_hypothesis_failures=2),)))
        self.assertEqual(Standing.BUILD_BROKEN, plan.standing); self.assertIn(DecisionKind.REPAIR_DEMAND, self.kinds(plan))

    def test_lab_scope_cannot_crown_production(self):
        plan = plan_closure(ClosureRequest(subject_id="repo@sha", exact_subject_executed=True, exact_subject_verified=True, receipt_present=True, evidence_scope="lab", target_scope="production"))
        self.assertEqual(Standing.PARTIAL_ALIVE, plan.standing); self.assertIn(DecisionKind.VERIFY_EXACT_SUBJECT, self.kinds(plan))

    def test_generated_projection_cannot_claim_source_authority(self):
        plan = plan_closure(ClosureRequest(subject_id="projection", source_authority="generated_projection")); refusal = next(d for d in plan.decisions if d.kind == DecisionKind.REFUSE)
        self.assertEqual(Standing.REFUSED, plan.standing); self.assertEqual(RefusalCode.E007_SOURCE_AUTHORITY, refusal.refusal_code)

    def test_hypothesis_has_no_ambient_actuation_authority(self):
        plan = plan_closure(ClosureRequest(subject_id="dream", hypothesis_requests_actuation=True)); refusal = next(d for d in plan.decisions if d.kind == DecisionKind.REFUSE)
        self.assertEqual(Standing.REFUSED, plan.standing); self.assertEqual(RefusalCode.E008_AMBIENT_EXECUTION, refusal.refusal_code)

    def test_authorized_irreversible_action_is_only_a_brce_intent(self):
        plan = plan_closure(ClosureRequest(subject_id="deploy", irreversible_action_requested=True, brce_authorized=True)); intent = next(d for d in plan.decisions if d.kind == DecisionKind.BRCE_INTENT)
        self.assertFalse(plan.actuated); self.assertTrue(intent.requires_brce)

    def test_irreversible_action_without_brce_is_typed_refusal(self):
        plan = plan_closure(ClosureRequest(subject_id="merge", irreversible_action_requested=True)); refusal = next(d for d in plan.decisions if d.kind == DecisionKind.REFUSE)
        self.assertEqual(Standing.REFUSED, plan.standing); self.assertEqual(RefusalCode.E001_AUTHORITY, refusal.refusal_code); self.assertTrue(refusal.requires_brce)

    def test_remaining_evidence_gap_prevents_alive(self):
        plan = plan_closure(ClosureRequest(subject_id="repo@sha", exact_subject_executed=True, exact_subject_verified=True, receipt_present=True, evidence_gaps=(EvidenceGap("E2E", "real provider execution missing", "integration"),)))
        self.assertEqual(Standing.PARTIAL_ALIVE, plan.standing); self.assertNotIn(DecisionKind.CLOSE, self.kinds(plan))

    def test_digest_is_order_invariant_for_set_like_inputs(self):
        a = ClosureRequest(subject_id="repo@sha", missing_capabilities=("b", "a"), evidence_gaps=(EvidenceGap("Z", "z"), EvidenceGap("A", "a")))
        b = ClosureRequest(subject_id="repo@sha", missing_capabilities=("a", "b"), evidence_gaps=(EvidenceGap("A", "a"), EvidenceGap("Z", "z")))
        self.assertEqual(plan_closure(a).digest, plan_closure(b).digest)

    def test_cli_emits_machine_readable_non_actuating_plan(self):
        payload = json.dumps({"subject_id":"repo@sha","exact_subject_executed":True,"exact_subject_verified":True,"receipt_present":True})
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "closure_kernel.py")], input=payload, text=True, capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr); doc = json.loads(result.stdout); self.assertEqual("ALIVE", doc["standing"]); self.assertFalse(doc["actuated"]); self.assertTrue(doc["digest"].startswith("sha256:"))

if __name__ == "__main__": unittest.main()
