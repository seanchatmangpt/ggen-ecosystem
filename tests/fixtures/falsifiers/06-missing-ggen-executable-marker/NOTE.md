# Missing GGen executable marker

`run-check.sh` is a REAL, runnable HOST-LEVEL analog of doctor.sh check-2
(`2-ggen-binary`), executed with `PATH=/usr/bin:/bin` so `command -v ggen` fails exactly as
it would if the composed container's final stage omitted the `COPY --from=builder
/usr/local/bin/ggen ...` step (Section 16.2).

The container-internal version of this check (`docker run --rm <image> ggen --version`,
i.e. doctor.sh check-4/check-11's territory) cannot be exercised for real here because no
image may be built or pulled under the orthogonal-swarm Docker read-only constraint, and
`ecosystem.lock.toml [container].tag` is still `UNKNOWN-TODO-not-yet-built`.

**Verdict**: host-level analog is `ALIVE` (real check, real REFUSED output above);
container-internal marker check is `UNSUPPORTED` pending a built image.
