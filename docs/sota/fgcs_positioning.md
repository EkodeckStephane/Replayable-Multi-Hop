# Positioning CAMH-CUFE for Future Generation Computer Systems

## 1. Scope fit

Future Generation Computer Systems (FGCS) explicitly lists the following relevant areas in its current Aims & Scope:

- security aspects;
- protocols and emerging standards;
- theoretical aspects of large-scale communication and computation;
- scaling and performance theory;
- protocols and their verification.

Official journal page: https://shop.elsevier.com/journals/future-generation-computer-systems/0167-739X

CAMH-CUFE should therefore be positioned as a **secure distributed encrypted-data evolution protocol with formal verification and measured scalability**, not as an isolated cryptographic primitive followed by a token cloud experiment.

## 2. FGCS literature that the manuscript should cite

### Proxy re-encryption and secure data sharing

**Eltayieb et al. — Certificateless Proxy Re-encryption with Cryptographic Reverse Firewalls for Secure Cloud Data Sharing.** Future Generation Computer Systems 162 (2025), 107478. DOI: 10.1016/j.future.2024.08.002.

Relevance: recent FGCS evidence that a new re-encryption construction is publishable when it combines a clear cloud-security problem, formal attack/security analysis, revocation/security mechanisms, and computational/communication evaluation.

CAMH-CUFE difference: FE function-output semantics, repeated update composability, and authenticated history rather than recipient/key delegation alone.

**Zhou et al. — PCL-BPRE: privacy-preserving certificateless-based broadcast proxy re-encryption for data sharing in cloud-based IIoT.** Future Generation Computer Systems 178 (2026), 108307. DOI: 10.1016/j.future.2025.108307.

Relevance: current FGCS benchmark for PRE-oriented cloud/IIoT cryptography: formal CCA proof plus experimental validation.

CAMH-CUFE difference: repeatedly updated functional ciphertext state, path-security model, dual history/checkpoint verification semantics, and distributed audit roles.

**A pairing-free certificate-based proxy re-encryption scheme for secure data sharing in public clouds.** Future Generation Computer Systems 62 (2016), 140–147. DOI: 10.1016/j.future.2015.11.012.

Relevance: establishes long-running FGCS interest in efficient and formally secure PRE for cloud data sharing.

### Dynamic encrypted data and verifiability

**Xu et al. — Forward-Secure multi-user and verifiable dynamic searchable encryption scheme within a zero-trust environment.** Future Generation Computer Systems 166 (2025), 107701. DOI: 10.1016/j.future.2024.107701.

Relevance: especially important. It uses a multiset-hash **state chain** to support encrypted-data updates, forward privacy, and verifiable results.

CAMH-CUFE must explicitly distinguish its history state from this line of work: the CAMH-CUFE chain authenticates a sequence of cryptographic **ciphertext transformation authorizations and resulting FE states**, rather than a searchable-encryption update index/state used for search privacy and result verification.

**Verifiable multi-client blockchain-based dynamic data retrieval.** Future Generation Computer Systems 174 (2026), 108008. DOI: 10.1016/j.future.2025.108008.

Relevance: combines dynamic encrypted data, public verification, multiset hashing/smart contracts, and updatable encryption for revocation. It is a useful systems-level comparator for the cost of maintaining verifiability under dynamic state.

**Blockchain-assisted verifiable certificate-based searchable encryption against untrusted cloud server for Industrial Internet of Things.** Future Generation Computer Systems 153 (2024), 97–112. DOI: 10.1016/j.future.2023.11.016.

Relevance: explicitly separates multiple **levels of verifiability**, supporting our decision to define full-history and checkpoint verification as distinct semantics rather than collapse them into one “verifiable” label.

### Audit, integrity, freshness, and update security

**A verifiable data integrity scheme for distributed data sharing in fog computing architecture.** Future Generation Computer Systems 150 (2024), 64–77. DOI: 10.1016/j.future.2023.08.016.

Relevance: distributed public integrity verification and dynamic update/insert/delete operations without relying on a TPA.

CAMH-CUFE difference: security of the cryptographic ciphertext-evolution path, not only integrity of outsourced data records.

**Full integrity and freshness for cloud data.** Future Generation Computer Systems 80 (2018), 640–652. DOI: 10.1016/j.future.2016.06.013.

Relevance: explicitly considers freshness checks to resist replay attacks. This should be cited when motivating CAMH-CUFE’s replay/rollback state-security requirements.

**Privacy preserving cloud data auditing with efficient key update.** Future Generation Computer Systems 78 (2018), 789–798. DOI: 10.1016/j.future.2016.09.003.

