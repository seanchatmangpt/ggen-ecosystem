## Subject

- Repository: `seanchatmangpt/ggen-ecosystem`
- Base ref: `main`
- Exact base SHA: `<sha>`
- Exact head SHA: `<sha>`

## What this changes

<!-- One or two sentences. If this regenerates the sync workflow, name the authoritative ontology/config/pack input that changed. -->

## Standing and evidence

<!-- Use only the standing vocabulary from AGENTS.md. Paste commands plus exits/output; GitHub status metadata alone is not execution proof. -->

Standing: `UNKNOWN`

- [ ] Narrowest relevant verifier executed
- [ ] `just doctor` (or `bash scripts/doctor.sh`) executed when the environment supports it
- [ ] If certification changed: `just certify-test` executed
- [ ] If the container/customer journey changed: `just chicago` executed or the unavailable boundary is typed below
- [ ] Exact PR head re-read after the last push

```text
command: <exact command>
exit: <exit code>
output: <bounded evidence>
```

## Generated projections

- [ ] `.github/workflows/ggen-ecosystem-sync.yml`, `generated/`, `consumer/`, and `.ggen-v2/` were not hand-edited
- [ ] If a generated projection changed, its authoritative semantic input changed in the same lineage and real `ggen sync run` evidence is attached

## Authority / actuation

- [ ] SELECT, CONSTRUCT, and DO remain separated
- [ ] No new ambient write authority or secret exposure was introduced
- [ ] Any actuation path retains a receipt/replay boundary

## Review receipt

- Falsifier: `<what would prove this change wrong>`
- Remaining blocker or exclusion: `<none or typed boundary>`
