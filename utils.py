import hashlib

def hash(plaintext):
    _salt = "pkekspkekspkekspkekspkekspkekspkekspkeks00000000000000000000000000"
    hr = hashlib.scrypt(plaintext.encode("utf-8"), _salt.encode("utf-8"),
    16384, 8, 1)
    return hr
