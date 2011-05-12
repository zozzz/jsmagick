'''
Created on 2011.05.12.

@author: Zozzz
'''
from base import ScriptElement
from base import HasChildren
from base import memoize

class Statement(ScriptElement):
    __slots__ = (
    )

    def __init__(self):
        ScriptElement.__init__(self)

class Assign(Statement, HasChildren):
    __slots__ = (
        "target",
        "value"
    )

    def __init__(self, target, value):
        Statement.__init__(self)
        HasChildren.__init__(self)
        self.target = target
        self.value = value

    def __repr__(self):
        return "<Assign %s=%s>" % (self.target, self.value)

class AugAssign(Assign):
    __slots__ = (
        "op"
    )

    def __init__(self, target, op, value):
        Assign.__init__(self, target, value)
        self.op = op

    def __repr__(self):
        return "<AugAssign %s>" % (self.op)

class Return(Statement):
    __slots__ = (
        "expr"
    )

    def __init__(self, expr):
        Statement.__init__(self)
        self.expr = expr

    def __repr__(self):
        return "<Return %s>" % self.expr

class TestElse(Statement):
    __slots__ = (
        "test",
        "body",
        "orelse"
    )

    def __init__(self, test, body, orelse):
        self.test = test
        self.body = body
        self.orelse = orelse
        Statement.__init__(self)

    def __repr__(self):
        s = "<%s" % (self.__class__.__name__)
        s += " %s:%s" % (self.test, self.body)
        if self.orelse:
            s += " else:%s>" % self.orelse
        else:
            s += ">"
        return s

class For(TestElse):
    __slots__ = (
        "target"
    )

    def __init__(self, target, test, body, orelse):
        TestElse.__init__(self, test, body, orelse)
        self.target = target

    def __repr__(self):
        return "<For %s in %s: %s else: %s>" % (self.target, self.test, self.body, self.orelse)


class While(TestElse):
    def __init__(self, test, body, orelse):
        TestElse.__init__(self, test, body, orelse)

class If(TestElse):
    def __init__(self, test, body, orelse):
        TestElse.__init__(self, test, body, orelse)

class With(Statement):
    __slots__ = (
        "expr",
        "vals",
        "body"
    )

    def __init__(self, expr, vals, body):
        self.expr = expr
        self.vals = vals
        self.body = body
        Statement.__init__(self)

    def __repr__(self):
        return "<With %s:%s body:%s>" % (self.expr, self.vals, self.body)

class Raise(Statement):
    __slots__ = (
        "type",
        "inst",
        "trace"
    )

    def __init__(self, type, inst, trace):
        self.type = type
        self.inst = inst
        self.trace = trace
        Statement.__init__(self)

    def __repr__(self):
        return "<Raise %s, %s, %s>" % (self.type, self.inst, self.trace)

class TryExcept(Statement, HasChildren):
    __slots__ = (
        "body",
        "orelse"
    )

    def __init__(self, body, orelse):
        self.body = body
        self.orelse = orelse
        Statement.__init__(self)
        HasChildren.__init__(self)

    def __repr__(self):
        return "<TryExcept %s, else:%s>" % (self.body, self.orelse)

class TryFinally(Statement):
    __slots__ = (
        "body",
        "final"
    )

    def __init__(self, body, final):
        Statement.__init__(self)
        self.body = body
        self.final = final

    @memoize
    def isSimple(self):
        if self.body and not isinstance(self.body.children[0], TryExcept):
            return True
        return False

    def __repr__(self):
        return "<TryFinally simple:%s, %s, %s>" % (self.isSimple(), self.body, self.final)


class ExceptHandler(Statement):
    __slots__ = (
        "type",
        "name",
        "body"
    )

    def __init__(self, type, name, body):
        self.type = type
        self.name = name
        self.body = body
        Statement.__init__(self)

    def __repr__(self):
        return "<ExceptHandler %s as %s body:%s>" % (self.type, self.name, self.body)

class Assert(Statement):
    __slots__ = (
        "test",
        "msg"
    )

    def __init__(self, test, msg):
        Statement.__init__(self)
        self.test = test
        self.msg = msg

    def __repr__(self):
        return "<Assert %s %s>" % (self.test, self.msg)

class Delete(Statement):
    __slots__ = (
        "targets"
    )

    def __init__(self, targets):
        Statement.__init__(self)
        self.targets = targets

    def __repr__(self):
        return "<Delete %s>" % self.targets

class Global(Statement):
    __slots__ = (
        "ids"
    )

    def __init__(self, ids):
        Statement.__init__(self)
        self.ids = ids

    def __repr__(self):
        return "<Global %s>" % (self.ids)

class Break(Statement):
    def __init__(self):
        Statement.__init__(self)

    def __repr__(self):
        return "<Break>"

class Continue(Statement):
    def __init__(self):
        Statement.__init__(self)

    def __repr__(self):
        return "<Continue>"