# CAMH-CUFE domain-separation registry

## Status

This registry is normative for protocol version `1`. Security-critical hashing, hash-to-curve derivation, signatures, and proof statements must use purpose-specific labels. A semantically new purpose receives a new label; an existing label is never repurposed.

The executable source of truth is `src/camh_cufe/domains.py`.

| Purpose | Domain label | Status |
|---|---|---|
| pi4 commitment-base derivation | `CAMH-CUFE/PI4/BASES/v1` | implemented |
| history-root commitment | `CAMH-CUFE/HISTORY/INIT/v1` | implemented |
| history-link commitment | `CAMH-CUFE/HISTORY/LINK/v1` | implemented |
| symbolic tag scalar | `CAMH-CUFE/SYMBOLIC/TAG/v1` | implemented; test oracle only |
| real-backend state hash | `CAMH-CUFE/REAL/STATE/v1` | reserved |
| real-backend token identifier | `CAMH-CUFE/REAL/TOKEN-ID/v1` | reserved |
| checkpoint signature statement | `CAMH-CUFE/CHECKPOINT/SIGN/v1` | reserved until signer implementation |
| final-result proof statement | `CAMH-CUFE/PI4/STATEMENT/v1` | reserved until proof relation freezes |

## Canonical-object separation

Canonical protocol objects also carry distinct 16-bit object-type identifiers inside the versioned `CAMH-CUFE\0` TLV envelope:

| Object | Type |
|---|---:|
| authorization state | `0x1001` |
| group-element vector | `0x1002` |
| transition statement | `0x1003` |
| history root | `0x1004` |
| history link | `0x1005` |
| checkpoint statement | `0x1006` |

Object-type separation complements, rather than replaces, cryptographic domain separation. History digests therefore hash a canonical typed object under a dedicated history-purpose label.

## Root-state binding

Protocol version `1` history initialization commits explicitly to:

```text
suite_id || exact initial authorization state || canonical fresh ciphertext
```

The initial state is included even if a concrete ciphertext encoding also carries the tag/level. This avoids making audit binding depend on an implicit parser invariant of a future backend.

## Audit rule

Before a real cryptographic backend is accepted, review every call to:

- cryptographic hash;
- hash-to-field/hash-to-curve;
- signature prehash or signing transcript;
- Fiat-Shamir transcript/challenge derivation;
- KDF/PRF derivation;
- token/ciphertext identifiers.

Every call must map to a registered purpose or to an independently standardized primitive-specific DST whose relationship to this registry is documented.

A green unit test for uniqueness checks accidental duplicate labels in code; it does not establish that every future cryptographic call has been audited. The latter remains a manual/code-review gate until automated static checking is added.
