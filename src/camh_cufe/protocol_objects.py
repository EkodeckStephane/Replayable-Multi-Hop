"""Canonical CAMH-CUFE protocol statements and history commitments."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable

from .domains import HISTORY_INIT, HISTORY_LINK
from .encoding import Field, encode_object, uint32, uint64

OBJ_STATE = 0x1001
OBJ_ELEMENT_VECTOR = 0x1002
OBJ_TRANSITION = 0x1003
OBJ_HISTORY_INIT = 0x1004
OBJ_HISTORY_LINK = 0x1005
OBJ_CHECKPOINT = 0x1006
OBJ_RETAINED_TRANSITION = 0x1007
OBJ_FINAL_RESULT_STATEMENT = 0x1008


@dataclass(frozen=True)
class AuthorizationState:
    tag: bytes
    epoch: int

    def encode(self, *, suite_id: bytes) -> bytes:
        return encode_state(self, suite_id=suite_id)


def _nonempty(value: bytes, name: str) -> bytes:
    value = bytes(value)
    if not value:
        raise ValueError(f"{name} must be non-empty")
    return value


def _digest32(value: bytes, name: str) -> bytes:
    value = bytes(value)
    if len(value) != 32:
        raise ValueError(f"{name} must be 32 bytes")
    return value


def _domain_hash(domain: bytes, body: bytes) -> bytes:
    """Hash a canonical object under an explicit semantic domain."""
    h = hashlib.sha256()
    h.update(len(domain).to_bytes(2, "big"))
    h.update(domain)
    h.update(body)
    return h.digest()


def encode_state(state: AuthorizationState, *, suite_id: bytes) -> bytes:
    return encode_object(OBJ_STATE, [
        Field(1, _nonempty(suite_id, "suite_id")),
        Field(2, _nonempty(state.tag, "tag")),
        Field(3, uint32(state.epoch)),
    ])


def encode_element_vector(elements: Iterable[bytes]) -> bytes:
    elements = tuple(bytes(e) for e in elements)
    if not elements:
        raise ValueError("element vector must be non-empty")
    if len(elements) >= 2**16:
        raise ValueError("too many elements")
    fields = [Field(1, uint32(len(elements)))]
    for index, element in enumerate(elements, start=2):
        if not element:
            raise ValueError("group element encoding must be non-empty")
        fields.append(Field(index, element))
    return encode_object(OBJ_ELEMENT_VECTOR, fields)


def encode_transition_statement(
    *,
    suite_id: bytes,
    source: AuthorizationState,
    destination: AuthorizationState,
    dimension: int,
    update_elements: Iterable[bytes],
) -> bytes:
    if destination.epoch != source.epoch + 1:
        raise ValueError("destination epoch must equal source epoch + 1")
    if dimension <= 0:
        raise ValueError("dimension must be positive")
    return encode_object(OBJ_TRANSITION, [
        Field(1, _nonempty(suite_id, "suite_id")),
        Field(2, encode_state(source, suite_id=suite_id)),
        Field(3, encode_state(destination, suite_id=suite_id)),
        Field(4, uint32(dimension)),
        Field(5, encode_element_vector(update_elements)),
    ])


def history_init(
    *,
    suite_id: bytes,
    initial_state: AuthorizationState,
    fresh_ciphertext: bytes,
) -> bytes:
    """Commit to the exact accepted fresh root state and ciphertext.

    Binding the authorization state explicitly prevents a byte-identical payload
    from being re-labelled as a different root tag/epoch by the audit layer.
    """
    body = encode_object(OBJ_HISTORY_INIT, [
        Field(1, _nonempty(suite_id, "suite_id")),
        Field(2, encode_state(initial_state, suite_id=suite_id)),
        Field(3, _nonempty(fresh_ciphertext, "fresh_ciphertext")),
    ])
    return _domain_hash(HISTORY_INIT, body)


def history_link(
    *,
    suite_id: bytes,
    previous_digest: bytes,
    transition_statement: bytes,
    source_ciphertext: bytes,
    destination_ciphertext: bytes,
    token_signature: bytes,
) -> bytes:
    previous_digest = _digest32(previous_digest, "previous_digest")
    body = encode_object(OBJ_HISTORY_LINK, [
        Field(1, _nonempty(suite_id, "suite_id")),
        Field(2, previous_digest),
        Field(3, _nonempty(transition_statement, "transition_statement")),
        Field(4, _nonempty(source_ciphertext, "source_ciphertext")),
        Field(5, _nonempty(destination_ciphertext, "destination_ciphertext")),
        Field(6, _nonempty(token_signature, "token_signature")),
    ])
    return _domain_hash(HISTORY_LINK, body)


def encode_checkpoint_statement(
    *,
    suite_id: bytes,
    final_state: AuthorizationState,
    final_ciphertext: bytes,
    history_digest: bytes,
    history_length: int,
    policy_id: bytes,
    application_context: bytes = b"",
) -> bytes:
    history_digest = _digest32(history_digest, "history_digest")
    fields = [
        Field(1, _nonempty(suite_id, "suite_id")),
        Field(2, encode_state(final_state, suite_id=suite_id)),
        Field(3, _nonempty(final_ciphertext, "final_ciphertext")),
        Field(4, history_digest),
        Field(5, uint64(history_length)),
        Field(6, _nonempty(policy_id, "policy_id")),
    ]
    if application_context:
        fields.append(Field(7, bytes(application_context)))
    return encode_object(OBJ_CHECKPOINT, fields)


def encode_retained_transition_record(
    *,
    suite_id: bytes,
    transition_statement: bytes,
    source_ciphertext: bytes,
    destination_ciphertext: bytes,
    token_signature: bytes,
    history_digest: bytes,
) -> bytes:
    """Encode one retained lineage record for storage/communication metrics.

    Concrete ciphertext and signature byte strings supplied here must themselves
    already be canonical encodings from their respective backend/suite.  This
    function does not legitimize Python-object or pickle serialization.
    """
    history_digest = _digest32(history_digest, "history_digest")
    return encode_object(OBJ_RETAINED_TRANSITION, [
        Field(1, _nonempty(suite_id, "suite_id")),
        Field(2, _nonempty(transition_statement, "transition_statement")),
        Field(3, _nonempty(source_ciphertext, "source_ciphertext")),
        Field(4, _nonempty(destination_ciphertext, "destination_ciphertext")),
        Field(5, _nonempty(token_signature, "token_signature")),
        Field(6, history_digest),
    ])


def encode_final_result_statement(
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
) -> bytes:
    """Encode the complete public statement for a final-result proof.

    The byte strings supplied for ciphertext, function/key public views, and
    claimed result must already be canonical according to the retained concrete
    suite.  This envelope freezes *what* a final proof is about; it does not by
    itself establish proof-system soundness.
    """
    if dimension <= 0:
        raise ValueError("dimension must be positive")
    public_parameters_digest = _digest32(
        public_parameters_digest, "public_parameters_digest"
    )
    history_digest = _digest32(history_digest, "history_digest")
    fields = [
        Field(1, _nonempty(suite_id, "suite_id")),
        Field(2, _nonempty(relation_id, "relation_id")),
        Field(3, public_parameters_digest),
        Field(4, encode_state(final_state, suite_id=suite_id)),
        Field(5, uint32(dimension)),
        Field(6, _nonempty(final_ciphertext, "final_ciphertext")),
        Field(7, _nonempty(function_public_view, "function_public_view")),
        Field(8, _nonempty(functional_key_public_view, "functional_key_public_view")),
        Field(9, _nonempty(result_encoding_id, "result_encoding_id")),
        Field(10, _nonempty(claimed_result, "claimed_result")),
        Field(11, history_digest),
        Field(12, uint64(history_length)),
    ]
    if application_context:
        fields.append(Field(13, bytes(application_context)))
    return encode_object(OBJ_FINAL_RESULT_STATEMENT, fields)
