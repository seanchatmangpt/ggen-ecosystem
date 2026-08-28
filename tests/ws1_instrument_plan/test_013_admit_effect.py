from pathlib import Path
def test_admit_effect():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':effect (capability-vocabulary-admitted)' in t
