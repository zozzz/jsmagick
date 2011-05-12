'''
Created on 2011.05.08.

@author: Zozzz
'''

a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

# BinOp
x = a0 & a1
x = a0 | a1
x = a0 << a1
x = a0 >> a1
x = a0 ^ a1
x = a0 + a1
x = a0 - a1
x = a0 * a1
x = a0 ** a1
x = a0 / a1
x = a0 % a1
x = a0 // a1

# Compare
x = a0 < a1
x = a0 > a1
x = a0 <= a1
x = a0 >= a1
x = a0 == a1
x = a0 != a1
x = a0 is a1
x = a1 is not a2
x = a1 in a2
x = a1 not in a2

# BoolOp
x = a0 and a1
x = a0 or a1

# UnaryOp
x = +a0
x = -a0
x = ~a0
x = not a0

# AugAssign
x &= a0
x |= a0
x <<= a0
x >>= a0
x ^= a0
x += a0
x -= a0
x *= a0
x **= a0
x /= a1
x //= a1
x %= a1
