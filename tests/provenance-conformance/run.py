#!/usr/bin/env python3
import json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
G="c61ee99359c9dbc7b3cb71687976932a3e737ed4"; M="89adf4c8476f7edc8067fdbb1c256cfbfa22df6a"; D="sha256:"+"b"*64
LOCK=f"""version=2
[ggen]
commit_sha = "{G}"
linux_x86_64_asset_sha256 = "UNKNOWN-TODO"
observed_executable_sha256 = "UNKNOWN-TODO"
[ggen_marketplace]
sha = "{M}"
[submodules]
ggen_commit = "{G}"
ggen_marketplace_commit = "{M}"
[container]
tag = "v26.8.28"
digest = "{D}"
"""
MAN='[packs]\ngithub-actions = { path = "vendor/ggen-marketplace/packs/github-actions-pack" }\n'
def w(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s)
def setup(root,c):
 w(root/"ecosystem.lock.toml",LOCK); w(root/"ggen.toml",MAN); w(root/"docs/DEFINITION-OF-DONE.md","# dod\n"); w(root/".github/workflows/ggen-ecosystem-sync.yml","x"); w(root/".github/workflows/ggen-ecosystem-container.yml","x")
 (root/"vendor/ggen").mkdir(parents=True); (root/"vendor/ggen-marketplace/packs/github-actions-pack").mkdir(parents=True)
 (root/"scripts").mkdir(parents=True,exist_ok=True); shutil.copy2(Path(__file__).resolve().parents[2]/"scripts/verify-provenance.sh",root/"scripts/verify-provenance.sh")
 b=root/"bin"; b.mkdir(); gr=c.get("ggen_real",G); mr=c.get("market_real",M)
 git='#!/bin/sh\ncase "$*" in *ggen-marketplace*) echo "'+mr+'";; *vendor/ggen*) echo "'+gr+'";; *) exit 3;; esac\n'
 if c.get("git_mode")=="fail": git='#!/bin/sh\nexit 128\n'
 w(b/"git",git); (b/"git").chmod(0o755); w(b/"python3",'#!/bin/sh\nexec /usr/bin/python3 -S "$@"\n'); (b/"python3").chmod(0o755)
 if c.get("ggen_mode")!="absent":
  if c.get("ggen_mode")=="fail": gs='#!/bin/sh\nexit 9\n'
  else:
   payload=json.dumps({"written":c.get("written",[]),"decisions":c.get("decisions",{".github/workflows/ggen-ecosystem-sync.yml":"unchanged: content identical",".github/workflows/ggen-ecosystem-container.yml":"unchanged: content identical"})}); gs='#!/bin/sh\ncat <<EOF\n'+payload+'\nEOF\n'
  w(b/"ggen",gs); (b/"ggen").chmod(0o755)
 for rel in c.get("remove",[]):
  p=root/rel
  if p.is_dir(): shutil.rmtree(p)
  elif p.exists(): p.unlink()
 for rel,s in c.get("replace_files",{}).items(): w(root/rel,s)
 for rel in c.get("mkdir",[]): (root/rel).mkdir(parents=True,exist_ok=True)
 return b
def main():
 d=Path(sys.argv[1] if len(sys.argv)>1 else "tests/provenance-conformance/cases"); files=sorted(d.glob("*.json")); bad=[]
 for cp in files:
  c=json.loads(cp.read_text())
  with tempfile.TemporaryDirectory() as td:
   r=Path(td); b=setup(r,c); e=os.environ.copy(); e["PATH"]=str(b)+os.pathsep+e["PATH"]
   p=subprocess.run(["bash","scripts/verify-provenance.sh"],cwd=r,env=e,text=True,capture_output=True); out=p.stdout+p.stderr
   if p.returncode!=c["expected_exit"] or any(x not in out for x in c["must_contain"]): bad.append({"id":c["id"],"exit":p.returncode,"out":out})
 if bad: print(json.dumps(bad,indent=2)); return 1
 print(f"ALIVE {len(files)}/{len(files)} provenance conformance cases"); return 0
if __name__=="__main__": raise SystemExit(main())
