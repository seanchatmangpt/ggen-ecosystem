## What this changes

<!-- One or two sentences. If this regenerates a workflow, name which ontology fact changed. -->

## Verification

<!-- Real command + real output, not a claim. Standing vocabulary: ALIVE / PARTIAL_ALIVE / BLOCKED / UNKNOWN -- see docs/STANDING.md. -->

- [ ] `just doctor` (or `bash scripts/doctor.sh`) run, output pasted below
- [ ] If this touches `ontology.ttl` or a marketplace pack template: regenerated via real `ggen sync run`, generated `.github/workflows/*.yml` diff reviewed (never hand-edited)
- [ ] If this touches the container path: `just chicago` (real, no-mocks smoke test) passes

```
<paste real command output here>
```

## Checklist

- [ ] No generated file (`.github/workflows/*.yml`, `generated/`) hand-edited directly
- [ ] Commit message written to a file and committed with `-F` if multi-line
- [ ] Base branch is `main` at an exact resolved SHA, not a moving target
