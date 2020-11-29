from aspects import log_errors

from secrets import randbelow

class Curve:
    # https://martin.kleppmann.com/papers/curve25519.pdf
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
    def negatePoint(self, point):
        '''Returns -point'''
        assert is_on_curve(point)

        if point is None:
            return None

        x, y = point
        negation = (x, -y % self.p)

        assert is_on_curve(negation)

        return negation
