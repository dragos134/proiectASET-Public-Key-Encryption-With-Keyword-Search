import hashlib

def hash(plaintext):
    _salt = "pkekspkekspkekspkekspkekspkekspkekspkeks00000000000000000000000000"
    hr = hashlib.scrypt(plaintext.encode("utf-8"), salt = _salt.encode("utf-8"),
    n = 16384, r = 8, p = 1)
    return hr.hex()
