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
        self.pp = b"p" * 32
        self.rel = b"ipfe-final-v1"

    def derive(self, dimension=8, suite=b"toy-v1", pp=None, rel=None):
        return derive_pi4_bases(
            self.G,
            dimension,
            suite_id=suite,
            public_parameters_digest=self.pp if pp is None else pp,
            relation_id=self.rel if rel is None else rel,
        )

    def test_derivation_is_deterministic(self):
        a = self.derive()
        b = self.derive()
        self.assertTrue(bases_equal(self.G, a, b))

    def test_dimension_is_domain_bound(self):
        a = self.derive(8)
        b = self.derive(9)
        self.assertNotEqual(a.hv, b.hv)

    def test_suite_is_domain_bound(self):
        a = self.derive(suite=b"suite-a")
        b = self.derive(suite=b"suite-b")
        self.assertNotEqual(a.hv, b.hv)

    def test_public_parameters_are_domain_bound(self):
        a = self.derive(pp=b"a" * 32)
        b = self.derive(pp=b"b" * 32)
        self.assertNotEqual(a.hv, b.hv)

    def test_relation_is_domain_bound(self):
        a = self.derive(rel=b"relation-a")
        b = self.derive(rel=b"relation-b")
        self.assertNotEqual(a.hv, b.hv)

    def test_mutated_base_is_rejected(self):
        canonical = self.derive(4)
        mutated = Pi4Bases(
            Gv=canonical.Gv,
            hv=b"\x00" * 32,
            Gk=canonical.Gk,
            hk=canonical.hk,
        )
        with self.assertRaises(ValueError):
            require_canonical_pi4_bases(
                self.G,
                mutated,
                4,
                suite_id=b"toy-v1",
                public_parameters_digest=self.pp,
                relation_id=self.rel,
            )

    def test_canonical_base_is_accepted(self):
        canonical = self.derive(4)
        returned = require_canonical_pi4_bases(
            self.G,
            canonical,
            4,
            suite_id=b"toy-v1",
            public_parameters_digest=self.pp,
            relation_id=self.rel,
        )
        self.assertTrue(bases_equal(self.G, canonical, returned))

    def test_invalid_dimension_rejected(self):
        with self.assertRaises(ValueError):
            self.derive(0)

    def test_bad_public_parameters_digest_rejected(self):
        with self.assertRaises(ValueError):
            self.derive(pp=b"short")


if __name__ == "__main__":
    unittest.main()
