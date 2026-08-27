import unittest

from camh_cufe.authorization_graph import AuthorizationError, AuthorizationGraph
from camh_cufe.protocol_objects import AuthorizationState


class AuthorizationGraphTests(unittest.TestCase):
    def setUp(self):
        self.A0 = AuthorizationState(b"A", 0)
        self.B0 = AuthorizationState(b"B", 0)
        self.B1 = AuthorizationState(b"B", 1)
        self.C1 = AuthorizationState(b"C", 1)
        self.C2 = AuthorizationState(b"C", 2)
        self.D1 = AuthorizationState(b"D", 1)

    def test_tag_projection_does_not_create_composition(self):
        graph = AuthorizationGraph()
        graph.issue(self.A0, self.B1)
        graph.issue(self.B0, self.C1)

        self.assertFalse(graph.reachable(self.A0, self.C1))
        self.assertFalse(graph.reachable(self.A0, self.C2))
        with self.assertRaises(AuthorizationError):
            graph.validate_state_path((self.A0, self.B1, self.C2))

    def test_explicit_level_compatible_edge_enables_composition(self):
        graph = AuthorizationGraph()
        graph.issue(self.A0, self.B1)
        graph.issue(self.B1, self.C2)

        self.assertTrue(graph.reachable(self.A0, self.C2))
        self.assertEqual(
            graph.validate_state_path((self.A0, self.B1, self.C2)),
            (self.A0, self.B1, self.C2),
        )

    def test_branching_is_allowed_in_global_authorization_graph(self):
        graph = AuthorizationGraph()
        graph.issue(self.A0, self.B1)
        graph.issue(self.A0, self.D1)

        self.assertEqual(len(graph.outgoing(self.A0)), 2)
        self.assertTrue(graph.reachable(self.A0, self.B1))
        self.assertTrue(graph.reachable(self.A0, self.D1))

    def test_cycle_edge_is_structurally_rejected(self):
        graph = AuthorizationGraph()
        graph.issue(self.A0, self.B1)
        with self.assertRaises(ValueError):
            graph.issue(self.B1, self.A0)

    def test_same_visible_tag_at_different_epochs_is_distinct(self):
        graph = AuthorizationGraph()
        A1 = AuthorizationState(b"A", 1)
        A2 = AuthorizationState(b"A", 2)
        graph.issue(self.A0, A1)
        graph.issue(A1, A2)

        self.assertTrue(graph.reachable(self.A0, A2))
        self.assertNotEqual(self.A0, A1)
        self.assertNotEqual(A1, A2)

    def test_unrelated_adaptive_edges_do_not_enlarge_claimed_path(self):
        graph = AuthorizationGraph()
        graph.issue(self.A0, self.B1)
        graph.issue(self.B0, self.C1)
        graph.issue(AuthorizationState(b"X", 0), AuthorizationState(b"B", 1))
        graph.issue(AuthorizationState(b"B", 7), AuthorizationState(b"C", 8))

        self.assertFalse(graph.reachable(self.A0, self.C2))

    def test_zero_hop_path_is_valid_but_empty_path_is_not(self):
        graph = AuthorizationGraph()
        self.assertEqual(graph.validate_state_path((self.A0,)), (self.A0,))
        with self.assertRaises(AuthorizationError):
            graph.validate_state_path(())


if __name__ == "__main__":
    unittest.main()
