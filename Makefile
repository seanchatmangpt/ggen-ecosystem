.PHONY: submodules image sync doctor verify chicago dod receipt-verify replay

# Initialize/update vendored submodules (vendor/ggen, vendor/ggen-marketplace).
submodules:
	git submodule update --init --recursive

# Build the local ggen-ecosystem container image from the repo Dockerfile.
image:
	docker build -t ggen-ecosystem:local .

# Regenerate ggen.lock from a clean slate, dry-run first, then run for real.
sync:
	rm -f ggen.lock
	ggen sync run --dry-run
	ggen sync run

# Run scripts/doctor.sh if present; otherwise no-op with a note.
doctor:
	@if [ -x scripts/doctor.sh ]; then \
		scripts/doctor.sh; \
	elif [ -f scripts/doctor.sh ]; then \
		sh scripts/doctor.sh; \
	else \
		echo "doctor: scripts/doctor.sh not found -- add a doctor script here to check local toolchain/env health"; \
	fi

# Provenance verification chain: submodules -> scripts/verify-provenance.sh.
verify: submodules
	@if [ -x scripts/verify-provenance.sh ]; then \
		scripts/verify-provenance.sh; \
	elif [ -f scripts/verify-provenance.sh ]; then \
		sh scripts/verify-provenance.sh; \
	else \
		echo "verify: TODO -- scripts/verify-provenance.sh not found yet"; \
	fi

# Docker container smoke test. WARNING: this target builds a Docker image
# itself (see tests/test_container_smoke.sh). During the orthogonal-swarm
# build (build6), only the single designated build owner may run this --
# do not run `make chicago` casually mid-swarm, it will race the
# authoritative build.
chicago:
	tests/test_container_smoke.sh

# Print the Definition of Done roll-up section (falls back to the whole file
# if no "## Roll-up" heading is found).
dod:
	@awk '/^## Roll-up/{p=1} p && /^## / && !/^## Roll-up/{p=0} p' docs/DEFINITION-OF-DONE.md | grep -q . \
		&& awk '/^## Roll-up/{p=1} p && /^## / && !/^## Roll-up/{p=0} p' docs/DEFINITION-OF-DONE.md \
		|| cat docs/DEFINITION-OF-DONE.md

# Verify a manufacturing receipt. Usage: make receipt-verify RECEIPT=path/to/receipt.json
receipt-verify:
	@test -n "$(RECEIPT)" || { echo "usage: make receipt-verify RECEIPT=<path>" >&2; exit 2; }
	@if [ -x scripts/verify-receipt.sh ]; then \
		scripts/verify-receipt.sh "$(RECEIPT)"; \
	elif [ -f scripts/verify-receipt.sh ]; then \
		sh scripts/verify-receipt.sh "$(RECEIPT)"; \
	else \
		echo "receipt-verify: TODO -- scripts/verify-receipt.sh not found yet"; \
	fi

# Dry-run replay check.
replay:
	@if [ -x tests/replay_check.sh ]; then \
		tests/replay_check.sh --dry-run; \
	elif [ -f tests/replay_check.sh ]; then \
		sh tests/replay_check.sh --dry-run; \
	else \
		echo "replay: TODO -- tests/replay_check.sh not found yet"; \
	fi
