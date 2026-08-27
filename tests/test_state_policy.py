import unittest

from camh_cufe.protocol_objects import AuthorizationState
from camh_cufe.state_policy import TransitionRule, validate_rule_path


class StatePolicyTests(unittest.TestCase):
    def test_visible_tag_match_is_not_enough_for_composition(self):
        a0_b1 = TransitionRule(
            AuthorizationState(b"A", 0),
            AuthorizationState(b"B", 1),
        )
        b0_c1 = TransitionRule(
            AuthorizationState(b"B", 0),
            AuthorizationState(b"C", 1),
        )
        self.assertFalse(a0_b1.composes_with(b0_c1))
        with self.assertRaises(ValueError):
            validate_rule_path([a0_b1, b0_c1])

    def test_explicit_level_compatible_edges_compose(self):
        a0_b1 = TransitionRule(
            AuthorizationState(b"A", 0),
            AuthorizationState(b"B", 1),
        )
        b1_c2 = TransitionRule(
            AuthorizationState(b"B", 1),
            AuthorizationState(b"C", 2),
        )
        self.assertTrue(a0_b1.composes_with(b1_c2))
        self.assertEqual(validate_rule_path([a0_b1, b1_c2]), (a0_b1, b1_c2))

    def test_state_global_rule_accepts_same_source_state_repeatedly(self):
        rule = TransitionRule(
            AuthorizationState(b"A", 0),
            AuthorizationState(b"B", 1),
        )
        # Two distinct ciphertext instances can share the same authorization state.
        # The rule is intentionally not ciphertext-bound.
        self.assertTrue(rule.accepts_source(AuthorizationState(b"A", 0)))
        self.assertTrue(rule.accepts_source(AuthorizationState(b"A", 0)))

    def test_wrong_epoch_is_rejected_even_when_tag_matches(self):
        rule = TransitionRule(
            AuthorizationState(b"B", 1),
            AuthorizationState(b"C", 2),
        )
        self.assertFalse(rule.accepts_source(AuthorizationState(b"B", 0)))
        self.assertFalse(rule.accepts_source(AuthorizationState(b"B", 2)))

    def test_transition_must_advance_one_epoch(self):
        with self.assertRaises(ValueError):
            TransitionRule(
                AuthorizationState(b"A", 0),
                AuthorizationState(b"B", 2),
            )


if __name__ == "__main__":
    unittest.main()
