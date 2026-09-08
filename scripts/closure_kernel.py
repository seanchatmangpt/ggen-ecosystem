#!/usr/bin/env python3
"""Deterministic SELECT/CONSTRUCT closure kernel. Never actuates."""
from __future__ import annotations
import argparse, hashlib, json, sys
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

class Standing(str, Enum):
    UNKNOWN="UNKNOWN"; PARTIAL_ALIVE="PARTIAL_ALIVE"; ALIVE="ALIVE"; BLOCKED="BLOCKED"
    BUILD_BROKEN="BUILD_BROKEN"; UNSUPPORTED="UNSUPPORTED"; REFUSED="REFUSED"
class DecisionKind(str, Enum):
    RETRY_ONCE="RETRY_ONCE"; REPAIR_DEMAND="REPAIR_DEMAND"; CHILD_MANUFACTURE="CHILD_MANUFACTURE"
    RESUME_PARENT="RESUME_PARENT"; VERIFY_EXACT_SUBJECT="VERIFY_EXACT_SUBJECT"; BRCE_INTENT="BRCE_INTENT"
    PRESERVE_ALTERNATIVES="PRESERVE_ALTERNATIVES"; CLOSE="CLOSE"; REFUSE="REFUSE"
class RefusalCode(str, Enum):
    E001_AUTHORITY="E001_AUTHORITY"; E007_SOURCE_AUTHORITY="E007_SOURCE_AUTHORITY"; E008_AMBIENT_EXECUTION="E008_AMBIENT_EXECUTION"

@dataclass(frozen=True, order=True)
class EvidenceGap:
    code:str; description:str; required_scope:str="subject"
@dataclass(frozen=True)
class DeadEdge:
    edge_id:str; hypothesis_id:str; same_hypothesis_failures:int=1; alternate_candidate_count:int=0
    unsupported:bool=False; blocked:bool=False
@dataclass(frozen=True)
class ChildState:
    child_id:str; verified_exact_subject:bool=False; receipt_present:bool=False
@dataclass(frozen=True)
class ClosureRequest:
    subject_id:str; source_authority:str="canonical"; requested_standing:Standing=Standing.ALIVE
    current_standing:Standing=Standing.UNKNOWN; exact_subject_executed:bool=False; exact_subject_verified:bool=False
    receipt_present:bool=False; evidence_scope:str="subject"; target_scope:str="subject"
    evidence_gaps:tuple[EvidenceGap,...]=field(default_factory=tuple); dead_edges:tuple[DeadEdge,...]=field(default_factory=tuple)
    missing_capabilities:tuple[str,...]=field(default_factory=tuple); child_states:tuple[ChildState,...]=field(default_factory=tuple)
    irreversible_action_requested:bool=False; brce_authorized:bool=False; hypothesis_requests_actuation:bool=False
    generated_projection_claims_authority:bool=False
@dataclass(frozen=True)
class ClosureDecision:
    kind:DecisionKind; target:str; reason:str; standing:Standing; requires_brce:bool=False; refusal_code:RefusalCode|None=None
@dataclass(frozen=True)
class ClosurePlan:
    subject_id:str; standing:Standing; decisions:tuple[ClosureDecision,...]; preserved_candidates:tuple[str,...]
    gaps:tuple[EvidenceGap,...]; digest:str; actuated:bool=False
    def to_dict(self)->dict[str,Any]:
        return {"subject_id":self.subject_id,"standing":self.standing.value,
            "decisions":[{"kind":d.kind.value,"target":d.target,"reason":d.reason,"standing":d.standing.value,
                "requires_brce":d.requires_brce,"refusal_code":d.refusal_code.value if d.refusal_code else None} for d in self.decisions],
            "preserved_candidates":list(self.preserved_candidates),"gaps":[asdict(g) for g in self.gaps],"digest":self.digest,"actuated":False}

def _canon(v:Any)->Any:
    if isinstance(v,Enum): return v.value
    if hasattr(v,"__dataclass_fields__"): return _canon(asdict(v))
    if isinstance(v,dict): return {k:_canon(v[k]) for k in sorted(v)}
    if isinstance(v,(tuple,list)):
        xs=[_canon(x) for x in v]
        return sorted(xs,key=lambda x:json.dumps(x,sort_keys=True,separators=(",",":")))
    return v

