from pathlib import Path
def test_action_merge_exists():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(:action merge-ecosystem-pr' in t
