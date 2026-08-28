from pathlib import Path
def test_action_record_plan_exists():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(:action record-ppddl-plan' in t
