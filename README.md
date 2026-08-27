# Composable Auditable Multi-Hop Ciphertext-Update Functional Encryption (CAMH-CUFE)

Research repository for **Composable Auditable Multi-Hop Ciphertext-Update Functional Encryption (CAMH-CUFE)**.

## Research objective

CAMH-CUFE studies how tag-changing ciphertext-updatable functional encryption can support repeated **explicitly authorized exact-state transitions** while preserving functional semantics, security after adversarially observable update prefixes, and auditable state evolution.

The baseline authorization state is

```text
Q = (tag, level)
```

and composition is opt-in at the exact-state level. For example,

```text
(A,0) -> (B,1)
(B,0) -> (C,1)
```

does **not** authorize a second hop from `(B,1)`; an explicit edge such as `(B,1) -> (C,2)` is required.

The project separates two verification semantics:

1. **Independent history verification** — replay and validate every authenticated transition from an accepted fresh root, including concrete transition-use validation.
2. **Compact checkpoint verification** — verify an attestation for an already-audited state under an explicitly stated checkpoint trust model.

A checkpoint is not a succinct proof of omitted hops merely because it contains a history digest.

## Scientific focus

The high-risk scientific question is whether a practical construction can satisfy **public-token multi-hop FE security (`MH-PUB`)** for this exact-state model without creating forbidden functional-key transfer across states.

The formal program covers:

- exact state and composition authorization;
- adaptive multi-hop confidentiality under public-token and honest-update profiles;
- functional-key non-transferability;
- sequential security after an adversarially observable valid prefix;
- replay, rollback, skip, reorder, splice, fork and history-binding properties;
- independent full-history replay versus trust-explicit checkpoint certification;
- distributed computation, communication and storage costs once a secure real backend exists.

## Current evidence status

### Established

- a level-aware exact-state authorization model and executable authorization-graph oracle;
- baseline adaptive oracle/leakage profile and `MH-PUB` / `MH-HU` distinction;
- canonical versioned TLV protocol framing and frozen v1 golden vectors;
- centralized domain-separation registry;
- history root binding to suite, exact initial state and fresh ciphertext;
- retained-history conformance verifier requiring both token authentication and concrete `VerifyTransitionUse`;
- canonical retained-record/checkpoint framing and typed wire-size accounting;
- CI guard against `pickle`/runtime-object protocol-size metrics;
- conditional history/checkpoint binding reduction sketches;
- baseline FGCS-oriented distributed threat model;
- multi-version CI on Python 3.11/3.12/3.13.

### Confirmed negative result

The supplied legacy pairing construction permits **functional-key switching with public update material**. It is therefore retained only as a correctness/regression baseline and is disqualified from supporting CAMH-CUFE confidentiality claims. See `docs/formal/legacy_key_switch_attack.md`.

### Still open / submission blockers

- a retained real CAMH-CUFE construction with exact-state cryptographic binding;
- functional-key non-transferability proof for that construction;
- `MH-PUB` multi-hop confidentiality/sequential-composition theorem;
- final-result proof relation/soundness if `pi4` remains in scope;
- real cryptographic backend and canonical concrete wire objects;
- distributed non-loopback evaluation and statistical analysis;
- exhaustive final SOTA closure through submission freeze.

**CAMH-CUFE is therefore not yet submission-ready.** No implementation test or symbolic result is being promoted as a cryptographic security theorem.

## Target venue

The current target is **Future Generation Computer Systems (Elsevier)**. The eventual manuscript/evaluation must therefore connect the cryptographic object to a real distributed secure-computing problem and use a real cryptographic backend for headline systems evidence.

## Repository map

```text
docs/formal/          Formal syntax, games, threat model, candidate constructions, proof map
docs/sota/            State-of-the-art matrix, novelty falsification, FGCS positioning
docs/protocol/        Canonical serialization, golden vectors, domain separation
src/camh_cufe/        Reference/model implementation; later real backend
tests/                Correctness and adversarial conformance tests
scripts/              Scientific-artifact/CI guards and later reproducibility tools
experiments/          Reserved for real local/distributed experiment runners
results/              Reserved for raw and processed measured evidence
reproducibility/      Reserved for frozen environments, manifests and checksums
legacy/               Provenance information for the supplied pre-CAMH-CUFE baseline
```

Key entry points:

- `docs/roadmap/research_gates.md` — evidence-gated research plan;
- `docs/formal/oracle_and_leakage_profile.md` — adaptive security interface;
- `docs/formal/system_threat_model.md` — roles, trust and corruption boundary;
- `docs/formal/security_games.md` — security properties/games;
- `docs/formal/audit_layer_theorems.md` — conditional audit-layer reductions;
- `docs/formal/checkpoint_trust_model.md` — explicit checkpoint semantics;
- `docs/sota/novelty_claims.md` — novelty claim register/falsification conditions;
- `docs/sota/sota_matrix.csv` — SOTA evidence matrix;
- `docs/protocol/canonical_serialization.md` — wire-format policy;
- `docs/protocol/domain_separation_registry.md` — cryptographic domain registry;
- `docs/protocol/golden_vectors.md` — v1 byte-level compatibility vectors.

## Reproducibility policy

The manuscript will report the scientific problem, method, theorems, measured evidence, boundary conditions and interpretation. Exact commands, hashes, manifests, frozen environments and regeneration instructions belong in this artifact rather than in the paper's main narrative.

Current CI can be reproduced locally with:

```bash
python -m pip install -e .
python scripts/check_protocol_metric_hygiene.py
python -m unittest discover -s tests -v
```

The current reference tests are model/conformance evidence only until the real cryptographic backend gate is closed.

## License

Licensing and citation metadata will be finalized after the CAMH-CUFE author list and artifact policy are frozen.
