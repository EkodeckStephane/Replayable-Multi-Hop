"""Canonical byte encoding for CAMH-CUFE protocol objects.

Authenticated objects use a versioned TLV envelope; every variable-length
field carries an explicit length. Parsing rejects truncation, duplicate field
identifiers, unsupported versions, non-canonical field ordering, and trailing
bytes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

MAGIC = b"CAMH-CUFE\x00"
VERSION = 1


class EncodingError(ValueError):
    """Raised when a purported canonical encoding is invalid."""


@dataclass(frozen=True)
class Field:
    type_id: int
    value: bytes


def _u16(value: int) -> bytes:
    if not 0 <= value < 2**16:
        raise EncodingError("uint16 out of range")
    return int(value).to_bytes(2, "big")


def _u32(value: int) -> bytes:
    if not 0 <= value < 2**32:
        raise EncodingError("uint32 out of range")
    return int(value).to_bytes(4, "big")


def _u64(value: int) -> bytes:
    if not 0 <= value < 2**64:
        raise EncodingError("uint64 out of range")
    return int(value).to_bytes(8, "big")


def uint32(value: int) -> bytes:
    """Canonical 32-bit unsigned integer payload."""
    return _u32(value)


def uint64(value: int) -> bytes:
    """Canonical 64-bit unsigned integer payload."""
    return _u64(value)


def opaque(value: bytes | bytearray | memoryview) -> bytes:
    """Convert an opaque byte string without text normalization."""
    return bytes(value)


def utf8(value: str) -> bytes:
    """UTF-8 helper for application-facing labels."""
    if not isinstance(value, str):
        raise EncodingError("expected str")
    return value.encode("utf-8")


def encode_object(
    object_type: int,
    fields: Sequence[Field] | Iterable[Field],
    *,
    version: int = VERSION,
) -> bytes:
    """Encode one canonical protocol object.

    Field identifiers must be unique and strictly increasing. Requiring a fixed
    order prevents semantically equivalent encodings with permuted TLVs.
    """
    if not 0 <= object_type < 2**16:
        raise EncodingError("object_type out of range")
    if version != VERSION:
        raise EncodingError("unsupported protocol version")

    fields = tuple(fields)
    previous = -1
    body = bytearray()
    for field in fields:
        if not isinstance(field, Field):
            raise EncodingError("expected Field")
        if not 0 <= field.type_id < 2**16:
            raise EncodingError("field type out of range")
        if field.type_id <= previous:
            raise EncodingError(
                "field identifiers must be unique and strictly increasing"
            )
        previous = field.type_id
        value = bytes(field.value)
        body += _u16(field.type_id)
        body += _u64(len(value))
        body += value

    return MAGIC + _u16(version) + _u16(object_type) + _u16(len(fields)) + bytes(body)


def decode_object(
    data: bytes | bytearray | memoryview,
    *,
    expected_type: int | None = None,
) -> tuple[int, tuple[Field, ...]]:
    """Strictly decode one canonical protocol object."""
    data = bytes(data)
    minimum = len(MAGIC) + 6
    if len(data) < minimum:
        raise EncodingError("truncated object header")
    if not data.startswith(MAGIC):
        raise EncodingError("wrong protocol magic")

    offset = len(MAGIC)
    version = int.from_bytes(data[offset:offset + 2], "big")
    offset += 2
    if version != VERSION:
        raise EncodingError("unsupported protocol version")

    object_type = int.from_bytes(data[offset:offset + 2], "big")
    offset += 2
    if expected_type is not None and object_type != expected_type:
        raise EncodingError("unexpected object type")

    field_count = int.from_bytes(data[offset:offset + 2], "big")
    offset += 2
    fields: list[Field] = []
    previous = -1

    for _ in range(field_count):
        if offset + 10 > len(data):
            raise EncodingError("truncated field header")
        type_id = int.from_bytes(data[offset:offset + 2], "big")
        offset += 2
        length = int.from_bytes(data[offset:offset + 8], "big")
        offset += 8
        if type_id <= previous:
            raise EncodingError("non-canonical field ordering")
        previous = type_id
        if length > len(data) - offset:
            raise EncodingError("truncated field value")
        value = data[offset:offset + length]
        offset += length
        fields.append(Field(type_id, value))

    if offset != len(data):
        raise EncodingError("trailing bytes")
    return object_type, tuple(fields)
