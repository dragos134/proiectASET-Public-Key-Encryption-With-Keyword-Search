from aspects import log_errors

from secrets import randbelow

@log_errors
def swap25519(a, b, bit):
    t = i = c = ~(bit-1)

    for i in range(16):
        t = c & (a[i*16:i*16+16] ^ b[i*16:i*16+16])
        a[i] ^= t
        b[i] ^= t

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
            y3 = ((2 * x1 + x2 + self.A)*(3 * x1**2 + 2 * self.A * x1 + 1) \
            / 2 * y1 - ((3 * x1**2 + 2 * self.A * x1 + 1) / 2 * y1)**3 - y1) \
            % self.p
        else:
            x3 = (((y2 - y1) / (x2 - x1))**2 - self.A - x1 - x2) % self.p
            y3 = ((2 * x1 + x2 + self.A)*(y2 - y1) / (x2 - x1) - ((y2 - y1) \
            / (x2 - x1))**3 - y1) % self.p

        return (x3, y3)

    @log_errors
    def scalarMult(self, point, scalar):

        assert self.onCurve(point)

        if scalar % self.q == 0 or point is None:
            return None

        if scalar < 0:
            return self.scalarMult(-scalar, self.inversePoint(point))

        _121665 = 0xDB41
        clamped = scalar.to_bytes(32, "big")
        clamped[0] &= 0xf8
        clamped[31] = (clamped[31] & 0x7f) | 0x40

        x = point[0]

        b = x.to_bytes(16, "big")
        d = a = c = (0).to_bytes(16*8, "big")
        a[0] = d[0] = 1

        for i in range(254,-1,-1):
            bit = (clamped[i>>3] >> (i & 7)) & 1
            swap25519(a, b, bit)
            swap25519(c, d, bit)
            a = int.from_bytes(a, "big")
            b = int.from_bytes(b, "big")
            c = int.from_bytes(c, "big")
            d = int.from_bytes(d, "big")
            e = a + c % p
            a = a - c % p
            c = b + d % p
            b = b - d % p
            d = e**2 % p
            f = a**2 % p
            a = c * a % p
            c = b * e % p
            e = a + c % p
            a = a - c % p
            b = a**2 % p
            c = d - f % p
            a = c * _121665 % p
            a = a + d % p
            c = c * a % p
            a = d * f % p
            d = b * x % p
            b = e**2 % p
            a = a.to_bytes(16, "big")
            b = b.to_bytes(16, "big")
            c = c.to_bytes(16, "big")
            d = d.to_bytes(16, "big")




        # if scalar % self.q == 0 or point is None:
        #     return None
        #
        # if scalar < 0:
        #     return self.scalarMult(-scalar, self.inversePoint(point))
        #
        # result = None
        # temp = point
        #
        # while scalar:
        #     if scalar & 1:
        #         result = self.pointAdd(result, temp)
        #
        #     temp = self.pointAdd(temp, temp)
        #
        #     scalar >>= 1

        assert self.onCurve(result)

        return result

    @log_errors
    def scalarMultBase(self, scalar):
        _point = (9,)
        return self.scalarMult(_point, scalar)

    @log_errors
    def generateKeypair(self):
        private_key = randbelow(self.q) + 1
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
