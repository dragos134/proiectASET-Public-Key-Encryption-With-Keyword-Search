from aspects import log_errors

from secrets import randbelow

@log_errors
def swap25519(a, b, bit):
    c = ~(bit-1)
    t = c & (a ^ b)
    a ^= t
    b ^= t
    return (a, b)

# https://martin.kleppmann.com/papers/curve25519.pdf
class Curve:

    def __init__(self):
        self.name = "x25519" # Montgomery curve
        self.p = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
        self.A = 486662
        self.h = 8 # cofactor
        self.q = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed


    @log_errors
    def inverse_mod(self, number):
        # check if number can be inversed:
        if number == 0:
            raise ZeroDivisionError("Division by zero.")

        if number < 0:
            return self.p - self.inverse_mod(-number)
        # By Fermat's little theorem, a**(-1) == a**(p-2) (mod p);
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
    def pointAdd(self, point1, point2):
        assert self.onCurve(point1)
        assert self.onCurve(point2)

        if point1 is None:
            return point2
        if point2 is None:
            return point1

        if point1 == self.inversePoint(point2):
            return None

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2:
            x3 = (((3 * x1**2 + 2 * self.A * x1 + 1) / 2 * y1)**2 - self.A \
            - 2 * x1) % self.p
            # y3 = ((2 * x1 + x2 + self.A)*(3 * x1**2 + 2 * self.A * x1 + 1) \
            # / 2 * y1 - ((3 * x1**2 + 2 * self.A * x1 + 1) / 2 * y1)**3 - y1) \
            # % self.p
        else:
            x3 = (((y2 - y1) / (x2 - x1))**2 - self.A - x1 - x2) % self.p
            # y3 = ((2 * x1 + x2 + self.A)*(y2 - y1) / (x2 - x1) - ((y2 - y1) \
            # / (x2 - x1))**3 - y1) % self.p

        return (x3, y3)

    # The Montgomery ladder for scalar multiplication.
    @log_errors
    def scalarMult(self, point, scalar):

        if scalar % self.q == 0 or point is None:
            return None

        if scalar < 0:
            return self.scalarMult(-scalar, self.inversePoint(point))

        _121665 = 0xDB41
        clamped = bytearray(32)
        scalar = scalar.to_bytes(32, "little")
        for i in range(32):
            clamped[i] = scalar[i]
        clamped[0] &= 0xf8
        clamped[31] = (clamped[31] & 0x7f) | 0x40

        x = point[0]
        # b = x.to_bytes(16, "little")
        b = x
        c = 0
        d = a = bytearray(16)
        a[0] = d[0] = 1
        a = int.from_bytes(a, "little")
        d = int.from_bytes(d, "little")

        for i in range(254,-1,-1):
            bit = (clamped[i>>3] >> (i & 7)) & 1
            a, b = swap25519(a, b, bit)
            c, d = swap25519(c, d, bit)
            e = a + c % self.p
            a = a - c % self.p
            c = b + d % self.p
            b = b - d % self.p
            d = e**2 % self.p
            f = a**2 % self.p
            a = c * a % self.p
            c = b * e % self.p
            e = a + c % self.p
            a = a - c % self.p
            b = a**2 % self.p
            c = d - f % self.p
            a = c * _121665 % self.p
            a = a + d % self.p
            c = c * a % self.p
            a = d * f % self.p
            d = b * x % self.p
            b = e**2 % self.p

        c = self.inverse_mod(c)
        a *= c % self.p
        return a

    @log_errors
    def scalarMultBase(self, scalar):
        _point = (9, None)
        return self.scalarMult(_point, scalar)

    @log_errors
    def generateKeypair(self):
        private_key = randbelow(self.q - 1) + 1
        public_key  = self.scalarMultBase(private_key)
        return (private_key, public_key)

    # call x25519 to produce shared secret.
    # if x25519 is called by sender: public_key is recipient's public_key
    #       and private_key is sender's private_key;
    # if x25519 is called by recipient: public_key is sender's public_key
    #       and private_key is recipient's private_key.
    @log_errors
    def x25519(self, public_key, private_key):
        return self.scalarMult(private_key, public_key)
