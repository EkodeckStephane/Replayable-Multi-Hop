"""Executable reference semantics for CAMH-CUFE transition authorization.

This module models *which exact state edges have been authorized*.  It is a
policy/conformance oracle only: it does not provide cryptographic enforcement
and must not be cited as a security proof for a concrete CUFE construction.

The baseline model permits branching in the global authorization graph, keeps
individual retained histories linear, and forbids cycles structurally because
every edge advances the authenticated epoch by exactly one.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .protocol_objects import AuthorizationState
from .state_policy import TransitionRule


class AuthorizationError(ValueError):
    """Raised when a claimed path contains an unauthorized exact state edge."""


@dataclass
class AuthorizationGraph:
    """Finite set of explicitly issued, state-global transition rules.

    Visible tag equality never creates an edge.  Reachability is the transitive
    closure of *exact* ``AuthorizationState`` edges that were actually issued.
    """

    _rules: set[TransitionRule] = field(default_factory=set)

    def add(self, rule: TransitionRule) -> TransitionRule:
        if not isinstance(rule, TransitionRule):
            raise TypeError("expected TransitionRule")
        self._rules.add(rule)
        return rule

    def issue(
        self,
        source: AuthorizationState,
        destination: AuthorizationState,
    ) -> TransitionRule:
        """Create and record one exact state-global authorization edge."""
        return self.add(TransitionRule(source, destination))

    def contains(self, rule: TransitionRule) -> bool:
        return rule in self._rules

    def outgoing(self, state: AuthorizationState) -> tuple[TransitionRule, ...]:
        """Return all explicitly authorized outgoing edges from *state*."""
        rules = (rule for rule in self._rules if rule.source == state)
        return tuple(
            sorted(
                rules,
                key=lambda r: (
                    r.destination.epoch,
                    r.destination.tag,
                    r.source.tag,
                ),
            )
        )

    def validate_state_path(
        self,
        states: Iterable[AuthorizationState],
    ) -> tuple[AuthorizationState, ...]:
        """Validate a linear path against the exact issued-edge set.

        A zero-hop path (one state) is valid.  An empty path is rejected because
        it has no claimed starting state.
        """
        path = tuple(states)
        if not path:
            raise AuthorizationError("path must contain a starting state")
        if any(not isinstance(state, AuthorizationState) for state in path):
            raise TypeError("path entries must be AuthorizationState values")

        for source, destination in zip(path, path[1:]):
            try:
                rule = TransitionRule(source, destination)
            except ValueError as exc:
                raise AuthorizationError(str(exc)) from exc
            if rule not in self._rules:
                raise AuthorizationError(
                    "unauthorized exact transition: visible-tag compatibility "
                    "does not substitute for an issued state edge"
                )
        return path

    def reachable(
        self,
        source: AuthorizationState,
        destination: AuthorizationState,
    ) -> bool:
        """Return whether *destination* is reachable through issued exact edges."""
        if source == destination:
            return True
        frontier = [source]
        visited = {source}
        while frontier:
            current = frontier.pop(0)
            for rule in self.outgoing(current):
                nxt = rule.destination
                if nxt == destination:
                    return True
                if nxt not in visited:
                    visited.add(nxt)
                    frontier.append(nxt)
        return False

    def issued_rules(self) -> tuple[TransitionRule, ...]:
        """Return a deterministic snapshot of the issued authorization set."""
        return tuple(
            sorted(
                self._rules,
                key=lambda r: (
                    r.source.epoch,
                    r.source.tag,
                    r.destination.epoch,
                    r.destination.tag,
                ),
            )
        )
