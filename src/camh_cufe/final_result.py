"""Reference boundary for CAMH-CUFE final-result proof verification.

This module freezes the public statement and verifier context.  It deliberately
does NOT implement or claim a sound cryptographic proof system.  A concrete
backend supplies the proof object and relation verifier; this wrapper ensures
that the verifier sees the exact canonical statement and internally derived
bases rather than caller-selected proof parameters.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .domains import FINAL_RESULT_STATEMENT
from .pi4_context import Pi4Bases, derive_pi4_bases
from .protocol_objects import AuthorizationState, encode_final_result_statement


ProofRelationVerifier = Callable[[bytes, bytes, Pi4Bases], bool]


@dataclass(frozen=True)
class FinalResultStatement:
    """Complete public statement whose fields define the final-result claim."""

    suite_id: bytes
    relation_id: bytes
    public_parameters_digest: bytes
    final_state: AuthorizationState
    dimension: int
    final_ciphertext: bytes
    function_public_view: bytes
    functional_key_public_view: bytes
    result_encoding_id: bytes
    claimed_result: bytes
    history_digest: bytes
    history_length: int
    application_context: bytes = b""

    def encode(self) -> bytes:
        return encode_final_result_statement(
            suite_id=self.suite_id,
            relation_id=self.relation_id,
            public_parameters_digest=self.public_parameters_digest,
            final_state=self.final_state,
            dimension=self.dimension,
            final_ciphertext=self.final_ciphertext,
            function_public_view=self.function_public_view,
            functional_key_public_view=self.functional_key_public_view,
            result_encoding_id=self.result_encoding_id,
            claimed_result=self.claimed_result,
            history_digest=self.history_digest,
            history_length=self.history_length,
            application_context=self.application_context,
        )


def final_result_transcript(statement: FinalResultStatement) -> bytes:
    """Return a domain-separated transcript prefix plus canonical statement.

    The concrete proof system may hash this transcript according to its own
    standard.  Returning framed bytes here avoids silently committing to a
    Fiat-Shamir hash before the proof system is selected.
    """
    if not isinstance(statement, FinalResultStatement):
        raise TypeError("statement must be FinalResultStatement")
    encoded = statement.encode()
    domain = FINAL_RESULT_STATEMENT
    return (
        len(domain).to_bytes(2, "big")
        + domain
        + len(encoded).to_bytes(8, "big")
        + encoded
    )


def derive_statement_pi4_bases(G, statement: FinalResultStatement) -> Pi4Bases:
    """Derive verifier-critical bases only from the bound statement context."""
    if not isinstance(statement, FinalResultStatement):
        raise TypeError("statement must be FinalResultStatement")
    # Calling encode first performs all statement-domain validation, including
    # digest widths and positive dimension, before deriving proof context.
    statement.encode()
    return derive_pi4_bases(
        G,
        statement.dimension,
        suite_id=statement.suite_id,
        public_parameters_digest=statement.public_parameters_digest,
        relation_id=statement.relation_id,
    )


def verify_final_result_reference(
    G,
    statement: FinalResultStatement,
    proof: bytes,
    verify_relation: ProofRelationVerifier,
) -> bool:
    """Verify a final proof using only internally derived verifier context.

    This function intentionally has no `bases` or `pi4_bases` parameter.
    `verify_relation` receives:

        (domain-separated canonical transcript, proof, canonical bases)

    Its return value is only as meaningful as the concrete proof verifier it
    wraps.  This reference layer establishes statement/base binding and API
    discipline; it does not establish proof-system soundness.
    """
    if not isinstance(statement, FinalResultStatement):
        raise TypeError("statement must be FinalResultStatement")
    if not isinstance(proof, (bytes, bytearray, memoryview)):
        raise TypeError("proof must be bytes-like")
    if not callable(verify_relation):
        raise TypeError("verify_relation must be callable")

    transcript = final_result_transcript(statement)
    bases = derive_statement_pi4_bases(G, statement)
    return bool(verify_relation(transcript, bytes(proof), bases))
