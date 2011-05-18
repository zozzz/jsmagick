'''
Created on 2011.05.12.

@author: Zozzz
'''

import ast

from base import ScriptElement
from base import HasChildren

from definition import Identifier

class Context:
    LOAD = 1
    STORE = 2
    DEL = 4
    AUG_LOAD = 8
    AUG_STORE = 16
    PARAM = 32

    @classmethod
    def getCtxFromAstNode(cls, node):
        if isinstance(node, ast.Load):
            return cls.LOAD

        elif isinstance(node, ast.Store):
            return cls.STORE

        elif isinstance(node, ast.Del):
            return cls.DEL

        elif isinstance(node, ast.AugLoad):
            return cls.AUG_LOAD

        elif isinstance(node, ast.AugStore):
            return cls.AUG_STORE

        elif isinstance(node, ast.Param):
            return cls.PARAM

class Expression(ScriptElement, HasChildren):
    __slots__ = (
        "ctx"
    )

    def __init__(self, ctx=0):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)
        self.ctx = ctx

class Attribute(Expression):

    def __init__(self, ctx):
        Expression.__init__(self, ctx)

    def __repr__(self):
        return "<Attribute %s>" % (self.children)

class Call(Expression):
    __slots__ = (
        "id",
        "args",
        "kwargs",
        "args_ref",
        "kwargs_ref"
    )

    def __init__(self, id, args, kwargs, args_ref, kwargs_ref):
        Expression.__init__(self, Context.LOAD)
        self.id = id
        self.args = args
        self.kwargs = kwargs
        self.args_ref = args_ref
        self.kwargs_ref = kwargs_ref

    def __repr__(self):
        return "<Call %s(%s, %s, %s, %s)>" % (self.id, self.args, self.kwargs, self.args_ref, self.kwargs_ref)

class Subscript(Expression):
    __slots__ = (
        "id",
        "slice"
    )

    def __init__(self, id, slice, ctx):
        Expression.__init__(self, ctx)
        self.id = id
        self.slice = slice

    def __repr__(self):
        return "<Subscript %s, %s, %s>" % (self.id, self.slice, self.ctx)

class Slice(ScriptElement):
    __slots__ = (
        "lower",
        "upper",
        "step"
    )

    def __init__(self, lower, upper, step):
        ScriptElement.__init__(self)
        self.lower = lower
        self.upper = upper
        self.step = step

    def __repr__(self):
        return "<Slice %s, %s, %s>" % (self.lower, self.upper, self.step)

class Index(ScriptElement):
    __slots__ = (
        "value"
    )

    def __init__(self, value):
        ScriptElement.__init__(self)
        self.value = value

    def __repr__(self):
        return "<Index %s>" % self.value

class Print(Call):
    __slots__ = (
        "newLine",
        "dest"
    )

    def __init__(self, dest, args, nl):
        self.newLine = nl and True or False
        self.dest = dest;
        # TODO: find print refrence in GlobalScope
        Call.__init__(self, Identifier("print" + (self.newLine and "ln" or "")), args, None, None, None)

    def __repr__(self):
        return "<Print %s, %s>" % (Call.__repr__(self), self.dest)
