# Contributing to ggen-ecosystem

This repository is a semantic control-plane root, not conventional
application code -- there is no build/lint/test in the usual sense. Read
`CLAUDE.md` and `AGENTS.md` first; they are the binding operating doctrine
for this repo, not optional context.

## Before you start

1. **Clone with submodules.** `vendor/ggen` and `vendor/ggen-marketplace` are
   real git submodules: `git clone --recurse-submodules <url>`, or
   `git submodule update --init --recursive` (`make submodules`) after a
   plain clone.
2. **Never hand-edit generated files.** `.github/workflows/*.yml` are
   generated from `ontology.ttl` via `ggen sync run`. If a generated
   workflow is wrong, fix the ontology facts (or the marketplace pack
   template that renders it) and regenerate -- never hand-patch the `.yml`.
   The same rule applies to anything under `generated/`.
3. **Use the operator surface**, not ad hoc commands: `just --list` (or
   `make verify` if you don't have `just`) for the canonical recipes --
   `doctor`, `chicago`, `dod`, `bench`, `stress`, `replay`, `falsify`.

## Workflow

1. Branch from `main` at an exact, resolved SHA -- never branch from a
   moving target.
2. Make your change. If it touches `ontology.ttl` or a marketplace pack
   template, regenerate with a real `ggen sync run` and commit the
   regenerated output alongside the source change.
3. Verify for real before opening a PR: `just doctor` (should report no
   `BLOCKED`/`BUILD_BROKEN`/`UNKNOWN`), and `just chicago` if your change
   touches the container/manufacturing path.
4. Use the repo's standing vocabulary (`docs/STANDING.md`) in your PR
   description if you're making a claim about what now works --
   `ALIVE`/`PARTIAL_ALIVE`/`BLOCKED`/`UNKNOWN`, not "done"/"works".
   Cite the command that verifies the claim.

## Commit messages

Write the message to a file and use `git commit -F <file>` for anything
multi-line -- avoids shell metacharacter corruption from backticks,
parentheses, etc. in `-m '...'` strings.

## Questions

Open a [Discussion](https://github.com/seanchatmangpt/ggen-ecosystem/discussions)
for design questions; use Issues for concrete bugs or well-scoped feature
requests.
