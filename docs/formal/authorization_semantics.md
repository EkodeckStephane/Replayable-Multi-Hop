# CAMH-CUFE Transition-Authorization Semantics

## 1. Why this distinction matters

A CUFE update token is naturally a **state-transition authorization**, not a one-time capability bound to one ciphertext instance.

For a source state

```text
s = (tag, epoch)
```

and destination state

```text
s' = (tag', epoch + 1),
```

an authority-issued token

```text
Delta_(s -> s')
```

is intended to authorize the corresponding transformation for **any otherwise valid ciphertext currently in source state `s`**, unless an application explicitly selects a stricter ciphertext-specific policy.

This preserves the semantics of tag-based CUFE, where update tokens are generated from authorization tags/states rather than from individual ciphertext identifiers.

## 2. Default CAMH-CUFE policy: state-global tokens

The baseline CAMH-CUFE model adopts **state-global transition tokens**.

### Allowed

The same valid token may be used on two different valid ciphertexts:

```text
C_s      --Delta_(s->s')--> C_s'
Cbar_s   --Delta_(s->s')--> Cbar_s'
```

This is not a replay attack.

### Rejected

The token must not be accepted when:

- the current ciphertext tag differs from the token source tag;
- the current epoch differs from the token source epoch;
- the token destination epoch is not the prescribed successor epoch;
- the token is reapplied to a ciphertext that has already advanced to `s'`;
- the signed token fields or update material are modified;
- a transcript claims that the token was used from a source state different from the actual preceding state.

## 3. Revised replay definition

**Stale-state replay** is the acceptance of a valid previously issued transition token outside its signed source-state coordinates.

A token's previous use elsewhere does not make it stale. Staleness is defined relative to the ciphertext state on which it is being applied.

This distinction must be preserved in prose, experiments, and theorem statements.

## 4. Ciphertext lineage versus token scope

Although tokens are state-global, an **audit transcript is ciphertext-lineage specific**.

The retained history must bind:

- the accepted fresh ciphertext/root state;
- each predecessor ciphertext state;
- each resulting ciphertext state;
- the token used at that hop;
- transition order;
- the rolling history commitment.

This prevents an auditor from treating an unrelated valid ciphertext history as evidence for the displayed final ciphertext.

It does **not** prevent a legitimately state-global token from being applied to another valid ciphertext in the same source state.

## 5. Splicing semantics

A cross-history splice attack should therefore be defined as:

> constructing a retained history for a displayed ciphertext by combining records from different ciphertext lineages such that the resulting history is accepted even though sequential replay from the claimed fresh root does not yield the displayed path/final state.

The security mechanism is coordinate/state continuity plus history commitment and transition verification, **not ciphertext-specific token issuance**.

## 6. Branches and reconvergence

State-global tokens permit different ciphertexts and different paths to share transition authorizations. The model must separately decide whether a *single ciphertext lineage* may branch.

Recommended baseline:

- a retained transcript describes one linear path;
- different valid paths can exist from a common prefix if the authority issues the corresponding state edges;
- path identity is carried by the history commitment, not by claiming that the underlying payload representation is necessarily path-dependent;
- when two paths reconverge on the same state, their history commitments must remain distinguishable even if the cryptographic payload coordinates coincide.

## 7. Optional stricter profile

A future application profile may bind a token to a ciphertext/lineage identifier:

```text
Delta_(lineage_id, s -> s')
```

Such a profile changes authority semantics, token reuse, storage, privacy, and scalability. It must be treated as a distinct policy/construction, not silently assumed by the baseline security games.

## 8. Testing implications

The adversarial suite needs both positive and negative controls:

### Positive

- reuse one token on two different valid ciphertexts in the same source state: **accept**.

### Negative

- reuse that token after either ciphertext has advanced: **reject**;
- use it at the same tag but a different epoch: **reject**;
- splice the destination record from ciphertext A into ciphertext B's retained history: **reject unless replay from B's claimed root actually yields that record**, in which case the histories are not semantically distinct at that point and the game must use a stronger lineage-distinguishing input.

This test design prevents the implementation from “passing” an incorrect ciphertext-specific security property that the protocol never intended to provide.
