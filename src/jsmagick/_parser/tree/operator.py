'''
Created on 2011.05.12.

@author: Zozzz
'''

from expression import Expression

class Operator(Expression):

    def __init__(self):
        Expression.__init__(self)

class TwoSidedOp(Operator):
    __slots__ = (
        "left", "right"
    )

    def __init__(self, left, right):
        Operator.__init__(self)
        self.left = left
        self.right = right

    def __repr__(self):
        return "<%s %s, %s>" % (self.__class__.__name__, self.left, self.right)

class BinaryOp(TwoSidedOp):
    def __init__(self, left, right):
        TwoSidedOp.__init__(self, left, right)

class opAdd(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opSub(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opMult(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opDiv(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opMod(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opPow(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opLShift(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opRShift(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opBitOr(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opBitXor(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opBitAnd(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class opFloorDiv(BinaryOp):
    def __init__(self, left, right):
        BinaryOp.__init__(self, left, right)

class UnaryOp(Operator):
    __slots__ = (
        "right"
    )

    def __init__(self, right):
        Operator.__init__(self)
        self.right = right

    def __repr__(self):
        return "<%s, %s>" % (self.__class__.__name__, self.right)

class opInvert(UnaryOp):
    def __init__(self, right):
        UnaryOp.__init__(self, right)

class opNot(UnaryOp):
    def __init__(self, right):
        UnaryOp.__init__(self, right)

class opUAdd(UnaryOp):
    def __init__(self, right):
        UnaryOp.__init__(self, right)

class opUSub(UnaryOp):
    def __init__(self, right):
        UnaryOp.__init__(self, right)

class Compare(TwoSidedOp):
    def __init__(self, left, right):
        TwoSidedOp.__init__(self, left, right)

class opEq(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opNotEq(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opLt(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opLtE(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opGt(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opGtE(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opIs(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opIsNot(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opIn(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class opNotIn(Compare):
    def __init__(self, left, right):
        Compare.__init__(self, left, right)

class BoolOp(TwoSidedOp):
    def __init__(self, left, right):
        TwoSidedOp.__init__(self, left, right)

class opAnd(BoolOp):
    def __init__(self, left, right):
        BoolOp.__init__(self, left, right)

class opOr(BoolOp):
    def __init__(self, left, right):
        BoolOp.__init__(self, left, right)