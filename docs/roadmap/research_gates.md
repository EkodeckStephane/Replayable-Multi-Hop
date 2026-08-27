# CAMH-CUFE Research Gates

The project advances only when each gate has explicit evidence. A later gate may expose a defect that reopens an earlier gate.

A checked item means only the scope stated by that item. In particular:

- **model/specification closed** does not mean a construction is proved secure;
- **implemented/tested** does not mean a reduction theorem exists;
- **symbolic/conformance evidence** must never be reported as real cryptographic performance or confidentiality evidence.

## G0 — Legacy freeze

**Goal:** preserve the previous prototype as a reproducibility baseline without allowing its manuscript/audit history to shape the new scientific narrative.

Exit criteria:

- [x] baseline source/archive snapshot identified by SHA-256 in `legacy/BASELINE.md` and `legacy/source_manifest.sha256`;
- [ ] old raw/processed results fully retained and independently inventoried outside headline CAMH-CUFE evidence;
- [x] JISA submission PDFs/cover letters/audit-history reports excluded from the CAMH-CUFE scientific source tree;
- [x] any reused legacy result must be labeled legacy/regression evidence.

**Important negative result:** the legacy pairing construction admits public-token functional-key switching and is disqualified from CAMH-CUFE confidentiality claims. See `docs/formal/legacy_key_switch_attack.md`.

## G1 — SOTA closure

**Goal:** demonstrate that the exact CAMH-CUFE scientific object remains unresolved.

Required families:

- [x] ciphertext-updatable FE / IPFE;
- [x] Updatable Functional Encryption;
- [x] generic Cryptography with Updates;
- [x] functional re-encryption;
- [x] functional proxy re-encryption;
- [x] multi-hop PRE / ciphertext evolution;
- [x] verifiable multi-hop PRE;
- [x] composable/updatable encryption;
- [x] recent multi-hop ciphertext-updatable ABE/PE neighbor identified;
- [x] dynamic encrypted-state verification in FGCS;
- [x] FE papers in FGCS;
- [ ] adaptive/key-evolving FE literature exhaustively checked for overlapping repeated-state semantics;
- [ ] transparency/checkpoint/accountability literature exhaustively checked;
- [ ] recent IACR ePrint/CRYPTO/EUROCRYPT/ASIACRYPT/PKC/CCS/S&P/USENIX Security search completed through submission date;
- [ ] every high-impact novelty row independently verified from publisher/full paper;
- [ ] final priority-claim falsification pass performed immediately before manuscript freeze.

**Exit:** the exact central claim survives the falsification criteria in `docs/sota/novelty_claims.md`. Until then, `first`, `novel`, `state of the art`, and equivalent priority wording remain prohibited.

## G2 — Formal object freeze

### Closed at baseline model/specification level

- [x] preliminary CAMH-CUFE syntax;
- [x] cryptographic authorization state `Q=(tag,level)`;
- [x] state-global token semantics separated from lineage-specific audit semantics;
- [x] full-history vs checkpoint evidence semantics separated;
- [x] branching/reconvergence policy frozen for the baseline model;
- [x] cycles excluded structurally by one-level advancement per edge;
- [x] fresh retained histories start at level 0;
- [x] root history commitment binds exact initial state and fresh ciphertext;
- [x] baseline adaptive oracle interfaces frozen in `docs/formal/oracle_and_leakage_profile.md`;
- [x] public leakage profile frozen for the baseline model;
- [x] public-token (`MH-PUB`) and honest-update (`MH-HU`) exposure profiles distinguished;
- [x] challenge admissibility rule frozen at model level;
- [x] baseline distributed roles/trust boundaries/corruption profiles frozen in `docs/formal/system_threat_model.md`;
- [x] untrusted-proxy `MH-PUB` profile selected as the intended headline FGCS threat model.

### Still open before complete construction freeze

- [ ] notation harmonized across every construction/proof document (`Q` vs legacy/candidate `S`, `level` vs `epoch`);
- [ ] construction-specific oracle restrictions reconciled with the baseline game without weakening the intended untrusted-proxy model;
- [ ] functionality/message domains and exact adaptive/selective choices frozen for the retained secure construction;
- [ ] construction-specific corruption restrictions proven compatible with the baseline distributed threat model.

## G3 — Security definitions

### Defined at model/reference-protocol level

- [x] exact state-authorization game;
- [x] explicit composition-authorization game;
- [x] replay game;
- [x] rollback game;
- [x] skip/reorder games;
- [x] splice/fork/cross-lineage games;
- [x] history-binding game;
- [x] functional-key non-transferability game;
- [x] checkpoint forgery/state-binding/equivocation semantics;
- [x] baseline adaptive multi-hop FE confidentiality experiment (`MH-PUB` / `MH-HU`);
- [x] sequential-composition security target tied to the accumulated adversarial view;
- [x] branch-aware challenge-derived ciphertext policy;
- [x] key-query admissibility designed not to define away key-switch attacks;
- [x] final-result canonical public statement/transcript/base-binding boundary frozen in `docs/formal/final_result_relation.md`.

