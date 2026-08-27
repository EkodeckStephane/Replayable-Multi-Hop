# LWE key-security / noise-growth coupling in multi-hop CAMH-CUFE

## Status

**Derived design invariant — not yet a theorem of a secure construction.**

This note isolates a technical coupling that appears when the one-hop lattice CUFE algebra is generalized to multiple levels. It explains why correctness/noise control and functional-key non-transferability cannot be optimized independently.

## 1. Level-indexed decryption error

Assume a level/state `l` has matrices

\[
H_l Z_l=D_l
\]

and ciphertext components

\[
c_{1,l}=H_l^T s_l+E_{1,l},
\]

\[
c_{2,l}=D_l^T s_l+E_{2,l}+M x.
\]

For an inner-product query vector \(y\), the corresponding key is represented by \(Z_l y\). The decryption expression is

\[
\begin{aligned}
y^T c_{2,l}-(Z_l y)^T c_{1,l}
&=M\langle x,y\rangle+\varepsilon_l(y),
\end{aligned}
\]

where

\[
\varepsilon_l(y)=y^T(E_{2,l}-Z_l^T E_{1,l}).
\tag{1}
\]

## 2. Update recurrence

For a transition `l -> l+1`, suppose

\[
H_l\Delta_{1,l}=H_{l+1},
\]

\[
H_l\Delta_{2,l}=D_{l+1}-D_l,
\]

and

\[
E_{1,l+1}=\Delta_{1,l}^T E_{1,l}+f_{1,l},
\]

\[
E_{2,l+1}=E_{2,l}+\Delta_{2,l}^T E_{1,l}+f_{2,l}.
\]

Substituting into (1) gives

\[
\begin{aligned}
\varepsilon_{l+1}(y)
&=\varepsilon_l(y)
+y^T R_l^T E_{1,l}
+y^T(f_{2,l}-Z_{l+1}^T f_{1,l}),
\tag{2}
\end{aligned}
\]

where the **transition residual** is

\[
R_l:=Z_l+\Delta_{2,l}-\Delta_{1,l}Z_{l+1}.
\tag{3}
\]

## 3. Kernel identity

The residual always satisfies

\[
\begin{aligned}
H_lR_l
&=H_lZ_l+H_l\Delta_{2,l}-H_l\Delta_{1,l}Z_{l+1}\\
&=D_l+(D_{l+1}-D_l)-H_{l+1}Z_{l+1}\\
&=0\pmod q.
\end{aligned}
\tag{4}
\]

Thus \(R_l\) lies in the appropriate kernel lattice of \(H_l\).

This identity is structural; it does not establish that \(R_l\) is short enough for correctness or hidden enough for security.

## 4. Why this couples correctness and key security

Equation (2) shows that accumulated error is not governed only by the size of \(\Delta_1\). It is also governed by the size/distribution of \(R_l\).

A tempting correctness optimization is to enforce

\[
\Delta_{2,l}=\Delta_{1,l}Z_{l+1}-Z_l,
\tag{5}
\]

which makes \(R_l=0\) and removes the inherited-error term \(y^TR_l^TE_{1,l}\).

However, (5) exposes an explicit algebraic relation between the source and target key bases. Such a relation is security-sensitive: public update material must not enable transformation of a source functional key into a target functional key or equivalent decryption capability.

Therefore **`R_l = 0` is not adopted as a construction rule**. It is a diagnostic extreme illustrating the trade-off.

The legacy pairing scheme failed for exactly this type of reason: its public transition material gave a direct linear relation that switched the functional-key group element to the target state.

## 5. Multi-hop error decomposition

Iterating (2) yields

\[
\varepsilon_L(y)=\varepsilon_0(y)
+\sum_{l=0}^{L-1} y^T R_l^T E_{1,l}
+\sum_{l=0}^{L-1} y^T(f_{2,l}-Z_{l+1}^Tf_{1,l}).
\tag{6}
\]

This decomposition separates three sources:

1. the fresh-ciphertext error \(\varepsilon_0\);
2. **history-coupled inherited error** through \(R_l^TE_{1,l}\);
3. fresh per-hop update noises.

A viable CAMH-CUFE lattice construction must control all three simultaneously.

## 6. Security property induced by the legacy counterexample

The concrete construction must satisfy a functional-key non-transferability experiment strong enough to rule out algorithms of the form

\[
\mathcal{A}(sk_{f,s},\Delta_{s\to s'},f,mpk)
\to \widetilde{sk}_{f,s'}
\]

where \(\widetilde{sk}_{f,s'}\) is either:

- a valid target-state functional key;
- an algebraically equivalent key representation; or
- any surrogate that computes \(f(x)\) on target-state ciphertexts outside the permissions of the security game.

The experiment must test **capability**, not merely byte equality with an authority-issued key.

## 7. Candidate design directions

### A. Independently randomized short preimages

Retain Cini-style independent/randomized sampling of key matrices and update matrices so that the public token does not expose a simple key-switch map. Then derive a tight distributional bound on \(R_l\).

**Risk:** the residual may be too large for practical multi-hop correctness.

### B. Kernel-masked correlation

Construct

\[
\Delta_{2,l}=\Delta_{1,l}Z_{l+1}-Z_l+N_l,
\]

where \(H_lN_l=0\), and choose \(N_l\) from a distribution intended to hide the key relation while keeping the error term manageable.

**Risk:** a short/public \(N_l\) may still leak a transform; a sufficiently wide masking distribution may destroy correctness. This direction requires a full reduction, not heuristic reasoning.

### C. Refresh-oriented update

Use an update mechanism that cryptographically refreshes the ciphertext noise/state rather than linearly carrying the inherited error forward.

**Risk:** may require stronger assumptions or techniques closer to recent multi-hop ciphertext-updatable ABE/PE work.

### D. Separate theoretical and practical instantiations

Provide a stronger generic/theoretical multi-hop construction and a bounded practical IPFE instantiation with an explicit maximum depth.

**Risk:** must avoid presenting the practical instantiation as evidence for guarantees it does not realize.

## 8. GO criterion

A candidate lattice transition is not accepted merely because it satisfies the public matrix equations. It must simultaneously establish:

- target-state functional correctness;
- a depth-dependent decryption-error bound;
- functional-key non-transferability;
- challenge-security simulation for update paths;
- implementable parameters.

The first candidate satisfying only correctness is insufficient for CAMH-CUFE.
