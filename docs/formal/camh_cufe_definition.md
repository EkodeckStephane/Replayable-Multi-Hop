# CAMH-CUFE: Preliminary Formal Definition

> Status: research specification. This document defines proof obligations; it does **not** assert that the current implementation satisfies them.

## 1. Scientific object

**Composable Auditable Multi-Hop Ciphertext-Update Functional Encryption (CAMH-CUFE)** extends tag-based ciphertext-updatable functional encryption from a single authorized ciphertext update to an explicitly authorized sequence of level-aware state transitions with an authenticated audit history.

The starting point is CUFE as defined by Cini, Ramacher, Slamanig, Striecks, and Tairi, where a ciphertext can be updated from tag `t` to tag `t'` once and already-updated ciphertexts are intentionally excluded from further updates (Journal of Cryptology 37, Art. 8, DOI: 10.1007/s00145-023-09486-y).

CAMH-CUFE does not treat repeated calls to a one-hop `Update` algorithm as sufficient. Multi-hop evolution is a separate security object because:

- repeated updates change the valid state space and adversarial view;
- public update material must not switch functional keys;
- tag-only transition graphs may compose in unintended ways;
- an adversary may replay, reorder, splice, fork, skip, or combine transition evidence.

## 2. Two-layer state model

CAMH-CUFE distinguishes the **cryptographic authorization state** from the **auditable lineage state**.

### 2.1 Cryptographic authorization state

At hop `i`, define

\[
Q_i=(t_i,\ell_i),
\]

where:

- `t_i` is the visible CUFE tag/domain;
- `l_i` is a monotone cryptographic level/epoch.

The same visible tag at two levels is a different authorization state:

