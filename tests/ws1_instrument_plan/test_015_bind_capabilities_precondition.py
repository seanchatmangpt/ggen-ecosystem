from pathlib import Path
def test_bind_capabilities_precondition():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':precondition (capability-vocabulary-admitted)' in t