### Open

- [ ] retained construction's exact confidentiality theorem game instantiated with all query bounds;
- [ ] concrete final-result proof witness/relation and soundness theorem finalized, or `pi4` removed;
- [ ] corruption/accountability games finalized for any quorum/transparency extension retained in the article.

## G4 — Construction and proofs

### Results already established

- [x] legacy repeated-update algebraic correctness/telescoping invariant derived;
- [x] legacy pairing confidentiality path rejected by explicit functional-key switching counterexample;
- [x] bounded multi-level LWE candidate recurrence and conservative noise-growth risk derived;
- [x] generic multi-level iO/PTDE/PRF feasibility candidate specified at correctness-sketch level;
- [x] audit-layer history/checkpoint binding reductions stated conditionally on canonical encoding, collision resistance, token authentication and transition-use soundness.

These checked items are **research findings/candidate analyses**, not secure CAMH-CUFE construction theorems.

### Secure-construction gate

- [ ] determine whether a useful generic feasibility theorem can be proved under defensible assumptions;
- [ ] select/complete one retained secure CAMH-CUFE construction;
- [ ] construction-level cryptographic binding to exact `(tag,level)` proved;
- [ ] correctness theorem;
- [ ] depth-dependent multi-hop functional consistency theorem;
- [ ] functional-key non-transferability theorem;
- [ ] replay/state-authorization theorem(s);
- [ ] path/composition-authorization theorem(s);
- [ ] unconditional/instantiated history-binding theorem with final concrete encodings/hash;
- [ ] concrete checkpoint security theorem;
- [ ] `MH-PUB` multi-hop confidentiality/sequential-composition theorem for the intended untrusted-proxy deployment, or architecture/claims narrowed explicitly to `MH-HU`;
- [ ] final-result soundness theorem if a final-result proof remains in scope;
- [ ] assumptions mapped one-to-one to theorem statements;
- [ ] reduction losses/query bounds stated explicitly.

**Hard rule:** if the intended `MH-PUB` reduction fails, narrow the architecture/claim or redesign the construction before distributed scaling work becomes headline evidence.

## G5 — Protocol closure

### Implemented/tested reference protocol layer

- [x] canonical serialization policy drafted;
- [x] strict versioned length-delimited canonical encoder/decoder implemented;
- [x] ambiguous concatenation, ordering, duplicate-field, truncation, wrong-type, and trailing-byte tests added;
- [x] frozen protocol-v1 golden encoding vectors added;
- [x] central domain-separation registry implemented;
- [x] history-root and history-link hashing use explicit separate domains;
- [x] initial authorization state cryptographically committed by the history root;
- [x] state/lineage continuity reference verifier implemented;
- [x] skip/reorder/splice/final-state/final-ciphertext/history-digest substitution tests added;
- [x] `VerifyTransitionUse` hook required so a public hash-chain recomputation cannot substitute for cryptographic transition validation;
- [x] `pi4` verifier-critical bases deterministically derived from suite, exact public-parameter digest, relation identifier and dimension;
- [x] caller-substituted `pi4` bases rejected by tests;
- [x] final reference verifier API exposes no caller-supplied base parameter;
- [x] canonical final-result statement binds setup, state, ciphertext, function/key public views, result encoding/value, history and application context;
- [x] canonical checkpoint statement binds final state, ciphertext, history digest, history length, policy and application context;
- [x] baseline single-honest-auditor checkpoint trust semantics frozen;
- [x] typed canonical-wire measurement helpers implemented for state, transition, retained record, checkpoint and final-result statement;
- [x] CI guard rejects Python-object/pickle/runtime-size paths from protocol metric code.

### Open before protocol closure

- [ ] complete domain-separation audit of the eventual real cryptographic backend;
- [ ] canonical encodings for every concrete backend ciphertext, token, functional key, proof, signature/certificate and public parameter object;
- [ ] strict standards-conformant group/lattice element decoding with subgroup/canonicality checks as applicable;
- [ ] concrete `pi4` proof relation/soundness, or removal/replacement of `pi4`;
- [ ] concrete checkpoint signing implementation and security theorem;
- [ ] canonical wire-size measurement over the final real backend objects and network messages.

## G6 — Implementation validity

### Current reference/conformance implementation

