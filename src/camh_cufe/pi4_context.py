"""Deterministic public context for the CAMH-CUFE final-result proof.

The verifier never accepts caller-selected commitment bases as part of the
meaning of pi4. Bases are deterministically derived from the authenticated
suite, exact public-parameter digest, relation identifier, and statement
dimension.
"""
from __future__ import annotations

from dataclasses import dataclass

from .domains import PI4_BASES

DOMAIN = PI4_BASES


@dataclass(frozen=True)
class Pi4Bases:
    Gv: tuple
    hv: object
    Gk: tuple
    hk: object


def _bytes_1_255(value: bytes, name: str) -> bytes:
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes-like")
    value = bytes(value)
    if not value or len(value) > 255:
        raise ValueError(f"{name} length must be in 1..255")
    return value


def _digest32(value: bytes, name: str) -> bytes:
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes-like")
    value = bytes(value)
    if len(value) != 32:
        raise ValueError(f"{name} must be 32 bytes")
    return value


def _context(
    suite_id: bytes,
    dimension: int,
    *,
    public_parameters_digest: bytes,
    relation_id: bytes,
) -> tuple[bytes, bytes]:
    suite_id = _bytes_1_255(suite_id, "suite_id")
    relation_id = _bytes_1_255(relation_id, "relation_id")
    public_parameters_digest = _digest32(
        public_parameters_digest, "public_parameters_digest"
    )
    if dimension <= 0 or dimension >= 2**32:
        raise ValueError("dimension must be in 1..2^32-1")

    # Fixed/length-delimited framing: no caller-controlled textual concatenation.
    encoded = (
        bytes([len(suite_id)])
        + suite_id
        + public_parameters_digest
        + bytes([len(relation_id)])
        + relation_id
        + dimension.to_bytes(4, "big")
    )
    return DOMAIN, encoded


def derive_pi4_bases(
    G,
    dimension: int,
    *,
    suite_id: bytes,
    public_parameters_digest: bytes,
    relation_id: bytes,
) -> Pi4Bases:
    """Derive all pi4 commitment bases deterministically.

    `G` must expose `hash_to_g1(*parts)`; the concrete real backend is
    responsible for standards-conformant hash-to-curve and subgroup handling.
    The derived bases are setup/relation specific because the context commits to
    the exact public-parameter digest and relation identifier.
    """
    domain, ctx = _context(
        suite_id,
        dimension,
        public_parameters_digest=public_parameters_digest,
        relation_id=relation_id,
    )
    Gv = tuple(G.hash_to_g1(domain, ctx, b"v", i) for i in range(dimension))
    hv = G.hash_to_g1(domain, ctx, b"v-rand")
    Gk = tuple(G.hash_to_g1(domain, ctx, b"k", j) for j in range(2))
    hk = G.hash_to_g1(domain, ctx, b"k-rand")
    return Pi4Bases(Gv=Gv, hv=hv, Gk=Gk, hk=hk)


def bases_equal(G, left: Pi4Bases, right: Pi4Bases) -> bool:
    if len(left.Gv) != len(right.Gv) or len(left.Gk) != len(right.Gk):
        return False
    return (
        all(G.eq(a, b) for a, b in zip(left.Gv, right.Gv))
        and G.eq(left.hv, right.hv)
        and all(G.eq(a, b) for a, b in zip(left.Gk, right.Gk))
        and G.eq(left.hk, right.hk)
    )


def require_canonical_pi4_bases(
    G,
    supplied: Pi4Bases,
    dimension: int,
    *,
    suite_id: bytes,
    public_parameters_digest: bytes,
    relation_id: bytes,
) -> Pi4Bases:
    """Return canonical bases or reject any caller-substituted set.

    This helper remains useful for migration/testing. The final-result reference
    verifier derives bases internally and therefore does not accept `supplied`
    bases at all.
    """
    canonical = derive_pi4_bases(
        G,
        dimension,
        suite_id=suite_id,
        public_parameters_digest=public_parameters_digest,
        relation_id=relation_id,
    )
    if not bases_equal(G, supplied, canonical):
        raise ValueError("non-canonical pi4 bases")
    return canonical