def _d(kind,req,reason,standing,target=None,requires_brce=False,refusal_code=None):
    return ClosureDecision(kind,target or req.subject_id,reason,standing,requires_brce,refusal_code)

def _finish(req,standing,decisions,preserved,gaps):
    ds=tuple(sorted(decisions,key=lambda d:(d.kind.value,d.target,d.reason)))
    payload={"request":_canon(req),"decisions":_canon(ds),"standing":standing.value}
    digest="sha256:"+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return ClosurePlan(req.subject_id,standing,ds,tuple(sorted(preserved)),gaps,digest)

def plan_closure(req:ClosureRequest)->ClosurePlan:
    ds=[]; preserved=set(); gaps=tuple(sorted(req.evidence_gaps))
    if req.generated_projection_claims_authority or req.source_authority=="generated_projection":
        s=Standing.REFUSED; ds.append(_d(DecisionKind.REFUSE,req,"Generated projections cannot acquire source authority.",s,refusal_code=RefusalCode.E007_SOURCE_AUTHORITY)); return _finish(req,s,ds,preserved,gaps)
    if req.hypothesis_requests_actuation:
        s=Standing.REFUSED; ds.append(_d(DecisionKind.REFUSE,req,"Hypotheses/dreams/planner output have no ambient execution authority.",s,refusal_code=RefusalCode.E008_AMBIENT_EXECUTION)); return _finish(req,s,ds,preserved,gaps)
    if req.irreversible_action_requested and not req.brce_authorized:
        s=Standing.REFUSED; ds.append(_d(DecisionKind.REFUSE,req,"Irreversible action lacks admitted BRCE authority.",s,requires_brce=True,refusal_code=RefusalCode.E001_AUTHORITY)); return _finish(req,s,ds,preserved,gaps)
    if req.irreversible_action_requested:
        ds.append(_d(DecisionKind.BRCE_INTENT,req,"Admitted consequential action is an intent for BRCE; kernel does not actuate.",Standing.PARTIAL_ALIVE,requires_brce=True))

    ready={c.child_id for c in req.child_states if c.verified_exact_subject and c.receipt_present}
    for c in sorted(req.child_states,key=lambda x:x.child_id):
        if c.child_id in ready: ds.append(_d(DecisionKind.RESUME_PARENT,req,f"Verified+receipted child {c.child_id} may resume parent.",Standing.PARTIAL_ALIVE,c.child_id))
        elif c.verified_exact_subject or c.receipt_present: ds.append(_d(DecisionKind.VERIFY_EXACT_SUBJECT,req,f"Child {c.child_id} lacks verification+receipt pair.",Standing.PARTIAL_ALIVE,c.child_id))
    for cap in sorted(set(req.missing_capabilities)-ready): ds.append(_d(DecisionKind.CHILD_MANUFACTURE,req,f"Manufacture and qualify missing capability: {cap}.",Standing.PARTIAL_ALIVE,cap))

    hard_block=hard_unsup=failed_no_alt=0
    for e in sorted(req.dead_edges,key=lambda x:(x.edge_id,x.hypothesis_id)):
        for i in range(e.alternate_candidate_count): preserved.add(f"{e.edge_id}:alternate:{i+1}")
        if e.unsupported:
            ds.append(_d(DecisionKind.PRESERVE_ALTERNATIVES,req,f"Unsupported edge {e.edge_id}; preserve alternatives.",Standing.UNSUPPORTED,e.edge_id)); hard_unsup+=not e.alternate_candidate_count; continue
        if e.blocked:
            ds.append(_d(DecisionKind.PRESERVE_ALTERNATIVES,req,f"Blocked edge {e.edge_id}; preserve alternatives.",Standing.BLOCKED,e.edge_id)); hard_block+=not e.alternate_candidate_count; continue
        failed_no_alt+=not e.alternate_candidate_count
        if e.same_hypothesis_failures<=1: ds.append(_d(DecisionKind.RETRY_ONCE,req,f"First failure for hypothesis {e.hypothesis_id}; one retry admissible.",Standing.BUILD_BROKEN,e.edge_id,True))
        else: ds.append(_d(DecisionKind.REPAIR_DEMAND,req,f"Repeated unchanged failure on {e.edge_id}; manufacture repair demand.",Standing.BUILD_BROKEN,e.edge_id))
    if hard_block and not preserved and not req.missing_capabilities: return _finish(req,Standing.BLOCKED,ds,preserved,gaps)
    if hard_unsup and not preserved and not hard_block and not req.missing_capabilities: return _finish(req,Standing.UNSUPPORTED,ds,preserved,gaps)

    mismatch=req.evidence_scope!=req.target_scope
    if req.requested_standing==Standing.ALIVE and mismatch: ds.append(_d(DecisionKind.VERIFY_EXACT_SUBJECT,req,"Evidence scope does not match target scope.",Standing.PARTIAL_ALIVE))
    exact=req.exact_subject_executed and req.exact_subject_verified and req.receipt_present and not gaps and not mismatch and not req.missing_capabilities and not any(d.kind in {DecisionKind.RETRY_ONCE,DecisionKind.REPAIR_DEMAND} for d in ds)
    if exact: ds.append(_d(DecisionKind.CLOSE,req,"Exact subject executed, independently verified, and receipted with no gaps.",Standing.ALIVE)); return _finish(req,Standing.ALIVE,ds,preserved,gaps)
    if not req.exact_subject_executed: ds.append(_d(DecisionKind.VERIFY_EXACT_SUBJECT,req,"Exact admitted subject has not been observed executing.",Standing.PARTIAL_ALIVE))
    elif not req.exact_subject_verified: ds.append(_d(DecisionKind.VERIFY_EXACT_SUBJECT,req,"Execution exists; independent verification missing.",Standing.PARTIAL_ALIVE))
    elif not req.receipt_present: ds.append(_d(DecisionKind.VERIFY_EXACT_SUBJECT,req,"Verification exists; required receipt missing.",Standing.PARTIAL_ALIVE))
    for g in gaps: ds.append(_d(DecisionKind.VERIFY_EXACT_SUBJECT,req,f"Evidence gap {g.code}: {g.description}",Standing.PARTIAL_ALIVE,g.required_scope))
    return _finish(req,Standing.BUILD_BROKEN if failed_no_alt and not preserved else (Standing.PARTIAL_ALIVE if ds else req.current_standing),ds,preserved,gaps)

