# Generic multi-level iO candidate for CAMH-CUFE

## Status

**Theoretical construction candidate — correctness sketch only; security proof OPEN.**

This candidate generalizes the architecture of Cini et al.'s generic iO-based one-update CUFE construction. It is intended as a possible **feasibility construction** for the CAMH-CUFE model, not as the practical FGCS implementation.

Generic updatable cryptography and Updatable Functional Encryption predate CAMH-CUFE. Therefore the scientific value of this candidate, if proved, is to instantiate the **specific CAMH-CUFE tag/state and security model**, not to claim that iO-based repeated updates are new.

## 1. Design intuition

The one-hop generic CUFE construction separates fresh and updated ciphertext domains using two puncturable-PRF secrets. An obfuscated update program decrypts an input ciphertext from the source domain and re-encrypts the same plaintext under the target domain/tag.

For bounded depth `L`, replace the two domains by

\[
k_0,k_1,\ldots,k_L,
\]

where `k_l` is a puncturable-PRF key for ciphertexts at level `l`.

A ciphertext carries an authenticated/plainly parseable public state marker

\[
S=(t,l).
\]

The level marker is intentionally public; CAMH-CUFE does not claim to hide the update depth unless a separate privacy extension is defined.

## 2. Candidate algorithms

### Setup

Sample independent puncturable-PRF keys

\[
k_0,\ldots,k_L.
\]

Create an obfuscated initialization program `PInit[k_0]` that, on fresh randomness `r`, outputs a public point `p` and a PTDE key derived from `k_0` and `p`.

The master secret contains the level PRF keys. The public key contains the obfuscated initialization program plus public protocol/audit parameters.

### Enc

To encrypt message `m` at initial tag `t_0`:

1. obtain `(p,k_ptde)` from `PInit` using fresh randomness;
2. compute a PTDE ciphertext under tag `t_0`;
3. output

\[
C_{(t_0,0)}=(t_0,0,p,c).
\]

### KeyGen

For function `f` and state `(t,l)`, output an obfuscation of

```text
PKey[k_l, f, t, l]
```

that accepts only a ciphertext encoded at exactly state `(t,l)`, derives the relevant PTDE key from `k_l` and the ciphertext point `p`, decrypts the payload, and returns `f(m)`.

A key for `(t,l)` is therefore not intended to decrypt `(t,l')` for `l' != l` even if the tag string is identical.

### TokGen

For an authorized transition

