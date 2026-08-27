import unittest


Q = 101


def dot(row, col):
    return sum(a * b for a, b in zip(row, col)) % Q


def mat_vec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def row_mat(row, matrix):
    return [
        sum(row[i] * matrix[i][j] for i in range(len(row))) % Q
        for j in range(len(matrix[0]))
    ]


def centered(value):
    value %= Q
    return value if value <= Q // 2 else value - Q


class LWESurrogateCriterionTests(unittest.TestCase):
    """Executable algebra oracle for the conditional NO-GO criterion.

    This toy example is not evidence about the security of Cini et al.'s
    published one-hop construction. It demonstrates that a multi-level
    candidate satisfying the documented public equations can become
    key-switchable when Delta1 is publicly invertible and the derived preimage
    stays inside the decryption-noise budget.
    """

    def setUp(self):
        # Source matrix and publicly invertible update transport.
        self.H_source = [1, 2]
        self.delta1 = [[1, 1], [0, 1]]
        self.delta1_inv = [[1, -1], [0, 1]]
        self.H_target = row_mat(self.H_source, self.delta1)

        # One-dimensional function family (y=1) represented by short preimages.
        self.Z_source_y = [1, 0]
        self.delta2_y = [2, 1]
        self.Z_target_y = [2, 1]

        self.D_source_y = dot(self.H_source, self.Z_source_y)
        self.D_target_y = dot(self.H_target, self.Z_target_y)

    def test_candidate_public_equations_hold(self):
        self.assertEqual(self.H_target, [1, 3])
        self.assertEqual(self.D_source_y, 1)
        self.assertEqual(
            dot(self.H_source, self.delta2_y),
            (self.D_target_y - self.D_source_y) % Q,
        )

    def test_public_source_key_and_token_recover_target_preimage(self):
        w = [
            (a + b) % Q
            for a, b in zip(self.Z_source_y, self.delta2_y)
        ]
        surrogate = mat_vec(self.delta1_inv, w)

        self.assertEqual([centered(x) for x in surrogate], self.Z_target_y)
        self.assertEqual(
            dot(self.H_target, surrogate),
            self.D_target_y,
        )

    def test_surrogate_decrypts_independent_target_ciphertext(self):
        # This ciphertext is generated directly in the target state; it is not
        # a descendant of any source ciphertext used by the attacker.
        secret = 7
        message = 2
        scale = 20
        e1 = [1, 0]
        e2 = 1

        c1 = [
            (h * secret + e) % Q
            for h, e in zip(self.H_target, e1)
        ]
        c2 = (self.D_target_y * secret + e2 + scale * message) % Q

        w = [
            (a + b) % Q
            for a, b in zip(self.Z_source_y, self.delta2_y)
        ]
        surrogate_mod_q = mat_vec(self.delta1_inv, w)
        surrogate = [centered(x) for x in surrogate_mod_q]

        value = centered(c2 - sum(k * c for k, c in zip(surrogate, c1)))
        decoded = round(value / scale)

        self.assertEqual(value, 39)  # 40 plus a small decryption error (-1).
        self.assertEqual(decoded, message)

    def test_source_key_alone_is_not_the_target_capability_in_example(self):
        secret = 7
        message = 2
        scale = 20
        c1 = [8, 21]
        c2 = 76

        value_with_source_key = centered(
            c2 - sum(k * c for k, c in zip(self.Z_source_y, c1))
        )
        decoded_with_source_key = round(value_with_source_key / scale)

        self.assertNotEqual(decoded_with_source_key, message)


if __name__ == "__main__":
    unittest.main()
