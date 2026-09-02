# Downstream Gym Factory

`ggen-ecosystem` manufactures customer-specific gyms from admitted ontology instead of cloning and editing a reference gym.

## Production function

```text
customer intent / constraints
        |
        v
ontology.ttl (O*)
        |
        v
vendor/ggen-ecosystem/packs/gym-pack
        |
        v
vendor/ggen-ecosystem/bin/ggen-ecosystem manufacture .
        |
        v
Cargo.toml + src/main.rs + src/gym_profile.rs + gym/manifest.toml
        |
        v
compile / execute / qualify / receipt / replay
```

The reference gyms composed by `gym-ecosystem` are evidence and design capital. They are not copied into downstream customer repositories. Repeated structure is promoted into this pack; customer variability remains ontology input.

## Canonical customer topology

```text
customer-gym/
├── ggen.toml
├── ontology.ttl
├── templates/
└── vendor/
    └── ggen-ecosystem/   # pinned git submodule
```

Example `ggen.toml`:

```toml
[project]
name = "customer-gym"

[ontology]
source = "ontology.ttl"

[packs]
gym = { path = "vendor/ggen-ecosystem/packs/gym-pack" }

[templates]
dir = "templates"
```

Manufacture with:

```bash
vendor/ggen-ecosystem/bin/ggen-ecosystem manufacture .
```

## Admitted semantic contract

A gym is represented as `sosa:Platform` and must carry exactly one string `dct:identifier`, `dct:title`, and `dct:description`.

Each executable capability is represented as `sosa:Procedure` with exactly one string `dct:identifier`, one string `dct:title`, and one `dct:type`. Consequence classification is restricted to:

- `<urn:gymact:consequence:read>`
- `<urn:gymact:consequence:do>`

SHACL rejects malformed input before it obtains manufacturing standing.

## Chicago definition of done

`.github/workflows/gym-factory-chicago.yml` executes the complete downstream path against a fresh customer fixture:

1. bind the exact pull-request head;
2. manufacture through the public `ggen-ecosystem manufacture` wrapper;
3. prove no `generated/` editing surface exists;
4. compile the manufactured Rust project with the real Rust toolchain;
5. execute it and assert the expected READ/DO procedures;
6. manufacture a second time and prove byte-identical replay;
7. mutate the ontology and prove the artifact changes;
8. remove a required ontology fact and prove SHACL refuses manufacture.

The desired standing is `GYM_FACTORY_CHICAGO_ALIVE`.