Relevance: formalizes an auditing model with key updates, proves soundness/privacy, and implements the construction. Useful precedent for combining dynamic cryptographic state, audit guarantees, and implementation evidence.

### Functional encryption inside FGCS

**Deng et al. — Non-interactive and privacy-preserving neural network learning using functional encryption.** Future Generation Computer Systems 145 (2023), 454–465. DOI: 10.1016/j.future.2023.03.036.

Relevance: direct evidence that FGCS publishes FE-based systems when FE enables a distributed/privacy-preserving application and the paper provides both security and performance evaluation.

**Towards leakage-resilient fine-grained access control in fog computing.** Future Generation Computer Systems 78 (2018), 763–777. DOI: 10.1016/j.future.2017.01.025.

Relevance: presents a generic framework using functional encryption for fog access control. It is useful when explaining why CAMH-CUFE is not out of scope merely because its core mechanism is FE.

**PSCD: A privacy-preserving framework for structural constraint mitigation in deep neural networks on encrypted distributed datasets.** Future Generation Computer Systems 180 (2026), 108390. DOI: 10.1016/j.future.2026.108390.

Relevance: very recent FE-based FGCS work tied to encrypted distributed datasets. CAMH-CUFE should similarly make the distributed-system problem primary rather than present cryptography without systems consequences.

**Timed-release and partially private access control for decentralized IoT collaboration systems.** Future Generation Computer Systems 178 (2026), 108300. DOI: 10.1016/j.future.2025.108300.

Relevance: recent use of functional encryption in decentralized collaboration/access control, useful for motivating state- and policy-sensitive encrypted collaboration workflows.

### Verifiable cryptographic computation

**Blockchain-enabled reliable outsourced decryption CP-ABE using responsive zkSNARK for mobile computing.** Future Generation Computer Systems 176 (2026), 108182. DOI: 10.1016/j.future.2025.108182.

Relevance: demonstrates the current journal bar for a verifiable cryptographic system: formal mechanism, explicit trust/fairness problem, prototype, and end-to-end performance evidence.

CAMH-CUFE must not imply that signed checkpoints offer the same semantics as zkSNARK-style proof verification; the distinction should become part of the contribution.

## 3. Required manuscript positioning

The Related Work section should not be organized by a chronological list of cryptographic primitives. It should end each family with the unresolved gap that CAMH-CUFE actually evaluates.

Suggested structure:

1. **Ciphertext-updatable functional encryption** — Cini et al.; single-update restriction.
2. **Functional PRE and multi-hop ciphertext evolution** — Chandran et al.; Liang et al.; Yao et al.; why multi-hop PRE does not solve repeated-update FE semantics.
3. **Verifiable multi-hop re-encryption** — Cai et al. 2026; why verification of proxy re-encryption differs from replayable CUFE history and checkpoint certification.
4. **Composable/updatable encryption** — composition and leakage models; why the word composable needs a theorem.
5. **Dynamic encrypted-state verification in FGCS** — DSSE, integrity, freshness, auditing, and public verification.
6. **Functional encryption in FGCS** — show journal fit and identify the missing state-evolution capability.

## 4. FGCS system story

The paper should evaluate a distributed workflow such as:

```text
Data Owner / Authority
        |
        v
Encrypted functional state S0
        |
        v
Update Proxy A ----> Update Proxy B ----> ... ----> Update Proxy k
        |                                      |
        +---------- authenticated path --------+
                                               |
                                               v
                                      Independent Auditor(s)
                                               |
                         full replay / checkpoint issuance
                                               |
                                               v
                                           Verifier
                                               |
                                               v
                                      Functional Consumer
```

The protocol should be evaluated across independent processes/hosts so that FGCS claims concern a distributed system rather than local function-call timing.

## 5. Experimental bar inferred from FGCS neighbors

At minimum:

- real cryptographic backend for headline results;
- multiple path lengths and FE dimensions;
- distributed roles;
- end-to-end and per-operation latency;
- communication bytes using canonical wire encoding;
- retained-history/checkpoint storage;
- CPU and memory;
- throughput/concurrency where meaningful;
- adversarial rejection tests mapped to formal games;
- ablation of unauthenticated chaining vs authenticated history vs checkpoint mode;
- uncertainty based on the actual repeated-measures design;
- explicit trust/performance trade-off.

## 6. Scope-risk rule

If the final study contains only local microbenchmarks of cryptographic operations, FGCS fit remains weak even if the cryptography is correct. The system evaluation must demonstrate consequences for distributed encrypted-data processing, protocol verification, and scalability, which are explicit parts of FGCS scope.
