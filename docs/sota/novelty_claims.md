# CAMH-CUFE Novelty Claims Register

> Status: provisional. No priority claim (`first`, `novel`, `state of the art`) is authorized until the SOTA matrix is complete and independently checked.

## Central claim under investigation

**CAMH-CUFE studies sequential composability for the tag-based ciphertext-updatable functional-encryption (CUFE) model across multiple authorized state transitions, with explicit security over the resulting update path and two deliberately separated verification semantics: independently replayable history verification and trust-explicit compact checkpoint certification.**

This wording is deliberately scoped. It does **not** claim that updatable FE, repeated execution over updated encrypted state, multi-hop re-encryption, ciphertext evolution, verifiability, state chaining, signed checkpoints, or witness/quorum checkpointing are new in isolation.

## Critical prior-art boundaries

### 1. The Cini et al. CUFE abstraction is intentionally one-update

Cini et al. define tag-based CUFE so that a fresh ciphertext may be updated once from tag `t` to `t'`; updating an already-updated ciphertext is excluded by the intended correctness/security model (Journal of Cryptology 37, Article 8; DOI: 10.1007/s00145-023-09486-y).

Therefore, **multi-hop tag-update CUFE** is not obtained merely by restating the published syntax with a larger hop counter: the valid state space, token use, and adversarial interaction model must change.

### 2. Updatable functional encryption already predates CUFE

Arriaga, Iovino, and Tang define **Updatable Functional Encryption (UFE)** for RAM programs (Mycrypt 2016; DOI: 10.1007/978-3-319-61273-7_17). Their abstraction explicitly envisions tokens that can update encrypted memory/ciphertext over which subsequent tokens can execute.

Ananth, Cohen, and Jain subsequently develop **Cryptography with Updates** (EUROCRYPT 2017; DOI: 10.1007/978-3-319-56614-6_15), using updatable randomized encodings to generically obtain updatable counterparts of primitives including functional encryption.

**Forbidden novelty statements:**

> We introduce repeated updates in functional encryption.

> We are the first to make functional encryption updatable.

The defensible distinction must be specific to **Cini-style tag-changing CUFE semantics**, repeated authorized tag/state transitions, their compositional security, and audit evidence over the transition path.

### 3. Multi-hop re-encryption alone is not new

Chandran et al. already study multi-hop re-encryption and functional re-encryption (PKC 2014; DOI: 10.1007/978-3-642-54631-0_6). Yao et al. explicitly study multi-hop ciphertext evolution in proxy re-encryption (IEEE TIFS 2023; DOI: 10.1109/TIFS.2023.3282577).

**Forbidden novelty statement:**

> We introduce multi-hop ciphertext evolution.

### 4. Functional proxy re-encryption already exists

Liang et al. define DFA-based functional proxy re-encryption (IEEE TIFS 2014; DOI: 10.1109/TIFS.2014.2346023).

CAMH-CUFE must explain the distinction between:

- PRE/functional-PRE transformation and delegation semantics; and
- FE function-output semantics under repeatedly updated CUFE tags/states.

### 5. Verifiable multi-hop PRE now exists

Cai et al. publish a verifiable and fair registered attribute-based multi-hop PRE scheme with verification mechanisms including NIZK and a zkSNARK alternative (IEEE TIFS 2026; DOI: 10.1109/TIFS.2026.3711852).

**Forbidden novelty statement:**

> We are the first to provide verifiable multi-hop encrypted-data transformation.

The defensible distinction must instead be established at the level of CUFE composability, FE semantics, path-aware transition security, replayable authenticated history, and checkpoint semantics.

### 6. Composable updatable encryption exists

Levy-dit-Vehel and Roméas give a composable treatment of updatable encryption in Constructive Cryptography (arXiv:2204.11653).

Use of **composable** in CAMH-CUFE therefore requires an explicit composition definition and proof. It cannot mean only that the implementation accepts an updated ciphertext as the next input.

### 7. Signed checkpoints, consistency proofs, and witness quorums are not new

Transparency-log systems already use signed compact checkpoints, append-only consistency proofs, and witness cosignatures/quorums to reduce split-view/equivocation risk. The C2SP transparency-log checkpoint and witness specifications are explicit examples.

