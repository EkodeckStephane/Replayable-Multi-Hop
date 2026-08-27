"""Deterministic public context for the CAMH-CUFE final-result proof.

The verifier never accepts caller-selected commitment bases as part of the
meaning of pi4. Bases are deterministically derived from authenticated suite
context and the statement dimension.
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


def _context(suite_id: bytes, dimension: int) -> tuple[bytes, bytes]:
    if not isinstance(suite_id, (bytes, bytearray, memoryview)):
        raise TypeError("suite_id must be bytes-like")
    suite_id = bytes(suite_id)
    if not suite_id or len(suite_id) > 255:
        raise ValueError("suite_id length must be in 1..255")
    if dimension <= 0 or dimension >= 2**32:
        raise ValueError("dimension must be in 1..2^32-1")
    encoded = bytes([len(suite_id)]) + suite_id + dimension.to_bytes(4, "big")
    return DOMAIN, encoded


def derive_pi4_bases(G, dimension: int, *, suite_id: bytes) -> Pi4Bases:
    """Derive all pi4 commitment bases deterministically.

    `G` must expose `hash_to_g1(*parts)`; the concrete real backend is
    responsible for standards-conformant hash-to-curve and subgroup handling.
    """
    domain, ctx = _context(suite_id, dimension)
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
) -> Pi4Bases:
    """Return canonical bases or reject any caller-substituted set."""
    canonical = derive_pi4_bases(G, dimension, suite_id=suite_id)
    if not bases_equal(G, supplied, canonical):
        raise ValueError("non-canonical pi4 bases")
    return canonical
