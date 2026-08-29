# Tutorial: manufacture your first artifact

This tutorial uses GitHub Actions as the execution surface. The consumer supplies
intent; the pinned ecosystem supplies the manufacturing instrument and marketplace.

## 1. Create the consumer inputs

Add `ggen.toml`, `ontology.ttl`, and the generated-output directory expected by your
selected pack. Start from a small example and keep semantic inputs in your repository.

## 2. Add the caller workflow

Create `.github/workflows/manufacture.yml` using the caller shown in the root README.
Pin both the ecosystem workflow ref and the OCI digest. Do not use `latest` or a tag
when producing a release receipt.

## 3. Open a pull request

The pull-request event runs exact checkout, marketplace admission, `ggen sync run`,
patch capture, receipt construction, and standing enforcement. A failed step is a
typed observation, not permission to edit generated output manually.

## 4. Inspect the evidence

Download the workflow artifact and record the consumer SHA, marketplace SHA, capsule
digest, sync exit code, patch digest, and receipt. The receipt is evidence; it is not
merge authority.

## 5. Replay before merge

Run `make replay RECEIPT=path/to/receipt.json` in a checkout containing the exact
subject commit. Replay must match the recorded consequence digest or refuse.

## 6. Choose the next route

Use [FAILURE-ROUTING.md](FAILURE-ROUTING.md) to determine whether the defect belongs
to consumer intent, a marketplace pack, GGen, or the transport capsule.
