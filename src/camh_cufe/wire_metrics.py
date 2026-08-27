"""Canonical wire-size accounting for CAMH-CUFE protocol objects.

Only bytes produced by CAMH-CUFE canonical encoders are measured here.  This
module intentionally exposes typed helpers rather than a generic Python object
serializer so that protocol-size evidence cannot silently become a pickle or
`sys.getsizeof` measurement.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .protocol_objects import (
    AuthorizationState,
    encode_checkpoint_statement,
    encode_final_result_statement,
    encode_retained_transition_record,
    encode_state,
    encode_transition_statement,
)


@dataclass(frozen=True)
class WireSize:
    object_class: str
    byte_length: int
    evidence_class: str = "canonical-wire"

    def __post_init__(self) -> None:
        if self.byte_length < 0:
            raise ValueError("byte_length must be non-negative")
        if self.evidence_class != "canonical-wire":
            raise ValueError("wire metrics must be canonical-wire evidence")


def _measurement(name: str, encoded: bytes) -> WireSize:
    if not isinstance(encoded, bytes):
        raise TypeError("canonical encoder must return bytes")
    return WireSize(name, len(encoded))


def measure_state(*, suite_id: bytes, state: AuthorizationState) -> WireSize:
    return _measurement("authorization-state", encode_state(state, suite_id=suite_id))


def measure_transition(
    *,
    suite_id: bytes,
    source: AuthorizationState,
    destination: AuthorizationState,
    dimension: int,
    update_elements: Iterable[bytes],
) -> WireSize:
    return _measurement(
        "transition-statement",
        encode_transition_statement(
            suite_id=suite_id,
            source=source,
            destination=destination,
            dimension=dimension,
            update_elements=update_elements,
        ),
    )


def measure_retained_transition(
    *,
    suite_id: bytes,
    transition_statement: bytes,
    source_ciphertext: bytes,
    destination_ciphertext: bytes,
    token_signature: bytes,
    history_digest: bytes,
) -> WireSize:
    return _measurement(
        "retained-transition-record",
        encode_retained_transition_record(
            suite_id=suite_id,
            transition_statement=transition_statement,
            source_ciphertext=source_ciphertext,
            destination_ciphertext=destination_ciphertext,
            token_signature=token_signature,
            history_digest=history_digest,
        ),
    )


def measure_checkpoint_statement(
    *,
    suite_id: bytes,
    final_state: AuthorizationState,
    final_ciphertext: bytes,
    history_digest: bytes,
    history_length: int,
    policy_id: bytes,
    application_context: bytes = b"",
) -> WireSize:
    return _measurement(
        "checkpoint-statement",
        encode_checkpoint_statement(
            suite_id=suite_id,
            final_state=final_state,
            final_ciphertext=final_ciphertext,
            history_digest=history_digest,
            history_length=history_length,
            policy_id=policy_id,
            application_context=application_context,
        ),
    )


def measure_final_result_statement(
    *,
    suite_id: bytes,
    relation_id: bytes,
    public_parameters_digest: bytes,
    final_state: AuthorizationState,
    dimension: int,
    final_ciphertext: bytes,
    function_public_view: bytes,
    functional_key_public_view: bytes,
    result_encoding_id: bytes,
    claimed_result: bytes,
    history_digest: bytes,
    history_length: int,
    application_context: bytes = b"",
) -> WireSize:
    return _measurement(
        "final-result-statement",
        encode_final_result_statement(
            suite_id=suite_id,
            relation_id=relation_id,
            public_parameters_digest=public_parameters_digest,
            final_state=final_state,
            dimension=dimension,
            final_ciphertext=final_ciphertext,
            function_public_view=function_public_view,
            functional_key_public_view=functional_key_public_view,
            result_encoding_id=result_encoding_id,
            claimed_result=claimed_result,
            history_digest=history_digest,
            history_length=history_length,
            application_context=application_context,
        ),
    )
