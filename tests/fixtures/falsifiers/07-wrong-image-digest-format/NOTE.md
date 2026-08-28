# Wrong image digest format — UNSUPPORTED (gap)

Section 17 (Container Identity) states the OCI digest format binding
(`ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:<digest>`, Section 19). Neither
`scripts/doctor.sh` (checks 4/11 test image *presence*, not digest *format*) nor
`ontology.ttl`'s `ex:admit`/`ex:evidence` steps validate that
`ecosystem.lock.toml [container].digest` matches `^sha256:[0-9a-f]{64}$` before use.

**Fixture**: `ecosystem.lock.toml` in this directory with
`[container].digest = "not-a-real-digest-12345"` (fails that regex).

No real local check exists to run against it. Marking this **UNSUPPORTED** honestly rather
than inventing a new production checker as part of this falsifier-fixture task (that
checker, if added, would belong in `scripts/doctor.sh` as a new check, or in `ex:admit`,
which is out of scope for this read-only fixture-authoring task).

**Expected typed refusal once implemented**: `REFUSED[INVALID_IMAGE_DIGEST_FORMAT]`.
