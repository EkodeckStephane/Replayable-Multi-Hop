import unittest

from camh_cufe import domains


class DomainRegistryTests(unittest.TestCase):
    def test_all_registered_domains_are_unique(self):
        domains.assert_unique_domains()
        values = tuple(domains.REGISTERED.values())
        self.assertEqual(len(values), len(set(values)))

    def test_every_registered_domain_is_versioned_and_namespaced(self):
        for label in domains.REGISTERED.values():
            self.assertTrue(label.startswith(b"CAMH-CUFE/"))
            self.assertTrue(label.endswith(b"/v1"))

    def test_symbolic_and_real_state_domains_are_distinct(self):
        self.assertNotEqual(domains.SYMBOLIC_TAG, domains.REAL_STATE_HASH)


if __name__ == "__main__":
    unittest.main()