\[
(t,l)\rightarrow(t',l+1),
\]

return an obfuscation of

```text
PUpdate[k_l, k_{l+1}, t, l, t', l+1]
```

plus the authenticated public transition statement required by the audit layer.

### Update

The update program:

1. parses and requires exact source state `(t,l)`;
2. derives the source PTDE key from `k_l` and the source point;
3. decrypts the PTDE payload;
4. samples fresh target-domain randomness `r'` and derives a fresh target point `p'`;
5. derives the target PTDE key using `k_{l+1}` and `p'`;
6. re-encrypts the unchanged plaintext under target tag `t'`;
7. outputs

\[
C_{(t',l+1)}=(t',l+1,p',c').
\]

The program exposes neither `k_l` nor `k_{l+1}`.

### Dec

Run the state-specific obfuscated functional-key program on the ciphertext. A state mismatch returns `bottom`.

## 3. Functional correctness

For an honestly generated path

\[
(t_0,0)\rightarrow(t_1,1)\rightarrow\cdots\rightarrow(t_j,j),
\]

each update decrypts the current PTDE layer and re-encrypts the **same message** into the next level domain. Therefore, by induction on `j`, a compatible functional key for `(t_j,j)` returns `f(m)` assuming correctness of the underlying PTDE, PRF-derived key generation, and obfuscated programs.

This is only a correctness argument. It does not establish confidentiality or safe composition of exposed update/key programs.

## 4. Why the construction is attractive for feasibility

Unlike the direct lattice chaining candidate, an update does not algebraically multiply an inherited LWE error by a new transition matrix. It conceptually **refreshes the encryption representation** at every hop by decrypting and re-encrypting inside the obfuscated update program.

Therefore update depth does not create the same lattice-noise recurrence.

This benefit comes at the cost of strong assumptions and impractical obfuscation. Hence this candidate is not intended to supply the FGCS performance evidence.

## 5. Mandatory security questions

A proof must address at least:

1. **Source-state enforcement:** an update program for `(t,l)->(t',l+1)` cannot be used on a different level or tag.
2. **Forward-only behavior:** possession of the obfuscated update program does not enable reverse transformation or extraction of either level PRF key.
3. **Functional-key non-transferability:** combining `PKey[k_l,...]` with `PUpdate[k_l,k_{l+1},...]` does not yield forbidden target-state functional capability.
4. **Sequential exposure:** security still holds after the adversary sees a collection of adjacent update programs that share hidden level keys.
5. **Adaptive path selection:** the proof must state whether tags/paths are selected adaptively or semi-adaptively and quantify any guessing loss.
6. **Forks:** exposure of multiple outgoing or incoming update programs at a level must be modeled explicitly.
7. **Challenge-path tokens:** define which update programs touching challenge states may be corrupted/revealed without trivializing the game.
8. **Program composition:** iO hybrids must remain valid when the adversary can execute the obfuscated programs in arbitrary compositions, rather than only through the intended API sequence.

## 6. Hybrid-proof strategy under investigation

A plausible bounded-depth proof strategy is to hybridize one level/domain at a time:

\[
G_0\approx G_1\approx\cdots\approx G_L,
\]

puncturing the relevant PRF/PTDE challenge points and replacing challenge-dependent values level by level.

The security loss must remain polynomial for the permitted path/token-query structure. This cannot be assumed from the one-hop theorem because adjacent update programs share level keys and the adversarial view contains an entire transition graph.

A useful proof organization may index hybrids by the challenge-path DAG rather than only by hop number.

## 7. Relation to existing updatable-cryptography results

This candidate is not presented as a generic-updatability novelty:

- Arriaga–Iovino–Tang already define UFE with mutable encrypted memory and subsequent token execution.
- Ananth–Cohen–Jain give generic transformations toward updatable cryptographic primitives, including FE-related objects.
- Cini et al. give the direct one-update tag-based CUFE iO construction on which this design is structurally based.

The candidate matters only if it realizes the **new CAMH-CUFE security object**: repeated tag/state transitions with FE function-output semantics, functional-key non-transferability over update prefixes, and explicit path/audit semantics.

## 8. Interaction with auditing

Confidentiality/security of the iO construction and audit integrity are separated.

Each public transition token is associated with a canonical authenticated statement containing at least:

- protocol version/suite;
- source `(tag,level)`;
- destination `(tag,level)`;
- token/program identifier or digest;
- issuer/policy context.

A history link additionally binds the source and destination ciphertext identifiers/digests. This does not make the underlying state-global token ciphertext-specific.

## 9. GO/NO-GO criteria

### GO

Retain as the CAMH-CUFE **generic feasibility theorem** if:

- a complete bounded-depth correctness definition is satisfied;
- a multi-hop security reduction can be written without circular assumptions;
- key non-transferability follows from the proof rather than API discipline;
- proof loss is polynomial for the stated token/path query bounds;
- the distinction from prior UFE/generic update work remains meaningful.

### NO-GO

Do not retain if:

- the proof only restates Cryptography with Updates without a distinct CAMH-CUFE security result;
- adjacent obfuscated update programs make the desired key/token exposure unprovable;
- the restrictions required to prove security eliminate the relevant multi-hop behavior.

## 10. Manuscript role if successful

If proved, this construction should appear as the **generic theoretical instantiation** establishing feasibility of CAMH-CUFE. A separate lattice/IPFE construction, if feasible, supplies the concrete cryptographic and distributed-system evaluation.
