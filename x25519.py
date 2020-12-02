'''
typedef unsigned charu8;
typedef long long i64;
typedef i64 field_elem[16];
'''

from secrets import randbelow

q = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed

BYTE_ORDER = "little"

_9 = [9]
[_9.append(0) for k in range(31)]


_121665 = [0xDB41, 1]
[_121665.append(0) for i in range(14)]

def unpack25519(field_elem_out, u8_in32):
    field_elem_out.clear()
    if type(u8_in32) == type(list()):
        u8_in = u8_in32.copy()
    else:
        u8_in = u8_in32.to_bytes(32, BYTE_ORDER)
    [field_elem_out.append(u8_in[2*i] + (u8_in[2*i + 1] << 8))
    for i in range(16)]
    field_elem_out[15] &= 0x7fff

def carry25519(field_elem):
    for i in range(16):
        carry = field_elem[i] >> 16
        field_elem[i] -= carry << 16
        if (i < 15):
            elem[i + 1] += carry
        else:
            elem[0] += 38 * carry

# out = a + b
def fadd(field_elem_out, field_elem_a, field_elem_b):
    field_elem_out.clear()
    [ field_elem_out.append(field_elem_a[i] + field_elem_b[i])
    for i in range(16) ]

# out = a - b
def fsub(field_elem_out, field_elem_a, field_elem_b):
    field_elem_out.clear()
    [ field_elem_out.append(field_elem_a[i] - field_elem_b[i])
    for i in range(16) ]

def fmul(field_elem_out, field_elem_a, field_elem_b):
    product = [0] * 31
    field_elem_out.clear()

    for i in range(16):
        for j in range(16):
            product[i+j] += field_elem_a[i] * field_elem_b[j]

    for i in range(15):
        product[i] += 38 * product[i+16]

    field_elem_out = product[:16]

    carry25519(field_elem_out)
    carry25519(field_elem_out)

def finverse(field_elem_out, field_elem_in):
    c = field_elem_in.copy()

    for i in range(253, -1, -1):
        fmul(c, c, c)
        if (i != 2 and i != 4): fmul(c, c, field_elem_in)

    field_elem_out = c[:16]

def swap25519(field_elem_p, field_elem_q, bit):
    c = ~(bit - 1)
    for i in range(16):
        t = c & (field_elem_p[i] ^ field_elem_q[i])
        field_elem_p[i] ^= t
        field_elem_q[i] ^= t
        # problem is it should use .append, .insert, pop()

def pack25519(u8_out32, field_elem_int):
    u8_out32.clear()

    m = [0] * 16
    t = field_elem_in.copy()

    carry25519(t); carry25519(t); carry25519(t)

    for j in range(2):
        m[0] = t[0] - 0xffed

        for i in range(1,15):
            m[i] = t[i] - 0xffff - ((m[i-1] >> 16) & 1)
            m[i-1] &= 0xffff

        m[15] = t[15] - 0x7fff - ((m[14] >> 16) & 1)
        carry = (m[15] >> 16) & 1
        m[14] &= 0xffff

        swap25519(t, m, 1 - carry)

    for i in range(16):
        u8_out32.append(t[i] & 0xff)
        u8_out32.append(t[i] >> 8)

def scalarmult_base(u8_out, u8_scalar):
    scalarmult(u8_out, u8_scalar, _9)

def generate_keypair(u8_pk, u8_sk):
    u8_sk_int = randbelow(q - 1) + 1
    u8_sk = list(u8_sk_int.to_bytes(32, BYTE_ORDER))
    scalarmult_base(u8_pk, u8_sk)

def x25519(u8_out, u8_pk, u8_sk):
    scalarmult(u8_out, u8_sk, u8_pk)

def scalarmult(u8_out, u8_scalar, u8_point):
    a = list(); b = list(); c = list(); d = list(); e = list(); f = list()
    x = list()
    clamped = u8_scalar.copy()
    clamped[0] &= 0xf8
    clamped[31] = (clamped[31] & 0x7f) | 0x40
    unpack25519(x, u8_point)
    b = x.copy
    [c.append(0) for i in range(16)]
    d = [1]
    a = [1]
    [d.append(0) for i in range(15)]
    [a.append(0) for i in range(15)]

    for i in range(254, -1, -1):
        bit = (clamped[i >> 3] >> (i & 7)) & 1
        swap25519(a, b, bit)
        swap25519(c, d, bit)
        fadd(e, a, c)
        fsub(a, a, c)
        fadd(c, b, d)
        fsub(b, b, d)
        fmul(d, e, e)
        fmul(f, a, a)
        fmul(a, c, a)
        fmul(c, b, e)
        fadd(e, a, c)
        fsub(a, a, c)
        fmul(b, a, a)
        fsub(c, d, f)
        fmul(a, c, _121665)
        fadd(a, a, d)
        fmul(c, c, a)
        fmul(a, d, f)
        fmul(d, b, x)
        fmul(b, e, e)
        swap25519(a, b, bit)
        swap25519(c, d, bit)

    finverse(c, c)
    fmul(a, a, c)
    pack25519(u8_out, a)
