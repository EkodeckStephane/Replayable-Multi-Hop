# CAMH-CUFE audit-layer theorem program

## Status

**Conditional theorem statements with reduction sketches.** These results isolate what can already be established about the audit layer independently of the unresolved CAMH-CUFE confidentiality construction. They are not a substitute for construction-level proofs of `VerifyTransitionUse`, token unforgeability, or multi-hop FE security.

## 1. Definitions

For protocol version `1`, let:

\[
H_0 = H(D_{init} \parallel EncInit(suite,Q_0,C_0))
\]

and for retained transition `i >= 1`,

\[
H_i = H(D_{link} \parallel EncLink(
 suite,H_{i-1},T_i,C_{i-1},C_i,\sigma_i)).
\]

The executable implementation length-prefixes the domain before hashing; the notation above suppresses that deterministic framing.

`T_i` is the canonical transition statement containing the exact source/destination authorization states and concrete public update material. `sigma_i` authenticates `T_i` under the selected token-authentication scheme.

A complete retained history is accepted only if `verify_retained_history` establishes:

1. exact level-0 root state binding;
2. exact issued authorization edge for every hop;
3. canonical reconstruction of every `T_i`;
4. token authentication for every `T_i`;
5. sound `VerifyTransitionUse(C_{i-1},T_i,C_i)` for every hop;
6. exact state and ciphertext continuity;
7. exact rolling-digest recomputation;
8. equality with any displayed final state/ciphertext/digest claim.

## 2. Assumptions

The following assumptions are separated deliberately.

### A1 — Canonical encoding injectivity

For every typed protocol object in the valid domain, the canonical encoder is injective and parsing is unambiguous. The current TLV implementation provides structural evidence through strict field ordering, explicit lengths, unique field identifiers, version/type binding, golden vectors, and malformed-input tests. A full concrete-backend encoding audit remains required.

### A2 — Collision resistance of the history hash

The selected history hash is collision resistant for the domain-separated inputs used by `H_0` and `H_i`. The reference implementation currently uses SHA-256.

### A3 — Token-statement authentication

An accepted token signature/authenticator implies that an authorized issuer authenticated the exact canonical transition statement, except with the forgery advantage of the retained authentication scheme.

### A4 — Transition-use soundness

If

```text
VerifyTransitionUse(C, T, C') = 1
```

then `C'` is a valid concrete cryptographic result of applying the update material encoded in canonical statement `T` to valid source ciphertext `C` under the exact state relation asserted by `T`, except with the soundness/error probability of the retained construction/proof mechanism.

**A4 is not yet established for a secure real CAMH-CUFE backend.** The reference verifier injects this predicate explicitly so that hash-chain tests cannot be mistaken for cryptographic transition validation.

### A5 — Exact authorization-set integrity

The verifier obtains the authoritative set of issued exact state edges from an authenticated policy source. Visible tag equality alone does not add edges.

## 3. Theorem H — history-commitment binding

### Statement

Under A1 and A2, an efficient adversary that produces two semantically distinct valid retained histories with the same final rolling history digest yields a collision in the history hash, except for histories whose canonical encoded sequences are identical.

### Reduction sketch

Take two accepted histories `P` and `P'` with the same final digest.

- If their final link encodings differ while their hash outputs are equal, those two domain-separated inputs form an immediate collision.
- If their final link encodings are equal, injectivity implies equality of all final-link fields, including the previous digest. Recurse to the previous link.
- If the histories have different lengths, recursion eventually compares a history-root input with a link-derived path position; the explicit domain labels distinguish those input classes, so equality of final digest again yields a hash collision unless a prior differing link already did.
- At the root, two distinct `(suite,Q_0,C_0)` values produce distinct canonical root objects by A1; equal root digests therefore give a collision.

Hence a pair of distinct accepted canonical histories with equal final digest contradicts A2.

### Scope

This theorem binds the *encoded retained evidence*. It does not prove that an encoded transition is cryptographically valid; that property enters through A3/A4 in the history-verification theorem below.

## 4. Theorem V — accepted-history validity

### Statement

Assume A1, A3, A4, and A5. If the complete-history verifier accepts a retained history from accepted root `(Q_0,C_0)`, then every retained hop in that accepted sequence:

1. is an exact authorized state edge;
2. carries an authenticated canonical transition statement;
3. has a destination ciphertext accepted by the concrete transition-use relation for the displayed source ciphertext and transition material; and
4. is state/ciphertext-contiguous with its predecessor.

