# Qualification workflow — scope for this pass

Local-capsule qualification only (no GHCR credentials in this session). Image under
test: `ggen-ecosystem:qual`, built fresh from the now-clean `vendor/ggen-marketplace`
submodule checkout (191 packs, 0 diff vs pinned SHA c779aec2) and `vendor/ggen`
(c61ee9935).

Tasks run:
1. Pack-tree identity: BLAKE3/sha256 of committed `vendor/ggen-marketplace/packs`
   vs `/opt/ggen-marketplace/packs` inside the image.
2. GGen binary identity: sha256 of the in-image `ggen` binary, `ggen --version`.
3. Fresh-consumer rehearsal: clean temp dir, no host ggen/marketplace, run
   `docker run ggen-ecosystem:qual ggen sync run` against a minimal consumer
   ggen.toml + ontology, assert generated output.
4. Clean-room dependency test: same as #3 but with PATH/HOME/GGEN_* scrubbed.
5. Local receipt: record {ecosystem git sha, ggen submodule sha, marketplace
   submodule sha, image id, consumer tree, command, exit code, generated file
   hash} to receipts/local-qualification-<timestamp>.json, then replay once and
   diff.

Standing produced: `PARTIAL_ALIVE[LOCAL_CAPSULE]` — not release ALIVE (that needs
GHCR digest + fresh-consumer-against-digest + sealed receipt).
