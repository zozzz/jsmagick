'''
Created on 2011.05.12.

@author: Zozzz
'''

from base import ScriptElement
from base import HasChildren

class Literal(ScriptElement):
    __slots__ = (
        "val"
    )

    def __init__(self, val):
        ScriptElement.__init__(self)
        self.val = val

    def __repr__(self):
        return "<%s>" % self.val

class ConstLiteral(Literal):
    __slots__ = (
    )

    MAP = {
        "None":"null",
        "True":"true",
        "False":"false"
    }

    def __init__(self, val):
        Literal.__init__(self, val)

class StringLiteral(Literal):
    __slots__ = (
    )

    def __init__(self, val):
        Literal.__init__(self, val)

class NumberLiteral(Literal):
    __slots__ = (
    )

    def __init__(self, val):
        Literal.__init__(self, val)

class ArrayLiteral(Literal, HasChildren):
    def __init__(self):
        Literal.__init__(self, None)
        HasChildren.__init__(self)

    def __repr__(self):
        return "<ArrayLiteral %s>" % (self.children)

class TupleLiteral(ArrayLiteral):
    def __init__(self):
        ArrayLiteral.__init__(self)

    def __repr__(self):
        return "<TupleLiteral %s>" % (self.children)

class ObjectLiteral(Literal, HasChildren):

    def __init__(self):
        Literal.__init__(self, None)
        HasChildren.__init__(self)

    def __repr__(self):
        return "<ObjectLiteral %s>" % (self.children)

class KeyValuePair(ScriptElement):
    __slots__ = (
        "key",
        "value"
    )

    def __init__(self, key, value):
        ScriptElement.__init__(self)
        self.key = key
        self.value = value

    def __repr__(self):
        return "<KeyVal k:%s, v:%s>" % (self.key, self.value)