If A2 also holds, the accepted final digest binds that exact retained sequence as in Theorem H.

### Proof sketch

The verifier checks the four conditions explicitly at every iteration and aborts on the first failure. The result follows by induction on the number of retained records. The cryptographic meaning of checks (2) and (3) is inherited only from A3 and A4; the Python control flow itself provides no stronger guarantee.

## 5. Corollaries for skip, reorder, and splice manipulations

The following corollaries require careful wording because CAMH-CUFE tokens are state-global and the authorization graph may branch.

### 5.1 Deletion / skipped retained hop

Deleting a record from an already accepted linear history while leaving its later suffix unchanged causes the next retained source state and/or source ciphertext to disagree with the verifier's current state/ciphertext, so verification rejects.

An adversary can replace the deleted segment only by presenting a different sequence that itself passes A3/A4/A5 and continuity. If a separately authorized direct transition genuinely produces that sequence, it is a different valid history, not a successful skipped-hop forgery.

### 5.2 Reordering

Permuting retained records rejects whenever exact state/ciphertext continuity breaks. A permutation that independently forms an exact authorized, cryptographically valid path is not evidence that the original ordering was forged; it is a separately valid path and receives a separately computed history commitment.

### 5.3 Cross-lineage splice

Copying a suffix record from another lineage rejects immediately if its source ciphertext differs from the current lineage ciphertext or if its stored rolling digest was computed under the other prefix.

Because history hashing is public, an attacker can always *recompute* a new rolling digest. Recomputed hashing alone therefore does not establish provenance. The recomposed suffix must still pass `VerifyTransitionUse` for the current source ciphertext and token authentication for the canonical statement.

If the state-global token legitimately produces the displayed destination from the current source, the result is an authorized use and is not a splice attack under the baseline token semantics. If it does not, acceptance contradicts A4.

This distinction prevents the audit theorem from silently imposing ciphertext-specific token semantics that CAMH-CUFE does not claim.

## 6. Theorem C — checkpoint authenticity and state binding

Let a checkpoint issuer sign the exact domain-separated canonical checkpoint statement

```text
suite_id
final_state
final_ciphertext
history_digest
history_length
policy_id
application_context
```

only after accepting a full retained history under the selected policy.

### Statement

Under:

- EUF-CMA security of the checkpoint signature scheme;
- A1 for the checkpoint encoding;
- Theorem H for history-digest binding;
- honesty of the single checkpoint issuer with respect to performing the required audit,

a third party cannot produce an accepted checkpoint for a different bound field tuple or for a different retained history represented by the same digest except with the sum of the relevant signature-forgery and hash-collision advantages.

### Reduction sketch

If an attacker changes any checkpoint field while reusing a signature, injectivity yields a distinct signed message, so acceptance implies a signature forgery unless the exact message was previously signed. If the message is unchanged but the attacker claims a distinct retained history under the same digest, Theorem H yields a hash collision.

### Trust boundary

This theorem does **not** protect against the trusted single issuer deliberately signing a false audit result or equivocating between conflicting checkpoints. Those behaviors require an accountability/transparency/quorum extension or a proof system that directly proves the omitted history relation.

## 7. Quantitative advantage form

For a concrete instantiation, the paper should state bounds in the form

\[
Adv_{bind}^{hist}(A)
\leq Adv_{cr}^{H}(B_H) + Adv_{enc-canon}(B_E),
\]

where the encoding term is zero once injectivity is established over the valid object domain, and

\[
Adv_{forge}^{checkpoint}(A)
\leq Adv_{euf-cma}^{Sig}(B_S)
+ Adv_{bind}^{hist}(B_H).
\]

For complete-history acceptance, the overall failure probability additionally includes the concrete token-authentication and transition-use soundness terms.

Exact running-time/query losses must be instantiated after the concrete primitives are fixed.

## 8. What this closes and what remains open

These reductions justify treating the following as separable audit-layer proof obligations:

- history hash binding;
- checkpoint field binding;
- skip/reorder/splice rejection conditioned on exact transition verification.

They do **not** close:

- CAMH-CUFE functional correctness;
- exact-state binding inside the yet-unselected real update construction;
- functional-key non-transferability;
- `MH-PUB` confidentiality;
- sequential cryptographic composition;
- final-result proof soundness.

The manuscript must preserve this boundary.
