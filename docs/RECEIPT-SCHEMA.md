# Receipt Schema — v26.8.28

**Last Updated:** 2026-08-28

Defines the exact required fields for a v26.8.28 release receipt, ahead of any real
receipt being produced (PR-019 dependency). Derived from `ontology.ttl`'s `ex:evidence`
step (the embedded Python receipt-writing block) and
`docs/PRD-ARD-v26.8.28.md` Section 28's illustrative schema. This document is the
authoritative field contract; Section 28's JSON block remains illustrative only.

A receipt is a single JSON object, UTF-8, one document. `scripts/verify-receipt.sh`
validates a receipt file against exactly this contract.

## Standing vocabulary

Per PR-021 (`docs/PRD-ARD-v26.8.28.md` Section 8) and `no-overclaiming-rust.md`, every
`standing` field (top-level and nested `verification.*`) must be one of:

`UNKNOWN`, `PARTIAL_ALIVE`, `ALIVE`, `BLOCKED`, `BLOCKED[reason]`, `BUILD_BROKEN`,
`UNSUPPORTED`, `REFUSED`, `REFUSED[reason]`

Bracketed forms carry a typed reason (e.g. `BLOCKED[IMAGE_NOT_FOUND]`,
`REFUSED[MARKETPLACE_IDENTITY_MISMATCH]`) — the bracket content may be any non-empty
token, but the base word before the bracket must be one of the vocabulary values above.

## Field contract

| Field | Type | Mandatory | Notes |
|---|---|---|---|
| `subject.repository` | string | yes | `owner/repo` form, e.g. `seanchatmangpt/ggen-ecosystem` |
| `subject.commit` | string | yes | 40-char lowercase hex SHA (full git commit SHA of the subject repo) |
| `ecosystem.version` | string | yes | Release version tag, e.g. `v26.8.28` |
| `ecosystem.ggen_commit` | string | yes | 40-char lowercase hex SHA of the `vendor/ggen` submodule commit |
| `ecosystem.marketplace_commit` | string | yes | 40-char lowercase hex SHA of the `vendor/ggen-marketplace` submodule commit |
| `ecosystem.container_digest` | string | yes | `sha256:<64-hex>` form (OCI content digest of the release container image) |
| `admission.result` | string | yes | One of `ADMITTED`, `REFUSED`, `REFUSED[reason]` |
| `execution.command` | string | yes | Exact command line executed, e.g. `ggen sync run` |
| `execution.exit_code` | integer | yes | Process exit code of `execution.command`; `0` on success |
| `consequence.digest` | string | yes | `sha256:<64-hex>` or bare `<64-hex>` digest of the generated consequence artifact (e.g. the sync patch) |
| `verification.doctor` | string | yes | Standing value (see vocabulary above) for the `make doctor` gate |
| `verification.chicago` | string | yes | Standing value for the `make chicago` (real-collaborator test) gate |
| `verification.dod` | string | yes | Standing value for the `make dod` (Definition-of-Done) gate |
| `standing` | string | yes | Top-level standing value for the release as a whole |
| `run_id` | string | optional | CI run identifier (e.g. GitHub Actions `run_id`), when produced in CI |
| `run_attempt` | string \| integer | optional | CI run attempt number |
| `patch_sha256` | string | optional | 64-hex sha256 of the raw sync patch file, when a patch was produced |
| `packs` | array \| object | optional | Marketplace pack identities admitted during the run |
| `schema` | string | optional | Schema URI/version tag for the receipt itself (e.g. `https://ggen.dev/receipts/ecosystem-sync/v2`) |

Any other field not listed above is permitted (forward-compatible) but is not validated.

## Validation rules enforced by `scripts/verify-receipt.sh`

1. The file must be valid JSON.
2. Every mandatory field above must be present (dotted path resolves to a non-null,
   non-missing value).
3. Every field whose type is documented as a sha256-hex digest (`ecosystem.container_digest`,
   `consequence.digest`, `patch_sha256` if present) must match sha256 hex format:
   optionally prefixed `sha256:`, followed by exactly 64 lowercase hex characters.
4. `subject.commit`, `ecosystem.ggen_commit`, `ecosystem.marketplace_commit` must each be
   exactly 40 lowercase hex characters (a full git SHA-1).
5. `execution.exit_code` must be an integer.
6. Every standing-vocabulary field (`standing`, `verification.doctor`,
   `verification.chicago`, `verification.dod`) must match the vocabulary in
   "Standing vocabulary" above (base word, optional bracketed reason).
7. **No placeholder values when `standing == "ALIVE"`.** If the top-level `standing`
   field is exactly `ALIVE`, no mandatory string field anywhere in the document may equal
   (case-insensitively) a placeholder marker: `UNKNOWN-TODO`, `TODO`, `TBD`, `PLACEHOLDER`,
   `FIXME`, `XXX`, or the empty string. A receipt claiming `ALIVE` standing while any
   required field is still a placeholder is rejected.

Any rule violation causes the validator to exit non-zero with a message naming the exact
field and rule that failed.

## See Also

- `docs/PRD-ARD-v26.8.28.md` Section 28 (Receipt Schema, illustrative) and Section 8
  (PR-021, Typed Standing)
- `ontology.ttl` `ex:evidence` step — the real receipt-writing Python block this schema
  formalizes
- `~/.claude/rules/no-overclaiming-rust.md` — standing vocabulary floor
- `scripts/verify-receipt.sh` — the executable validator for this contract
- `tests/fixtures/receipts/` — valid and invalid fixtures exercising this contract
