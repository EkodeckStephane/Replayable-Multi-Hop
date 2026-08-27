# CAMH-CUFE claim–evidence register

## Purpose

This register prevents a model definition, conformance test, candidate derivation, or legacy measurement from being promoted into a stronger scientific claim than its evidence supports.

Statuses are deliberately conservative:

- **MODEL** — definition/security target only;
- **DERIVED** — algebraic/formal consequence established from stated candidate equations;
- **CONDITIONAL THEOREM** — theorem/reduction holds only if explicitly listed assumptions/interfaces are instantiated;
- **IMPLEMENTED/TESTED** — executable conformance evidence, not a cryptographic reduction;
- **NEGATIVE RESULT** — a concrete candidate/legacy construction is falsified for a stated property;
- **OPEN** — required proof/measurement absent;
- **PROHIBITED** — manuscript wording not authorized by current evidence.

## Register

| ID | Candidate paper claim | Current evidence | Status | Manuscript language currently allowed | Blocking evidence |
|---|---|---|---|---|---|
| C0 | One-update tag-based CUFE leaves a distinct repeated tag/state-update problem | Cini CUFE identified as one-update foundation; UFE/generic updates/multi-hop PRE/CU-ABE/PE neighbors identified | SOTA OPEN | “we study repeated tag/state updates beyond the one-update CUFE setting” | exhaustive SOTA/falsification pass through submission freeze |
| C1 | CAMH-CUFE formalizes level-aware repeated tag-changing CUFE transitions | syntax/state/oracle/security-game documents | MODEL | “we define/formalize a CAMH-CUFE model” | notation/construction-specific theorem instantiation |
| C2 | Multi-hop reachability is opt-in through exact `(tag,level)` edges rather than inherited from tag equality | formal semantics + authorization-graph reference model + tests | MODEL + IMPLEMENTED/TESTED | “the model requires explicit level-compatible transition authorization” | cryptographic construction-level state-binding theorem |
| C3 | Public transition material must not switch functional-key capability | capability-based game + legacy pairing counterexample | MODEL + NEGATIVE RESULT | “we require key non-transferability; the legacy pairing baseline fails this property” | proof for retained secure construction |
| C4 | Direct additive pairing baseline supports secure CAMH-CUFE confidentiality | explicit public-token key-switch derivation falsifies it | NEGATIVE RESULT | only as a rejected baseline / design lesson | cannot be repaired by API metadata; construction redesign required |
| C5 | Direct multi-level LWE composition is a secure practical CAMH-CUFE instantiation | correctness/noise recurrences only; surrogate-key NO-GO criterion derived | OPEN / HIGH RISK | “a bounded LWE route is under investigation” | issue #9 + exact noise bound + key non-transferability + confidentiality theorem |
| C6 | Publicly solvable `Delta1` can induce a surrogate target preimage in the direct LWE candidate | algebraic theorem from candidate equations; executable toy instance decrypts an independent target ciphertext | DERIVED + IMPLEMENTED/TESTED EXAMPLE | “we derive a sufficient public-token surrogate-key attack criterion for this candidate architecture” | concrete sampled matrix characterization before applying criterion to any published/retained scheme |
| C7 | Generic multi-level iO/PTDE/PRF construction securely realizes CAMH-CUFE | correctness sketch; proof barriers recorded | OPEN | “we investigate a generic feasibility construction” | complete iO hybrid proof, shared-key puncturing, branch/adaptivity, key non-transferability |
| C8 | Retained history commitments bind ordered lineage transitions | canonical root/link encodings; SHA-256; strict verifier; theorem sketch conditional on token authentication and transition-use soundness; adversarial tests | CONDITIONAL THEOREM + IMPLEMENTED/TESTED | “under canonical encoding, collision resistance, token authentication, and transition-use soundness, the history layer binds accepted retained paths” | instantiate real token authentication and sound `VerifyTransitionUse` |
| C9 | Full-history verification independently validates omitted hops | reference replay verifier validates each retained record via injected transition-use predicate | IMPLEMENTED/TESTED REFERENCE | “the reference verifier replays every retained transition”; no real-backend effectiveness claim | real backend + final transition verifier + theorem instantiation |
| C10 | A compact checkpoint is equivalent to independently replaying all omitted transitions | checkpoint deliberately has different trust semantics | PROHIBITED | “checkpoint verification certifies an already-audited state under an explicit issuer policy” | only a different succinct proof construction could justify equivalence |
| C11 | Checkpoint forgery/state binding is secure | canonical statement exists; conditional reduction target identified | OPEN / CONDITIONAL DESIGN | “checkpoint statement binds state/history/policy/context” | concrete signature/threshold implementation + theorem + corruption threshold |
| C12 | `pi4` proves the claimed FE result | statement/transcript/base context now fully bound at reference level; toy binding tests only | OPEN | “the reference layer binds the final-result proof statement and derives verifier bases internally” | concrete witness relation + soundness theorem + real proof backend |
| C13 | Caller-controlled `pi4` bases are excluded from verifier semantics | deterministic setup/relation/dimension base derivation; final verifier API has no base argument; substitution tests | IMPLEMENTED/TESTED | direct implementation fact may be stated in methods/supplement | real backend hash-to-curve/canonical point validation still required |
| C14 | CAMH-CUFE has a secure real cryptographic backend | none retained yet | OPEN | none | secure construction selection + real implementation + CI |
| C15 | CAMH-CUFE is demonstrated as a distributed secure-computing system | threat model frozen only; no headline non-loopback experiment | OPEN | “we plan/evaluate only after backend closure” — omit future-work language from final Results | real backend + independent processes/hosts + non-loopback evidence |
| C16 | Checkpoint verification has path-length-independent cost in practice | expected by certificate semantics, not yet measured | OPEN | complexity statement only if derived from concrete certificate verifier | implementation + scaling measurements + complexity proof |
| C17 | Full-history verification scales linearly with path length in practice | reference algorithm iterates records; no real cryptographic measurements | OPEN | implementation-complexity statement may be derived once per-hop verifier cost is fixed | real backend measurement across `k` |
| C18 | CAMH-CUFE is first/novel/SOTA | SOTA closure incomplete | PROHIBITED | none | exhaustive current literature verification and explicit priority-claim audit |
| C19 | CAMH-CUFE outperforms PRE/ABE/other cryptographic systems | no comparable real baseline experiment | PROHIBITED | none | fair comparable baseline implementation + uncertainty/statistics |
| C20 | Current symbolic timings are cryptographic performance evidence | symbolic backend is an exponent-level correctness oracle | PROHIBITED | none | real cryptographic backend only |

