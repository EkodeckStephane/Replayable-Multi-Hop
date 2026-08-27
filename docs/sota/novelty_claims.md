# CAMH-CUFE Novelty Claims Register

> Status: provisional. No priority claim (`first`, `novel`, `state of the art`) is authorized until the SOTA matrix is complete and independently checked.

## Central research target

**CAMH-CUFE studies controlled sequential composition of tag-changing ciphertext updates in functional encryption. It refines the CUFE authorization state from a tag `t` to a product state `(t, level)` so that repeated tag changes compose only along explicitly issued exact state edges; it additionally requires functional-key non-transferability across public update material and binds each ciphertext lineage to an independently replayable authenticated history, with trust-explicit compact checkpoint certification as a separate evidence regime.**

This is a research target, not yet a theorem or priority claim.

## Why the wording is deliberately narrow

The following ingredients already exist and are **not** claimed as new in isolation:

- repeated ciphertext updates and epoch-indexed update tokens in Updatable Encryption;
- Updatable Functional Encryption and generic cryptography-with-updates constructions;
- multi-hop ciphertext-updatable ABE/PE;
- multi-hop re-encryption and ciphertext evolution;
- functional proxy re-encryption;
- verifiable multi-hop PRE;
- composable updatable encryption;
- state chains, authenticated logs, signed checkpoints, consistency proofs, and witness/quorum checkpoints.

The candidate contribution is the exact **CUFE function-output security object and its controlled composition semantics**, not a collection of these known mechanisms.

## Critical prior-art boundaries

### 1. Cini-style CUFE is intentionally one-update

Cini et al., *(Inner-Product) Functional Encryption with Updatable Ciphertexts*, Journal of Cryptology 37, Article 8 (DOI: 10.1007/s00145-023-09486-y), define tag-based CUFE and intentionally restrict a ciphertext to one tag-changing update.

Their motivation gives the precise policy-composition problem that CAMH-CUFE targets: if tokens for `t -> t'` and `t' -> t''` automatically compose, ciphertexts originally under `t` may become movable to `t''` even when this transitive permission was never intended. They also explicitly identify update-token **function-key switching** as a security concern.

CAMH-CUFE therefore must solve both:

1. controlled authorization of repeated tag-changing transitions; and
2. preservation of functional-key separation while transition material is public/exposed as permitted by the game.

### 2. Epoch-indexed repeated updates are standard in Updatable Encryption

Updatable Encryption already models ciphertexts and tokens by epochs `e -> e+1`, and a ciphertext can be sequentially updated across many epochs. Ciphertext-independent UE may use one epoch token to update all ciphertexts of the source epoch.

Therefore:

> `level`, `epoch`, monotone update counters, and exact epoch transitions are not novelty claims.

The role of `(tag, level)` in CAMH-CUFE is more specific: it refines **tag-based CUFE policy reachability**, so equality of an intermediate visible tag does not by itself authorize composition of two tag-changing permissions.

### 3. Updatable Functional Encryption predates CUFE

Arriaga, Iovino, and Tang define **Updatable Functional Encryption (UFE)** for RAM programs (Mycrypt 2016; DOI: 10.1007/978-3-319-61273-7_17). Their abstraction allows tokens to update encrypted memory/ciphertext on which other tokens can subsequently execute.

Ananth, Cohen, and Jain, **Cryptography with Updates** (EUROCRYPT 2017; DOI: 10.1007/978-3-319-56614-6_15), give generic transformations toward updatable cryptographic primitives, including functional-encryption-related objects.

Forbidden statements:

> We introduce repeated updates in functional encryption.

> We are the first to make functional encryption updatable.

### 4. Multi-hop ciphertext-updatable ABE/PE exists

Schädlich, Scheu-Hachtel, Tairi, and Wang, **Ciphertext-Updatable Attribute-Based and Predicate Encryption from Lattices** (SCN 2026 / IACR ePrint 2026/1045), provide ciphertext-updatable ABE/PE and explicitly extend to multi-hop and an unbounded-token setting.

Forbidden statement:

> We introduce the first multi-hop ciphertext-updatable fine-grained encryption scheme.

The required distinction is FE **function-output semantics**, functional-key security across update states, controlled tag-level CUFE composition, and path audit/certification.

### 5. Multi-hop re-encryption and functional PRE are established

Chandran et al. study multi-hop re-encryption and functional re-encryption (PKC 2014; DOI: 10.1007/978-3-642-54631-0_6). Liang et al. define DFA-based functional PRE (IEEE TIFS 2014; DOI: 10.1109/TIFS.2014.2346023). Yao et al. explicitly study multi-hop ciphertext evolution in PRE (IEEE TIFS 2023; DOI: 10.1109/TIFS.2023.3282577).

Forbidden statement:

> We introduce multi-hop ciphertext evolution.

### 6. Verifiable multi-hop PRE exists

Cai et al. publish a verifiable and fair registered attribute-based multi-hop PRE construction with NIZK and a zkSNARK alternative (IEEE TIFS 2026; DOI: 10.1109/TIFS.2026.3711852).

Forbidden statement:

> We are the first to provide verifiable multi-hop encrypted-data transformation.

### 7. Composable UE exists

Levy-dit-Vehel and Roméas give a composable treatment of updatable encryption in Constructive Cryptography (arXiv:2204.11653).

