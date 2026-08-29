# ggen-ecosystem

Canonical governed composition root for the ggen ecosystem.

This repository owns ecosystem identity, composition, admission, closure, qualification, transport, and release standing. It does not absorb the source identity of `ggen`, `ggen-marketplace`, or independently versioned ecosystem repositories.

## Manufacturing contract

The repository is a first-class GGen consumer:

```text
ggen.toml + ontology.ttl
        +
ggen-marketplace@4c4232515b43d40cef8288c43eacfab2c31ab485
        |
        v
    ggen sync run
        |
        v
.github/workflows/ggen-ecosystem-sync.yml
```

The workflow is a generated consequence. Edit `ontology.ttl` or `ggen.toml`, then regenerate with `ggen sync run`; do not hand-edit the workflow.

### Exact producer pins

- GGen release: `v26.8.27`
- Linux x86_64 release asset SHA-256: `ab442ced90a9836fd4eb07a5d61eb58293843cd515d864699fc0d0453444a035`
- GGen executable SHA-256 observed during manufacture: `01d0f5e624d12eeda503db4fb4b00618472bd775ee4850c9a2f850651db76680`
- Marketplace commit: `4c4232515b43d40cef8288c43eacfab2c31ab485`
- Marketplace pack: `packs/github-actions-pack`
- Pack content BLAKE3: `1ce72f06a115995a37b9416013d607d4898f3cd707819681a76f663d69c99da8`

## GitHub-native cloud bootstrap

`.github/workflows/ggen-ecosystem-sync.yml` is both a reusable `workflow_call` target and a manual `workflow_dispatch` rail. It:

1. checks out the exact candidate with persisted credentials disabled;
2. fails closed unless every `[packs]` entry is an exact commit under `seanchatmangpt/ggen-marketplace/packs/*`;
3. restores an untrusted GitHub Actions cache for GGen's native `.ggen-v2/git-packs` transport cache, keyed by marketplace SHA;
4. downloads the pinned prebuilt GGen Linux release asset and verifies its SHA-256;
5. invokes `ggen sync run` as the manufacturing boundary;
6. captures the generated patch, GGen lock/receipt, pack identities, logs, and replay receipt as a GitHub artifact;
7. keeps repository mutation authority outside this workflow (`contents: read` only).

That makes GitHub the distribution layer while GGen and the marketplace pack remain the semantic/manufacturing authority.

## Complete GitHub ecosystem closure

`ecosystem/github-ecosystem.ttl` admits the complete owned GitHub estate by **set membership**, not by a brittle handwritten repository allowlist:

```text
E = { r | r.owner.login = seanchatmangpt }

|E| = 378
Epublic = 300
Eprivate = 78
```

The cardinalities were closed against the connected GitHub account on 2026-08-28. Owner enumeration had four non-empty 100-item pages and the next page was empty; item 377 existed and item 378 did not. Independent visibility searches proved public item 300 exists while 301 does not, and private item 78 exists while 79 does not.

### Identity law

The durable identity of a member is its GitHub **repository ID**, not its current name, default branch, or branch-head SHA. Names and branch heads are mutable observations. This prevents routine renames, branch changes, and commits from rewriting ecosystem membership.

The constitutional public identities are:

| Repository | GitHub repository ID | Ecosystem role |
| --- | ---: | --- |
| `seanchatmangpt/ggen` | `1071971708` | `MANUFACTURING_ENGINE` |
| `seanchatmangpt/ggen-marketplace` | `1328598648` | `PACK_DISTRIBUTION` |
| `seanchatmangpt/ggen-ecosystem` | `1349290571` | `COMPOSITION_AND_STANDING_ROOT` |

Every other owned repository is included extensionally by the owner predicate without surrendering its source identity or independent versioning.

### Public/private partition

`ggen-ecosystem` is public. Therefore the complete estate is represented as two partitions:

```text
PUBLIC_REPOSITORY_PARTITION        = 300 members
PROTECTED_PRIVATE_REPOSITORY_PARTITION = 78 members
```

The public root **must not** materialize private repository names, IDs, URLs, refs, SHAs, descriptions, or sizes. The private partition is acknowledged and counted, but its identities remain protected. This is a closure boundary, not an omission.

### Membership is not promotion

Inclusion in the ecosystem means only that a repository is an observed member of the owned GitHub estate. It does **not** confer production standing, release standing, pack standing, merge authority, or actuation authority. Reference forks, experiments, products, platforms, research repositories, archives, and empty test repositories remain distinct subjects until separately classified and qualified.

The machine-readable census receipt is `receipts/github-ecosystem-census-2026-08-28.json`.

## Provenance

The initial workflow bytes were manufactured by the real GGen release through GitHub Actions, not authored directly:

- GGen branch head: `dcd363b5bcc0ba526bb6ce5e6bc4ea5db0a1a716`
- GitHub self-test run: `33150915638`
- job: `98782446151`
- evidence artifact: `9677675572`
- evidence artifact digest: `sha256:0455db2b422807c78e64324a009cd7b2d393538be72eef543512df05ab6e80b5`
- generated workflow SHA-256: `e03c5da8306d7b7073787c5d4172cfecafd296a4283adb05272ae465b392308e`
- generated graph hash: `27500c768263ba41ad5343a08a8d521c1f12c06e74d7089c4650a298d0b02ad2`
- `ggen sync run` exit: `0`
- independent YAML parse: `PASS`

The machine-readable bootstrap receipt is in `receipts/bootstrap-ggen-ecosystem-sync.json`.

## Authority boundary

```text
SELECT / semantic inputs  -> ggen.toml + ontology.ttl + ecosystem/*.ttl
CONSTRUCT                 -> ggen sync run
EVIDENCE                  -> ggen.lock + receipts + GitHub artifact
DO                         -> external authorized Git/GitHub merge path
```

No workflow in this bootstrap path receives repository write authority. The complete GitHub census adds observation/composition standing only and grants no exception to the rule that consumer code is manufactured through admitted `ggen sync run` paths.
