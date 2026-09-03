---
applyTo: "ontology.ttl,ggen.toml,admission/**/*.ttl,certification/**/*.toml,ecosystem.lock.toml"
---

Treat these files as authority-bearing semantic/control inputs.

- Preserve public ontology terms and existing identity predicates unless a migration is explicitly required.
- Do not infer admission from observation; encode or cite the gate that admits the fact.
- Any producer pin change must remain consistent with gitlinks, lock contracts, receipts, and the relevant consumer path.
- A current release claim must be backed by current execution evidence; historical receipts remain historical.
- Prefer reversible declarative changes over encoded one-off procedural policy.
- Run the lock/certification falsifiers after changing identity, admission, release, or standing data.
