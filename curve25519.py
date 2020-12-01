from aspects import log_errors

from secrets import randbelow

# https://martin.kleppmann.com/papers/curve25519.pdf
class Curve:

    def __init__(self):
        name = "x25519" # Montgomery curve
        p = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
        A = 486662
        h = 8 # cofactor
        q = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed

    @log_errors
    def inverse_mod(self, number):
        # check if number can be inversed:
        if number == 0:
            raise ZeroDivisionError("Division by zero.")

        if number < 0:
            return self.p - self.inverse_mod(-number)
        # pm2 = p - 2
        pm2 = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeb
        return number**pm2 % self.p

    @log_errors
    def onCurve(self, point):
        '''True if the point is found on the curve'''
        # None represents the point at infinity.
        if point is None:
            return True

        x, y = point

        return (y**2 - x**3 - self.A*(x**2) - x) % self.p == 0

    @log_errors
    def inversePoint(self, point):
        '''Returns -point'''
        assert self.onCurve(point)

        if point is None:
            return None

        x, y = point
        inverse = (x, -y % self.p)

        assert self.onCurve(inverse)

        return inverse

    @log_errors
    def scalarMult(self, point, scalar):
        return None

    @log_errors
    def scalarMultBase(self, scalar):
        _point = (9,)
        return self.scalarMult(_point, scalar)

    @log_errors
    def generateKeypair(self):
        private_key = randbelow(self.q) + 1
        public_key  = self.scalarMultBase(private_key)

    # call x25519 to produce shared secret.
    @log_errors
    def x25519(self, public_key, private_key):
        return self.scalarMult(private_key, public_key)
