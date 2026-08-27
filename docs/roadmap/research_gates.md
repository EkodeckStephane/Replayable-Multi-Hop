# CAMH-CUFE Research Gates

The project advances only when each gate has explicit evidence. A later gate may expose a defect that reopens an earlier gate.

## G0 — Legacy freeze

**Goal:** preserve the previous prototype as a reproducibility baseline without allowing its manuscript/audit history to shape the new scientific narrative.

Exit criteria:

- [ ] baseline source snapshot identified by hash/tag;
- [ ] old raw/processed results retained outside headline CAMH-CUFE evidence;
- [ ] no JISA submission material or audit-history prose imported into the new manuscript branch;
- [ ] baseline claims labeled as legacy where reused for regression comparison.

## G1 — SOTA closure

**Goal:** demonstrate that the exact CAMH-CUFE scientific object remains unresolved.

Required families:

- [x] ciphertext-updatable FE / IPFE;
- [x] functional re-encryption;
- [x] functional proxy re-encryption;
- [x] multi-hop PRE / ciphertext evolution;
- [x] verifiable multi-hop PRE;
- [x] composable/updatable encryption;
- [x] dynamic encrypted-state verification in FGCS;
- [x] FE papers in FGCS;
- [ ] adaptive/key-evolving FE literature checked for overlapping repeated-state semantics;
- [ ] transparency/checkpoint/accountability literature checked;
- [ ] recent IACR ePrint/CRYPTO/EUROCRYPT/ASIACRYPT/PKC/CCS/S&P/USENIX Security search completed through submission date;
- [ ] every high-impact novelty row independently verified from publisher/full paper.

**Exit:** central novelty survives falsification criteria in `docs/sota/novelty_claims.md`.

## G2 — Formal object freeze

- [x] preliminary CAMH-CUFE syntax;
- [x] preliminary state model;
- [x] full-history vs checkpoint semantics separated;
- [ ] exact allowed branching/cycles policy;
- [ ] exact state identity/lineage semantics;
- [ ] final oracle interfaces frozen;
- [ ] leakage profile frozen;
- [ ] protocol notation frozen.

## G3 — Security definitions

- [x] replay game drafted;
- [x] rollback game drafted;
- [x] skip/reorder games drafted;
- [x] splice/fork/cross-state games drafted;
- [x] history-binding game drafted;
- [x] checkpoint games drafted;
- [ ] adaptive multi-hop FE confidentiality game finalized;
- [ ] sequential composability definition finalized;
- [ ] final-result proof relation finalized.

## G4 — Construction and proofs

- [ ] determine whether a generic one-hop-to-multi-hop compiler is provable;
- [ ] correctness theorem;
- [ ] multi-hop functional consistency theorem;
- [ ] replay/rollback theorem(s);
- [ ] path integrity theorem(s);
- [ ] history-binding theorem;
- [ ] checkpoint security theorem;
- [ ] multi-hop confidentiality/composition theorem;
- [ ] final-result binding theorem;
- [ ] assumptions mapped one-to-one to theorem statements.

**Hard rule:** if the multi-hop confidentiality reduction fails, narrow the claim before implementation scaling work continues.

## G5 — Protocol closure

- [x] canonical serialization policy drafted;
- [ ] concrete canonical encoder implemented;
- [ ] golden encoding vectors;
- [ ] domain separation audited;
- [ ] state/lineage binding audited;
- [ ] pi4 verifier-critical bases derived/authenticated;
- [ ] checkpoint statement complete;
- [ ] no `pickle` metric used as protocol-size evidence.

## G6 — Implementation validity

- [ ] symbolic backend isolated as test oracle;
- [ ] real cryptographic backend is default scientific backend;
- [ ] all formal checks mapped to implementation checks;
- [ ] failed = 0;
- [ ] skipped = 0 in official CI;
- [ ] differential tests between symbolic and real backend;
- [ ] adversarial tests generated from security-game classes;
- [ ] dependency versions and cryptographic suite frozen.

## G7 — Distributed FGCS prototype

Required independent roles:

- [ ] authority/data owner;
- [ ] at least two update proxies/processes;
- [ ] independent auditor/checkpoint issuer;
- [ ] verifier;
- [ ] functional consumer.

Evidence:

- [ ] non-loopback communication for headline distributed experiment;
- [ ] TLS/authenticated channels where relevant;
- [ ] frozen deployment topology;
- [ ] fault/adversarial injection procedure.

## G8 — Experimental validity

Factors:

- [ ] path length `k`;
- [ ] FE dimension `n`;
- [ ] verifier mode;
- [ ] backend;
- [ ] number of auditors/quorum size if implemented;
- [ ] concurrency/load if meaningful.

Metrics:

- [ ] end-to-end latency;
- [ ] update latency;
- [ ] full-history verification;
- [ ] checkpoint issuance;
- [ ] checkpoint verification;
- [ ] canonical communication bytes;
- [ ] retained-history/checkpoint bytes;
- [ ] CPU;
- [ ] RAM;
- [ ] throughput.

Statistics:

- [ ] technical repeats labeled as such;
- [ ] paired design where same instances are compared;
- [ ] run/session independence documented;
- [ ] bootstrap/CI method justified;
- [ ] multiplicity handled if inferential families are used;
- [ ] negative/boundary results retained.

## G9 — Manuscript reconstruction

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
- unresolved placeholders.

## G10 — Submission readiness

- [ ] every headline claim maps to theorem or direct measurement;
- [ ] conceptual/implemented/simulated/measured elements distinguished;
- [ ] references verified and current;
- [ ] FGCS literature integrated, not merely appended;
- [ ] title identical everywhere;
- [ ] authors/corresponding author identical everywhere;
- [ ] article, code, raw data, processed data, tables and figures cross-checked;
- [ ] no operational claim exceeds distributed evidence;
- [ ] reproducibility README is sufficient without turning manuscript into a runbook;
- [ ] final Q1 gate audit PASS.
