import hashlib
import inspect
import unittest
from dataclasses import replace

from camh_cufe.final_result import (
    FinalResultStatement,
    derive_statement_pi4_bases,
    final_result_transcript,
    verify_final_result_reference,
)
from camh_cufe.protocol_objects import AuthorizationState


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


def toy_proof(transcript, bases):
    h = hashlib.sha256()
    h.update(transcript)
    for value in (*bases.Gv, bases.hv, *bases.Gk, bases.hk):
        h.update(value)
    return h.digest()


def toy_verify(transcript, proof, bases):
    return toy_proof(transcript, bases) == proof


class FinalResultTests(unittest.TestCase):
    def setUp(self):
        self.G = FakeGroup()
        self.statement = FinalResultStatement(
            suite_id=b"toy-suite-v1",
            relation_id=b"ipfe-final-v1",
            public_parameters_digest=b"p" * 32,
            final_state=AuthorizationState(b"C", 2),
            dimension=3,
            final_ciphertext=b"canonical-final-ct",
            function_public_view=b"canonical-function-v",
            functional_key_public_view=b"canonical-fk-view",
            result_encoding_id=b"signed-int-be-v1",
            claimed_result=b"\x00\x00\x00\x24",
            history_digest=b"h" * 32,
            history_length=2,
            application_context=b"fgcs-eval",
        )

    def proof_for(self, statement):
        transcript = final_result_transcript(statement)
        bases = derive_statement_pi4_bases(self.G, statement)
        return toy_proof(transcript, bases)

    def test_honest_bound_reference_verification_accepts(self):
        proof = self.proof_for(self.statement)
        self.assertTrue(
            verify_final_result_reference(
                self.G, self.statement, proof, toy_verify
            )
        )

    def test_verifier_api_has_no_caller_supplied_bases(self):
        parameters = inspect.signature(verify_final_result_reference).parameters
        self.assertNotIn("bases", parameters)
        self.assertNotIn("pi4_bases", parameters)
        self.assertEqual(
            tuple(parameters), ("G", "statement", "proof", "verify_relation")
        )

    def test_every_security_relevant_statement_field_changes_encoding(self):
        original = self.statement.encode()
        mutations = (
            replace(self.statement, suite_id=b"other-suite"),
            replace(self.statement, relation_id=b"other-relation"),
            replace(self.statement, public_parameters_digest=b"q" * 32),
            replace(self.statement, final_state=AuthorizationState(b"D", 2)),
            replace(self.statement, dimension=4),
            replace(self.statement, final_ciphertext=b"other-ct"),
            replace(self.statement, function_public_view=b"other-function"),
            replace(self.statement, functional_key_public_view=b"other-fk"),
            replace(self.statement, result_encoding_id=b"other-codec"),
            replace(self.statement, claimed_result=b"other-result"),
            replace(self.statement, history_digest=b"x" * 32),
            replace(self.statement, history_length=3),
            replace(self.statement, application_context=b"other-app"),
        )
        for mutated in mutations:
            with self.subTest(mutated=mutated):
                self.assertNotEqual(original, mutated.encode())

    def test_existing_proof_rejects_any_statement_substitution(self):
        proof = self.proof_for(self.statement)
        mutations = (
            replace(self.statement, public_parameters_digest=b"q" * 32),
            replace(self.statement, final_state=AuthorizationState(b"D", 2)),
            replace(self.statement, final_ciphertext=b"other-ct"),
            replace(self.statement, function_public_view=b"other-function"),
            replace(self.statement, functional_key_public_view=b"other-fk"),
            replace(self.statement, claimed_result=b"other-result"),
            replace(self.statement, history_digest=b"x" * 32),
            replace(self.statement, history_length=3),
        )
        for mutated in mutations:
            with self.subTest(mutated=mutated):
                self.assertFalse(
                    verify_final_result_reference(
                        self.G, mutated, proof, toy_verify
                    )
                )

    def test_bad_digest_widths_rejected(self):
        with self.assertRaises(ValueError):
            replace(self.statement, public_parameters_digest=b"short").encode()
        with self.assertRaises(ValueError):
            replace(self.statement, history_digest=b"short").encode()

    def test_zero_dimension_rejected(self):
        with self.assertRaises(ValueError):
            replace(self.statement, dimension=0).encode()

    def test_empty_relation_and_result_encoding_rejected(self):
        with self.assertRaises(ValueError):
            replace(self.statement, relation_id=b"").encode()
        with self.assertRaises(ValueError):
            replace(self.statement, result_encoding_id=b"").encode()

    def test_setup_change_also_changes_derived_bases(self):
        original = derive_statement_pi4_bases(self.G, self.statement)
        changed = derive_statement_pi4_bases(
            self.G,
            replace(self.statement, public_parameters_digest=b"q" * 32),
        )
        self.assertNotEqual(original.hv, changed.hv)


if __name__ == "__main__":
    unittest.main()
