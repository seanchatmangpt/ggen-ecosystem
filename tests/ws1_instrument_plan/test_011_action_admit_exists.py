from pathlib import Path
def test_action_admit_exists():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(:action admit-capability-vocabulary' in t
