# Critical Prior-Art Boundaries for CAMH-CUFE

This document records prior art that materially constrains the CAMH-CUFE novelty claim. It is intentionally adversarial: each entry states a claim the manuscript must **not** make and the narrower distinction that still requires proof.

## 1. Updatable Functional Encryption (Mycrypt 2016)

**Afonso Delerue Arriaga, Vincenzo Iovino, Qiang Tang.** “Updatable Functional Encryption.” Mycrypt 2016, LNCS 10311, pp. 347–363. DOI: `10.1007/978-3-319-61273-7_17`.

The work defines UFE for RAM programs and explicitly envisions tokens that can update encrypted memory/ciphertext over which subsequent tokens can execute.

### Consequence

CAMH-CUFE cannot claim that repeated processing or updating of encrypted FE state is new in general.

### Remaining distinction to establish

CAMH-CUFE targets **tag-changing CUFE access-control semantics**: functional keys and ciphertext states are associated with authorization tags/states, and repeated updates change those authorization states while preserving function-output semantics. The paper must show that its security object is not merely a rephrasing of UFE’s encrypted RAM-memory update semantics.

## 2. Cryptography with Updates (EUROCRYPT 2017)

**Prabhanjan Ananth, Aloni Cohen, Abhishek Jain.** “Cryptography with Updates.” EUROCRYPT 2017, Part II, pp. 445–472. DOI: `10.1007/978-3-319-56614-6_15`.

The work develops updatable randomized encodings and generic transformations that add updatability to primitives including functional encryption.

### Consequence

CAMH-CUFE cannot claim a generic “one-hop-to-updatable-FE compiler” merely because it wraps a primitive in update metadata.

### Remaining distinction to establish

Any CAMH-CUFE compiler claim must state exactly which **tag-CUFE transition security**, adaptive prefix exposure, and authenticated path guarantees it adds, and how those guarantees differ from the generic updatable-cryptography abstraction.

## 3. Cini et al. CUFE (Journal of Cryptology 2024)

**Valerio Cini, Sebastian Ramacher, Daniel Slamanig, Christoph Striecks, Erkan Tairi.** “(Inner-Product) Functional Encryption with Updatable Ciphertexts.” Journal of Cryptology 37, Article 8. DOI: `10.1007/s00145-023-09486-y`.

This is the direct foundation for tag-changing CUFE. Its stated security/correctness design permits a fresh ciphertext to be updated once and explicitly excludes successfully updating an already-updated ciphertext.

### Consequence

This one-update restriction is the correct starting gap for CAMH-CUFE, but only relative to this **specific CUFE model**.

### Remaining distinction to establish

CAMH-CUFE must define how an already-updated tag/state becomes a legitimate later update source, and prove that the resulting adaptive multi-hop behavior preserves the intended FE guarantees.

## 4. Multi-hop re-encryption and ciphertext evolution

**Chandran et al.** “Re-encryption, Functional Re-encryption, and Multi-Hop Re-encryption.” PKC 2014. DOI: `10.1007/978-3-642-54631-0_6`.

**Yao et al.** “An Identity-Based Proxy Re-Encryption Scheme With Single-Hop Conditional Delegation and Multi-Hop Ciphertext Evolution for Secure Cloud Data Sharing.” IEEE TIFS 2023. DOI: `10.1109/TIFS.2023.3282577`.

### Consequence

Neither “multi-hop re-encryption” nor “multi-hop ciphertext evolution” is a CAMH-CUFE novelty claim.

### Remaining distinction to establish

The comparison must focus on FE function-output semantics and repeated **authorization-state** evolution, not merely the number of transformations.

## 5. Functional proxy re-encryption

**Liang et al.** “DFA-Based Functional Proxy Re-Encryption for Secure Public Cloud Data Sharing.” IEEE TIFS 2014. DOI: `10.1109/TIFS.2014.2346023`.

### Consequence

“Functional” plus “re-encryption” is not new.

### Remaining distinction to establish

CAMH-CUFE must separate FE’s constrained function output from PRE/functional-PRE delegation and transformation semantics.

## 6. Verifiable multi-hop PRE (IEEE TIFS 2026)

**Cai et al.** “Verifiable and Fair Registered Attribute-Based Multi-Hop Proxy Re-Encryption Scheme for LLM Agents.” IEEE TIFS 2026. DOI: `10.1109/TIFS.2026.3711852`.

The work already combines multi-hop proxy re-encryption, verifiability, formal security, NIZK/zkSNARK mechanisms, and implementation evidence.

### Consequence

CAMH-CUFE cannot claim to introduce verifiable multi-hop encrypted-data transformation.

### Remaining distinction to establish

The paper must compare security objects directly: tag-CUFE composability, FE output semantics, replayable authenticated update histories, and the semantics of checkpoint certification.

## 7. Composable updatable encryption

**Levy-dit-Vehel and Roméas.** “Interactivity in Constructive Cryptography: Modeling and Applications to Updatable Encryption and Private Information Retrieval.” arXiv:2204.11653.

### Consequence

“Composable” is established terminology backed by formal composition frameworks.

### Remaining distinction to establish

CAMH-CUFE may retain “Composable” in the title only if it supplies an exact sequential-composition definition and theorem appropriate to its CUFE setting.

## 8. Checkpoints and witness quorums in transparency logs

The C2SP transparency-log specifications define compact signed checkpoints over Merkle-tree states and witness cosignatures after consistency verification. Witness quorums are used to reduce split-view/equivocation risk.

### Consequence

Signed checkpoints, checkpoint consistency, and quorum/witness cosigning are not individually novel CAMH-CUFE mechanisms.

### Remaining distinction to establish

The contribution can be the **semantic integration** of checkpoint evidence into a ciphertext-update FE history model: a checkpoint certifies an already-audited state under an explicit trust policy, whereas independent history replay verifies the retained transitions themselves. If transparency-style consistency/witnessing is added, it must be presented as an adopted mechanism, not invented by CAMH-CUFE.

## 9. Current novelty target

After these exclusions, the high-value claim remains:

> CAMH-CUFE defines and studies sequentially composable **tag-changing CUFE state evolution**, where security is evaluated after adversarially observable update prefixes and includes authenticated path properties, while the verification model separates independent transition replay from trust-explicit compact certification of an already-audited state.

This claim remains **OPEN** until the sequential confidentiality/composition theorem and the SOTA closure gate are complete.
