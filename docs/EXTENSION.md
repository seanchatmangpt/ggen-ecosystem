# Extension

The ecosystem is designed to grow without centralizing all source code.

A new repository, pack, profile, transport, verifier, or release surface is added by extending the graph while preserving the calculus:

```text
observe -> candidate -> admit relation -> close dependencies -> construct -> execute -> receipt -> replay -> standing
```

Prefer reversible candidate edges first. Promote only the relation actually proved. Do not hand-edit generated projections to simulate admission. Reusable executable behavior belongs in `ggen-marketplace`; this repository owns composition and evidence about that behavior.
