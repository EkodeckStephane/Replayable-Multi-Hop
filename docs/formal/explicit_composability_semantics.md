# Explicit (opt-in) composability semantics for CAMH-CUFE

## Status

**Core model property.** This document formalizes why CAMH-CUFE refines a visible tag into a level-aware cryptographic state rather than allowing tag-only update tokens to compose transitively.

## 1. Motivation from one-update CUFE

Cini et al. deliberately restrict their CUFE model to one update. Their motivating concern is that if a ciphertext can move from `t` to `t'` and then from `t'` to `t''`, a ciphertext originally under `t` may acquire reachability to `t''` even when the authority intended the second transition only for ciphertexts that belong to the `t'` class in its original context.

CAMH-CUFE treats this as an **authorization-semantics problem**, not merely as an implementation limitation.

## 2. Level-aware state

A CAMH-CUFE state is

\[
S=(t,\ell),
\]

where:

- `t` is the visible access-control tag/domain; and
- `l` is a monotone update level/epoch that is part of the cryptographically authenticated transition state.

The same visible tag at two levels denotes distinct transition states:

\[
(t,0)\ne(t,1).
\]

A functional key and an update transition are defined against the relevant state semantics of the concrete construction.

## 3. Opt-in composition

Consider two independently authorized one-hop transitions:

\[
(A,0)\rightarrow(B,1)
\]

and

\[
(B,0)\rightarrow(C,1).
\]

They do **not** compose, because the first transition outputs state `(B,1)` whereas the second accepts only `(B,0)`.

Therefore an adversary cannot infer the path

\[
(A,0)\rightarrow(B,1)\rightarrow C
\]

merely from the existence of a token whose visible source tag is also `B`.

To authorize the second hop of that path, the authority must explicitly issue

\[
(B,1)\rightarrow(C,2).
\]

Composition is therefore **opt-in at the state level**.

## 4. No automatic transitive closure of tag-only policy

Let `E` be the set of issued state transitions. Define authorized reachability only by exact state matching:

\[
S_0\leadsto S_k
\]

iff there exists

\[
S_0\to S_1\to\cdots\to S_k
\]

with every exact edge in `E` and every destination state equal to the next edge's exact source state.

Projecting states down to visible tags can create a misleading graph. In general,

\[
\pi_t(S_i)=\pi_t(S_j)
\]

does not imply

\[
S_i=S_j.
\]

Hence **tag equality alone is insufficient to authorize composition**.

## 5. Security property: composition authorization

### G-CompositionAuthorization

The challenger issues a set of valid state-global update tokens for explicitly authorized state edges.

The adversary wins if it transforms a valid challenge ciphertext along a path containing a step

\[
S\rightarrow S'
\]

for which no compatible state edge was authorized, even if the visible source/destination tag names match tags appearing in other authorized tokens.

The game must include at least:

1. same visible tag, wrong source level;
2. same visible tag, wrong destination level;
3. attempted composition of `(A,0)->(B,1)` with `(B,0)->(C,1)`;
4. stale-token reuse after advancement;
5. legitimate explicitly enabled composition `(A,0)->(B,1)->(C,2)`.

## 6. Distinction from history audit

Composition authorization and history audit are related but distinct.

- The **cryptographic state** determines whether a transition token is applicable.
- The **history layer** proves which sequence of accepted transitions produced a particular lineage.

A state-global token may update many ciphertexts in the same exact source state. The history commitment remains ciphertext-lineage-specific.

## 7. Relationship to replay and rollback

The monotone level has three roles:

1. prevents a tag-only token from automatically composing with an updated state;
2. makes stale-token application detectable at the cryptographic state boundary;
3. gives the audit layer an unambiguous monotone coordinate for replay/rollback reasoning.

These roles should not be collapsed into a generic statement that 'the level prevents replay'. The central semantics is **explicit authorization of composition**.

## 8. Why this matters to CAMH-CUFE novelty

The model should not sell `level` as an engineering counter. Its scientific role is to transform the unsafe tag-only transitive composition identified in one-update CUFE motivation into an explicit state-transition authorization model.

The candidate contribution is therefore:

> repeated CUFE updates are permitted only through exact level-aware state edges, so multi-hop reachability is explicitly authorized rather than inherited from equality of intermediate tag names.

This statement still requires SOTA comparison against multi-hop ciphertext-updatable ABE/PE and other stateful update models. It is not a priority claim.

## 9. Consequence for construction design

Every retained construction must cryptographically enforce the source level, rather than append an unauthenticated metadata field checked only by the API.

If removing or changing the level field while leaving the cryptographic payload unchanged lets the same update token operate successfully, then the construction does not realize this model property.

## 10. Experimental regression cases

The implementation must demonstrate both rejection and acceptance cases:

```text
ALLOW: token (A,0)->(B,1) on multiple ciphertexts genuinely in (A,0)
REJECT: token (B,0)->(C,1) on a ciphertext in (B,1)
ALLOW: explicit token (B,1)->(C,2) on a ciphertext in (B,1)
REJECT: stale token (A,0)->(B,1) after the ciphertext has advanced
REJECT: tampered source/destination level in an authenticated transition statement
```

These tests support implementation conformance; the cryptographic theorem must establish the corresponding state-binding property.
