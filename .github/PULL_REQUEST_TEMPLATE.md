## Intent

<!-- One sentence: what invariant or customer journey changes? -->

## Exact subjects

- Base `main`: `________________` (40-char SHA)
- Proposed head: `________________` (40-char SHA)
- GGen / Marketplace / capsule identities changed? `no / yes — list exact identities`

## Authority classification

- [ ] Semantic source / admission input
- [ ] Hand-authored verifier, test, docs, or DX surface
- [ ] Generated projection (must be produced by its declared manufacturer; never hand-edited)
- [ ] Release / package / external DO path

If generated, name the semantic source and real manufacturing command:

```text
source:
command:
receipt:
```

## Verification

<!-- Real commands + real output. Inspection is not execution. -->

- [ ] `just github-dx` or the relevant GitHub DX court passes
- [ ] `just doctor` / `just explain` run when the change affects ecosystem standing
- [ ] Relevant narrow tests pass before broader tests
- [ ] Generated workflow changes, if any, were regenerated from semantic source and reviewed as projections
- [ ] No verifier or CI workflow conferred standing beyond its authority ceiling

```text
<paste concise real command output or link exact-head GitHub Actions evidence>
```

## Standing

Before: `________________`

After: `________________`

Evidence scope / remaining gaps:

<!-- Use UNKNOWN / PARTIAL_ALIVE / ALIVE / BLOCKED / BUILD_BROKEN / UNSUPPORTED / REFUSED with typed reasons. -->

## Risk and rollback

- Irreversible effects: `none / describe`
- Security or permission change: `none / describe exact permission delta`
- Rollback: `revert this PR / describe other bounded rollback`

## Review checklist

- [ ] Base SHA was resolved before mutation; the PR does not silently assume a moving base.
- [ ] All third-party GitHub Actions added or changed are pinned to an exact commit SHA.
- [ ] Workflow permissions are explicit and least-privilege.
- [ ] `pull_request_target` is not combined with checkout/execution of untrusted PR code.
- [ ] No secret, token, private repository identity, or credential material is committed or logged.
- [ ] Historical receipts are not promoted into current-head proof.
- [ ] Generated files are not treated as semantic editing surfaces.
- [ ] The PR has an independent falsifier for its main claim.
