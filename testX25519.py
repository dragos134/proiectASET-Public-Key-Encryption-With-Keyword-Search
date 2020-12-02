import unittest

import x25519

p = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed

class TestX25519(unittest.TestCase):

    def test_unpack(self):
        a = 50000
        field_elem_out = list()
        x25519.unpack25519(field_elem_out, a)
        self.assertNotEqual(field_elem_out, list(), "Field_elem_out is empty.")

    def test_add(self):
        a = []
        b = []
        field_elem_r = []
        field_elem_out = []
        x25519.unpack25519(a, 2**5)
        x25519.unpack25519(b, 2**100)
        x25519.fadd(field_elem_r, a, b)
        x25519.unpack25519(field_elem_out, (2**100 + 2**5) % p)
        self.assertEqual(field_elem_r, field_elem_out, "Faulty addition")

    def test_sub(self):
        a = []
        b = []
        field_elem_r = []
        field_elem_out = []
        x25519.unpack25519(a, 5)
        x25519.unpack25519(b, 3)
        x25519.fsub(field_elem_r, a, b)
        x25519.unpack25519(field_elem_out, 5-3)
        self.assertEqual(field_elem_r, field_elem_out, "Faulty substraction")

    def test_mul(self):
        a = []
        b = []
        field_elem_r = []
        field_elem_out = []
        x25519.unpack25519(a, 5)
        x25519.unpack25519(b, 3)
        x25519.fmul(field_elem_r, a, b)
        x25519.unpack25519(field_elem_out, 5*3)
        self.assertEqual(field_elem_r, field_elem_out, "Faulty multiplication")

    def test_generate_keypair(self):
        pk = list()
        sk = list()
        x25519.generate_keypair(pk, sk)
        self.assertNotEqual(pk, list(), "Faulty keygeneration; pk is empty.")
        self.assertNotEqual(sk, list(), "Faulty keygeneration; sk is empty.")

if __name__ == '__main__':
    unittest.main()
