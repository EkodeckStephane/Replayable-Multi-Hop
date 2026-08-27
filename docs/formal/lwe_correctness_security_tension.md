# Quantitative correctness–security tension for the direct LWE route

## Status

**Conditional bound derived from the candidate equations. Not an impossibility theorem for all lattice CUFE.**

This note combines:

- the transition residual governing inherited multi-hop decryption error; and
- the public-token surrogate-key criterion.

It identifies a parameter region in which making the direct LWE transition sufficiently well behaved for correctness also guarantees a usable target surrogate when `Delta_1` is publicly invertible and not too ill-conditioned.

## 1. Definitions

For transition `l -> l+1`, recall

\[
R_l=Z_l+\Delta_{2,l}-\Delta_{1,l}Z_{l+1}.
\tag{1}
\]

Assume `Delta_1` is invertible over the relevant modular domain. From the public surrogate derivation,

\[
\begin{aligned}
k^*_{l+1}(y)
&=\Delta_{1,l}^{-1}(Z_ly+\Delta_{2,l}y)\\
&=Z_{l+1}y+\Delta_{1,l}^{-1}R_ly.
\end{aligned}
\tag{2}
\]

Define the surrogate perturbation

\[
\delta_l(y):=\Delta_{1,l}^{-1}R_ly.
\tag{3}
\]

Hence

\[
k^*_{l+1}(y)=k_{l+1}(y)+\delta_l(y).
\tag{4}
\]

## 2. Target decryption with the surrogate

For an independently generated target-state ciphertext

\[
c_1=H_{l+1}^Ts+E_1,
\qquad
c_2=D_{l+1}^Ts+E_2+Mx,
\]

the honest functional-key error is

\[
\varepsilon_{\mathrm{hon}}(y)
=y^TE_2-(Z_{l+1}y)^TE_1.
\tag{5}
\]

Using the surrogate gives

\[
\begin{aligned}
\varepsilon_*(y)
&=y^TE_2-(k^*_{l+1}(y))^TE_1\\
&=\varepsilon_{\mathrm{hon}}(y)-\delta_l(y)^TE_1.
\end{aligned}
\tag{6}
\]

Therefore

\[
|\varepsilon_*(y)|
\le
|\varepsilon_{\mathrm{hon}}(y)|
+\|\delta_l(y)\|_2\|E_1\|_2.
\tag{7}
\]

By submultiplicativity,

\[
\|\delta_l(y)\|_2
\le
\|\Delta_{1,l}^{-1}\|_2
\|R_l\|_2
\|y\|_2.
\tag{8}
\]

Combining (7) and (8),

\[
|\varepsilon_*(y)|
\le
|\varepsilon_{\mathrm{hon}}(y)|
+
\|\Delta_{1,l}^{-1}\|_2
\|R_l\|_2
\|y\|_2
\|E_1\|_2.
\tag{9}
\]

## 3. Sufficient attack-success bound

Let the target decoder accept whenever

\[
|\varepsilon|<D_{\mathrm{dec}}
\]

for the concrete decoding radius `D_dec`.

Suppose honest target correctness provides a bound

\[
|\varepsilon_{\mathrm{hon}}(y)|\le B_{\mathrm{hon}}
<D_{\mathrm{dec}}.
\tag{10}
\]

Then a sufficient condition for the surrogate to remain inside the decoding radius is

\[
B_{\mathrm{hon}}
+
\|\Delta_{1,l}^{-1}\|_2
\|R_l\|_2
\|y\|_2
\|E_1\|_2
< D_{\mathrm{dec}}.
\tag{11}
\]

Equivalently, whenever the denominator is nonzero,

\[
\|R_l\|_2
<
\frac{D_{\mathrm{dec}}-B_{\mathrm{hon}}}
{\|\Delta_{1,l}^{-1}\|_2\|y\|_2\|E_1\|_2},
\tag{12}
\]

the norm bound is sufficient for successful unauthorized functional decoding by the surrogate.

Equation (12) is **sufficient, not necessary**. A surrogate may succeed outside this conservative region.

## 4. Correctness pressure on the same residual

The previously derived next-level legitimate error recurrence contains

\[
y^TR_l^TE_{1,l}.
\tag{13}
\]

and therefore admits the bound

\[
|y^TR_l^TE_{1,l}|
\le
\|y\|_2\|R_l\|_2\|E_{1,l}\|_2.
\tag{14}
\]

Thus the direct repeated-update design has a structural pressure to keep `R_l` controlled in order to prevent inherited error from consuming the decryption margin.

But equations (11)–(12) show that a small `R_l` also keeps the public surrogate close to the honest target key whenever `Delta_1^{-1}` has moderate norm.

## 5. Conditional incompatibility region

Assume a proposed parameterization proves correctness only when

\[
\|R_l\|_2\le R_{\mathrm{corr}}.
\tag{15}
\]

If it also proves/bounds

\[
\|\Delta_{1,l}^{-1}\|_2\le I_l,
\quad
\|y\|_2\le Y,
\quad
\|E_1\|_2\le E,
\tag{16}
\]

and

\[
B_{\mathrm{hon}}+I_lR_{\mathrm{corr}}YE
<D_{\mathrm{dec}},
\tag{17}
\]

then **every transition satisfying that correctness residual bound also satisfies this sufficient surrogate-decoding bound** for the stated parameter envelope.

Under the other attack conditions (public invertibility/solvability and public source key/token exposure), such a parameterization cannot simultaneously claim key non-transferability for those functions/ciphertexts.

This is a conditional incompatibility statement, not a universal lattice impossibility theorem.

## 6. Important escape routes

The criterion does not rule out a secure lattice design if, for example:

1. `Delta_1 z = w` is not efficiently solvable for attacker-generated `w`;
2. every public solution is necessarily too large/noisy to decrypt;
3. the update construction changes the target key/decryption relation so equation (9) no longer characterizes functional capability;
4. ciphertext refresh changes the inherited-error structure rather than carrying `R_l` as above;
5. public transition material no longer exposes the algebra needed to construct `w`;
6. the concrete security construction uses additional hidden/randomized structure backed by a reduction.

Each escape route requires a proof; it cannot be inferred from API design.

## 7. Parameter-search implications

For every concrete candidate transition, the experimental/theoretical diagnostic should record at least:

```text
||R_l||
||Delta1_l||
||Delta1_l^{-1}|| or relevant solver amplification
condition number / modular rank information
||Z_{l+1} y||
||k*_{l+1}(y)||
honest decryption error
surrogate decryption error
decoding radius
```

for representative and worst-case/quantile parameter regimes justified by the proof.

These are **construction diagnostics**, not final systems performance metrics.

## 8. Scientific consequence

The direct multi-level LWE route is now blocked by more than generic “noise growth”. It must navigate a measurable security/correctness trade-off involving the same residual matrix.

This strengthens the project scientifically even if the candidate is ultimately rejected: a rigorous negative design boundary is preferable to reporting benchmark results for an algebraically vulnerable construction.
