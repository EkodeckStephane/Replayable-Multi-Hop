import unittest

from camh_cufe.protocol_objects import (
    AuthorizationState,
    encode_checkpoint_statement,
    encode_retained_transition_record,
    encode_state,
    encode_transition_statement,
)
from camh_cufe.wire_metrics import (
    measure_checkpoint_statement,
    measure_retained_transition,
    measure_state,
    measure_transition,
)


class WireMetricTests(unittest.TestCase):
    def test_state_measurement_is_exact_canonical_length(self):
        state = AuthorizationState(b"A", 0)
        encoded = encode_state(state, suite_id=b"suite")
        measured = measure_state(suite_id=b"suite", state=state)
        self.assertEqual(measured.byte_length, len(encoded))
        self.assertEqual(measured.evidence_class, "canonical-wire")

    def test_transition_measurement_is_exact_canonical_length(self):
        source = AuthorizationState(b"A", 0)
        destination = AuthorizationState(b"B", 1)
        kwargs = dict(
            suite_id=b"suite",
            source=source,
            destination=destination,
            dimension=2,
            update_elements=(b"u0", b"u1"),
        )
        encoded = encode_transition_statement(**kwargs)
        measured = measure_transition(**kwargs)
        self.assertEqual(measured.byte_length, len(encoded))

    def test_retained_record_measurement_uses_canonical_envelope(self):
        statement = encode_transition_statement(
            suite_id=b"suite",
            source=AuthorizationState(b"A", 0),
            destination=AuthorizationState(b"B", 1),
            dimension=1,
            update_elements=(b"u",),
        )
        kwargs = dict(
            suite_id=b"suite",
            transition_statement=statement,
            source_ciphertext=b"canonical-ct-a",
            destination_ciphertext=b"canonical-ct-b",
            token_signature=b"canonical-sig",
            history_digest=b"h" * 32,
        )
        encoded = encode_retained_transition_record(**kwargs)
        measured = measure_retained_transition(**kwargs)
        self.assertEqual(measured.byte_length, len(encoded))

    def test_checkpoint_measurement_is_exact_canonical_length(self):
        kwargs = dict(
            suite_id=b"suite",
            final_state=AuthorizationState(b"C", 2),
            final_ciphertext=b"canonical-ct-c",
            history_digest=b"h" * 32,
            history_length=2,
            policy_id=b"single-auditor-v1",
            application_context=b"app",
        )
        encoded = encode_checkpoint_statement(**kwargs)
        measured = measure_checkpoint_statement(**kwargs)
        self.assertEqual(measured.byte_length, len(encoded))

    def test_python_runtime_object_size_is_not_an_api(self):
        # The module deliberately has no generic measure_object/pickle path.
        import camh_cufe.wire_metrics as wm

        self.assertFalse(hasattr(wm, "measure_object"))
        self.assertFalse(hasattr(wm, "measure_pickle"))


if __name__ == "__main__":
    unittest.main()
