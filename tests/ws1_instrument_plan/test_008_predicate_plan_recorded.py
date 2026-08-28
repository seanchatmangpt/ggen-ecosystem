from pathlib import Path
def test_predicate_plan_recorded():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(ppddl-plan-recorded)' in t