\[
(t,\ell)\ne(t,\ell').
\]

An update token is **state-global**: a token for

\[
Q_i\rightarrow Q_{i+1}
\]

may legitimately update multiple ciphertexts that are genuinely in the exact source state `Q_i`. It is not inherently bound to one ciphertext instance.

### 2.2 Auditable lineage state

For one ciphertext lineage, define

\[
S_i=(Q_i,C_i,h_i,\mathsf{lid}),
\]

where:

- `Q_i` is the cryptographic authorization state;
- `C_i` is the current ciphertext payload;
- `h_i` commits to the authenticated history prefix;
- `lid` is a lineage identifier or equivalent canonical lineage-binding value used by the audit layer.

The exact representation of `lid` is an implementation/protocol choice; it must not be silently imported into the cryptographic update-token semantics.

A valid audited path is

```text
S_0 --Delta_0,1--> S_1 --Delta_1,2--> ... --Delta_(k-1,k)--> S_k
```

with exact authorization-state continuity

\[
Q_{i+1}^{\text{output}}=Q_{i+1}^{\text{next-source}}.
\]

## 3. Explicit / opt-in composability

CAMH-CUFE does not define composition by visible-tag equality.

For example, issuing

\[
(A,0)\rightarrow(B,1)
\]

and independently issuing

\[
(B,0)\rightarrow(C,1)
\]

does **not** authorize

\[
(A,0)\rightarrow(B,1)\rightarrow(C,2).
\]

To authorize that second hop, the authority must explicitly issue an edge whose exact source state is `(B,1)`, e.g.

\[
(B,1)\rightarrow(C,2).
\]

Thus multi-hop reachability is opt-in at the state level rather than an automatic transitive closure of tag names.

See `docs/formal/explicit_composability_semantics.md`.

## 4. Syntax

A CAMH-CUFE scheme for functionality family `F` consists of PPT algorithms plus an authenticated audit layer.

### Setup

```text
Setup(1^lambda, F, Lmax) -> (mpk, msk)
```

Creates public and secret system parameters and, for bounded constructions, the supported maximum update depth `Lmax`.

Verifiers must not accept unauthenticated proof bases or protocol parameters supplied ad hoc by an untrusted caller.

### KeyGen

```text
KeyGen(msk, f, Q) -> sk_f,Q
```

where `Q=(tag,level)` or where the concrete construction defines an equivalent state-compatibility relation.

A retained construction must prove functional-key non-transferability across public update transitions. API metadata checks are not sufficient.

### Enc

```text
Enc(mpk, x, tag_0) -> (Q_0, C_0)
```

Creates a fresh ciphertext in canonical initial state

\[
Q_0=(tag_0,0).
\]

The audit layer then initializes `S_0` with canonical lineage/history data.

### TokGen

```text
TokGen(msk, Q_src, Q_dst) -> Delta_Qsrc,Qdst
```

Generates an authorization token for exactly one **state-global** transition.

At minimum, its authenticated/public transition description binds:

```text
protocol-domain || version ||
source-tag || source-level ||
destination-tag || destination-level ||
construction/suite parameters || token identifier/digest
```

The token does not become ciphertext-specific merely because the audit history later records which ciphertext used it.

### Update

```text
Update(mpk, Q_i, C_i, Delta_Qi,Qj) -> (Q_j, C_j) or bottom
```

Checks/enforces exact source-state compatibility in the cryptographic construction and performs the ciphertext update.

Changing only unauthenticated metadata while leaving the cryptographic payload applicable is not sufficient realization of state binding.

### VerifyTransition

```text
VerifyTransition(mpk, S_i, Delta_i,j, S_j) -> {0,1}
```

Publicly checks one **lineage-specific audited use** of a state-global transition token. It verifies the cryptographic state transition plus the required ciphertext/history bindings.

### VerifyHistory

```text
VerifyHistory(mpk, S_0, transcript, S_k) -> {0,1}
```

Independently replays and validates the complete authenticated path from an accepted starting lineage state to the displayed final state.

### Certify

```text
Certify(ask, S_k, h_k, policy_context) -> cert_k
```

After a complete history audit, an authorized checkpoint issuer or quorum certifies the audited final state. `ask` denotes the auditor signing material or a threshold/quorum mechanism.

### VerifyCheckpoint

```text
VerifyCheckpoint(apk, S_k, cert_k, policy_context) -> {0,1}
```

Verifies that the accepted checkpoint authority/quorum certified the stated final state and history commitment.

**Semantic boundary:** checkpoint verification does not independently establish every omitted transition unless the checkpoint mechanism itself is replaced by a proof system that provides that property.

### Dec

```text
Dec(sk_f,Q, Q_i, C_i) -> f(x) or bottom
```

Returns the functional output only when the functional-key/state compatibility relation defined by the CAMH-CUFE instantiation is satisfied.

## 5. Correctness target

For every honestly generated authorized path

\[
Q_0\to Q_1\to\cdots\to Q_k,
\]

and compatible functional key `sk_f,Qk`,

\[
\mathsf{Dec}(sk_{f,Q_k},Q_k,C_k)=f(x)
\]

except with negligible probability.

For lattice instantiations this requires a depth-dependent decryption-error theorem. Syntactic successful execution is insufficient.

## 6. Sequential composability target

A CAMH-CUFE construction is *sequentially update-composable* only if a ciphertext resulting from any valid accepted prefix of updates remains a valid input to the next **explicitly authorized level-compatible update** while preserving the defined functional and security properties under adaptive interaction.

The research goal is stronger than syntactic closure of `Update`:

```text
valid output of Update_i
        + exact compatible authorization Delta_i,i+1
        + adversarially observable previous view/history
        -> secure valid input/output relation for Update_(i+1)
```

In particular, composition must preserve functional-key separation; a public update token must not become a function-key update mechanism.

## 7. Required security classes

At minimum, the retained model/construction must address:

- multi-hop functional consistency;
- exact state-transition authorization;
- explicit composition authorization;
- functional-key non-transferability;
- multi-hop confidentiality;
- stale replay and rollback;
- skip/reorder integrity;
- lineage splice/fork integrity;
- history-commitment binding;
- checkpoint forgery/state binding;
- final-result proof binding if `pi4` or an equivalent proof remains in scope.

Exact games are maintained in `docs/formal/security_games.md`.

## 8. Verification semantics

CAMH-CUFE intentionally distinguishes two evidence regimes.

### Full-history evidence

- verifier receives the required authenticated transcript;
- verification cost is expected to depend on path length `k`;
- verifier does not need to trust a checkpoint issuer for the omitted transitions.

### Checkpoint evidence

- verifier receives a compact certificate over an already-audited state;
- later verification should be independent of `k` except for data embedded in the certificate format;
- security explicitly depends on the checkpoint trust policy.

The experimental paper must report this as a trust/performance trade-off, not as equivalence between a certificate and an independently verified history.

## 9. Construction program

Two construction tracks are currently under investigation and must remain clearly separated.

### Generic/theoretical track

A bounded multi-level iO/PTDE/PRF construction generalizing the architecture of Cini et al. See `docs/formal/generic_io_multilevel_candidate.md`.

### Concrete/practical track

A bounded multi-level lattice/IPFE construction. Its feasibility depends on simultaneous closure of depth-dependent noise growth and functional-key non-transferability. See:

- `docs/formal/bounded_lwe_candidate.md`;
- `docs/formal/lwe_key_noise_coupling.md`.

The legacy pairing prototype is excluded from confidentiality claims because it admits a confirmed public-token functional-key switching attack. See `docs/formal/legacy_key_switch_attack.md`.

## 10. Required theorem program

No generic-compiler theorem is currently claimed.

The desired scientific result is a set of construction-specific theorems showing that the retained instantiations realize the CAMH-CUFE games under explicit assumptions. At minimum:

1. correctness / functional consistency;
2. key non-transferability;
3. sequential confidentiality/composition under the defined oracle model;
4. state/path authorization;
5. history and checkpoint binding under standard authentication/hash assumptions.

## 11. Immediate implementation obligations

1. Replace ambiguous concatenation with canonical length-delimited serialization.
2. Authenticate or deterministically derive every verifier-critical public base/statement component.
3. Separate symbolic/deterministic test backends from cryptographic performance evidence.
4. Ensure official CI executes all required tests with `failed = 0` and `skipped = 0`.
5. Define a canonical wire encoding before making protocol-size/compactness claims.
6. Add regression tests for legitimate same-state token reuse and rejected wrong-level composition.
