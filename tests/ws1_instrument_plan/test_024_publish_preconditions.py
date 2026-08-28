from pathlib import Path
def test_publish_preconditions():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text()
 for fact in ('(ecosystem-base-current)','(capability-vocabulary-admitted)','(ggen-capabilities-bound)','(provenance-bound)','(ppddl-plan-recorded)'): assert fact in t[t.index('(:action publish-ecosystem-pr'):]