**Forbidden novelty statements:**

> We introduce cryptographic checkpoints.

> We introduce quorum-signed checkpoints.

CAMH-CUFE's possible contribution is instead the **formal placement of checkpoint certification inside a CUFE multi-hop audit model**, with a precise statement of what the checkpoint does and does not prove about omitted ciphertext-update transitions.

## Candidate scientific contributions

### C1 — Multi-hop tag-update CUFE syntax and security model

Define a stateful extension of the Cini-style CUFE abstraction in which an already-updated ciphertext can become a legitimate source for a later authorized tag/state transition, with explicit lineage, epoch, and path semantics.

**Required evidence:** complete formal syntax + threat model + comparison showing how it differs from UFE, generic updatable cryptography, and PRE.

### C2 — Sequential CUFE update composability

Define and prove that the security of a next authorized CUFE transition is maintained after an adversarially observable valid prefix, rather than assuming the input is a fresh encryption.

**Required evidence:** composition theorem/reduction. This remains the highest-value and highest-risk claim.

### C3 — Path-aware transition security

Formalize replay, rollback, skip, reorder, splice, fork/cross-history substitution, and history-binding properties for repeated tag-changing CUFE updates.

**Required evidence:** games and reductions. Executable adversarial tests are supporting implementation evidence only.

### C4 — Dual verification semantics for CAMH-CUFE histories

Formalize:

1. full replay verification of every authenticated ciphertext-update transition; and
2. compact certification of an already-audited final state under an explicit checkpoint trust policy.

**Required evidence:** definitions that prevent checkpoint certification from being described as an independent succinct proof of omitted hops; comparison with transparency-log checkpoint/witness semantics.

### C5 — Concrete CUFE/IPFE instantiation

Instantiate the model over a concrete ciphertext-updatable inner-product FE construction or a carefully justified compatible construction.

**Required evidence:** exact mapping from generic properties to construction assumptions. No proof may silently iterate a one-hop theorem outside its security experiment.

### C6 — Distributed-system realization and evaluation

Evaluate CAMH-CUFE as secure encrypted-data state evolution across distributed authority/update/audit/verifier roles.

**Required evidence:** real cryptographic backend, independent processes/hosts, canonical wire sizes, scalability, repeated-measures statistics, adversarial campaign, and ablations.

## Central novelty candidate after current SOTA review

The strongest claim currently worth attempting is:

> **CAMH-CUFE extends one-update tag-based CUFE into a stateful multi-hop model whose security is defined over adversarially observable transition prefixes and authenticated update paths, while separating independent path replay from trust-explicit certification of an already-audited state.**

This is a **research target**, not yet a theorem. It survives only if C2 (sequential composition/confidentiality) and C3 (path security) can be proved and the remaining SOTA review does not find an equivalent prior construction.

## Claim language policy

### Allowed before exhaustive SOTA closure

- `we define`
- `we study`
- `we construct`
- `we provide`
- `we formalize`
- `our evaluation measures`
- `to our knowledge` only after documented final search and verification

### Prohibited until verified

- `the first`
- `first-ever`
- `novel multi-hop`
- `state of the art`
- `unprecedented`
- `first updatable FE`
- `first multi-update FE`
- `first cryptographic checkpoint`
- `fully composable` unless the exact composition theorem supports the qualifier
- `constant-time verification` unless complexity and measured implementation evidence both justify the statement

## Falsification conditions for the central novelty

The central novelty must be revised or abandoned if the SOTA review finds prior work that already provides, for tag-based CUFE or a materially equivalent FE access-control model, substantially the same combination of:

1. repeated adaptive tag-changing ciphertext updates;
2. a security definition explicitly covering already-updated ciphertexts as later update sources;
3. FE function-output semantics after arbitrary valid update prefixes;
4. transition-path integrity against replay/rollback/skip/reorder/splice/fork or equivalent history attacks; and
5. the same distinction between independent path replay and trust-explicit compact certification.

Finding prior work for any individual ingredient does not by itself establish novelty or destroy it; the manuscript must compare the exact security objects and assumptions rather than count features.
