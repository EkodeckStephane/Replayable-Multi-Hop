# Public-token surrogate-key criterion for the multi-level LWE candidate

## Status

**Conditional algebraic attack criterion.** This result is derived from the candidate matrix equations already used by the multi-level LWE track. It is not a claim that every Cini-style CUFE construction is broken, nor that the published one-hop construction satisfies the attack conditions below.

Its role is to provide an early **NO-GO test** for any proposed repeated-update instantiation under the intended `MH-PUB` threat model.

## 1. Candidate equations

For authorization state/level `l`, let

\[
H_l Z_l=D_l \pmod q.
\tag{1}
\]

For a function vector `y`, the source functional-key capability contains the short preimage

\[
k_l(y)=Z_l y.
\tag{2}
\]

A public transition token from level `l` to `l+1` contains matrices satisfying

\[
H_l\Delta_{1,l}=H_{l+1}\pmod q
\tag{3}
\]

and

\[
H_l\Delta_{2,l}=D_{l+1}-D_l\pmod q.
\tag{4}
\]

These are precisely the structural equations used by the direct bounded multi-level generalization.

## 2. Lemma — source key plus public `Delta_2` gives a target-image preimage

Define

\[
w_l(y)=k_l(y)+\Delta_{2,l}y.
\tag{5}
\]

Then

\[
\begin{aligned}
H_l w_l(y)
&=H_lZ_ly+H_l\Delta_{2,l}y\\
&=D_ly+(D_{l+1}-D_l)y\\
&=D_{l+1}y\pmod q.
\end{aligned}
\tag{6}
\]

Therefore a holder of a source functional key and the public transition token can compute a preimage of the **target key image** under the source matrix `H_l` without the master secret.

This fact alone is not yet a target-state key-switch attack, because target decryption is defined against `H_{l+1}`.

## 3. Theorem — public solvability through `Delta_1` yields a surrogate target key

Assume there exists an efficient public algorithm

\[
\mathsf{Solve}_{\Delta_1}(w)\to z
\]

such that, for the attacker-computable value `w_l(y)`,

\[
\Delta_{1,l} z=w_l(y)\pmod q.
\tag{7}
\]

Then the resulting

\[
k^*_{l+1}(y):=z
\tag{8}
\]

satisfies the target key equation

\[
H_{l+1}k^*_{l+1}(y)=D_{l+1}y\pmod q.
\tag{9}
\]

### Proof

Using (3), (7), and (6),

\[
\begin{aligned}
H_{l+1}k^*_{l+1}(y)
&=H_l\Delta_{1,l}z\\
&=H_lw_l(y)\\
&=D_{l+1}y\pmod q.
\end{aligned}
\]

This proves (9). ∎

### Invertible special case

If `Delta_{1,l}` is invertible over `Z_q`, the public solver is immediate:

\[
k^*_{l+1}(y)
=\Delta_{1,l}^{-1}
   (Z_ly+\Delta_{2,l}y).
\tag{10}
\]

More generally, full invertibility is unnecessary. Any efficient public method that finds a sufficiently useful solution of (7) is enough for the attack criterion.

## 4. Capability condition

Equation (9) establishes an algebraically valid target preimage. CAMH-CUFE's key-non-transferability game is broken only if this preimage is also a **usable target decryption capability**.

For an independently generated target ciphertext

\[
c_{1,l+1}=H_{l+1}^Ts+E_1
\]

and

\[
c_{2,l+1}=D_{l+1}^Ts+E_2+Mx,
\]

the attacker can evaluate

\[
\begin{aligned}
y^Tc_{2,l+1}
-(k^*_{l+1}(y))^Tc_{1,l+1}
= M\langle x,y\rangle
+y^TE_2
-(k^*_{l+1}(y))^TE_1.
\end{aligned}
\tag{11}
\]

Thus the surrogate succeeds whenever the resulting error lies inside the same decoding interval used by the functional-decryption algorithm.

A conservative sufficient condition is of the form

\[
\|y\|_2\|E_2\|_2
+\|k^*_{l+1}(y)\|_2\|E_1\|_2
< \mathsf{DecodeRadius},
\tag{12}
\]

with the exact norm/error expression replaced by the concrete construction's actual correctness bound.

## 5. Security consequence

Under the intended `MH-PUB` profile, the adversary may possess:

- a permitted source-state functional key for `y`;
- the public transition material `Delta_1, Delta_2`;
- independently generated ciphertexts in the destination state.

If (7) can be solved efficiently and the resulting `k^*` satisfies the target decryption bound, then the scheme fails `G-KeyNonTransferability`: the adversary obtains target-state functional capability without `KeyGen(msk,y,Q_{l+1})`.

An API-level signature, state label, or key-object metadata check does not repair this failure, because the attacker can evaluate equation (11) directly.

## 6. Relation to the transition residual

Recall

\[
R_l=Z_l+\Delta_{2,l}-\Delta_{1,l}Z_{l+1}.
\tag{13}
\]

For function vector `y`,

\[
w_l(y)=\Delta_{1,l}Z_{l+1}y+R_ly.
\tag{14}
\]

If `Delta_1` is invertible,

\[
k^*_{l+1}(y)
=Z_{l+1}y+\Delta_{1,l}^{-1}R_ly.
\tag{15}
\]

This equation makes the correctness/security coupling explicit:

- if `R_l=0`, public transition material switches the target preimage **exactly**;
- if `R_l` is very small after inversion, the attacker obtains a nearby surrogate key that may still decrypt;
- making the residual large enough to destroy the surrogate may also increase the inherited decryption-error term identified in `lwe_key_noise_coupling.md`.

Therefore the residual cannot be tuned only for correctness. Its distribution and the conditioning/solvability of `Delta_1` are security-critical.

## 7. Required NO-GO experiment for any concrete LWE candidate

Before a proposed LWE backend is accepted, the implementation must measure or derive, for every tested depth/parameter set:

1. rank and public solvability properties of `Delta_1` modulo `q`;
2. whether equation (7) can be solved efficiently for attacker-generated `w_l(y)`;
3. centered norm of the resulting surrogate `k^*`;
4. target decryption error using `k^*` on **independent target-state ciphertexts**;
5. empirical success/failure of unauthorized target functional decoding;
6. comparison against the exact theoretical decryption radius.

The attack experiment is a falsification test. A failure to obtain a surrogate in sampled trials is not a proof of key non-transferability.

## 8. Hard decision rule

### Immediate NO-GO

Reject a candidate for `MH-PUB` if an efficient public solver produces a surrogate satisfying the target decoding bound with non-negligible probability.

### Still OPEN

If the surrogate is too long/noisy, security is **not automatically established**. A reduction must still show that no different public algorithm derives target functional capability.

### Design response

If the criterion repeatedly fires, do not patch the API. Change the cryptographic transition design, for example by:

- avoiding publicly solvable key-image transport through `Delta_1`;
- using refreshed/re-randomized ciphertext-update techniques whose public token does not induce a short target preimage;
- adopting a construction with a proof that explicitly covers public-token exposure and key non-transferability.

## 9. Scientific interpretation

This criterion is a useful negative structural result because it turns the vague requirement “update tokens must not switch keys” into a concrete algebraic falsification condition for the direct multi-level LWE architecture.

It does **not** authorize any novelty/priority statement. Its value for the paper depends on whether the retained construction analysis and SOTA review show that the criterion materially explains the design boundary of multi-hop tag-changing CUFE.
