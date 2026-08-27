import unittest

from camh_cufe.protocol_objects import (
    AuthorizationState,
    encode_checkpoint_statement,
    encode_state,
    encode_transition_statement,
    history_init,
    history_link,
)


class ProtocolObjectTests(unittest.TestCase):
    def test_state_tag_boundaries_are_unambiguous(self):
        a = encode_state(AuthorizationState(b"ab", 1), suite_id=b"toy")
        b = encode_state(AuthorizationState(b"a", 1), suite_id=b"toy-b")
        self.assertNotEqual(a, b)

    def test_transition_is_state_global_not_ciphertext_specific(self):
        tr = encode_transition_statement(
            suite_id=b"toy",
            source=AuthorizationState(b"A", 1),
            destination=AuthorizationState(b"B", 2),
            dimension=2,
            update_elements=[b"d0", b"d1", b"d2", b"d3"],
        )
        self.assertNotIn(b"ciphertext-id", tr)

    def test_bad_epoch_step_rejected(self):
        with self.assertRaises(ValueError):
            encode_transition_statement(
                suite_id=b"toy",
                source=AuthorizationState(b"A", 1),
                destination=AuthorizationState(b"B", 3),
                dimension=1,
                update_elements=[b"d0"],
            )

    def test_zero_dimension_rejected(self):
        with self.assertRaises(ValueError):
            encode_transition_statement(
                suite_id=b"toy",
                source=AuthorizationState(b"A", 1),
                destination=AuthorizationState(b"B", 2),
                dimension=0,
                update_elements=[b"d0"],
            )

    def test_history_root_binds_initial_authorization_state(self):
        root = b"fresh-ct-canonical"
        a0 = history_init(
            suite_id=b"toy",
            initial_state=AuthorizationState(b"A", 0),
            fresh_ciphertext=root,
        )
        b0 = history_init(
            suite_id=b"toy",
            initial_state=AuthorizationState(b"B", 0),
            fresh_ciphertext=root,
        )
        self.assertNotEqual(a0, b0)

    def test_different_paths_have_different_history_commitments(self):
        root = b"fresh-ct-canonical"
        root_state = AuthorizationState(b"A", 1)
        d0 = history_init(
            suite_id=b"toy",
            initial_state=root_state,
            fresh_ciphertext=root,
        )
        ab = encode_transition_statement(
            suite_id=b"toy",
            source=root_state,
            destination=AuthorizationState(b"B", 2),
            dimension=1,
            update_elements=[b"AB"],
        )
        ac = encode_transition_statement(
            suite_id=b"toy",
            source=root_state,
            destination=AuthorizationState(b"C", 2),
            dimension=1,
            update_elements=[b"AC"],
        )
        d_ab = history_link(
            suite_id=b"toy",
            previous_digest=d0,
            transition_statement=ab,
            source_ciphertext=root,
            destination_ciphertext=b"state-B",
            token_signature=b"sig-ab",
        )
        d_ac = history_link(
            suite_id=b"toy",
            previous_digest=d0,
            transition_statement=ac,
            source_ciphertext=root,
            destination_ciphertext=b"state-C",
            token_signature=b"sig-ac",
        )
        self.assertNotEqual(d_ab, d_ac)

    def test_checkpoint_binds_policy_and_context(self):
        common = dict(
            suite_id=b"toy",
            final_state=AuthorizationState(b"D", 3),
            final_ciphertext=b"ct-D3",
            history_digest=b"h" * 32,
            history_length=2,
            policy_id=b"single-auditor-v1",
        )
        a = encode_checkpoint_statement(**common, application_context=b"app-A")
        b = encode_checkpoint_statement(**common, application_context=b"app-B")
        self.assertNotEqual(a, b)


if __name__ == "__main__":
    unittest.main()