## Headline-claim gate

A statement may enter the abstract/conclusion as a headline contribution only when it is one of:

1. a definition/model contribution whose novelty survives the final SOTA falsification pass;
2. a theorem with all assumptions instantiated and clearly stated;
3. a direct measurement from the final real experimental protocol with uncertainty/statistical treatment where appropriate;
4. a scientifically material negative result whose scope is stated exactly.

`IMPLEMENTED/TESTED` alone is insufficient for a cryptographic-security headline.

## Current abstract-safe contribution envelope

Before G4/G6 close, the strongest safe description is approximately:

> We define a level-aware model for repeated tag-changing ciphertext updates in CUFE, distinguish exact transition authorization from lineage audit semantics, and derive security requirements including functional-key non-transferability and path binding. Analysis of the legacy pairing baseline exposes a public-token key-switch failure, while the direct multi-level lattice route exhibits coupled correctness/key-security constraints including a sufficient surrogate-key attack criterion. A canonical audit/reference layer implements explicit history and proof-statement binding, while secure concrete multi-hop instantiation and distributed performance remain separate open gates.

This paragraph is **not** intended as the final abstract; it records the current evidence boundary.

## Conditions for promoting the central CAMH-CUFE claim

The intended final central claim requires all of:

- SOTA closure showing the exact security object remains unresolved;
- one retained construction proving key non-transferability;
- exact state-binding and controlled-composition theorem;
- multi-hop confidentiality/sequential-composition theorem under the stated public-token exposure profile;
- real cryptographic implementation;
- distributed FGCS measurements if operational/system claims are made.

Until then, the project has a strong formal problem definition and useful negative/conditional results, but **not yet a submission-ready secure CAMH-CUFE system**.
