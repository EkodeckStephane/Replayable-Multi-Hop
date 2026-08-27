# CAMH-CUFE system and threat model

## Status

**Baseline distributed threat model.** Construction-specific proofs may impose additional restrictions, but any such restriction must be surfaced explicitly rather than silently weakening this model.

The intended FGCS deployment uses the public-token profile `MH-PUB`: update proxies may possess the concrete update material for authorized transitions.

## 1. Roles

### Policy / key authority `A`

- runs setup;
- authenticates the protocol suite and public parameters;
- issues functional keys according to policy;
- issues/authenticates exact state-global transition tokens for authorized edges;
- defines the authoritative transition graph.

### Data owner / encryptor `O`

- supplies plaintext/vector input;
- creates the accepted fresh ciphertext root in state `(tag,0)`;
- initializes lineage/audit context.

`A` and `O` may be colocated in a deployment but remain logically distinct in the model.

### Update proxies `P_1,...,P_m`

- receive public/authenticated update material for specific exact state edges;
- apply authorized ciphertext transitions;
- may be independent processes/hosts;
- are **not trusted for confidentiality, ordering, provenance, or honest execution** in the baseline model.

### Full-history verifier / auditor `V_H`

- starts from an accepted fresh root;
- independently validates exact authorization edges, token authentication, concrete transition uses, ciphertext/state continuity, and the rolling history commitment.

### Checkpoint issuer `A_CP`

- performs a full history audit;
- if successful, signs a canonical checkpoint statement under an explicit trust policy.

The baseline checkpoint profile assumes `A_CP` is honest with respect to performing the audit. A checkpoint verifier relies on this assumption for omitted hops.

### Checkpoint verifier `V_CP`

- verifies the accepted checkpoint authority/policy and exact signed final-state statement;
- does not replay omitted transitions.

### Functional consumer `U_f`

- receives one or more functional keys for authorized functions/states;
- obtains only the corresponding functional outputs when the construction security conditions hold.

## 2. Adversary capabilities

The baseline adversary may:

- observe all public parameters, tags, levels, public transition descriptions, history/checkpoint metadata, and wire lengths listed in `oracle_and_leakage_profile.md`;
- obtain public update tokens/programs for policy-authorized edges (`MH-PUB`);
- control one or more update proxies;
- copy a challenge-derived ciphertext and send branches through different authorized proxies/edges;
- delay, drop, replay, reorder, duplicate, replace, or splice network messages and retained records;
- apply valid state-global tokens to multiple ciphertexts genuinely in the exact source state;
- submit malformed/non-canonical protocol encodings;
- query encryption and permitted functional-key interfaces adaptively under the challenge-admissibility rule;
- combine public transition material with functional keys it legitimately obtained;
- attempt rollback to archived states;
- attempt false final-state, false-history, or false checkpoint claims;
- observe execution timing and network endpoints in the evaluated deployment unless a separate traffic-analysis defense is introduced.

The game intentionally does not remove source-state functional-key queries merely because a public token touches a challenge state. A resulting key-switch capability is a construction failure.

## 3. Honest/trusted components in the baseline

### Authority honesty

The baseline confidentiality and authorization claims assume that the policy/key authority:

- protects the master secret;
- generates keys/tokens according to the declared algorithms;
- authenticates the exact transition edges it intends to authorize.

If the authority maliciously issues an edge, key, or token, CAMH-CUFE cannot reinterpret that deliberately authorized capability as an external forgery.

Authority compromise and post-compromise recovery are separate extensions unless a retained construction explicitly proves them.

### Fresh-root acceptance

A full-history verifier must possess or authenticate an accepted fresh root `(Q_0,C_0)`. The history mechanism prevents mutation of a retained lineage relative to that root; it does not solve the bootstrapping problem of deciding which root is trusted.

### Single checkpoint issuer

For checkpoint mode only, the baseline assumes the configured issuer performs the required audit honestly. Third-party signature forgery remains a cryptographic threat; deliberate issuer equivocation/false certification requires an optional transparency/quorum/accountability profile.

## 4. Security goals

### Confidentiality / FE semantics

- multi-hop FE indistinguishability under `MH-PUB` for the retained construction;
- functional-key non-transferability under public transition material;
- intended functional output preserved after every valid authorized prefix.

### Authorization

- exact `(tag,level)` source/destination binding;
- no composition inferred from visible-tag equality;
- only explicitly issued exact edges contribute to reachability;
- stale token use against an advanced/wrong-level ciphertext rejected.

### Audit integrity

- retained path starts from the accepted root;
- every retained destination is a valid concrete transition result;
- skip/reorder/false-splice manipulations do not validate as the original lineage;
- rolling history commitment binds the retained evidence under the stated hash/encoding assumptions;
- displayed final state/ciphertext/digest must equal independently replayed output.

### Checkpoint authenticity

- certificate binds exact final state, ciphertext, history digest, history length, trust policy, and application context;
- untrusted third parties cannot forge the checkpoint under the selected signature assumption;
- verification semantics remain explicitly weaker/different from independent history replay with respect to omitted hops.

## 5. Out-of-scope baseline threats

Unless separately implemented and measured, the baseline makes no claim for:

- denial of service, message suppression, or guaranteed progress;
- traffic-analysis resistance or hiding path length/timing;
- side-channel, microarchitectural, power, cache, or fault-injection resistance at primitive implementation level;
- endpoint compromise that reads plaintext before encryption or authorized functional output after decryption;
- malicious setup by the master authority;
- recovery after master-secret compromise;
- anonymity of proxies/auditors/users;
- malicious checkpoint-issuer accountability in the single-issuer profile;
- succinct cryptographic proof of omitted history merely from a checkpoint signature.

These exclusions are validity boundaries, not implementation defects to hide in prose.

## 6. Network model

For headline distributed experiments:

- roles execute in separate processes, and the main distributed evidence must use non-loopback communication;
- channel authentication/confidentiality such as TLS protects transport endpoints where appropriate;
- protocol-level signatures/statements remain necessary because a retained audit transcript must be verifiable independently of the live TLS session;
- a network attacker may schedule/drop/replay packets even when unable to forge the transport endpoints.

Local loopback runs remain development/conformance evidence only.

## 7. Corruption profiles to report

At minimum the experimental/security table should distinguish:

| Profile | Authority | Update proxies | Checkpoint issuer | Functional consumers | Intended evidence |
|---|---|---|---|---|---|
| `P0` | honest | honest | honest | honest | correctness/performance control |
| `P1` | honest | malicious/untrusted | honest | admissibly corrupted/querying | primary `MH-PUB` + path-integrity target |
| `P2` | honest | malicious/untrusted | not trusted/unused | admissibly corrupted/querying | full-history mode without checkpoint trust |
| `P3` | honest | malicious/untrusted | honest | admissibly corrupted/querying | checkpoint mode, explicit issuer trust |

A malicious authority profile is not a baseline confidentiality claim and must be labeled as a different research extension.

## 8. Experimental consequences

The adversarial campaign must map each injected fault to a defined threat/security class. In particular:

- token reuse on a second valid ciphertext in the same exact source state is a **positive control**, not an attack;
- same visible tag at the wrong level is a rejection case;
- an arbitrary destination ciphertext wrapped in a freshly recomputed public history digest is a rejection case unless the concrete transition-use verifier establishes it as a legitimate update;
- branch/reconvergence tests must compare lineage commitments separately from payload equality;
- checkpoint verification timings cannot be interpreted as independent verification of omitted hops.
