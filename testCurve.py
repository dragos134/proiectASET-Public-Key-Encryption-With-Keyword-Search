import unittest

import timeit

import curve25519

class TestX25519(unittest.TestCase):

    def test_swap(self):
        a = 5000
        b = 10000
        # a shoud be swapped with b:
        a,b = curve25519.swap25519(a, b, 1)
        self.assertEqual(a, 10000, "a should've been 10000")
        self.assertEqual(b, 5000, "b should've been 5000")
        # a and b should remain the same:
        a = 5000
        b = 10000
        a,b = curve25519.swap25519(a, b, 0)
        self.assertEqual(b, 10000, "b should've been 10000")
        self.assertEqual(a, 5000, "a should've been 5000")

    def test_init(self):

        _curve = curve25519.Curve()
        self.assertEqual(_curve.name, "x25519", "Curve name should be 'x25519'")

    def test_generate_keys(self):

        _curve = curve25519.Curve()
        private_key, public_key = _curve.generateKeypair()
        self.assertNotEqual(public_key, None, "Public key should not be empty")
        self.assertNotEqual(private_key, None, "Private key should not be empty")
        private_key2, public_key2 = _curve.generateKeypair()
        self.assertEqual(public_key, public_key2, "Generated public keys must \
        differ.")
        self.assertEqual(private_key, private_key2, "Generated private keys \
        must differ.")

if __name__ == '__main__':
    unittest.main()
