from utils import H1,H2
import rsa

def peks(Apub, W):
    t = e(H1(W), h**r)
    return [g,H2(t)]
