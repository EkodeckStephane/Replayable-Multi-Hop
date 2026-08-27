"""Reference model for CAMH-CUFE level-aware transition authorization.

This module specifies protocol semantics used by tests and documentation.  It is
NOT a cryptographic enforcement mechanism and must not be cited as security
evidence for a concrete CUFE construction.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .protocol_objects import AuthorizationState


@dataclass(frozen=True)
class TransitionRule:
    """One exact state-global authorization edge."""

    source: AuthorizationState
    destination: AuthorizationState

    def __post_init__(self) -> None:
        if self.destination.epoch != self.source.epoch + 1:
            raise ValueError("transition must advance exactly one epoch")

    def accepts_source(self, state: AuthorizationState) -> bool:
        """Return True iff *state* is the exact authorized source state."""
        return state == self.source

    def composes_with(self, next_rule: "TransitionRule") -> bool:
        """Composition is opt-in: exact destination/source state equality."""
        return self.destination == next_rule.source


def validate_rule_path(rules: Iterable[TransitionRule]) -> tuple[TransitionRule, ...]:
    """Validate exact level-aware continuity of a transition-rule sequence.

    Visible tag equality alone is deliberately insufficient.
    """
    path = tuple(rules)
    for previous, current in zip(path, path[1:]):
        if not previous.composes_with(current):
            raise ValueError(
                "transition path is not explicitly composable: "
                "previous destination must equal next source exactly"
            )
    return path
