import hashlib
import unittest
from dataclasses import replace

from camh_cufe.audit_history import (
    HistoryVerificationError,
    make_retained_transition,
    verify_retained_history,
)
from camh_cufe.authorization_graph import AuthorizationGraph
from camh_cufe.protocol_objects import (
    AuthorizationState,
    encode_transition_statement,
    history_init,
)


TOY_AUTH_KEY = b"test-only-auth-key"
SUITE = b"toy-suite"


def toy_sign(statement: bytes) -> bytes:
    return hashlib.sha256(TOY_AUTH_KEY + statement).digest()


def toy_verify(statement: bytes, signature: bytes) -> bool:
    return toy_sign(statement) == signature


class AuditHistoryTests(unittest.TestCase):
    def setUp(self):
        self.A0 = AuthorizationState(b"A", 0)
        self.B1 = AuthorizationState(b"B", 1)
        self.C2 = AuthorizationState(b"C", 2)
        self.D2 = AuthorizationState(b"D", 2)
        self.root = b"ct-A0"
        self.ct_b = b"ct-B1"
        self.ct_c = b"ct-C2"

        self.graph = AuthorizationGraph()
        self.graph.issue(self.A0, self.B1)
        self.graph.issue(self.B1, self.C2)

        d0 = history_init(
            suite_id=SUITE,
            initial_state=self.A0,
            fresh_ciphertext=self.root,
        )

        stmt_ab = encode_transition_statement(
            suite_id=SUITE,
            source=self.A0,
            destination=self.B1,
            dimension=2,
            update_elements=(b"ab0", b"ab1"),
        )
        self.r1 = make_retained_transition(
            suite_id=SUITE,
            previous_digest=d0,
            source=self.A0,
            destination=self.B1,
            dimension=2,
            update_elements=(b"ab0", b"ab1"),
            source_ciphertext=self.root,
            destination_ciphertext=self.ct_b,
            token_signature=toy_sign(stmt_ab),
        )

        stmt_bc = encode_transition_statement(
            suite_id=SUITE,
            source=self.B1,
            destination=self.C2,
            dimension=2,
            update_elements=(b"bc0", b"bc1"),
        )
        self.r2 = make_retained_transition(
            suite_id=SUITE,
            previous_digest=self.r1.history_digest,
            source=self.B1,
            destination=self.C2,
            dimension=2,
            update_elements=(b"bc0", b"bc1"),
            source_ciphertext=self.ct_b,
            destination_ciphertext=self.ct_c,
            token_signature=toy_sign(stmt_bc),
        )

        # This set stands in for a real backend VerifyTransition relation. It is
        # deliberately independent of the public history digest.
        self.valid_transition_uses = {
            (self.root, self.r1.transition_statement, self.ct_b),
            (self.ct_b, self.r2.transition_statement, self.ct_c),
        }

    def verify_transition_use(self, source_ct, statement, destination_ct):
        return (source_ct, statement, destination_ct) in self.valid_transition_uses

    def verify(self, records=None, **kwargs):
        if records is None:
            records = (self.r1, self.r2)
        return verify_retained_history(
            suite_id=SUITE,
            initial_state=self.A0,
            fresh_ciphertext=self.root,
            records=records,
            authorization_graph=self.graph,
            verify_token_signature=toy_verify,
            verify_transition_use=self.verify_transition_use,
            **kwargs,
        )

    def test_honest_complete_history_accepts(self):
        result = self.verify(
            expected_final_state=self.C2,
            expected_final_ciphertext=self.ct_c,
            expected_history_digest=self.r2.history_digest,
        )
        self.assertEqual(result.history_length, 2)
        self.assertEqual(result.final_state, self.C2)

    def test_skip_middle_predecessor_rejected(self):
        with self.assertRaises(HistoryVerificationError):
            self.verify(records=(self.r2,))

    def test_reordered_records_rejected(self):
        with self.assertRaises(HistoryVerificationError):
            self.verify(records=(self.r2, self.r1))

    def test_spliced_suffix_from_other_lineage_rejected(self):
        other_root = b"other-ct-A0"
        d0_other = history_init(
            suite_id=SUITE,
            initial_state=self.A0,
            fresh_ciphertext=other_root,
        )
        stmt_ab = encode_transition_statement(
            suite_id=SUITE,
            source=self.A0,
            destination=self.B1,
            dimension=2,
            update_elements=(b"ab0", b"ab1"),
        )
        other_r1 = make_retained_transition(
            suite_id=SUITE,
            previous_digest=d0_other,
            source=self.A0,
            destination=self.B1,
            dimension=2,
            update_elements=(b"ab0", b"ab1"),
            source_ciphertext=other_root,
            destination_ciphertext=b"other-ct-B1",
            token_signature=toy_sign(stmt_ab),
        )
        stmt_bc = encode_transition_statement(
            suite_id=SUITE,
            source=self.B1,
            destination=self.C2,
            dimension=2,
            update_elements=(b"bc0", b"bc1"),
        )
        other_r2 = make_retained_transition(
            suite_id=SUITE,
            previous_digest=other_r1.history_digest,
            source=self.B1,
            destination=self.C2,
            dimension=2,
            update_elements=(b"bc0", b"bc1"),
            source_ciphertext=b"other-ct-B1",
            destination_ciphertext=b"other-ct-C2",
            token_signature=toy_sign(stmt_bc),
        )

        with self.assertRaises(HistoryVerificationError):
            self.verify(records=(self.r1, other_r2))

    def test_arbitrary_destination_with_recomputed_public_digest_rejected(self):
        # A valid state-global token signature plus a freshly recomputed rolling
        # digest must not authenticate an arbitrary destination ciphertext.
        forged = make_retained_transition(
            suite_id=SUITE,
            previous_digest=self.r1.history_digest,
            source=self.B1,
            destination=self.C2,
            dimension=2,
            update_elements=(b"bc0", b"bc1"),
            source_ciphertext=self.ct_b,
            destination_ciphertext=b"attacker-chosen-ct-C2",
            token_signature=self.r2.token_signature,
        )
        with self.assertRaises(HistoryVerificationError):
            self.verify(records=(self.r1, forged))

    def test_final_ciphertext_substitution_rejected(self):
        with self.assertRaises(HistoryVerificationError):
            self.verify(expected_final_ciphertext=b"substituted-final")

    def test_final_state_substitution_rejected(self):
        with self.assertRaises(HistoryVerificationError):
            self.verify(expected_final_state=self.D2)

    def test_history_digest_substitution_rejected(self):
        with self.assertRaises(HistoryVerificationError):
            self.verify(expected_history_digest=b"x" * 32)

    def test_record_digest_tampering_rejected(self):
        tampered = replace(self.r2, history_digest=b"z" * 32)
        with self.assertRaises(HistoryVerificationError):
            self.verify(records=(self.r1, tampered))

    def test_transition_statement_tampering_rejected(self):
        tampered = replace(
            self.r2,
            transition_statement=self.r2.transition_statement + b"x",
        )
        with self.assertRaises(HistoryVerificationError):
            self.verify(records=(self.r1, tampered))

    def test_token_authentication_failure_rejected(self):
        tampered = replace(self.r2, token_signature=b"bad-signature")
        with self.assertRaises(HistoryVerificationError):
            self.verify(records=(self.r1, tampered))

    def test_unauthorized_exact_edge_rejected_even_if_tag_graph_looks_chainable(self):
        C1 = AuthorizationState(b"C", 1)
        graph = AuthorizationGraph()
        graph.issue(self.A0, self.B1)
        graph.issue(AuthorizationState(b"B", 0), C1)
        with self.assertRaises(HistoryVerificationError):
            verify_retained_history(
                suite_id=SUITE,
                initial_state=self.A0,
                fresh_ciphertext=self.root,
                records=(self.r1, self.r2),
                authorization_graph=graph,
                verify_token_signature=toy_verify,
                verify_transition_use=self.verify_transition_use,
            )

    def test_nonzero_root_epoch_rejected(self):
        with self.assertRaises(HistoryVerificationError):
            verify_retained_history(
                suite_id=SUITE,
                initial_state=AuthorizationState(b"A", 3),
                fresh_ciphertext=self.root,
                records=(),
                authorization_graph=AuthorizationGraph(),
                verify_token_signature=toy_verify,
                verify_transition_use=lambda *_: True,
            )


if __name__ == "__main__":
    unittest.main()
