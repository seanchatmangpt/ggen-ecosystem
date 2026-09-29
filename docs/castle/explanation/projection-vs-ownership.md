# Explanation: projection is not ownership

CASTLE has more useful code than it has architectural owners. That is intentional.

## Why not make every useful repository a service?

A large repository fleet tends to accumulate overlapping implementations: runtimes, planners, receipt systems, semantic engines, UI layers, and adapters.

If every useful implementation becomes a permanent first-class CASTLE subsystem, composition becomes ambiguous. A caller can no longer tell which component is authoritative.

The CASTLE projection solves the opposite problem: preserve capability while reducing ownership.

## Three different statements

These statements are not equivalent:

```text
repository contains capability
repository may be projected into CASTLE
repository owns the CASTLE capability
```

The first is an observation. The second is what `ontology/castle-projection.ttl` records. The third is deliberately not granted by this graph.

## Why XaaS remains the runtime core

DTeam, MCPP, OSTAR and older repositories contain runtime-like or manufacturing-like primitives. Those implementations may contain valuable work. They still do not need to become parallel crowns.

```text
DTeam / MCPP runtime primitives
       ↓ absorb proven capability
      XaaS
       ↓
single runtime topology
```

The same rule applies elsewhere:

```text
Praxis semantic capability -> GraphLaw
OSTAR manufacture patterns -> ggen_igniter
wasm4pm-compat structures  -> wasm4pm
UNRDF kernel capability    -> GraphLaw / projection layer
```

A successful extraction should decrease the number of components that must be trusted as owners.

## Why some repositories stay wrappers

Adapters and surfaces are real capabilities, but they live at edges.

```text
Atlassian -> ash_atlassian -> SA2A/XaaS -> CASTLE
ChatGPT   -> chatgpt-cloud-elixir -> XaaS -> CASTLE
CI/CD     -> cargo-cicd -> CASTLE BRCE -> protected mutation
```

The adapter knows how to speak to the external system. It does not invent its own authorization model.

## Why knowledge-plane repositories remain outside runtime

Strategy doctrine, engineering standards and protocol specifications can constrain or manufacture runtime artifacts without being live runtime services.

```text
knowledge plane
   ↓ manufacture / constrain
runtime plane
   ↓ observe / execute
evidence plane
   ↓ verify
consequence plane
```

## Why CANDIDATE matters

The projection records an architectural hypothesis.

A source SHA proves what was inspected, not that its projected capability has executed successfully inside CASTLE.

Therefore every projection starts at CANDIDATE and stops at CONSTRUCT. The receiving owner is responsible for execution, receipts, replay and standing.

## The intended convergence

The end state is not a larger CASTLE graph. It is a smaller ownership graph with a larger reusable capability library:

```text
more reusable capability
        +
fewer sovereign owners
        =
lower coordination complexity
```

That is what the ggen-ecosystem projection is for.
