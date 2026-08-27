# Proof barriers for the generic multi-level iO CAMH-CUFE candidate

## Status

**Proof-audit document. No security theorem is claimed.**

The generic candidate uses obfuscated update and functional-key programs with hidden level PRF/PTDE secrets. Its appeal is conceptual refresh at every hop. Its main risk is proof misuse of indistinguishability obfuscation (`iO`).

This document records the minimum conditions a valid proof must satisfy before issue #8 can close.

## 1. Forbidden proof shortcut: “the obfuscated program hides its keys”

Indistinguishability obfuscation is not a virtual-black-box guarantee. A proof cannot argue security merely because `k_l` appears only inside an obfuscated program.

Every replacement of a secret-dependent program by a simulated/punctured program must be justified by:

1. functional equivalence of the two programs on **all inputs** relevant to the iO definition; and
2. the underlying PRF/PTDE/security hybrid used to remove the challenge-dependent value.

If two compared circuits differ on an input that the adversary could in principle provide, iO cannot be invoked simply because the proof hopes that input is “unlikely”.

## 2. Shared-secret program graph

At internal level `l`, the same hidden key `k_l` can occur in several public obfuscated objects:

```text
incoming update programs:   PUpdate[k_{l-1}, k_l, ...]
outgoing update programs:   PUpdate[k_l, k_{l+1}, ...]
functional keys:            PKey[k_l, f, t, l]
```

With branching, there may be polynomially many incoming/outgoing programs sharing `k_l`.

Therefore a one-program puncturing hybrid is insufficient. The proof must maintain a **consistent punctured view across every public program containing the same level secret**.

## 3. Challenge-point consistency problem

Let a challenge ciphertext at level `l` expose public point `p_l` whose PTDE key is derived from `k_l`.

To replace challenge-dependent PRF material at `p_l`, the proof may need to puncture `k_l` at `p_l`. Once punctured, every program that needs `k_l(p_l)` must be rewritten so that:

- its behavior on the challenge path remains well defined;
- its behavior on non-challenge inputs remains identical;
- no public program offers an alternate route that evaluates the missing PRF point and reveals a distinguishing behavior.

This is straightforward neither under arbitrary branching nor under adaptive post-challenge token issuance.

## 4. Adjacent-update composition barrier

For a valid path

```text
Q_{l-1} -> Q_l -> Q_{l+1}
```

the adversary receives two public programs sharing `k_l`:

```text
PUpdate[k_{l-1}, k_l, ...]
PUpdate[k_l, k_{l+1}, ...]
```

The proof must justify security of their **joint exposure and arbitrary composition**, not only security of each program in isolation.

A valid reduction must answer:

1. which program is changed first in the hybrid sequence;
2. how the shared `k_l` is punctured/replaced consistently;
3. why the two program descriptions remain functionally equivalent at every iO step;
4. how rerandomized target points prevent an old challenge point from reappearing at a later level;
5. how malformed/adversarial inputs are handled by both compared programs identically.

## 5. Functional-key non-transferability barrier

A source functional key is itself an obfuscated program `PKey[k_l,f,t,l]`. The proof must rule out the possibility that combining it with a public outgoing update program creates target-state capability.

The required property is capability-based:

> the adversary must not evaluate `f` on an independently generated target-state ciphertext merely because it owns an authorized source-state functional key and public transition programs.

It is insufficient to show that the adversary cannot serialize or extract the exact target `PKey` object.

Any hybrid must therefore include **independent target ciphertexts**, not only descendants of the challenge/source ciphertext.

## 6. Exact state/level enforcement

The candidate's program guard must check the full cryptographic authorization state

\[
Q=(t,l),
\]

not only the visible tag.

The state check must be inside the semantics of the obfuscated cryptographic program. An outer Python/API metadata comparison does not realize `G-StateAuthorization` or `G-CompositionAuthorization`.

The proof must show that a program for

```text
(B,0) -> (C,1)
```

cannot process a ciphertext in `(B,1)` even when the visible tag bytes are identical.

## 7. Adaptive token-issuance barrier

