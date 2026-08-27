"""Transparent exponent-level oracle for CAMH-CUFE algebra.

This module is a differential/correctness oracle only. It does not model group
hardness and must never be used as cryptographic performance or confidentiality
evidence.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .domains import SYMBOLIC_TAG
from .protocol_objects import AuthorizationState


def _dot(left, right, p):
    if len(left) != len(right):
        raise ValueError("dimension mismatch")
    return sum((int(a) * int(b)) % p for a, b in zip(left, right)) % p


@dataclass(frozen=True)
class SymbolicCiphertext:
    state: AuthorizationState
    c0_r: tuple[int, int]
    payload_exponents: tuple[int, ...]


class SymbolicCAMHCUFE:
    """Exponent-level algebraic oracle for the repeated-update invariant."""

    def __init__(self, *, p: int, U, tag_key: bytes):
        if p <= 2:
            raise ValueError("p must be > 2")
        self.p = int(p)
        self.U = tuple(tuple(int(x) % p for x in row) for row in U)
        if not self.U or any(len(row) != 2 for row in self.U):
            raise ValueError("U must contain 2-dimensional rows")
        self.tag_key = bytes(tag_key)
        if not self.tag_key:
            raise ValueError("tag_key must be non-empty")

    def h(self, state: AuthorizationState) -> int:
        h = hashlib.sha256()
        h.update(SYMBOLIC_TAG)
        h.update(len(self.tag_key).to_bytes(4, "big"))
        h.update(self.tag_key)
        h.update(len(state.tag).to_bytes(4, "big"))
        h.update(state.tag)
        h.update(int(state.epoch).to_bytes(4, "big"))
        return int.from_bytes(h.digest(), "big") % self.p

    def encrypt(self, x, *, state: AuthorizationState, r=(7, 11)) -> SymbolicCiphertext:
        x = tuple(int(v) % self.p for v in x)
        if len(x) != len(self.U):
            raise ValueError("message dimension mismatch")
        r = tuple(int(v) % self.p for v in r)
        if len(r) != 2:
            raise ValueError("r must have dimension 2")
        hs = self.h(state)
        payload = tuple(
            (x[j] + hs * _dot(r, self.U[j], self.p)) % self.p
            for j in range(len(x))
        )
        return SymbolicCiphertext(state=state, c0_r=r, payload_exponents=payload)

    def update(
        self,
        ct: SymbolicCiphertext,
        *,
        source: AuthorizationState,
        destination: AuthorizationState,
    ) -> SymbolicCiphertext:
        if ct.state != source:
            raise ValueError("source state mismatch")
        if destination.epoch != source.epoch + 1:
            raise ValueError("destination epoch must equal source epoch + 1")
        delta = (self.h(destination) - self.h(source)) % self.p
        r = ct.c0_r
        payload = tuple(
            (ct.payload_exponents[j] + delta * _dot(r, self.U[j], self.p)) % self.p
            for j in range(len(self.U))
        )
        return SymbolicCiphertext(
            state=destination,
            c0_r=ct.c0_r,
            payload_exponents=payload,
        )

    def decrypt_inner_product(self, ct: SymbolicCiphertext, v) -> int:
        v = tuple(int(x) % self.p for x in v)
        if len(v) != len(self.U):
            raise ValueError("function dimension mismatch")
        S = tuple(
            sum(v[j] * self.U[j][coord] for j in range(len(v))) % self.p
            for coord in range(2)
        )
        aggregate = _dot(v, ct.payload_exponents, self.p)
        mask = self.h(ct.state) * _dot(ct.c0_r, S, self.p)
        return (aggregate - mask) % self.p
