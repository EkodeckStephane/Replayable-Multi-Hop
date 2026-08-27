"""Reference verifier for CAMH-CUFE retained linear histories.

This module checks canonical statement reconstruction, exact authorization-state
continuity, ciphertext continuity, rolling-history commitments, and an injected
token-signature predicate.  It is a conformance/reference layer, not a proof of
cryptographic unforgeability or CUFE confidentiality.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .authorization_graph import AuthorizationGraph
from .protocol_objects import (
    AuthorizationState,
    encode_transition_statement,
    history_init,
    history_link,
)
from .state_policy import TransitionRule


class HistoryVerificationError(ValueError):
    """Raised when a retained history is inconsistent or unauthenticated."""


TokenSignatureVerifier = Callable[[bytes, bytes], bool]


@dataclass(frozen=True)
class RetainedTransition:
    """One lineage-specific retained use of a state-global transition token."""

    source: AuthorizationState
    destination: AuthorizationState
    dimension: int
    update_elements: tuple[bytes, ...]
    transition_statement: bytes
    source_ciphertext: bytes
    destination_ciphertext: bytes
    token_signature: bytes
    history_digest: bytes

    def __post_init__(self) -> None:
        object.__setattr__(self, "update_elements", tuple(bytes(x) for x in self.update_elements))
        object.__setattr__(self, "transition_statement", bytes(self.transition_statement))
        object.__setattr__(self, "source_ciphertext", bytes(self.source_ciphertext))
        object.__setattr__(self, "destination_ciphertext", bytes(self.destination_ciphertext))
        object.__setattr__(self, "token_signature", bytes(self.token_signature))
        object.__setattr__(self, "history_digest", bytes(self.history_digest))


@dataclass(frozen=True)
class VerifiedHistory:
    initial_state: AuthorizationState
    final_state: AuthorizationState
    final_ciphertext: bytes
    history_digest: bytes
    history_length: int


def make_retained_transition(
    *,
    suite_id: bytes,
    previous_digest: bytes,
    source: AuthorizationState,
    destination: AuthorizationState,
    dimension: int,
    update_elements: Iterable[bytes],
    source_ciphertext: bytes,
    destination_ciphertext: bytes,
    token_signature: bytes,
) -> RetainedTransition:
    """Build one canonical retained record after a token has been authenticated.

    This helper does not create a signature.  The caller supplies the signature
    over the canonical transition statement according to the selected token
    authentication mechanism.
    """
    elements = tuple(bytes(x) for x in update_elements)
    statement = encode_transition_statement(
        suite_id=suite_id,
        source=source,
        destination=destination,
        dimension=dimension,
        update_elements=elements,
    )
    digest = history_link(
        suite_id=suite_id,
        previous_digest=previous_digest,
        transition_statement=statement,
        source_ciphertext=source_ciphertext,
        destination_ciphertext=destination_ciphertext,
        token_signature=token_signature,
    )
    return RetainedTransition(
        source=source,
        destination=destination,
        dimension=dimension,
        update_elements=elements,
        transition_statement=statement,
        source_ciphertext=source_ciphertext,
        destination_ciphertext=destination_ciphertext,
        token_signature=token_signature,
        history_digest=digest,
    )


def verify_retained_history(
    *,
    suite_id: bytes,
    initial_state: AuthorizationState,
    fresh_ciphertext: bytes,
    records: Iterable[RetainedTransition],
    authorization_graph: AuthorizationGraph,
    verify_token_signature: TokenSignatureVerifier,
    expected_final_state: AuthorizationState | None = None,
    expected_final_ciphertext: bytes | None = None,
    expected_history_digest: bytes | None = None,
) -> VerifiedHistory:
    """Replay and verify a complete retained history from an accepted fresh root.

    Verification is strict:
    - the root must be a canonical level-0 fresh state;
    - every transition must be an exact issued authorization edge;
    - the retained transition statement must equal canonical reconstruction;
    - the state and ciphertext outputs of one record must be the inputs of the
      next record exactly;
    - the injected token-signature verifier must accept each statement;
    - every rolling history digest is recomputed and compared;
    - optional displayed final claims are checked exactly.
    """
    if initial_state.epoch != 0:
        raise HistoryVerificationError("fresh retained history must start at epoch 0")
    if not callable(verify_token_signature):
        raise TypeError("verify_token_signature must be callable")

    current_state = initial_state
    current_ciphertext = bytes(fresh_ciphertext)
    try:
        current_digest = history_init(
            suite_id=suite_id,
            initial_state=initial_state,
            fresh_ciphertext=current_ciphertext,
        )
    except (TypeError, ValueError) as exc:
        raise HistoryVerificationError(str(exc)) from exc

    path = tuple(records)
    for index, record in enumerate(path):
        if not isinstance(record, RetainedTransition):
            raise TypeError("records must contain RetainedTransition values")

        if record.source != current_state:
            raise HistoryVerificationError(
                f"record {index}: source authorization state breaks path continuity"
            )
        if record.source_ciphertext != current_ciphertext:
            raise HistoryVerificationError(
                f"record {index}: source ciphertext breaks lineage continuity"
            )

        try:
            rule = TransitionRule(record.source, record.destination)
        except ValueError as exc:
            raise HistoryVerificationError(f"record {index}: {exc}") from exc
        if not authorization_graph.contains(rule):
            raise HistoryVerificationError(
                f"record {index}: exact transition edge was not authorized"
            )

        try:
            canonical_statement = encode_transition_statement(
                suite_id=suite_id,
                source=record.source,
                destination=record.destination,
                dimension=record.dimension,
                update_elements=record.update_elements,
            )
        except (TypeError, ValueError) as exc:
            raise HistoryVerificationError(f"record {index}: {exc}") from exc

        if record.transition_statement != canonical_statement:
            raise HistoryVerificationError(
                f"record {index}: retained transition statement is non-canonical or altered"
            )
        if not verify_token_signature(canonical_statement, record.token_signature):
            raise HistoryVerificationError(
                f"record {index}: token authentication failed"
            )

        try:
            computed_digest = history_link(
                suite_id=suite_id,
                previous_digest=current_digest,
                transition_statement=canonical_statement,
                source_ciphertext=record.source_ciphertext,
                destination_ciphertext=record.destination_ciphertext,
                token_signature=record.token_signature,
            )
        except (TypeError, ValueError) as exc:
            raise HistoryVerificationError(f"record {index}: {exc}") from exc

        if record.history_digest != computed_digest:
            raise HistoryVerificationError(
                f"record {index}: rolling history commitment mismatch"
            )

        current_state = record.destination
        current_ciphertext = record.destination_ciphertext
        current_digest = computed_digest

    if expected_final_state is not None and current_state != expected_final_state:
        raise HistoryVerificationError("displayed final authorization state mismatch")
    if (
        expected_final_ciphertext is not None
        and current_ciphertext != bytes(expected_final_ciphertext)
    ):
        raise HistoryVerificationError("displayed final ciphertext mismatch")
    if expected_history_digest is not None:
        expected_history_digest = bytes(expected_history_digest)
        if len(expected_history_digest) != 32:
            raise HistoryVerificationError("expected history digest must be 32 bytes")
        if current_digest != expected_history_digest:
            raise HistoryVerificationError("displayed final history digest mismatch")

    return VerifiedHistory(
        initial_state=initial_state,
        final_state=current_state,
        final_ciphertext=current_ciphertext,
        history_digest=current_digest,
        history_length=len(path),
    )
