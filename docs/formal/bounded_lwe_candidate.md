# Bounded multi-level LWE candidate for CAMH-CUFE

## Status

**Research candidate only — no security claim.**

This document studies whether the lattice CUFE construction of Cini et al. can be generalized from its two ciphertext levels (fresh / once-updated) to a bounded sequence of level-indexed CUFE states. It records algebraic feasibility, correctness/noise recurrences, and explicit GO/NO-GO conditions.

The construction must not be described as secure until functional-key non-transferability and sequential confidentiality are proved.

## 1. Starting point: one-hop lattice CUFE

Cini et al. use tag/level-dependent matrices

\[
H_{t,\ell}=(A\mid B_{t,\ell}), \qquad \ell\in\{1,2\},
\]

and an update token from a fresh ciphertext under `t` to an updated ciphertext under `t'` containing matrices \(\Delta_1,\Delta_2\) conditioned on

\[
H_{t,1}\Delta_1=H_{t',2},
\]

and

\[
H_{t,1}\Delta_2=D_{t'}-D_t.
\]

The updated ciphertext satisfies

\[
\begin{aligned}
c'_{1}&=\Delta_1^T c_1+H_{t',2}^T r+f_1,\\
c'_{2}&=c_2+\Delta_2^T c_1+D_{t'}^T r+f_2.
\end{aligned}
\]

The published construction intentionally stops after this update.

## 2. Candidate bounded-level state space

Let

\[
s=(t,\ell),\qquad \ell\in\{0,\dots,L\}.
\]

For each state, define a public matrix family

\[
H_{t,\ell}=(A\mid B_{t,\ell}).
\]

A transition token

