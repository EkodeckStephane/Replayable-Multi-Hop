# CAMH-CUFE oracle interfaces and leakage profile

## Status

**Baseline formal profile for the security reduction.** This document freezes the intended adversarial interface of the CAMH-CUFE model independently of any particular candidate construction. A concrete instantiation may expose *more* public information, but that additional leakage must be stated explicitly and the security claim must be narrowed accordingly.

This profile does not constitute a security theorem.

## 1. Authorization graph and lineage policy

A cryptographic authorization state is

\[
Q=(t,\ell),
\]

where `t` is a public tag and `l` is an authenticated level/epoch.

The baseline policy is:

1. every issued transition advances exactly one level,
   \[
   (t,\ell)\rightarrow(t',\ell+1);
   \]
2. the global authorization graph may branch;
3. cycles are excluded structurally by the strictly increasing level;
4. several incoming paths may reconverge on the same authorization state;
5. an individual retained history is a linear sequence from one fresh ciphertext root;
6. if a ciphertext is copied and updated along two authorized outgoing edges, the two resulting retained histories are distinct lineages/branches even when they later reconverge cryptographically;
7. update tokens are state-global, while history records are lineage-specific.

Visible-tag projection never creates authorization. Exact state-edge issuance determines reachability.

## 2. Public leakage baseline

CAMH-CUFE makes **no metadata-hiding claim** for the following values. They are treated as public leakage in the baseline games:

- security parameter and protocol/suite identifier;
- construction parameters and maximum supported depth;
- FE vector/functionality dimension and declared message/function domains;
- public authorization tags;
- public level/epoch values;
- the source and destination states of every publicly issued transition;
- public transition identifiers/digests and authenticated transition statements;
- public-key material required by the concrete construction;
- ciphertext, token, functional-key, proof, history-record, and checkpoint byte lengths;
- the number of retained transitions in a disclosed history;
- the rolling history commitment/digest;
- public lineage/branch identifiers if the selected audit encoding exposes them;
- checkpoint issuer/quorum identifiers, policy identifier, certified final state, history length, and application context when present;
- timing, network endpoint, and access-pattern leakage inherent in the evaluated distributed deployment unless a separate traffic-analysis defense is defined.

Consequently, the paper must not claim hidden update depth, hidden transition graph, hidden access pattern, or anonymous audit participation under this baseline profile.

## 3. Scheme-level adversarial oracles

Let `A` be a PPT adversary. The following interfaces define the baseline adaptive experiment.

### `O_Enc(x,t)`

Returns an honest fresh encryption in state

\[
Q=(t,0).
\]

The adversary may request chosen-message encryptions outside the challenge instance.

### `O_Key(f,Q)`

Returns a functional key for function `f` at exact authorization state `Q`, subject only to the challenge-admissibility rule in Section 5.

A query at a state that is *not* a legitimate challenge-decryption state is intentionally allowed even when public transition tokens touch that state. This is necessary for the game to detect functional-key switching attacks rather than excluding them by definition.

### `O_Tok(Q,Q')`

For a policy-authorized exact edge with

\[
Q'=(t',\ell+1)
\]

when `Q=(t,l)`, returns the update token and its authenticated public statement in the **public-token** game.

A request for an edge outside the authority policy returns `bottom`.

### `O_Update(C,Delta)`

Runs the honest update algorithm. In the public-token game this oracle is convenience only because the adversary already receives `Delta`. It remains useful for defining a token-hidden comparison profile.

### `O_VerifyTransition`, `O_VerifyHistory`

Expose the public verification algorithms exactly as deployed. They do not receive hidden correctness advice.

### `O_Certify`

If checkpoint certification is in scope, returns a certificate only for a state/history pair that the modeled honest auditor accepts and only under the declared checkpoint trust policy. The certificate may reveal all metadata listed in Section 2.

Checkpoint access is not a decryption oracle.

## 4. Public-token and honest-update profiles

Two token-exposure profiles are named explicitly.

### `MH-PUB`

The adversary receives the concrete update token/program for every successful `O_Tok` query and may execute or combine those tokens arbitrarily.

This is the **required baseline for any paper claim that update material is publicly transferable or distributed to untrusted proxies**.

### `MH-HU`

The adversary learns the authenticated transition description but interacts with challenge-path updates only through an honest update oracle; the secret update material is not exposed.

`MH-HU` is a strictly different deployment model and must not be reported as evidence for `MH-PUB` security.