Accordingly, `composable` in CAMH-CUFE must be backed by an explicit security definition/reduction. It cannot mean only that `Update` accepts its own output as a later input.

### 8. Checkpoints and transparency mechanisms are established

Signed checkpoints, append-only consistency proofs, witness cosignatures/quorums, and authenticated state chains are existing techniques.

Forbidden statements:

> We introduce cryptographic checkpoints.

> We introduce quorum-signed checkpoints.

The possible contribution is the formal placement of checkpoint certification inside a CAMH-CUFE history model, with a precise boundary between **independent path replay** and **trust-based certification of a previously audited state**.

## Confirmed negative result that constrains construction design

The supplied legacy pairing prototype is **not a secure CUFE instantiation**. A source-state functional-key group element plus public update-token components linearly derives the target-state functional-key group element for the same function vector. The attack was reproduced against the supplied code and follows directly from the algebra.

Consequences:

- API signatures/tag metadata do not repair the cryptographic capability;
- the legacy backend is retained only as correctness/audit evidence;
- every retained construction must prove **functional-key non-transferability** before supporting confidentiality or composability claims.

See `docs/formal/legacy_key_switch_attack.md`.

## Candidate scientific contributions

### C1 — Controlled tag-level composition semantics

Define the cryptographic authorization state as

\[
Q=(t,\ell)
\]

and require exact state continuity for composition. Thus

\[
(A,0)\to(B,1)
\]

and

\[
(B,0)\to(C,1)
\]

do **not** compose. The authority must explicitly issue

\[
(B,1)\to(C,2)
\]

to permit the second hop for a ciphertext that reached `B` through the first transition.

This uses an epoch-like coordinate, which is known in UE, for the specific purpose of controlling **CUFE tag-policy reachability**.

**Required evidence:** formal `G-CompositionAuthorization`, construction-level state binding, and SOTA falsification against UE/CU-ABE/PE/PRE models.

### C2 — Functional-key non-transferability across update states

Define and prove that permitted public transition material and a functional key at one state do not create unauthorized target-state functional capability.

**Required evidence:** security game + reduction. The legacy key-switch attack is the mandatory negative regression.

### C3 — Sequential CUFE security after adversarial prefixes

Define and prove security of a next authorized CUFE transition after an adversarially observable valid prefix, without relying on the current ciphertext being a fresh encryption.

**Required evidence:** a construction-specific composition/confidentiality theorem with explicit oracle restrictions and proof loss.

### C4 — Path-aware lineage integrity

Separate state-global cryptographic authorization from lineage-specific evidence. Formalize stale replay, rollback, skip, reorder, splice, fork, and history-binding attacks over authenticated histories.

**Required evidence:** games/reductions plus executable conformance tests.

### C5 — Dual verification semantics

Formalize:

1. independent replay of every authenticated update in a lineage; and
2. compact trust-explicit certification of an already-audited final state.

A checkpoint must not be described as an independent succinct proof of omitted hops.

### C6 — Two construction tracks

- **Generic/theoretical:** bounded multi-level iO/PTDE/PRF construction, retained only if its security proof closes.
- **Concrete/practical:** bounded lattice/IPFE construction, retained only if depth-dependent correctness/noise and functional-key non-transferability both close.

### C7 — Distributed FGCS realization

Evaluate the retained practical construction across independent authority/update/audit/verifier/consumer roles using a real cryptographic backend, canonical wire sizes, distributed measurements, paired statistics, adversarial tests, and ablations.

## Central novelty candidate after the current SOTA pass

The strongest claim currently worth attempting is:

> **CAMH-CUFE formalizes controlled multi-hop composition for tag-changing CUFE by combining exact tag-level state authorization with functional-key non-transferability and security over adversarially observable update prefixes, while attaching lineage-specific replayable audit evidence and a separately trust-scoped checkpoint regime.**

This remains provisional. It survives only if the construction/security proof closes and the final SOTA review does not find a materially equivalent FE function-output model.

## Claim language policy

### Allowed before exhaustive closure

- `we define`
- `we study`
- `we construct`
- `we provide`
- `we formalize`
- `our evaluation measures`

`to our knowledge` is allowed only after documented final search and verification.

### Prohibited until verified

- `the first`
- `first-ever`
- `novel multi-hop`
- `state of the art`
- `unprecedented`
- `first updatable FE`
- `first multi-update FE`
- `first level-aware update scheme`
- `first multi-hop ciphertext-updatable fine-grained encryption`
- `first cryptographic checkpoint`
- `fully composable` unless the theorem supports that exact qualifier
- `constant-time verification` unless both asymptotic and measured evidence justify it

## Falsification conditions

The central novelty must be narrowed or abandoned if prior work is found that already provides, for tag-based CUFE or a materially equivalent FE function-output model, substantially the same combination of:

1. repeated adaptive tag-changing ciphertext updates;
2. exact state-aware authorization that prevents unintended transitive composition of tag permissions;
3. FE outputs after valid multi-hop prefixes;
4. functional-key non-transferability across public update transitions;
5. security defined over already-updated ciphertexts as future update sources;
6. path/lineage integrity against the relevant history attacks; and
7. the same independent-replay versus trust-explicit checkpoint distinction.

Finding a known mechanism for any individual ingredient is neither a novelty proof nor a novelty refutation; the comparison must be made at the level of the complete security object and construction assumptions.
