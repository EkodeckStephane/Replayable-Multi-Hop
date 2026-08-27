# CAMH-CUFE Security Games and Proof Obligations

> Status: design document. Names and exact oracle interfaces may change during proof development.

## 1. Design principle

Security must be defined over **state-transition histories**, not inferred from a finite list of implementation corruption tests. The adversarial tests are later derived from these games.

The adversary may interact adaptively with key, token, encryption, update, and verification interfaces subject to the restrictions required by the confidentiality definition.

### State-global transition semantics

Unless a different construction is explicitly defined, an update token authorizes a transition between **public cryptographic authorization states** `Q=(tag,level)`, not one ciphertext instance. Thus a token for `Q -> Q'` may legitimately update multiple valid ciphertexts currently in `Q`.

Ciphertext/lineage identity is introduced by the **audit-history layer** to prevent history splicing and false provenance claims. It must not be silently turned into a token restriction absent from the cryptographic construction.

The use of a level/epoch coordinate is not itself a novelty claim: epoch-indexed transitions are standard in Updatable Encryption. CAMH-CUFE uses the product state `(tag, level)` to control composition of **tag-changing CUFE permissions**.

## 2. Correctness properties

### Functional correctness

For every valid authorization state `Q_i` reached by an authorized path and every compatible functional key,

```text
Dec(sk_f,Q_i, Q_i, C_i) = f(x)
```

except with negligible probability.

### Transition correctness

Every honestly generated token for an exact source authorization state produces the defined destination state.

### History correctness

Every honestly generated sequence of accepted lineage transitions is accepted by `VerifyHistory`.

### Checkpoint correctness

Every certificate generated after an accepted history audit is accepted by `VerifyCheckpoint` under the corresponding trust policy.

## 3. State-authorization and history-integrity games

### G-StateAuthorization: wrong-source-state resistance

Goal: use a valid token for `Q -> Q'` to transform a ciphertext whose authenticated cryptographic source state is not exactly `Q`, and have that transformation accepted as authorized.

The source state includes every coordinate security-relevant to transition authorization, including tag and level/epoch.

**Non-goal:** preventing the same state-global token from updating two distinct ciphertexts that are both legitimately in `Q`.

### G-CompositionAuthorization: controlled tag-policy composition

This game captures the policy problem that motivates multi-hop CAMH-CUFE.

The challenger issues a set of exact state-transition tokens. The adversary wins if it produces an accepted transition path containing a step for which no exact compatible state edge was authorized, even if the visible tag names could be chained after projecting away the levels.

The canonical separating example is:

```text
issued:  (A,0) -> (B,1)
issued:  (B,0) -> (C,1)
```

These permissions must **not** authorize

```text
(A,0) -> (B,1) -> C
```

because the second token accepts `(B,0)`, not `(B,1)`.

The chain becomes authorized only after an exact edge such as

```text
(B,1) -> (C,2)
```

is issued.

The security experiment must include at least:

1. same visible tag but wrong source level;
2. same visible tag but wrong destination level;
3. attempted composition of `(A,0)->(B,1)` with `(B,0)->(C,1)`;
4. explicit successful composition after `(B,1)->(C,2)` is issued;
5. repeated tag names at different levels;
6. adaptive issuance of unrelated tag transitions that must not enlarge the challenge path beyond exact state reachability.

A proof must show **cryptographic enforcement** of the level/state coordinate. An API-only metadata comparison is insufficient.

### G-Replay: stale-token replay resistance

Goal: make a token authorized for an earlier exact state/epoch validate against a later state for which that transition was not authorized.

Applying a state-global token to another valid ciphertext that is genuinely in the authorized source state is **not** a replay attack.

### G-Rollback: rollback resistance

Goal: make a previously valid old state appear as the current accepted descendant of a newer state/history.

The game must distinguish legitimate archival verification of an old state from acceptance of that state as the current state.

### G-Skip: skipped-hop resistance

Goal: delete one or more required transitions while retaining an accepted final state/history claim.

### G-Reorder: transition-order integrity

Goal: permute individually valid transitions so that an invalid exact-state path is accepted.

### G-Splice: cross-history splice resistance

Goal: combine a valid prefix from one ciphertext lineage with a valid suffix from another lineage and obtain acceptance as one history.

This is an **audit/provenance** property. It remains meaningful even though the underlying update token is state-global.

### G-Fork: prefix/fork consistency

Goal: create conflicting accepted descendants from a context in which policy requires a unique evolution path, or make a verifier accept incompatible histories as one linear history.

If branching is legitimate, the game must instead enforce explicit branch identities and prevent implicit history equivalence.

### G-HistoryBinding: history-commitment binding

Goal: produce two semantically distinct accepted histories that yield the same accepted authenticated history commitment for a checkpoint/final-state claim.

Reduction target: collision resistance plus unambiguous/canonical encoding, unless a stronger construction-specific assumption is required.

## 4. Functional-encryption and composability games

### G-MH-FunctionalConsistency

Authorized repeated updates must preserve the intended plaintext/function relation. The output after any valid exact-state path must remain the defined functional result rather than a path-dependent transformed message, unless path-dependent functionality is explicitly part of the scheme.

### G-KeyNonTransferability

This game is mandatory because the supplied legacy pairing prototype fails it.

The adversary receives the public parameters, permitted public update material, and functional keys allowed by the experiment. It wins if it constructs, for a state where it was not entitled to the corresponding functional capability:

1. a valid target-state functional key;
2. an algebraically equivalent representation of that key; or
3. any surrogate procedure that computes a forbidden functional value on target-state ciphertexts with non-negligible advantage.

The game tests **decryption capability**, not byte equality with an authority-issued key.

For a transition `Q -> Q'`, a minimal regression asks whether

```text
(sk_f,Q, Delta_Q->Q', f, mpk)
```

enables deriving target-state capability for `f` beyond what the confidentiality experiment permits.

Any concrete construction that fails this game is disqualified from supporting CAMH-CUFE confidentiality claims, even if an API signature/metadata check rejects the transformed object.

### G-MH-Confidentiality

Target: define an indistinguishability game extending the underlying CUFE confidentiality model to adaptive multi-hop paths.

The adversary may request update tokens and/or honest update operations on allowed exact states. Restrictions must prevent trivial recovery of the challenge function value while still exposing the update behavior required by the deployment model.

Open questions before theorem statement:

1. May the challenge ciphertext follow multiple honest paths?
2. Are tokens touching the challenge path revealed, or only exposed through an honest-update oracle?
3. Are forks allowed for challenge ciphertexts?
4. What leakage is inherent in public tags, levels, path length, and history commitments?
5. Does checkpoint issuance reveal only already-public state, or additional audit metadata?
6. Which combinations of source-state keys, target-state keys, corrupted tokens, and honest tokens are valid without trivializing the challenge?
7. How is exact composition reachability represented in the validity predicate of the adversary?

### G-SequentialComposition

For any adaptively selected valid accepted prefix `P_i`, the security of the next **explicitly authorized exact-state transition** must hold in the environment containing the adversary's complete view of `P_i`.

A proof must explain why security does not silently rely on the current ciphertext being a fresh encryption.

Sequential composition is not established merely by functional correctness after several updates. It requires that the accumulated adversarial view creates neither an unauthorized path edge nor a new forbidden functional capability, including key switching.

`G-CompositionAuthorization` and `G-SequentialComposition` are distinct:

- the former asks **whether the path is authorized**;
- the latter asks **whether security survives along an authorized path**.

## 5. Checkpoint games

### G-CheckpointForgery

Goal: produce an accepted checkpoint not authorized by the checkpoint trust policy.

For a single issuer, a natural reduction target is EUF-CMA security of the checkpoint signature plus canonical encoding. For a quorum scheme, the exact corruption threshold and aggregation/threshold-signature security must be stated.

### G-CheckpointStateBinding

Goal: take a valid checkpoint for `(S_k, h_k)` and make it validate for a different final state, history commitment, path policy, protocol version, or application context.

All context that changes checkpoint semantics must be authenticated.

### G-CheckpointEquivocation / accountability

If the checkpoint model allows an issuer to certify conflicting states, the paper must either:

- define this as outside the trust model;
- detect equivocation using a transparency/accountability mechanism; or
- use a quorum/threshold design whose threat model bounds this behavior.

A single signature alone does not prove that the issuer performed a correct audit.

## 6. Proof map

| Property | Candidate assumptions / dependencies | Status |
|---|---|---|
| Functional correctness | retained FE/CUFE construction + exact-state update algebra | OPEN |
| Multi-hop functional consistency | induction + construction invariant + depth-dependent correctness/noise bound | OPEN |
| State authorization | construction-level binding to `(tag,level)` | HIGH-RISK OPEN |
| Controlled composition authorization | exact-state binding + token unforgeability/construction security | HIGH-RISK OPEN |
| Stale replay | exact state/level binding | OPEN |
| Rollback resistance | monotone authenticated level + accepted-root/current-state policy | OPEN |
| Reorder/skip resistance | exact state continuity + linked history commitment | OPEN |
| Splice resistance | lineage-bound history links + history commitment | OPEN |
| History binding | collision resistance + canonical serialization | OPEN |
| Functional-key non-transferability | construction-specific reduction; legacy pairing scheme is a confirmed FAIL | HIGH-RISK OPEN |
| Multi-hop confidentiality | retained CUFE security + new prefix/composition reduction + key non-transferability | HIGH-RISK OPEN |
| Checkpoint forgery | signature/threshold-signature security | OPEN |
| Checkpoint state binding | unforgeability + canonical encoding | OPEN |
| Final-result binding | construction-specific proof soundness + statement binding | HIGH-RISK OPEN |

## 7. Experimental/conformance derivation

The executable campaign should contain at least one test per applicable class:

```text
ALLOW same state-global token on two ciphertexts genuinely in same exact source state
REJECT token on same tag but wrong level
REJECT composition (A,0)->(B,1) followed by token (B,0)->(C,1)
ALLOW explicit composition using (B,1)->(C,2)
REJECT stale token after advancement
REJECT wrong source tag
REJECT wrong source level
REJECT skipped hop
REJECT reordered hops
REJECT spliced lineages
REJECT replaced final ciphertext
REJECT replaced history digest
REJECT functional-key switching using public transition material
REJECT surrogate unauthorized target-state decryption
REJECT checkpoint reuse on another state/context
REJECT insufficient/forged quorum if quorum mode is implemented
REJECT wrong proof bases / wrong statement parameters
```

Passing these tests demonstrates implementation conformance to specified checks; it does not substitute for cryptographic reductions.