- [x] symbolic algebra backend explicitly isolated and labeled as a correctness/differential oracle;
- [x] exact authorization-graph reference model implemented;
- [x] retained-history conformance verifier implemented;
- [x] adversarial tests derived from multiple formal game classes;
- [x] final-result statement/base substitution regression tests implemented;
- [x] current CAMH-CUFE reference CI runs on Python 3.11/3.12/3.13;
- [x] current reference CI has `failed = 0` and `skipped = 0` for the tests presently in scope;
- [x] latest protocol/refactoring tranche executes 71 tests successfully on all three Python versions.

### Required for scientific implementation validity

- [ ] real cryptographic backend is the default scientific backend;
- [ ] all retained formal checks mapped to construction-level implementation checks;
- [ ] official real-backend CI has `failed = 0`;
- [ ] official real-backend CI has `skipped = 0` for mandatory tests;
- [ ] differential tests between symbolic/reference and real backend;
- [ ] key-switch regression against the retained real construction;
- [ ] exact-state cryptographic-binding regression against the retained real construction;
- [ ] adversarial campaign covers every applicable final security-game class;
- [ ] dependency versions and cryptographic suite frozen;
- [ ] malformed/canonical-decoding fuzz or property-based tests added for real wire objects.

## G7 — Distributed FGCS prototype

Required independent roles:

- [ ] authority/data owner;
- [ ] at least two update proxies/processes;
- [ ] independent auditor/checkpoint issuer;
- [ ] verifier;
- [ ] functional consumer.

Evidence:

- [ ] real cryptographic backend used by headline distributed experiments;
- [ ] non-loopback communication for headline distributed experiment;
- [ ] TLS/authenticated channels where relevant;
- [ ] frozen deployment topology;
- [ ] deployed process/host identities documented against `docs/formal/system_threat_model.md`;
- [ ] fault/adversarial injection procedure;
- [ ] no local symbolic timing promoted to distributed-system evidence.

## G8 — Experimental validity

Factors:

- [ ] path length `k`;
- [ ] FE dimension `n`;
- [ ] verifier mode;
- [ ] backend/configuration;
- [ ] number of auditors/quorum size only if such a profile is actually implemented;
- [ ] concurrency/load if meaningful;
- [ ] independent deployment session/run where required by the statistical design.

Metrics:

- [ ] end-to-end latency;
- [ ] per-hop update latency;
- [ ] full-history replay latency;
- [ ] checkpoint issuance latency (including full audit);
- [ ] later checkpoint verification latency;
- [ ] canonical communication bytes;
- [ ] retained-history bytes;
- [ ] checkpoint/certificate bytes;
- [ ] CPU;
- [ ] RAM;
- [ ] throughput where meaningful.

Statistics:

- [ ] technical repeats labeled as technical repeats rather than independent samples;
- [ ] experimental unit declared for every analysis;
- [ ] paired/repeated-measures design used where the same instance/session is compared;
- [ ] run/session independence and ordering documented;
- [ ] confidence interval/bootstrap method justified;
- [ ] multiplicity handled if inferential families are used;
- [ ] negative/boundary results retained and reported when they constrain claims;
- [ ] implementation-level timings separated from primitive-level microbenchmarks.

## G9 — Manuscript reconstruction

**Do not begin numerical Results prose until G4/G6 establish which construction/backend supports headline evidence.**

Target structure:

1. Introduction
2. Related Work and Gap
3. System and Threat Model
4. CAMH-CUFE Definition
5. Security Definitions
6. Construction
7. Security Analysis
8. Concrete CUFE/IPFE Instantiation
9. Distributed Implementation
10. Experimental Methodology
11. Results
12. Discussion
13. Limitations
14. Conclusion

Remove from main narrative:

- development history;
- audit logs;
- command listings;
- algorithm-to-code QA tables;
- RQ1–RQ6 validation-report framing;
- legacy failure chronology except where the negative result is scientifically relevant to construction choice;
- unresolved placeholders;
- repo/tooling as the organizing principle.

## G10 — Submission readiness

- [ ] every headline claim maps to a theorem, direct measurement, or explicit assumption;
- [ ] conceptual/implemented/simulated/measured/inferred elements distinguished;
- [ ] negative results and boundary conditions retained when scientifically material;
- [ ] references verified and current through manuscript freeze;
- [ ] FGCS literature integrated into an experiment-linked unresolved gap, not merely appended;
- [ ] no unsupported priority/SOTA wording;
- [ ] title identical everywhere;
- [ ] authors/corresponding author identical everywhere;
- [ ] article, code, raw data, processed data, tables and figures cross-checked;
- [ ] no operational/distributed claim exceeds real non-loopback evidence;
- [ ] full-history and checkpoint evidence regimes described with their different trust semantics;
- [ ] reproducibility README is sufficient without turning manuscript into a runbook;
- [ ] no unresolved DOI/TODO/internal audit notes in article sources;
- [ ] final Q1 scientific-article gate audit PASS.
