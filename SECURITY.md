# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities privately via [GitHub Security
Advisories](https://github.com/seanchatmangpt/ggen-ecosystem/security/advisories/new)
rather than a public issue. This lets us assess and patch before public
disclosure.

Include, if known:

- The affected file(s) or workflow (e.g. `Dockerfile`, `.github/workflows/*.yml`,
  `ontology.ttl`/admission shapes).
- Reproduction steps and, if possible, a minimal example.
- The impact you believe it has (e.g. supply-chain, container escape,
  privilege escalation via the `container:` job path, secrets exposure in a
  generated workflow).

## Scope

This repository is a semantic control-plane root: RDF/TTL ontology, SHACL
admission shapes, a `ggen` manifest, and generated GitHub Actions workflows
(see `docs/ARCHITECTURE.md`). Security-relevant surface includes:

- The composed `ghcr.io/seanchatmangpt/ggen-ecosystem` container image
  (`Dockerfile`) and its supply chain (`vendor/ggen`, `vendor/ggen-marketplace`
  submodule pins).
- Generated workflow permissions (`.github/workflows/*.yml` are generated from
  `ontology.ttl` -- see `docs/ARCHITECTURE.md`'s authority boundary; a
  permissions escalation in a generated workflow is a real finding even
  though the `.yml` itself is never hand-edited).
- The admission/SHACL layer (`admission/`) that gates what enters the graph.

## Response

We aim to acknowledge reports within 5 business days and provide a remediation
timeline once triaged. Typed standing vocabulary (see `docs/STANDING.md`)
governs how any fix is verified before being claimed resolved -- a fix is not
considered done until `scripts/doctor.sh` and the relevant Chicago-style test
(`tests/test_container_smoke.sh` or equivalent) pass against it for real.
