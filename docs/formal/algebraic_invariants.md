# CAMH-CUFE Algebraic Invariants from the Legacy Prototype

> Status: **proved algebraic correctness target**, not a confidentiality theorem. This document extracts the useful invariant from the legacy pairing-based prototype and states exactly what it establishes.

## 1. Notation

Let `p` be prime, let `G1`, `G2`, `GT` be order-`p` groups with bilinear pairing

```text
e : G1 x G2 -> GT.
```

The legacy construction samples an invertible matrix

```text
A in Z_p^(2 x 2)
```

and vectors

```text
U_j in Z_p^2,  j = 1,...,n.
```

For each public authorization state

```text
s = (tag, epoch),
```

let `h_s` denote the authority-derived state scalar. The state scalar is secret in the prototype.

A fresh ciphertext uses randomness `r in Z_p^2` and has

```text
c0 = [A r]_1
```

and coordinate

```text
c_j^(1) = [x_j + h_s <r,U_j>]_1.
```

For a transition `s -> s'`, the token contains the public group element

```text
D_j(s,s') = [(h_s' - h_s) A^(-T) U_j]_2.
```

## 2. First-hop update invariant

The first update maps a fresh coordinate from `G1` to `GT`:

```text
c_hat_j' = e(c_j, g2) * e(c0, D_j(s,s')).
```

In exponent notation,

```text
c_hat_j'
 = [x_j + h_s <r,U_j> + (h_s' - h_s)<r,U_j>]_T
 = [x_j + h_s' <r,U_j>]_T.
```

The plaintext coordinate is unchanged; only the state-dependent mask changes.

## 3. Later-hop update invariant

Once a coordinate is in `GT`, a later update adds only the pairing correction:

```text
c_hat_j^(i+1)
 = c_hat_j^i * e(c0, D_j(s_i,s_(i+1))).
```

If

```text
c_hat_j^i = [x_j + h_(s_i)<r,U_j>]_T,
```

then

```text
c_hat_j^(i+1)
 = [x_j + h_(s_(i+1))<r,U_j>]_T.
```

This gives the induction step.

## 4. Theorem A — Sequential mask telescoping

For every honestly generated path

```text
s_0 -> s_1 -> ... -> s_k
```

and every coordinate `j`, the payload after the path satisfies:

```text
c_hat_j^k = [x_j + h_(s_k)<r,U_j>]_T.
```

### Proof

The first-hop equation establishes the invariant for `s_1`. Assume it holds at `s_i`. The next token contributes

```text
(h_(s_(i+1)) - h_(s_i))<r,U_j>,
```

which cancels the previous state mask coefficient and replaces it with `h_(s_(i+1))`. Induction completes the proof.

### Consequence

The intermediate state scalars telescope:

```text
h_(s_0)
+ (h_(s_1)-h_(s_0))
+ ...
+ (h_(s_k)-h_(s_(k-1)))
= h_(s_k).
```

This establishes **sequential algebraic closure/correctness** of the update operation. It does not establish semantic confidentiality or adaptive composability security.

## 5. Theorem B — Final functional correctness

For functional vector

```text
v = (v_1,...,v_n),
```

let

```text
S = sum_j v_j U_j
```

and let the functional key for final state `s_k` contain the group representation corresponding to

```text
K_(s_k) = h_(s_k) A^(-T) S.
```

Then the aggregated final ciphertext contributes

```text
sum_j v_j c_hat_j^k
 = [<x,v> + h_(s_k)<r,S>]_T,
```

whereas the key/ciphertext pairing contributes

```text
e(c0, [K_(s_k)]_2)
 = [h_(s_k)<r,S>]_T.
```

Subtracting/cancelling the mask leaves

```text
[<x,v>]_T.
```

Bounded discrete-log decoding therefore returns `<x,v>` whenever that value lies in the declared decoding interval.

## 6. Theorem C — Payload path-independence at a fixed final state

Consider two honestly authorized paths for the **same fresh ciphertext**:

```text
P : s_0 -> ... -> s_k
Q : s_0 -> ... -> s_k
```

with the same final state `s_k` and the same number/epoch coordinate implied by that state, but possibly different intermediate tags/states.

By Theorem A, both paths yield

```text
c_hat_j = [x_j + h_(s_k)<r,U_j>]_T
```

for every coordinate `j`.

Hence their final cryptographic payload coordinates coincide, subject to deterministic group representation.

### Scientific implication

The payload alone need not encode which authorized path was followed. If path provenance matters, it must be carried by a separate authenticated history object (e.g., the rolling history commitment and retained transition records).

This cleanly separates:

```text
payload state correctness      -> depends on final state
history provenance/audit       -> depends on the actual path
```

This separation is a useful organizing invariant for CAMH-CUFE, but it is not by itself a novelty claim.

## 7. Theorem D — History commitment must be path-sensitive

Because Theorem C allows two different valid paths to yield the same final payload at the same final state, any claimed **path auditability** must distinguish those paths independently of the final payload.

Therefore a history commitment used by CAMH-CUFE must bind, at minimum, the ordered transition records and their predecessor commitment. If two distinct valid transition sequences can generate the same accepted history commitment without a hash collision or encoding ambiguity, the audit layer does not provide path binding.

This theorem reduces the intended path distinction to the collision resistance of the chosen history hash plus canonical serialization, once the exact record grammar is frozen.

## 8. What remains unproved

The algebra above does **not** establish:

- IND-style plaintext confidentiality;
- adaptive security under token/key queries;
- a reduction from one-hop Cini-style CUFE to the repeated pairing update;
- function privacy;
- metadata hiding;
- security of the history/checkpoint layer against a malicious checkpoint issuer;
- soundness of the final-result proof `pi4`.

Those remain separate gates and must not be inferred from Theorems A–D.
