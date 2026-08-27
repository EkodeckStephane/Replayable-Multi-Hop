# CAMH-CUFE construction decision gate

## Status

**Decision document, not a security result.**

CAMH-CUFE now has a sufficiently precise model/audit layer that further systems work should be blocked until a cryptographic construction can realize the intended `MH-PUB` threat model. This document prevents the project from accumulating implementation/evaluation evidence around a construction that later fails the core key-security theorem.

## 1. Non-negotiable target

The intended FGCS architecture uses **untrusted update proxies with public/exposed update material** (`MH-PUB`). Therefore a retained headline construction must satisfy all of:

1. exact `(tag,level)` transition binding;
2. multi-hop functional correctness for the declared maximum depth;
3. functional-key non-transferability under public token exposure;
4. multi-hop confidentiality/sequential composition under the frozen challenge-admissibility rule;
5. a canonical real wire format and implementable security parameters;
6. enough performance to support a distributed-system evaluation without replacing the cryptographic backend by a symbolic oracle.

A construction that satisfies only correctness or only `MH-HU` is not equivalent to the intended deployment.

## 2. Candidate matrix

| Track | Correctness status | Key non-transferability | `MH-PUB` confidentiality | Practical backend | Current decision |
|---|---|---|---|---|---|
| legacy pairing prototype | sequential algebraic telescoping established | **FAIL**: explicit public-token key switching | disqualified | implemented legacy prototype | **REJECT for security claims** |
| direct bounded multi-level LWE generalization | recurrence/form derived; exact depth bound open | **HIGH-RISK OPEN**; public surrogate-key criterion now derived | open | no retained real implementation | **HOLD / falsify first** |
| bounded multi-level iO/PTDE/PRF candidate | correctness sketch by per-level refresh | open | open | impractical by design | **theoretical feasibility only** |
| refreshed/re-randomized lattice route inspired by recent CU-ABE/PE | not yet mapped to FE/CUFE | unknown | unknown | unknown | **INVESTIGATE** |

## 3. Legacy pairing track — definitive security NO-GO

The legacy pairing scheme remains useful for:

- regression of the update algebra;
- history/audit integration tests where confidentiality is not inferred;
- demonstrating why capability-based key non-transferability is necessary.

It is excluded from:

- CAMH-CUFE confidentiality theorems;
- secure distributed headline experiments;
- performance claims presented as costs of a secure CAMH-CUFE instantiation.

The failure is cryptographic, not an API defect: public token components linearly transform a permitted source functional-key group element into target-state capability.

## 4. Direct LWE track — strongest practical candidate, highest immediate risk

The direct bounded multi-level LWE route currently has two coupled blockers.

### 4.1 Depth-dependent correctness/noise

Repeated application of the one-hop-style matrix update carries inherited error through products of update matrices. Conservative operator bounds can grow geometrically with depth. A useful candidate needs a substantially tighter distributional argument or refresh mechanism.

### 4.2 Public-token surrogate-key criterion

For

\[
H_lZ_l=D_l,
\quad H_l\Delta_{1,l}=H_{l+1},
\quad H_l\Delta_{2,l}=D_{l+1}-D_l,
\]

a source key `Z_l y` plus public `Delta_2` yields

\[
w=Z_ly+\Delta_{2,l}y
\]

with

\[
H_lw=D_{l+1}y.
\]

If public `Delta_1` allows an efficient solution of

\[
\Delta_{1,l}z=w,
\]

then `z` satisfies the target key-image equation. If `z` is short enough for target decryption, the candidate fails key non-transferability.

This is now an explicit P0 falsification gate (`#9`).

### Decision

**Do not implement/benchmark the direct LWE route as the headline backend until issue #9 is resolved.**

A sampled attack failure is insufficient. The candidate still needs a reduction even if the simple surrogate is too long.

## 5. Generic iO/PTDE/PRF route — possible feasibility theorem, not FGCS backend

The generic candidate refreshes the encrypted representation inside an obfuscated update program at each level. This avoids the direct inherited-LWE-noise recurrence at the conceptual level.

Its price is substantial:

- very strong assumptions;
- adjacent public obfuscated update programs share hidden level secrets and complicate hybrids;
- fork/DAG exposure must be handled explicitly;
- no practical implementation suitable for the intended FGCS measurements.

### Decision

Continue only as a **generic feasibility theorem** if issue #8 can close with a complete bounded-depth proof whose security experiment genuinely matches CAMH-CUFE rather than restating generic updatable cryptography.

Do not use it as performance evidence.

## 6. Refreshed lattice direction — required investigation

The current SOTA matrix records Schädlich, Scheu-Hachtel, Tairi and Wang, *Ciphertext-Updatable Attribute-Based and Predicate Encryption from Lattices* (SCN 2026 / IACR ePrint 2026/1045), as providing multi-hop ciphertext-updatable ABE/PE in a different functionality model.

The verified metadata/abstract-level evidence is enough to establish this as a **mandatory neighboring construction family**. It is not enough to claim that its exact techniques automatically instantiate CAMH-CUFE.

Before adopting this route we must verify from the full construction/proofs:

1. how repeated update keys/tokens avoid unauthorized key-capability transport;
2. whether update depth is bounded/unbounded in the exact security theorem;
3. how ciphertext noise is refreshed or controlled;
4. whether the transition mechanism can coexist with **FE function-output semantics**, rather than only ABE/PE decryption predicates;
5. whether exact tag-level opt-in composition can be embedded cryptographically;
6. assumptions and implementation feasibility.

### Decision

Treat this as the highest-value alternative practical-design investigation if direct LWE fails.

## 7. Paper architecture implied by the decision gate

A defensible final paper may contain two construction layers only if their evidence is kept separate:

### Layer A — generic feasibility

A theorem-level construction establishes that the CAMH-CUFE security object is realizable under explicit strong assumptions.

### Layer B — concrete bounded instantiation

A real cryptographic construction supplies:

- exact parameterization;
- functional/key security theorem matching the implemented profile;
- canonical wire objects;
- distributed performance evidence.

If Layer B realizes a weaker threat model than Layer A, the manuscript must state that difference prominently and must not use Layer B's measurements as operational evidence for Layer A's stronger guarantees.

## 8. Submission decision

### GO toward FGCS experiments

Only when one real construction has:

- a complete correctness bound;
- a plausible/complete key non-transferability proof path;
- no active simple public-token surrogate attack;
- exact state binding;
- parameter sets suitable for implementation.

### STOP

Stop distributed scaling and manuscript Results drafting if the only available backends are:

- the legacy broken pairing prototype;
- the symbolic oracle;
- an unproved direct LWE extrapolation;
- an impractical iO feasibility construction.

That stop rule protects the paper from the Q1 failure mode where implementation volume obscures a contribution/evidence mismatch.

## 9. Current recommendation

1. **Keep the legacy pairing construction rejected for security.**
2. **Resolve issue #9 before spending effort on direct-LWE benchmarking.**
3. **Continue issue #8 only as a formal feasibility track.**
4. **Perform a full-paper technical mapping of SCN 2026 CU-ABE/PE before designing the refreshed lattice track.**
5. **Delay FGCS distributed measurements until a real secure candidate survives the cryptographic gates.**

This ordering prioritizes the scientific bottleneck rather than the easiest engineering work.
