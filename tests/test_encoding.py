import unittest

from camh_cufe.encoding import (
    EncodingError,
    Field,
    decode_object,
    encode_object,
    uint32,
    uint64,
    utf8,
)


class CanonicalEncodingTests(unittest.TestCase):
    def test_round_trip(self):
        encoded = encode_object(7, [
            Field(1, utf8("A")),
            Field(2, uint32(3)),
            Field(3, uint64(11)),
        ])
        object_type, fields = decode_object(encoded, expected_type=7)
        self.assertEqual(object_type, 7)
        self.assertEqual(fields[0].value, b"A")
        self.assertEqual(fields[1].value, b"\x00\x00\x00\x03")

    def test_ambiguous_text_concatenations_encode_differently(self):
        left = encode_object(9, [Field(1, b"ab"), Field(2, b"c")])
        right = encode_object(9, [Field(1, b"a"), Field(2, b"bc")])
        self.assertNotEqual(left, right)

    def test_field_order_is_canonical(self):
        with self.assertRaises(EncodingError):
            encode_object(1, [Field(2, b"x"), Field(1, b"y")])
        with self.assertRaises(EncodingError):
            encode_object(1, [Field(1, b"x"), Field(1, b"y")])

    def test_truncation_is_rejected(self):
        encoded = encode_object(1, [Field(1, b"abcdef")])
        for cut in (1, 5, len(encoded) - 1):
            with self.assertRaises(EncodingError):
                decode_object(encoded[:cut])

    def test_trailing_bytes_are_rejected(self):
        encoded = encode_object(1, [Field(1, b"x")])
        with self.assertRaises(EncodingError):
            decode_object(encoded + b"x")

    def test_wrong_type_is_rejected(self):
        encoded = encode_object(4, [])
        with self.assertRaises(EncodingError):
            decode_object(encoded, expected_type=5)

    def test_out_of_range_integer_is_rejected(self):
        with self.assertRaises(EncodingError):
            uint32(2**32)
        with self.assertRaises(EncodingError):
            uint64(-1)


if __name__ == "__main__":
    unittest.main()
