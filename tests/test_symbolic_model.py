import unittest

from camh_cufe.protocol_objects import AuthorizationState
from camh_cufe.symbolic_model import SymbolicCAMHCUFE


class SymbolicModelTests(unittest.TestCase):
    def setUp(self):
        self.M = SymbolicCAMHCUFE(
            p=2**127 - 1,
            U=[(3, 5), (7, 11), (13, 17)],
            tag_key=b"test-key",
        )
        self.x = (2, 3, 5)
        self.v = (4, 1, 2)
        self.A1 = AuthorizationState(b"A", 1)

    def test_sequential_functional_correctness(self):
        ct = self.M.encrypt(self.x, state=self.A1)
        ct = self.M.update(
            ct,
            source=self.A1,
            destination=AuthorizationState(b"B", 2),
        )
        ct = self.M.update(
            ct,
            source=ct.state,
            destination=AuthorizationState(b"D", 3),
        )
        self.assertEqual(self.M.decrypt_inner_product(ct, self.v), 21)

    def test_distinct_paths_reconverge_to_same_payload(self):
        root = self.M.encrypt(self.x, state=self.A1)
        p = self.M.update(
            root,
            source=self.A1,
            destination=AuthorizationState(b"B", 2),
        )
        p = self.M.update(
            p,
            source=p.state,
            destination=AuthorizationState(b"D", 3),
        )
        q = self.M.update(
            root,
            source=self.A1,
            destination=AuthorizationState(b"C", 2),
        )
        q = self.M.update(
            q,
            source=q.state,
            destination=AuthorizationState(b"D", 3),
        )
        self.assertEqual(p.state, q.state)
        self.assertEqual(p.payload_exponents, q.payload_exponents)
        self.assertEqual(self.M.decrypt_inner_product(p, self.v), 21)
        self.assertEqual(self.M.decrypt_inner_product(q, self.v), 21)

    def test_same_tag_at_different_epoch_is_different_state(self):
        self.assertNotEqual(
            self.M.h(AuthorizationState(b"A", 1)),
            self.M.h(AuthorizationState(b"A", 4)),
        )

    def test_stale_state_update_rejected(self):
        root = self.M.encrypt(self.x, state=self.A1)
        b2 = AuthorizationState(b"B", 2)
        ct = self.M.update(root, source=self.A1, destination=b2)
        with self.assertRaises(ValueError):
            self.M.update(ct, source=self.A1, destination=b2)


if __name__ == "__main__":
    unittest.main()