## 5. Challenge admissibility

The adversary selects equal-domain challenge vectors/messages `x0,x1` and an initial public tag `t*`. The challenger returns

\[
C^*\leftarrow Enc(mpk,x_b,t^*)
\]

for hidden bit `b`.

The adversary may then copy and evolve challenge-derived ciphertexts along any exact transition edges authorized by the experiment. This permits a challenge-derived DAG even though each retained history remains linear.

Let `D*` be the set of exact authorization states at which the adversary obtains a valid challenge-derived ciphertext during the complete experiment.

The transcript is **admissible** iff for every functional-key query

\[
O_{Key}(f,Q)
\]

with `Q` in `D*`,

\[
f(x_0)=f(x_1).
\]

This condition is evaluated over the final adaptive transcript. Therefore a later challenge update that brings a previously queried key state into `D*` can make the transcript inadmissible.

No equality restriction is imposed merely because a queried key state has an incoming or outgoing public transition relation with a challenge state. If the concrete algebra lets such a key and public token synthesize forbidden challenge-state capability, that is a security failure rather than an excluded query.

## 6. Composition authorization inside the challenge experiment

A challenge-derived update is legitimate only when all of the following hold:

1. the input challenge ciphertext is in exact source state `Q`;
2. an exact edge `Q -> Q'` was issued by the authority/policy;
3. the concrete cryptographic update mechanism accepts only that exact source state;
4. the output is cryptographically bound to exact destination state `Q'`.

The existence of

```text
(A,0) -> (B,1)
(B,0) -> (C,1)
```

must not authorize a second challenge update from `(B,1)`.

A proof of confidentiality cannot replace this requirement with an API-only comparison of metadata fields.

## 7. Multi-hop confidentiality experiment

For profile `X` in `{MH-PUB, MH-HU}`, define

\[
Adv^{mh-ind-X}_{CAMH-CUFE,A}(\lambda)
 = |Pr[b'=b]-1/2|.
\]

A construction is secure for the stated profile, depth bound, functionality family, and query bounds only if every PPT admissible adversary has negligible advantage.

The theorem statement must quantify:

- maximum supported level/depth `L`;
- number of encryption, functional-key, token/update, verification, and checkpoint queries;
- whether challenge tags and transition graph choices are adaptive, selective, or semi-adaptive;
- any corruption model for authority, proxy, or checkpoint entities;
- every construction-specific leakage item beyond Section 2;
- reduction loss as a function of these quantities.

## 8. Sequential composition requirement

Confidentiality after a single update is insufficient. For every challenge-derived state reached after an admissible prefix, the next explicitly authorized update must preserve the same indistinguishability guarantee under the adversary's entire accumulated view.

The proof must therefore cover:

- exposed prior ciphertexts and update outputs;
- all public transition material permitted by the profile;
- functional keys previously queried at other states;
- multiple authorized outgoing edges when branching is allowed;
- repeated visible tag names at distinct levels;
- reconvergent authorization states;
- the public audit/history metadata produced along each retained branch.

## 9. Key non-transferability is embedded, not assumed

The confidentiality game deliberately allows combinations such as:

```text
sk_(f,Qpre) + public Delta_(Qpre -> Qchallenge)
```

when `Qpre` itself is not a challenge-derived decryption state.

A secure construction must prevent this material from yielding an otherwise forbidden functional capability on challenge-derived ciphertexts. The legacy pairing construction fails precisely this requirement and is therefore excluded from CAMH-CUFE confidentiality claims.

## 10. Audit-integrity separation

`MH-PUB` / `MH-HU` protect message/function confidentiality under the declared FE semantics. They do not by themselves prove that a claimed retained history is authentic.

Replay, rollback, skip, reorder, splice, fork consistency, history binding, and checkpoint forgery/state binding remain separate games in `security_games.md`.

This separation is intentional: a construction may preserve confidentiality while an audit transcript is forgeable, or preserve audit integrity while the underlying update algebra leaks forbidden functional capability.

## 11. Construction gate

Before a concrete security theorem is authorized, the candidate construction must state whether it realizes `MH-PUB` or only `MH-HU` and must prove cryptographic binding to `(tag,level)`.

For the intended untrusted-proxy distributed setting, a practical headline claim requires `MH-PUB` unless the system architecture genuinely keeps update material secret from the proxies and this is reflected consistently in the threat model and measurements.
