# CAMH-CUFE canonical encoding golden vectors

These vectors freeze byte-level protocol encoding version `1`. They are intentionally small and human-checkable. Any intentional wire-format change must increment the protocol version and replace the vectors in a reviewed change.

All hex strings are lowercase renderings of the exact byte sequence.

## Vector 1 — generic TLV object

Input:

```python
encode_object(
    7,
    [
        Field(1, b"A"),
        Field(2, uint32(3)),
        Field(3, uint64(11)),
    ],
)
```

Expected bytes:

```text
43414d482d43554645000001000700030001000000000000000141000200000000000000040000000300030000000000000008000000000000000b
```

## Vector 2 — authorization state

Input:

```python
encode_state(
    AuthorizationState(tag=b"A", epoch=0),
    suite_id=b"S1",
)
```

Expected bytes:

```text
43414d482d435546450000011001000300010000000000000002533100020000000000000001410003000000000000000400000000
```

## Compatibility rule

A conforming implementation of protocol version `1` must produce these exact bytes and must decode them back to the same typed values. The decoder must continue to reject non-canonical field order, duplicate field identifiers, truncated values, unsupported versions, and trailing bytes.
