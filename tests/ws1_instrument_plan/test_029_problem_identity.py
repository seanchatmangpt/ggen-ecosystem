from pathlib import Path
def test_problem_identity():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(define (problem realize-instrument-gain-in-ggen-ecosystem)' in t
