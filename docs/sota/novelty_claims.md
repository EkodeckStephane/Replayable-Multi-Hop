# CAMH-CUFE Novelty Claims Register

> Status: provisional. No priority claim (`first`, `novel`, `state of the art`) is authorized until the SOTA matrix is complete and independently checked.

## Central claim under investigation

**CAMH-CUFE studies sequential composability for ciphertext-updatable functional encryption across multiple authorized state transitions, with explicit security over the resulting update path and two deliberately separated verification semantics: independently replayable history verification and trust-explicit compact checkpoint certification.**

This wording is deliberately scoped to the scientific object and does not claim that multi-hop re-encryption, ciphertext evolution, verifiability, or state chaining are new in isolation.

## Why the claim is potentially non-incremental

### 1. The starting CUFE abstraction is intentionally one-update

Cini et al. define CUFE so that a fresh ciphertext may be updated once from tag `t` to `t'`; updating an already-updated ciphertext is excluded by the intended security model (DOI: 10.1007/s00145-023-09486-y).

Therefore, repeated-update CUFE is not a parameter increase of the published primitive. It changes the valid state space and the adversarial interaction model.

### 2. Multi-hop re-encryption alone is not new

Chandran et al. already study multi-hop re-encryption and functional re-encryption (PKC 2014, DOI: 10.1007/978-3-642-54631-0_6). Yao et al. explicitly study multi-hop ciphertext evolution in PRE (IEEE TIFS 2023, DOI: 10.1109/TIFS.2023.3282577).

**Forbidden novelty statement:**

> We introduce multi-hop ciphertext evolution.

### 3. Functional proxy re-encryption already exists

Liang et al. define DFA-based functional PRE (IEEE TIFS 2014, DOI: 10.1109/TIFS.2014.2346023).

CAMH-CUFE must therefore explain the difference between:

- PRE/functional PRE transformation and delegation semantics; and
- FE function-output semantics under repeatedly updated ciphertext tags/states.

### 4. Verifiable multi-hop PRE now exists

Cai et al. publish a verifiable and fair registered attribute-based multi-hop PRE scheme with lightweight verification and NIZK/zkSNARK mechanisms (IEEE TIFS 2026, DOI: 10.1109/TIFS.2026.3711852).

**Forbidden novelty statement:**

> We are the first to provide verifiable multi-hop encrypted-data transformation.

The defensible distinction must instead be established at the level of CUFE composability, FE semantics, path-aware security, independently replayable history, and checkpoint semantics.

### 5. Composable updatable encryption exists

Levy-dit-Vehel and Romeas give a composable treatment of updatable encryption in Constructive Cryptography (arXiv:2204.11653).

Use of **composable** in CAMH-CUFE therefore requires an explicit composition definition and proof. It cannot mean only that the implementation accepts its own updated ciphertext as the next input.

## Candidate scientific contributions

### C1 — Multi-hop CUFE syntax and security model

Define a stateful CUFE abstraction in which already-updated ciphertexts are legitimate inputs to later authorized updates, with explicit state/path semantics.

**Required evidence:** complete formal syntax + games + threat model.

### C2 — Sequential update composability

Define and prove that security of a next transition is maintained after an adversarially observable valid prefix, rather than assuming the input is always a fresh encryption.

**Required evidence:** composition theorem/reduction. This is the highest-value and highest-risk claim.

### C3 — Path-aware history security

Formalize replay, rollback, skip, reorder, splice, fork/cross-history substitution, and history-binding properties for repeated ciphertext updates.

**Required evidence:** games and reductions; executable adversarial tests are supporting implementation evidence only.

### C4 — Dual verification semantics

Formalize:

1. full replay verification of the authenticated path; and
2. compact certification of an already-audited final state under an explicit trust policy.

**Required evidence:** security definitions that prevent checkpoint certification from being described as an independent succinct proof of omitted hops.

### C5 — CUFE/IPFE instantiation

Instantiate the framework over a concrete ciphertext-updatable inner-product FE construction or a carefully justified compatible construction.

**Required evidence:** exact mapping from generic properties to construction assumptions; no proof step may rely on unsupported iteration of a one-hop security theorem.

### C6 — Distributed-system evaluation

Evaluate the construction as secure encrypted-data state evolution across distributed authority/update/audit/verifier roles.

**Required evidence:** real cryptographic backend, separate hosts/processes, canonical wire sizes, scalability, paired statistics, adversarial campaign, and ablations.

## Claim language policy

### Allowed before exhaustive SOTA closure

- `we define`
- `we study`
- `we construct`
- `we provide`
- `we formalize`
- `our evaluation measures`
- `to our knowledge` only after documented search and final verification

### Prohibited until verified

- `the first`
- `first-ever`
- `novel multi-hop`
- `state of the art`
- `unprecedented`
- `fully composable` unless the exact composition theorem supports the qualifier
- `constant-time verification` unless complexity and implementation evidence both justify the statement

## Falsification conditions for the central novelty

The central novelty must be revised or abandoned if the SOTA review finds a prior work that already provides, in the CUFE/FE setting, substantially the same combination of:

1. repeated adaptive ciphertext updates;
2. a security definition explicitly covering already-updated ciphertexts as future update inputs;
3. FE function-output semantics after arbitrary valid update prefixes;
4. path/history integrity against replay/splicing/rollback-style attacks; and
5. the same full-replay versus trust-explicit checkpoint verification model.

The paper should then pivot to whichever strictly stronger property remains unsupported by prior work.
