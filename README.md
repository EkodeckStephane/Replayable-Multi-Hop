# Composable Auditable Multi-Hop Ciphertext-Update Functional Encryption (CAMH-CUFE)

Research repository for **Composable Auditable Multi-Hop Ciphertext-Update Functional Encryption (CAMH-CUFE)**.

## Research objective

CAMH-CUFE studies how ciphertext-updatable functional encryption can be extended from a single authorized update to a **sequentially composable, path-aware multi-hop ciphertext evolution** while preserving functional correctness, explicit security over the update history, and auditable verification.

The project separates two verification semantics:

1. **Independent history verification** — replay and validate every authenticated transition from a trusted starting state.
2. **Compact checkpoint verification** — verify a certificate for an already-audited state under an explicitly stated checkpoint trust model.

A checkpoint is not treated as a substitute for an independently verified history unless the formal construction and trust assumptions explicitly justify that interpretation.

## Scientific focus

The project is being rebuilt around the following questions:

- What does sequential composability mean for ciphertext-update functional encryption?
- Which security guarantees are required against replay, rollback, skip, reorder, splice, fork, and cross-history substitution attacks?
- Under which assumptions can one-step CUFE security be lifted to secure multi-hop evolution?
- How should history verification and compact certification be separated formally?
- What are the computational, communication, and storage costs of these guarantees in a distributed implementation?

## Current status

**Research refactoring in progress.** The previous prototype is retained outside the main scientific narrative as a reproducibility baseline. Claims in the new CAMH-CUFE work are considered provisional until they pass the formal-security, implementation, experimental, and bibliographic gates documented in this repository.

## Target venue

The current target is **Future Generation Computer Systems (Elsevier)**. The manuscript and evaluation are therefore being positioned at the intersection of cryptographic protocol verification, secure distributed systems, and scalable encrypted-data processing.

## Planned repository structure

```text
docs/formal/          Formal syntax, security games, theorem map
docs/sota/            State-of-the-art and FGCS positioning
docs/protocol/        Canonical serialization and protocol formats
src/camh_cufe/        CAMH-CUFE implementation
tests/                Correctness, adversarial, and differential tests
experiments/          Local and distributed experiment runners
results/              Raw and processed measurements
reproducibility/      Environments, manifests, checksums
```

## Reproducibility policy

The paper will report scientific evidence; exact commands, manifests, hashes, frozen environments, and regeneration instructions will live in this repository rather than dominate the manuscript.

## License

Licensing and citation metadata will be finalized after the CAMH-CUFE author list and artifact policy are frozen.
