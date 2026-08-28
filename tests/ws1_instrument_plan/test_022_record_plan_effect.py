from pathlib import Path
def test_record_plan_effect():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':effect (ppddl-plan-recorded)' in t
