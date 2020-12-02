from aspects import log_errors

import cryptography
import hashlib
import curve25519
# Construction using bilinear maps
class PEKSClient:
    def __init__(self):
        self._curve = curve25519.Curve()
        self.priv = None
        self.publ = None
        
    # Generates a public/private key pair (private, public)
    @log_errors
    def KeyGen(self):
        self.priv, self.publ =  self._curve.generateKeypair()
    # For a public key A_pub and a word W, produces a searchable encryption of W
    @log_errors
    def PEKS(self, A_pub, W):
        t = e(H1(W), h**r)
        output = [g,H2(t)]
        return output
    # Output T_w = H1(w)**alpha
    @log_errors
    def Trapdoor(self, A_priv, W):
        T_w = H1(w)**alpha
        return T_w
