# CAMH-CUFE checkpoint trust model

## Status

**Baseline semantics frozen; cryptographic signer implementation and theorem remain open.**

CAMH-CUFE deliberately separates an independently replayable retained history from a compact certificate issued *after* that history has been audited. A checkpoint is therefore an authenticated **attestation of prior audit**, not a succinct proof that lets an arbitrary verifier reconstruct or independently validate omitted hops.

## 1. Baseline single-auditor model

The initial implementation target uses one explicitly trusted checkpoint issuer `A` with signing key pair

\[
(sk_A,pk_A).
\]

The auditor receives the complete retained history and performs `VerifyHistory` from an accepted fresh root. Only after successful verification does it form the canonical checkpoint statement

\[
M_{cp}=EncodeCheckpoint(
 suite, Q_k, C_k, h_k, k, policy, context
)
\]

and signs the domain-separated checkpoint statement.

The existing canonical statement binds:

- protocol/suite identifier;
- exact final authorization state `(tag,level)`;
- exact final canonical ciphertext;
- final rolling history commitment;
- retained history length;
- checkpoint policy identifier;
- optional application context.

The future signer must additionally use the registered domain `CAMH-CUFE/CHECKPOINT/SIGN/v1` or a documented standardized signature context that is provably equivalent in purpose separation.

## 2. Verification meaning

Given `pk_A`, statement `M_cp`, and signature `sigma_A`, successful `VerifyCheckpoint` means:

> the accepted checkpoint issuer authenticated this exact final state/history commitment under the identified checkpoint policy and application context.

It does **not** mean:

- that the verifier independently replayed every transition;
- that every omitted token/proof was supplied to the verifier;
- that a malicious trusted auditor could not sign a false audit result;
- that the checkpoint reveals no metadata;
- that the certificate is a SNARK/recursive proof/accumulator proof of all omitted hops.

These boundaries must appear consistently in the manuscript, API documentation, benchmarks, and figures.

## 3. Security target for an honest issuer

For a single honest checkpoint issuer, third-party checkpoint forgery should reduce to:

1. EUF-CMA security of the selected signature scheme over the canonical domain-separated statement; and
2. injectivity/unambiguous parsing of the canonical encoding.

Checkpoint state/context substitution is prevented only insofar as every semantics-changing field is inside the signed statement.

Collision resistance of the history commitment is separately required to prevent a valid signed digest from representing two distinct retained histories.

## 4. Malicious or equivocating issuer

A single ordinary signature does not force the issuer to perform the audit correctly and does not prevent the issuer from signing two conflicting checkpoint statements.

Therefore the baseline single-issuer threat model makes **auditor honesty for audit execution** an explicit trust assumption.

If the final system needs accountability against a malicious/equivocating auditor, one of the following extensions must be implemented and analyzed separately:

- transparency log / append-only publication of signed checkpoints;
- witness cosigning;
- quorum or threshold checkpoint signatures with a stated corruption threshold;
- a succinct proof system whose verified relation directly establishes the omitted history property.

No such extension may be claimed merely because the current statement contains a history digest.

## 5. Cost semantics

The trust/performance trade-off is asymmetric:

### Checkpoint issuance

Issuance includes a complete history audit and therefore normally depends on path length `k`, in addition to cryptographic signing cost.

### Later checkpoint verification

Once a checkpoint has been issued, verifying its signature and canonical statement need not replay the `k` retained hops. Its cost can therefore be independent of `k` for a fixed signature/checkpoint construction, while still depending on other parameters such as final-ciphertext representation size.

This distinction forbids the misleading claim that "history verification is constant-time." The defensible statement is that **later verification of a trusted checkpoint avoids replaying the retained history** under the stated trust assumption.

## 6. Benchmark separation

The evaluation must report at least three distinct measurements:

1. `T_full_history_verify(k)` — independent replay from the accepted root;
2. `T_checkpoint_issue(k)` — full audit plus certificate production;
3. `T_checkpoint_verify` — later verification of the issued certificate.

Communication/storage measurements must likewise distinguish:

- retained full-history bytes;
- checkpoint statement bytes;
- checkpoint signature/certificate bytes;
- any public key or trust-policy material amortized separately.

## 7. Baseline policy identifier

The first concrete single-issuer profile should use an explicit stable policy identifier such as:

```text
camh-cufe/checkpoint/single-honest-auditor/v1
```

Changing trust semantics requires a distinct policy identifier and corresponding theorem/benchmark label.

## 8. Quorum profile is optional, not inherited

A future quorum profile must specify:

- number of auditors `N`;
- acceptance threshold `q`;
- allowed corruptions `f`;
- key-generation/distribution assumptions;
- whether signatures are independent, aggregated, or threshold-generated;
- equivocation and availability semantics;
- exact communication and verification costs.

Until those items are implemented and proved, the manuscript must describe quorum checkpoints only as future/optional design space, not as measured CAMH-CUFE capability.

## 9. Relationship to full-history evidence

A full-history verifier and a checkpoint verifier answer different questions:

```text
full replay:
    "Do the supplied authenticated records independently validate from my accepted root?"

checkpoint:
    "Did the checkpoint trust policy authenticate this final state/history digest?"
```

The paper should present this as an explicit evidence-regime trade-off rather than rank the two mechanisms on speed as if they provided identical assurance.
