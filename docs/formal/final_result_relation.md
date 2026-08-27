# CAMH-CUFE final-result relation boundary

## Status

**Public statement and verifier-context binding frozen at the reference-protocol level. Cryptographic proof-system soundness remains OPEN.**

This document defines exactly what a retained final-result proof is allowed to claim. It deliberately separates:

1. the canonical public statement;
2. deterministic verifier-critical base derivation; and
3. the still-unproved concrete proof relation.

A green conformance test for statement binding is not a soundness theorem.

## 1. Scientific purpose

A final-result proof, if retained, is intended to bind a claimed functional output to the exact final CAMH-CUFE context used by the verifier. It must not become a decorative proof whose meaning changes when the caller substitutes commitment bases, setup parameters, ciphertext identity, function metadata, or result encoding.

The proof is **not required for the core audit-history contribution**. If a concrete sound relation cannot be justified cleanly, `pi4` must be removed from the headline design rather than retained as an under-specified assurance mechanism.

## 2. Canonical public statement

Protocol version `1` assigns object type

```text
0x1008 = FINAL_RESULT_STATEMENT
```

to the canonical final-result statement. The encoded fields are, in order:

```text
suite_id
relation_id
public_parameters_digest
final_authorization_state = (tag, level)
dimension
canonical_final_ciphertext
canonical_function_public_view
canonical_functional_key_public_view
result_encoding_id
canonical_claimed_result
history_digest
history_length
application_context           [optional]
```

### 2.1 `suite_id`

Identifies the cryptographic/protocol suite. It is not sufficient by itself to identify one concrete setup.

### 2.2 `relation_id`

Identifies the exact final-result relation/proof semantics. A different relation requires a different identifier. The identifier must not be reused to mean a changed algebraic relation.

### 2.3 `public_parameters_digest`

A 32-byte digest of the **canonical concrete public parameters** for the setup used by the statement. The real backend must define the canonical public-parameter encoding before this digest can support scientific evidence.

The digest prevents two different setups using the same suite name from being silently treated as the same proof context.

### 2.4 Final authorization state

Binds the exact `(tag, level)` authorization state rather than only a visible tag.

### 2.5 Dimension

Binds the FE/function dimension and is also included in deterministic commitment-base derivation.

### 2.6 Final ciphertext

The statement embeds the canonical final ciphertext bytes. A hash-only representation may replace this in a future protocol version only after collision/binding semantics are specified explicitly.

### 2.7 Function public view

This is the canonical public description needed to define the function whose output is claimed. For an IPFE instantiation it may encode the function vector or a canonical commitment/public descriptor, depending on the final relation.

The current reference layer makes **no function-privacy claim**.

### 2.8 Functional-key public view

Binds whatever canonical public information about the functional key is necessary to define the proof relation. It must not expose secret key material merely to make verification easy.

The exact public view is construction-specific and remains open until the secure backend is selected.

### 2.9 Result encoding

`result_encoding_id` specifies how `claimed_result` bytes are interpreted. This prevents the same byte string from acquiring a different mathematical meaning under an implicit codec change.

For the intended inner-product setting, a signed/integer bounded encoding must specify width, sign convention, range, and canonical representation before experimental use.

### 2.10 History binding

The final statement includes both the 32-byte `history_digest` and `history_length`. This binds the proof claim to the retained lineage evidence used to reach the final state. It does not turn the final-result proof into a proof of every omitted transition unless the eventual relation explicitly proves that stronger property.

## 3. Deterministic `pi4` commitment bases

Verifier-critical bases are derived as

\[
B = \mathsf{DeriveBases}(
  \texttt{suite\_id},
  \texttt{public\_parameters\_digest},
  \texttt{relation\_id},
  n
).
\]

The domain label is

```text
CAMH-CUFE/PI4/BASES/v1
```

and the inputs are length/fixed-width framed before the selected real backend performs standards-conformant hash-to-curve.

The final verifier API does **not** accept caller-provided bases. `verify_final_result_reference` derives them internally from the statement.

The migration helper `require_canonical_pi4_bases` remains only for tests/legacy integration and rejects a supplied set unless it equals the deterministic set.

## 4. Final-result transcript

The reference layer frames

```text
len(DST) || CAMH-CUFE/PI4/STATEMENT/v1 ||
len(canonical_statement) || canonical_statement
```

as the proof transcript input.

The concrete proof system may then hash/process this transcript according to its own standard. This avoids inventing a Fiat-Shamir transform before the actual proof system is selected.

## 5. Reference verifier boundary

The executable interface is conceptually:

```text
VerifyFinalReference(G, statement, proof, VerifyRelation) -> {0,1}
```

and performs:

1. strict canonical statement validation;
2. deterministic derivation of bases from the bound setup/relation context;
3. domain-separated transcript construction;
4. invocation of the concrete relation verifier.

There is deliberately no argument of the form:

```text
pi4_bases
bases
caller_generators
```

in this verifier interface.

## 6. Soundness obligation — still OPEN

Statement binding alone does not establish the following implication:

\[
\mathsf{VerifyFinal}(st,\pi)=1
\Longrightarrow
\text{the claimed result is the correct authorized FE output}.
\]

A retained concrete proof must define witnesses and equations precise enough to establish that implication under explicit assumptions.

At minimum the proof relation must explain how the accepted proof binds simultaneously to:

- the canonical final ciphertext;
- the exact final authorization state;
- the function public descriptor;
- the functional-key public view;
- the claimed result and its encoding;
- the concrete public setup;
- any commitments/randomness used by the proof.

It must also explain why no alternative commitment bases, malformed group elements, dimension mismatch, or cross-setup statement can satisfy the verifier.

## 7. No hidden claims

Until a concrete proof system is selected and proved, the manuscript must not claim that `pi4` provides:

- zero knowledge;
- function privacy;
- key privacy;
- succinct verification;
- public verifiability of the complete update history;
- proof of correct proxy execution;
- proof of correct FE output.

Only the already-established **statement/context binding discipline** may be described at this stage.

## 8. GO / NO-GO criterion

### GO

Retain `pi4` only if the selected concrete CAMH-CUFE construction permits a clean proof relation with:

- explicit witness/public-input syntax;
- reduction/soundness argument;
- canonical group/field encoding;
- internally derived verifier context;
- adversarial substitution tests;
- measured proof size/generation/verification costs on the real backend.

### NO-GO

Remove `pi4` from the paper if:

- its verifier merely rechecks metadata already covered by history verification;
- the proof relation depends on secret information that cannot be exposed or proved safely;
- soundness relies on caller-selected parameters;
- the proof adds no scientifically meaningful guarantee beyond ordinary decryption/correctness checks;
- its proof/evaluation burden distracts from the central CAMH-CUFE composability contribution.

A smaller paper with one fully justified contribution is preferable to a feature-rich construction with an unproved proof component.
