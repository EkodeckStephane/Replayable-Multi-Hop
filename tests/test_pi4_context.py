import hashlib
import unittest

from camh_cufe.pi4_context import (
    Pi4Bases,
    bases_equal,
    derive_pi4_bases,
    require_canonical_pi4_bases,
)


class FakeGroup:
    def hash_to_g1(self, *parts):
        h = hashlib.sha256()
        for part in parts:
            if isinstance(part, int):
                part = part.to_bytes(8, "big")
            part = bytes(part)
            h.update(len(part).to_bytes(8, "big"))
            h.update(part)
        return h.digest()

    @staticmethod
    def eq(a, b):
        return a == b


class Pi4ContextTests(unittest.TestCase):
    def setUp(self):
        self.G = FakeGroup()

    def test_derivation_is_deterministic(self):
        a = derive_pi4_bases(self.G, 8, suite_id=b"toy-v1")
        b = derive_pi4_bases(self.G, 8, suite_id=b"toy-v1")
        self.assertTrue(bases_equal(self.G, a, b))

    def test_dimension_is_domain_bound(self):
        a = derive_pi4_bases(self.G, 8, suite_id=b"toy-v1")
        b = derive_pi4_bases(self.G, 9, suite_id=b"toy-v1")
        self.assertNotEqual(a.hv, b.hv)

    def test_suite_is_domain_bound(self):
        a = derive_pi4_bases(self.G, 8, suite_id=b"suite-a")
        b = derive_pi4_bases(self.G, 8, suite_id=b"suite-b")
        self.assertNotEqual(a.hv, b.hv)

    def test_mutated_base_is_rejected(self):
        canonical = derive_pi4_bases(self.G, 4, suite_id=b"toy-v1")
        mutated = Pi4Bases(
            Gv=canonical.Gv,
            hv=b"\x00" * 32,
            Gk=canonical.Gk,
            hk=canonical.hk,
        )
        with self.assertRaises(ValueError):
            require_canonical_pi4_bases(
                self.G, mutated, 4, suite_id=b"toy-v1"
            )

    def test_canonical_base_is_accepted(self):
        canonical = derive_pi4_bases(self.G, 4, suite_id=b"toy-v1")
        returned = require_canonical_pi4_bases(
            self.G, canonical, 4, suite_id=b"toy-v1"
        )
        self.assertTrue(bases_equal(self.G, canonical, returned))

    def test_invalid_dimension_rejected(self):
        with self.assertRaises(ValueError):
            derive_pi4_bases(self.G, 0, suite_id=b"toy-v1")


if __name__ == "__main__":
    unittest.main()
