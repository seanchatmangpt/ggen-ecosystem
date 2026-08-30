# BEAM consumer composition

`ggen-ecosystem` is the integration boundary for BEAM consumers such as `beam4pm`.

## Dependency direction

```text
beam4pm
  -> ggen-ecosystem
       -> ggen              compiler/manufacturing engine
       -> ggen-marketplace  packs/templates/executable knowledge
       -> ggen_igniter      BEAM-native reconciliation/control plane
       -> autofde-lab       diagnosis/search/falsification
```

Consumers MUST NOT independently select incompatible pins for these four components when operating in ecosystem mode. Exact identities are recorded in `ecosystem.lock.toml` and gitlinks.

## ggen_igniter role

`ggen_igniter` is not a replacement for ggen. It is the BEAM-native reconciliation/control surface around ontology-driven manufacture and structured actuation. Current admitted capabilities include Reactor coordination, Igniter mutation, planning/DO separation, receipts/replay, OCEL telemetry emission, Ash integration and doctor/sync/plan/replay tasks.

## beam4pm rule

`beam4pm` should contribute domain ontology/specification and select ecosystem-exposed packs/capabilities. It should not hand-author application source to bridge these components. Missing behavior is repaired in the ecosystem, marketplace pack, ggen_igniter, or the admitted beam4pm ontology and then re-manufactured.

## Standing

Adding/pinning a component is composition evidence only. A BEAM consumer crown requires exact-head execution of the consumer path, including recursive submodule identity, manufacture, compile/test, examples/playground where claimed, and receipts.
