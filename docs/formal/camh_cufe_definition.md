# CAMH-CUFE: Preliminary Formal Definition

> Status: research specification. This document defines proof obligations; it does **not** assert that the current implementation satisfies them.

## 1. Scientific object

**Composable Auditable Multi-Hop Ciphertext-Update Functional Encryption (CAMH-CUFE)** extends ciphertext-updatable functional encryption from a single authorized ciphertext update to a sequentially composable state evolution.

The starting point is CUFE as defined by Cini, Ramacher, Slamanig, Striecks, and Tairi, where a ciphertext can be updated from tag `t` to tag `t'` once and already-updated ciphertexts are intentionally excluded from further updates (Journal of Cryptology 37, Art. 8, DOI: 10.1007/s00145-023-09486-y).

CAMH-CUFE does not treat repeated calls to a one-hop `Update` algorithm as sufficient. Multi-hop evolution is a separate security object because an adversary may observe, replay, reorder, splice, fork, skip, or combine state transitions.

## 2. State model

A ciphertext state at hop `i` is modeled as

```text
S_i = (tag_i, epoch_i, C_i, h_i)
```

where:

- `tag_i` identifies the current CUFE authorization tag/domain;
- `epoch_i` is a monotone state coordinate used to distinguish repeated tag names and stale transitions;
- `C_i` is the current ciphertext payload;
- `h_i` is a cryptographic commitment to the authenticated history prefix ending at `S_i`.

A valid path is

```text
S_0 --Delta_0,1--> S_1 --Delta_1,2--> ... --Delta_(k-1,k)--> S_k
```

The tag sequence may revisit a tag name only if the security model explicitly permits cycles; the state remains distinct because the epoch and history commitment differ.

## 3. Syntax

A CAMH-CUFE scheme for functionality family `F` consists of PPT algorithms:

### Setup

```text
Setup(1^lambda, F) -> (mpk, msk)
```

Creates public and secret system parameters, including all parameters needed to verify transitions. Verifiers must not accept unauthenticated proof bases or protocol parameters supplied ad hoc by an untrusted caller.

### KeyGen

```text
KeyGen(msk, f, tag, epoch_policy) -> sk_f
```

Derives a functional key. The exact binding between the functional key and state coordinates is construction-specific and must be defined in the instantiation.

### Enc

```text
Enc(mpk, x, tag_0) -> S_0
```

Creates a fresh ciphertext state with canonical initial epoch and initial history commitment.

### TokGen

```text
TokGen(msk, S_meta, tag_next) -> Delta_i,i+1
```

Generates an authorization token for exactly one transition. `S_meta` contains the source state coordinates required to bind the token to its intended source.

At minimum, the authenticated transition statement should bind:

```text
protocol-domain || version || source-tag || source-epoch ||
destination-tag || destination-epoch || relevant-public-parameters
```

and any construction-specific proof statement.

### Update

```text
Update(mpk, S_i, Delta_i,i+1) -> S_(i+1) or bottom
```

Checks source-state binding, performs the cryptographic ciphertext update, advances the epoch, and derives the next history commitment.

### VerifyTransition

```text
VerifyTransition(mpk, S_i, Delta_i,i+1, S_(i+1)) -> {0,1}
```

Publicly checks one transition.

### VerifyHistory

```text
VerifyHistory(mpk, S_0, transcript, S_k) -> {0,1}
```

Independently replays and validates the complete authenticated path from an accepted starting state to the displayed final state.

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
Dec(sk_f, S_i) -> f(x) or bottom
```

Returns the functional output only when the functional-key/state compatibility relation defined by the CAMH-CUFE instantiation is satisfied.

## 4. Sequential composability target

A CAMH-CUFE construction is *sequentially update-composable* only if a ciphertext resulting from any valid accepted prefix of updates remains a valid input to the next authorized update while preserving the defined functional and security properties under adaptive interaction.

The research goal is therefore stronger than syntactic closure of `Update`:

```text
valid output of Update_i
        + valid authorization Delta_i,i+1
        + adversarially observable previous history
        -> secure valid input/output relation for Update_(i+1)
```

## 5. Verification semantics

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

## 6. Required construction theorem

The desired result is a theorem of the following form, with assumptions made construction-specific rather than hidden:

```text
one-step update security
+ functional-encryption security
+ transition authentication
+ collision-resistant history commitment
+ canonical injective serialization
+ [additional proof-system assumptions]
-------------------------------------------------
=> defined CAMH-CUFE multi-hop guarantees
```

Whether this can be obtained as a generic compiler is an open proof obligation. The repository must not claim a generic compiler until the reduction is complete.

## 7. Immediate implementation obligations

1. Replace ambiguous concatenation with canonical length-delimited serialization.
2. Authenticate or deterministically derive every verifier-critical public base/statement component.
3. Separate symbolic/deterministic test backends from cryptographic performance evidence.
4. Ensure official CI executes all required tests with `failed = 0` and `skipped = 0`.
5. Define a canonical wire encoding before making protocol-size/compactness claims.