\[
\Delta_{(t,\ell)\rightarrow(t',\ell+1)}=(\Delta_{1,\ell},\Delta_{2,\ell})
\]

is required to satisfy

\[
H_{t,\ell}\Delta_{1,\ell}=H_{t',\ell+1}
\tag{1}
\]

and, in the simplest direct generalization,

\[
H_{t,\ell}\Delta_{2,\ell}=D_{t'}-D_t.
\tag{2}
\]

A level-indexed family \(D_{t,\ell}\) remains an alternative if required by the security proof; equation (2) would then become

\[
H_{t,\ell}\Delta_{2,\ell}=D_{t',\ell+1}-D_{t,\ell}.
\]

No choice between these variants is authorized before the key-security reduction is attempted.

## 3. Algebraic correctness recurrence

Represent a level-\(\ell\) ciphertext as

\[
\begin{aligned}
c_{1,\ell}&=H_{t_\ell,\ell}^T s_\ell+E_{1,\ell},\\
c_{2,\ell}&=D_{t_\ell}^T s_\ell+E_{2,\ell}+M x,
\end{aligned}
\]

where \(M\) denotes the message scaling/embedding used by the underlying inner-product construction.

For fresh update randomness \(r_\ell\) and noises \(f_{1,\ell},f_{2,\ell}\), define

\[
\begin{aligned}
c_{1,\ell+1}
&=\Delta_{1,\ell}^T c_{1,\ell}
  +H_{t_{\ell+1},\ell+1}^T r_\ell
  +f_{1,\ell},\\
c_{2,\ell+1}
&=c_{2,\ell}
  +\Delta_{2,\ell}^T c_{1,\ell}
  +D_{t_{\ell+1}}^T r_\ell
  +f_{2,\ell}.
\end{aligned}
\]

Using (1) and (2), the structural terms telescope into the target state. The inherited errors obey

\[
E_{1,\ell+1}=\Delta_{1,\ell}^T E_{1,\ell}+f_{1,\ell},
\tag{3}
\]

and

\[
E_{2,\ell+1}=E_{2,\ell}+\Delta_{2,\ell}^T E_{1,\ell}+f_{2,\ell}.
\tag{4}
\]

Equations (3)-(4) establish **algebraic multi-hop correctness form**, but not a usable correctness bound.

## 4. Conservative norm recurrence

Let

\[
a_\ell=\|E_{1,\ell}\|,
\qquad
b_\ell=\|E_{2,\ell}\|,
\]

and suppose, uniformly over the path,

\[
\|\Delta_{1,\ell}\|\le R_1,
\qquad
\|\Delta_{2,\ell}\|\le R_2,
\]

\[
\|f_{1,\ell}\|\le F_1,
\qquad
\|f_{2,\ell}\|\le F_2.
\]

Then

\[
a_{\ell+1}\le R_1a_\ell+F_1
\tag{5}
\]

and

\[
b_{\ell+1}\le b_\ell+R_2a_\ell+F_2.
\tag{6}
\]

For \(R_1\ne1\), (5) yields

\[
a_\ell\le R_1^\ell a_0+F_1\frac{R_1^\ell-1}{R_1-1}.
\tag{7}
\]

Substitution into (6) gives

\[
b_\ell\le b_0+R_2\sum_{j=0}^{\ell-1}a_j+\ell F_2.
\tag{8}
\]

Thus, under a direct repeated application of the one-hop mechanism, the **standard conservative correctness bound grows geometrically in the update depth whenever \(R_1>1\)**.

This is a bound on the naive composition, not an impossibility theorem. A tighter distributional analysis, a refresh mechanism, or a different update construction may substantially change the conclusion.

## 5. Relation to the published one-hop bounds

Cini et al. bound the relevant token norms by

\[
\|\Delta_1\|\le 2m\rho,
\qquad
\|\Delta_2\|\le \sqrt{2}\,m\rho,
\]

under their Gaussian/trapdoor parameter requirements, and additionally bound the functional-key matrix norm by \(2m\rho_2\).

Their one-hop correctness theorem selects \(q\), \(\rho\), \(\rho_2\), \(\sigma\), \(\mu\), and \(\tau\) so that the **single updated-ciphertext** decryption error stays below the decoding threshold.

These published inequalities cannot simply be reused for depth \(L>1\), because after the first hop the error entering the next update is already the transformed error of (3), rather than a fresh-encryption error distributed as in the one-hop proof.

## 6. Main feasibility question

The bounded construction is useful only if we can produce a depth-dependent parameterization satisfying simultaneously:

1. LWE/trapdoor hardness requirements;
2. statistical-smudging requirements used by the security proof;
3. functional-key distribution requirements;
4. correct decryption after the maximum path length \(L\);
5. ciphertext/token/key sizes and computation acceptable for the intended distributed FGCS setting.

A formal correctness target is

\[
\operatorname{Err}(L)<\frac{q}{2K}
\]

for the exact decryption error expression of the generalized scheme, not merely for \(a_L\) or \(b_L\) separately.

## 7. GO/NO-GO gate

### GO for a practical bounded-LWE instantiation

Proceed if all of the following can be established:

- a closed depth-\(L\) correctness bound;
- a concrete parameter search giving credible settings for at least several nontrivial depths (target study points: \(L=1,2,4,8\), extending further only if feasible);
- no update-token functional-key switching attack;
- a security reduction whose loss and oracle restrictions remain scientifically defensible;
- measured implementation costs compatible with the intended FGCS system study.

### NO-GO for the naive bounded-LWE instantiation

Abandon direct repeated composition if:

- the required modulus/noise parameters become impractical at very small depth;
- the proof requires restrictions that make the multi-hop claim vacuous;
- key non-transferability cannot be proved;
- token/ciphertext growth defeats the intended systems use case.

A NO-GO result does **not** invalidate CAMH-CUFE as a model. It means the concrete instantiation must switch to a refreshed/re-randomized lattice design, a construction inspired by newer ciphertext-updatable ABE/PE techniques, or a theoretical generic construction while retaining a smaller practical instantiation.

## 8. Immediate proof obligations

1. Derive the exact level-indexed decryption equation and full error term.
2. Bound the products of the structured matrices \(\Delta_{1,0}\cdots\Delta_{1,L-1}\), exploiting their block structure rather than relying only on generic spectral-norm multiplication.
3. Determine whether the one-hop `NoiseGen`/smudging mechanism can be generalized to re-randomize accumulated error at every level without breaking correctness or security.
4. Define and prove functional-key non-transferability for the candidate matrices.
5. Compare the construction technically with Schädlich et al. (SCN 2026) before claiming that this is the appropriate lattice route.

## 9. Claim policy

Until these obligations close, the manuscript may say only that a **bounded multi-level LWE construction is under investigation**. It must not state that Cini's practical scheme composes across multiple updates.
