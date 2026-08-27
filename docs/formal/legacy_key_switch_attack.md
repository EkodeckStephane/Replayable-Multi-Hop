# Confirmed key-switch attack on the legacy pairing construction

## Status

**Confirmed negative result.** The legacy pairing construction must not be used to support a CUFE confidentiality claim.

This document records a cryptographic counterexample found while refactoring the original prototype into CAMH-CUFE. It is retained as a design boundary and regression target, not as manuscript audit narrative.

## Legacy algebra

For function vector `v = (v_1,...,v_n)`, define

\[
S=\sum_i v_i U_i.
\]

At public state `s`, the unmasked functional-key group element is

\[
[K_s]_2=[h_s A^{-T}S]_2.
\]

A public transition token from state `s` to state `s'` contains, for every coordinate `i`,

\[
D_i=[(h_{s'}-h_s)A^{-T}U_i]_2.
\]

A holder of a functional key necessarily knows the queried function vector `v`. Using public group operations only, the holder can compute

\[
\begin{aligned}
[K_s]_2+\sum_i v_iD_i
&=[h_sA^{-T}S]_2+[(h_{s'}-h_s)A^{-T}\sum_i v_iU_i]_2\\
&=[h_{s'}A^{-T}S]_2\\
&=[K_{s'}]_2.
\end{aligned}
\]

No discrete logarithm, master secret, tag hash, or signing key is required.

## Multi-hop extension

For a valid path

\[
s_0\rightarrow s_1\rightarrow\cdots\rightarrow s_k,
\]

with public tokens `D_i^(j)` for hop `j`, an old-key holder can derive

\[
[K_{s_k}]_2=[K_{s_0}]_2+\sum_{j=0}^{k-1}\sum_i v_iD_i^{(j)}.
\]

The masks telescope exactly. Therefore the failure persists for arbitrary path length.

## Reproduction against the supplied implementation

Using the supplied `ToyGroup` implementation with

- plaintext `x=(7,4,2)`,
- function vector `v=(2,3,5)`,
- source state `A, level 1`, and
- target state `B, level 2`,

the following were observed:

1. the group element derived from the source functional key and the public update token is exactly equal to the authority-issued target-state functional-key group element;
2. manual decryption of the updated ciphertext with the derived target key returns `36`;
3. `36 = <x,v>`;
4. the official API returns `None` when passed the old signed source key only because it checks signed tag/level metadata.

The signature check therefore enforces API discipline but does not repair the cryptographic key-switch relation: an adversary can perform the pairing/group computation directly.

## Relation to the CUFE security objective

Cini et al., *(Inner-Product) Functional Encryption with Updatable Ciphertexts*, explicitly identify as a security concern that update tokens might be usable to **switch function keys**. Their CUFE security framework is designed to prevent update tokens from acquiring unintended functionality beyond authorized ciphertext transformation.

Accordingly, the legacy pairing construction cannot be presented as an IND-CUFE-CPA-secure instantiation.

## Design consequence for CAMH-CUFE

The new construction must satisfy a **key non-transferability across state transitions** property:

> Given public transition material for an authorized state update, possession of a functional key for state `s` must not enable deriving a functional key, equivalent decryption capability, or a useful surrogate for state `s'`, except to the extent explicitly allowed by the security game.

This property must be tested before sequential composability is claimed.

## Manuscript policy

The old pairing backend may remain useful for:

- executable correctness checks;
- transcript/audit mechanics;
- performance diagnostics clearly labeled as legacy/symbolic.

It must not provide headline confidentiality or CUFE-security evidence.
