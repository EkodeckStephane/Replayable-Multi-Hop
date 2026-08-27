import unittest

from camh_cufe.encoding import Field, decode_object, encode_object, uint32, uint64
from camh_cufe.protocol_objects import AuthorizationState, encode_state


GENERIC_OBJECT_HEX = (
    "43414d482d43554645000001000700030001000000000000000141"
    "000200000000000000040000000300030000000000000008000000000000000b"
)

STATE_HEX = (
    "43414d482d4355464500000110010003000100000000000000025331"
    "00020000000000000001410003000000000000000400000000"
)


class GoldenVectorTests(unittest.TestCase):
    def test_generic_object_v1_exact_bytes(self):
        encoded = encode_object(
            7,
            [
                Field(1, b"A"),
                Field(2, uint32(3)),
                Field(3, uint64(11)),
            ],
        )
        self.assertEqual(encoded.hex(), GENERIC_OBJECT_HEX)
        object_type, fields = decode_object(bytes.fromhex(GENERIC_OBJECT_HEX))
        self.assertEqual(object_type, 7)
        self.assertEqual(tuple(field.value for field in fields), (b"A", uint32(3), uint64(11)))

    def test_authorization_state_v1_exact_bytes(self):
        state = AuthorizationState(tag=b"A", epoch=0)
        encoded = encode_state(state, suite_id=b"S1")
        self.assertEqual(encoded.hex(), STATE_HEX)
        object_type, fields = decode_object(bytes.fromhex(STATE_HEX), expected_type=0x1001)
        self.assertEqual(object_type, 0x1001)
        self.assertEqual(fields[0].value, b"S1")
        self.assertEqual(fields[1].value, b"A")
        self.assertEqual(fields[2].value, uint32(0))


if __name__ == "__main__":
    unittest.main()