The baseline CAMH-CUFE model targets adaptive interaction. After the challenge, the adversary may request unrelated transition tokens subject to the challenge-admissibility predicate.

A proof that must know the entire future transition DAG before setup/challenge is **selective/semi-adaptive**, not fully adaptive.

That may still be a valid theorem, but it must be labeled exactly and cannot silently replace the stronger baseline model.

A fully adaptive proof must explain how a simulator creates new obfuscated programs after relevant level keys have already been punctured/reprogrammed in earlier hybrids.

## 8. Branch/fork barrier

If two outgoing edges are authorized from the same state,

```text
Q_l -> Q_{l+1}^A
Q_l -> Q_{l+1}^B,
```

the adversary obtains two update programs sharing the same source secret and may execute both on the same challenge-derived ciphertext.

The security experiment and proof must state whether this is allowed. If allowed, both branches become challenge-derived and subsequent key-query admissibility must track both.

A proof that considers only a single linear challenge path does not establish security of the current branching baseline.

## 9. Fresh target randomness requirement

The candidate relies on each update program decrypting and re-encrypting under a fresh target-domain point/randomness.

The proof must formalize the event that a newly sampled target point collides with any prior punctured/challenge point and show that the collision probability is negligible for the chosen point domain.

If the construction uses deterministic target points, this argument changes fundamentally and must be reworked.

## 10. PTDE/PRF interface requirements

The final theorem must state the exact security required from each underlying primitive. At minimum the proof must identify whether it needs:

- puncturable PRF security under polynomially many punctures;
- selective/adaptive PTDE security for public tags;
- pseudorandomness of derived target keys;
- authenticated/canonical state parsing;
- one-time or multi-use properties of PTDE ciphertexts;
- any simulation-soundness or ciphertext-integrity property beyond confidentiality.

The construction cannot cite “PRF + iO” generically without mapping each hybrid transition to an assumption.

## 11. Candidate hybrid architecture

A potentially viable proof organization for bounded depth `L` is:

### H0 — real experiment

All level keys and programs are generated honestly.

### For each challenge-derived level `l`

1. identify the complete set of public programs containing `k_l`;
2. puncture/reprogram them consistently at the challenge point(s);
3. use iO only between functionally equivalent guarded programs;
4. replace the challenge PRF value using puncturable-PRF security;
5. replace the PTDE challenge payload/value using the exact PTDE security theorem;
6. propagate the new simulated representation into adjacent-level programs before moving to `l+1`.

### Final hybrid

The adversarial view is independent of the challenge bit subject to the admissibility predicate.

This is only a **proof architecture**. Every step above remains open until exact programs and equivalence arguments are written.

## 12. Quantitative proof-loss requirement

For bounded depth `L`, polynomially many token/key queries, and polynomial branch width, the total hybrid loss must remain polynomial in the security parameter.

The theorem must state explicit dependence on at least:

```text
L
number of exposed transition programs
number of functional-key programs
number of challenge-derived branches/points
number of punctures
```

A proof requiring exponential guessing over paths or branch choices is not acceptable for the intended claim.

## 13. GO/NO-GO criteria

### GO

Issue #8 may close only if a proof supplies:

- exact program syntax;
- exact selective/adaptive theorem statement;
- a consistent shared-key puncturing strategy;
- program-equivalence arguments for every iO hybrid;
- branch-aware challenge admissibility;
- capability-based key non-transferability;
- polynomial reduction loss.

### NO-GO

Reject the generic theorem if any essential step relies on:

- “iO hides embedded secrets” without an equivalence hybrid;
- API-level state checks outside the cryptographic program;
- forbidding every public token touching a challenge-derived state when those tokens are central to the multi-hop model;
- a single-path proof while claiming branching security;
- exponential path guessing;
- an assumption that already embeds the desired CAMH-CUFE security property.

## 14. Manuscript consequence

Until this proof closes, the iO construction may appear only as an **investigated feasibility candidate**, not as a proved CAMH-CUFE instantiation.

Even if the theorem succeeds, it remains a theoretical layer. It must not supply the real-system performance evidence required by FGCS.
