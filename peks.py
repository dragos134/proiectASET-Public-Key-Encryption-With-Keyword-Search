import rsa
from aspects import log_errors

@log_errors
def peks(Apub, W):
    t = e(H1(W), h**r)
    return [g,H2(t)]
