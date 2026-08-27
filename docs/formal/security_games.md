# CAMH-CUFE Security Games and Proof Obligations

> Status: design document. Names and exact oracle interfaces may change during proof development.

## 1. Design principle

Security must be defined over **state-transition histories**, not inferred from a finite list of implementation corruption tests. The adversarial tests are later derived from these games.

The adversary may interact adaptively with key, token, encryption, update, and verification interfaces subject to the restrictions required by the confidentiality definition.

## 2. Correctness properties

### Functional correctness

For every valid state `S_i` reached by an authorized path and every compatible functional key,

```text
Dec(sk_f, S_i) = f(x)
```

except with negligible probability.

### Transition correctness

Every honestly generated token for the displayed source state produces a next state accepted by `VerifyTransition`.

### History correctness

Every honestly generated sequence of accepted transitions is accepted by `VerifyHistory`.

### Checkpoint correctness

Every certificate generated after an accepted history audit is accepted by `VerifyCheckpoint` under the corresponding trust policy.

## 3. History-integrity games

### G-Replay: stale-token replay resistance

Goal of the adversary: make a token authorized for an earlier state/epoch validate against a later state for which that transition was not authorized.

Win condition: an unauthorized stale transition is accepted.

### G-Rollback: rollback resistance

Goal: make a previously valid old state appear as the current accepted descendant of a newer state/history.

The game must distinguish legitimate archival verification of an old state from acceptance of that state as the current state.

### G-Skip: skipped-hop resistance

Goal: delete one or more required transitions while retaining an accepted final state/history claim.

### G-Reorder: transition-order integrity

Goal: permute individually valid transitions so that an invalid path is accepted.

### G-Splice: cross-history splice resistance

Goal: combine a valid prefix from one ciphertext history with a valid suffix from another history and obtain acceptance.

The challenge is important even if both histories use identical tag names.

### G-Fork: prefix/fork consistency

Goal: create conflicting accepted descendants from a context in which the policy requires a unique evolution path, or make a verifier accept incompatible histories as one linear history.

The exact property depends on whether the system intends to allow authorized branching. If branching is legitimate, the game must instead enforce explicit branch identities and prevent implicit history equivalence.

### G-CrossState: source-state substitution resistance

Goal: apply an otherwise valid update authorization to a different ciphertext or source state that shares some public coordinates.

This game determines which ciphertext/state identifiers must be authenticated by the transition statement.

### G-HistoryBinding: history-commitment binding

Goal: produce two semantically distinct accepted histories that yield the same accepted authenticated history commitment for a checkpoint/final-state claim.

Reduction target: collision resistance plus unambiguous/canonical encoding, unless a stronger construction-specific assumption is required.

## 4. Functional-encryption and composability games

### G-MH-FunctionalConsistency

Authorized repeated updates must preserve the intended plaintext/function relation. The output after any valid path must remain the defined functional result rather than a path-dependent transformed message, unless path-dependent functionality is explicitly part of the scheme.

### G-MH-Confidentiality

Target: define an indistinguishability game extending the underlying CUFE confidentiality model to adaptive multi-hop paths.

The adversary may request update tokens and/or honest update operations on allowed states. Restrictions must prevent trivial recovery of the challenge function value while still exposing the update behavior needed to model deployment.

Open questions to resolve before theorem statement:

1. Is the challenge ciphertext allowed to follow multiple honest paths?
2. Are tokens for transitions touching the challenge path revealed or only exposed through an update oracle?
3. Are forks allowed for challenge ciphertexts?
4. What leakage is inherent in public tags, epochs, path length, and history commitments?
5. Does checkpoint issuance reveal only already-public state, or additional audit metadata?

### G-SequentialComposition

This is the central composability property.

For any adaptively selected valid accepted prefix `P_i`, the security of the next authorized transition must hold in the environment containing the adversary's complete view of `P_i`.

A proof must explain why security does not silently rely on `S_i` being a fresh encryption.

## 5. Checkpoint games

### G-CheckpointForgery

Goal: produce an accepted checkpoint not authorized by the checkpoint trust policy.

For a single issuer, a natural reduction target is EUF-CMA security of the checkpoint signature plus canonical encoding.

For a quorum scheme, the exact corruption threshold and aggregation/threshold signature security must be stated.

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
| Functional correctness | underlying CUFE/IPFE correctness + update algebra | OPEN |
| Multi-hop functional consistency | induction over update path + construction invariant | OPEN |
| Replay resistance | source epoch/state binding + signature/unforgeability | OPEN |
| Rollback resistance | monotone authenticated epoch + accepted-root/current-state policy | OPEN |
| Reorder/skip resistance | linked history commitment + transition source/destination binding | OPEN |
| Splice resistance | ciphertext/state identity binding + history commitment | OPEN |
| History binding | collision resistance + canonical serialization | OPEN |
| Multi-hop confidentiality | underlying CUFE security + new composition reduction | HIGH-RISK OPEN |
| Checkpoint forgery | signature/threshold signature security | OPEN |
| Checkpoint state binding | unforgeability + canonical encoding | OPEN |
| Final-result binding | construction-specific proof soundness + statement binding | HIGH-RISK OPEN |

## 7. Experimental derivation

The adversarial campaign should instantiate at least one executable test per security class, including:

```text
old-token replay
wrong source epoch
wrong source tag
skip a hop
reorder two hops
splice two histories
replace final ciphertext
replace history digest
reuse checkpoint on another state
modify checkpoint context
insufficient/forged quorum (if quorum checkpoints are implemented)
wrong proof bases / wrong statement parameters
```

Passing these tests is evidence that the implementation enforces the specified checks; it is not a substitute for the cryptographic reductions.
