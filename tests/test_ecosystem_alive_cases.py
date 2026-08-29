import json
import subprocess
import unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location("ecosystem_alive",ROOT/"scripts"/"ecosystem_alive.py")
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

class AliveCases(unittest.TestCase):
    def test_cases(self):
        paths=sorted((ROOT/"tests"/"fixtures"/"alive").glob("*.json"))
        self.assertGreaterEqual(len(paths),1)
        for path in paths:
            with self.subTest(case=path.name):
                case=json.loads(path.read_text())
                if case["kind"]=="plan":
                    plan=MOD.plan_closure_autofde(case["gates"])
                    for key,value in case.get("expect",{}).items():
                        if key=="step_count": self.assertEqual(len(plan["steps"]),value)
                        elif key=="first_type": self.assertEqual(plan["steps"][0]["type"],value)
                        elif key=="first_action": self.assertEqual(plan["steps"][0]["action"],value)
                        elif key=="action_contains": self.assertTrue(any(value in s["action"] for s in plan["steps"]))
                        elif key=="action_absent": self.assertFalse(any(value in s["action"] for s in plan["steps"]))
                        else: self.assertEqual(plan[key],value)
                else:
                    exits=list(case["exits"]); calls=[]
                    def runner(argv,**kwargs):
                        calls.append({"argv":argv,"kwargs":kwargs})
                        code=exits.pop(0)
                        return subprocess.CompletedProcess(argv,code,case.get("stdout",""),case.get("stderr",""))
                    steps=[MOD._step(s["argv"],s["cost"],s["description"],authority=s.get("authority")) for s in case["steps"]]
                    result=MOD.execute_safe_steps({"steps":steps},runner)
                    self.assertEqual(result["standing"],case["expect"]["standing"])
                    self.assertEqual(len(calls),case["expect"]["calls"])
                    self.assertEqual(len(result["receipts"]),case["expect"]["receipts"])
                    if calls:
                        self.assertNotIn("shell",calls[0]["kwargs"])
                        self.assertEqual(calls[0]["kwargs"]["cwd"],MOD.REPO_ROOT)
                    if result["receipts"]:
                        receipt=result["receipts"][-1]
                        for key,value in case["expect"].get("receipt",{}).items():
                            self.assertEqual(receipt[key],value)

if __name__=="__main__":
    unittest.main()