def from_dict(d):
    return ClosureRequest(subject_id=d["subject_id"],source_authority=d.get("source_authority","canonical"),requested_standing=Standing(d.get("requested_standing","ALIVE")),current_standing=Standing(d.get("current_standing","UNKNOWN")),exact_subject_executed=bool(d.get("exact_subject_executed")),exact_subject_verified=bool(d.get("exact_subject_verified")),receipt_present=bool(d.get("receipt_present")),evidence_scope=d.get("evidence_scope","subject"),target_scope=d.get("target_scope","subject"),evidence_gaps=tuple(EvidenceGap(**x) for x in d.get("evidence_gaps",[])),dead_edges=tuple(DeadEdge(**x) for x in d.get("dead_edges",[])),missing_capabilities=tuple(d.get("missing_capabilities",[])),child_states=tuple(ChildState(**x) for x in d.get("child_states",[])),irreversible_action_requested=bool(d.get("irreversible_action_requested")),brce_authorized=bool(d.get("brce_authorized")),hypothesis_requests_actuation=bool(d.get("hypothesis_requests_actuation")),generated_projection_claims_authority=bool(d.get("generated_projection_claims_authority")))
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("input",nargs="?"); a=p.parse_args(argv); f=open(a.input) if a.input else sys.stdin
    try: out=plan_closure(from_dict(json.load(f))).to_dict()
    finally:
        if a.input: f.close()
    print(json.dumps(out,sort_keys=True,separators=(",",":"))); return 0
if __name__=="__main__": raise SystemExit(main())
