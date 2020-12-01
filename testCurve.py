import unittest

import curve25519

class TestX25519(unittest.TestCase):

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
