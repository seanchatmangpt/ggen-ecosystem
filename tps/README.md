# PragProg TPS

`ggen-ecosystem` runs the 100 Pragmatic Programmer SPARQL courts automatically as its software-production TPS.

- `automatic-scope.ttl` activates all 100 courts against the ecosystem production-system subject. Activation is not compliance evidence.
- `ggen.toml` is an isolated runtime manifest for the TPS court so normal ecosystem manufacture is not blocked by newly discovered abnormalities.
- `.github/workflows/pragprog-tps.yml` runs on every pull request and every push to `main`.
- Normal automatic runs are **andon**: findings are receipted and surfaced but do not stop the line while sensor/countermeasure coverage is being established.
- Manual `workflow_dispatch` with `strict=true` uses the same exact subject and court execution as **jidoka**: any non-zero court result refuses the run.
- The marketplace pack and ggen release are exact-SHA/hash pinned.

The intended closed loop is: court finding -> andon -> RCA -> ggen countermeasure -> exact execution -> receipt -> permanent guard -> revised standard work.
