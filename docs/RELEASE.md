# Release closure

A release is an admitted graph closure, not a date label alone.

For a scoped ecosystem release, record:

- ecosystem source SHA;
- exact manufacturing dependency SHAs;
- selected profile;
- admitted repository/pack closure;
- verifier identities and results;
- ggen sync receipt;
- replay result;
- any typed refusals or unsupported edges;
- scoped standing.

`ALIVE` is never inherited from a previous release unless source, validator, toolchain, configuration, and environment identities satisfy the explicit reuse contract.
