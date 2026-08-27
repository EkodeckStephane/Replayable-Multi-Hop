# Canonical Serialization for CAMH-CUFE

> Security-critical design requirement. This document replaces ad hoc byte concatenation and Python-object serialization as protocol evidence.

## 1. Objective

Every value that is hashed, signed, committed, or measured as a protocol object must have a unique byte representation.

The encoding must prevent ambiguity such as different field tuples producing the same concatenated byte string.

## 2. General envelope

Each authenticated object uses:

```text
MAGIC || PROTOCOL_VERSION || OBJECT_TYPE || FIELD_COUNT || FIELDS...
```

Recommended fixed prefix:

```text
"CAMH-CUFE" || 0x00
```

Exact version and object identifiers must be frozen before archival release.

## 3. Field encoding

Each variable-length field uses an explicit type and length:

```text
TYPE_ID || UINT64_BE(length) || value
```

Fixed-width integers use unsigned canonical big-endian representation of a declared width. No leading-zero variants are accepted outside the defined width.

Strings are UTF-8 only after normalization policy is frozen. A safer protocol option is to treat tag identifiers as opaque bytes and let applications map human-readable strings to them outside the cryptographic encoding.

## 4. Required object encodings

### State identifier

```text
EncodeStateMeta(tag, epoch, ciphertext_id)
```

should bind at least:

```text
OBJECT_TYPE = STATE_META
protocol_version
suite_id
tag
epoch
ciphertext_id
```

Whether `ciphertext_id` is a hash of the initial ciphertext, lineage identifier, or explicit random identifier is a construction decision that must be analyzed for privacy and splice resistance.

### Update token statement

```text
EncodeTransitionStatement(
    source_state_meta,
    destination_state_meta,
    construction_parameters,
    proof_statement_context
)
```

A token signature/proof must not authenticate only tag names and levels if another state can share those values.

### History link

Candidate form:

```text
h_0 = H("CAMH-CUFE/HISTORY/INIT" || Encode(S_0))

h_(i+1) = H(
    "CAMH-CUFE/HISTORY/LINK" ||
    h_i ||
    Encode(Delta_i,i+1) ||
    Encode(S_(i+1))
)
```

The exact encoding must avoid circular definitions if the state itself contains `h_i`.

### Checkpoint statement

A checkpoint should authenticate at least:

```text
protocol_version
cryptographic_suite_id
final_state_identifier
final_epoch
final_tag
history_commitment
checkpoint_policy_id
auditor/quorum context
application/domain context if semantically relevant
```

If path length `k` is claimed as part of the certificate semantics, it must also be authenticated rather than merely displayed.

### Final-result proof statement

All verifier-critical proof bases, generators, dimensions, bounds, and context identifiers must be either:

1. derived deterministically from authenticated public parameters; or
2. included in the authenticated statement.

The verifier must not accept arbitrary caller-supplied bases whose selection changes the meaning or soundness of the proof.

## 5. Domain separation

Use independent labels for at least:

```text
CAMH-CUFE/KEY
CAMH-CUFE/TOKEN
CAMH-CUFE/STATE
CAMH-CUFE/HISTORY/INIT
CAMH-CUFE/HISTORY/LINK
CAMH-CUFE/CHECKPOINT
CAMH-CUFE/FINAL-PROOF
CAMH-CUFE/TRANSCRIPT
```

No object should rely on field structure alone to prevent cross-protocol or cross-object signature reuse.

## 6. Group-element encoding

For a real cryptographic backend:

- use the canonical compressed encoding defined by the selected curve/library/standard;
- reject non-canonical representations;
- perform subgroup/on-curve checks as required by the library and protocol;
- record the exact suite/version in reproducibility metadata.

Do not serialize group objects with `pickle` for protocol-size claims.

## 7. Wire-size measurement

Headline communication/storage measurements must use the canonical protocol encoding.

Acceptable labels:

```text
canonical wire bytes
encoded transition bytes
encoded retained-history bytes
encoded checkpoint bytes
```

Development-only metrics such as Python `pickle` size may be retained in diagnostic scripts but must not be reported as protocol compactness.

## 8. Test obligations

The test suite must include:

1. deterministic round-trip encoding/decoding;
2. rejection of truncated encodings;
3. rejection of trailing bytes when a single object is expected;
4. rejection of unknown protocol versions/object types unless explicitly supported;
5. distinct encodings for distinct field tuples;
6. property/fuzz tests for length-boundary cases;
7. golden test vectors frozen in the repository;
8. cross-process/cross-language vectors if a second implementation is introduced.

## 9. Proof obligation

The manuscript may assume injective/canonical serialization only after the concrete encoding is defined and the proof maps semantic objects to this byte-level grammar. The implementation tests support conformance; the mathematical argument establishes why distinct valid protocol objects cannot share one valid canonical encoding.
