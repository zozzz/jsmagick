'''
Created on 2011.05.06.

@author: Zozzz
'''

from jsmagick._util import Property, memoize
from ctx import *
import ast

class ScriptElement(object):
    __slots__ = (
        "parent",
        "_astNode",
        "_ctx"
    )

    class ctx(Property):
        @memoize
        def fget(self):
            if self._ctx:
                return self._ctx
            elif self.parent:
                return self.parent.ctx

        def fset(self, val):
            if val.node is None:
                val.node = self
            self._ctx = val

    class astNode(Property):
        def fset(self, val):
            self._astNode = val

    def __init__(self):
        self.parent = None

    def matchId(self, id):
        raise NotImplementedError("ScriptElement::matchId in %s" % self.__class__.__name__)

    def getType(self):
        raise NotImplementedError("ScriptElement::getType in %s" % self.__class__.__name__)

    def dump(self, indent=0):
        print ("\t" * indent) + self.__repr__()
        if hasattr(self, "children"):
            for child in getattr(self, "children"):
                child.dump(indent + 1)

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

class HasChildren:
    __slots__ = (
        "children"
    )

    def __init__(self):
        self.children = []

    def addChild(self, node):
        if node is None:
            return
        node.parent = self
        self.children.append(node)
        #self._onAddChild(self, node)

    def onAddChild(self, parent, child):
        pass

    def _onAddChild(self, parent, child):
        if self.onAddChild(parent, child) is False:
            return
        self.parent._onAddChild(parent, child)

    def lookupId(self, id):
        res = None
        for child in self.children:
            m = child.matchId(id)
            if m: res = m

        return res

class Statement(ScriptElement):
    __slots__ = (
    )

    def __init__(self):
        ScriptElement.__init__(self)

class Expression(ScriptElement, HasChildren):
    __slots__ = (
        "expContext"
    )

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

    def __init__(self, expContext=0):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)
        self.expContext = expContext

class Module(ScriptElement, HasChildren):
    __slots__ = (
        "_file",
        "doc"
    )

    class file(Property):
        def fget(self):
            return self._file

    def __init__(self, file):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)
        self._file = file
        self._ctx = ModuleContext(self)

    def __repr__(self):
        return "<Module file=%s>" % (self.file)


class ImportModule(ScriptElement):
    __slots__ = (
        "file",
        "alias",
        "_module"
    )

    class module(Property):
        def fget(self):
            if not self._module:
                self._module = self._loadModule()
            return self._module

    def __init__(self, file, alias):
        ScriptElement.__init__(self)
        self.file = file
        self.alias = alias
        self._module = None

    def matchId(self, id):
        if self.alias == id:
            return self.module
        return None

    def _loadModule(self):
        pass

    def __repr__(self):
        return "<ImportModule %s, %s>" % (self.alias, self.file)


class ImportDefinition(ImportModule):
    __slots__ = (
        "definition",
        "defAlias"
    )

    def __init__(self, file, alias, definition, defAlias):
        ImportModule.__init__(self, file, alias)
        self.definition = definition
        self.defAlias = defAlias

    def matchId(self, id):
        if self.defAlias == "*":
            pass
        elif self.defAlias == id:
            return self.module.lookupId(self.definition)
        return None

    def __repr__(self):
        return "<ImportDefinition %s.%s, %s>" % (self.alias, self.defAlias, self.file)

class Class(Statement, HasChildren):
    __slots__ = (
        "name",
        "base",
        "decors",
        "doc"
    )

    def __init__(self, name, base, decors):
        self.name = name
        self.base = base
        self.decors = decors
        Statement.__init__(self)
        HasChildren.__init__(self)

    def matchId(self, id):
        if self.name == id:
            return self
        return None

    def __repr__(self):
        return "<Class %s>" % self.name

class Function(Statement, HasChildren):
    __slots__ = (
        "name",
        "args",
        "decors",
        "locals",
        "doc"
    )

    def __init__(self, name, args, decors):
        Statement.__init__(self)
        HasChildren.__init__(self)
        self._ctx = FunctionContext()
        self.name = name
        self.args = args
        self.decors = decors
        self.locals = []
        a = self.locals.append

        for arg in self.args:
            a(arg.id)

    def matchId(self, id):
        if self.name == id:
            return self
        return None

    def onAddChild(self, parent, child):
        return False

    def __repr__(self):
        return "<Function %s(%s)>" % (self.name, self.args)

class FArgument(ScriptElement):
    __slots__ = (
        "id",
        "default"
    )

    def __init__(self, id, default):
        ScriptElement.__init__(self)
        self.id = id
        self.default = default

    def __repr__(self):
        return "<FArgument %s=%s>" % (self.id.name, self.default)

class VarArg(FArgument):

    def __init__(self, id):
        FArgument.__init__(self, id, None)

    def __repr__(self):
        return "<VarArg %s>" % self.id.qname

class KwArg(FArgument):

    def __init__(self, id):
        FArgument.__init__(self, id, None)

    def __repr__(self):
        return "<KwArg %s>" % self.id.qname

class Identifier(ScriptElement):
    __slots__ = (
        "qname",
        "name"
    )

    def __init__(self, qname):
        ScriptElement.__init__(self)
        p = qname.split(".")
        self.name = p.pop()
        self.qname = qname
        del p

    def getType(self):
        pass

    @memoize
    def declared(self):
        pass

    def matchId(self, id):
        if self.qname == id:
            return self
        return None

    def __repr__(self):
        return "<Identifier %s:%s>" % (self.qname, self.getType())

class Attribute(Expression):

    def __init__(self, ctx):
        Expression.__init__(self, ctx)

    def __repr__(self):
        return "<Attribute %s>" % (self.children)

class Assign(ScriptElement, HasChildren):
    __slots__ = (
        "target",
        "value"
    )

    def __init__(self, target, value):
        ScriptElement.__init__(self)
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

class ConstLiteral(ScriptElement):
    __slots__ = (
        "val"
    )

    MAP = {
        "None":"null",
        "True":"true",
        "False":"false"
    }

    def __init__(self, val):
        ScriptElement.__init__(self)
        self.val = val

    def __repr__(self):
        return "<%s>" % self.val

class StringLiteral(ScriptElement):
    __slots__ = (
        "val"
    )

    def __init__(self, val):
        ScriptElement.__init__(self)
        self.val = val

class NumberLiteral(ScriptElement):
    __slots__ = (
        "val"
    )

    def __init__(self, val):
        ScriptElement.__init__(self)
        self.val = val

class ArrayLiteral(ScriptElement, HasChildren):
    def __init__(self):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)

    def __repr__(self):
        return "<ArrayLiteral %s>" % (self.children)

class TupleLiteral(ArrayLiteral):
    def __init__(self):
        ArrayLiteral.__init__(self)

    def __repr__(self):
        return "<TupleLiteral %s>" % (self.children)

class ObjectLiteral(ScriptElement, HasChildren):

    def __init__(self):
        ScriptElement.__init__(self)
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

class CodeBlock(ScriptElement, HasChildren):
    def __init__(self):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)

    def __repr__(self):
        return "<CodeBlock %s>" % (self.children)

class For(Statement):
    __slots__ = (
        "target",
        "expr",
        "body",
        "orelse"
    )

    def __init__(self, target, expr, body, orelse):
        Statement.__init__(self)
        self.target = target
        self.expr = expr
        self.body = body
        self.orelse = orelse

    def __repr__(self):
        return "<For %s in %s: %s else: %s>" % (self.target, self.expr, self.body, self.orelse)

class Call(Expression):
    __slots__ = (
        "id",
        "args",
        "kwargs",
        "args_ref",
        "kwargs_ref"
    )

    def __init__(self, id, args, kwargs, args_ref, kwargs_ref):
        Expression.__init__(self, Expression.Context.LOAD)
        self.id = id
        self.args = args
        self.kwargs = kwargs
        self.args_ref = args_ref
        self.kwargs_ref = kwargs_ref

    def __repr__(self):
        return "<Call %s(%s, %s, %s, %s)>" % (self.id, self.args, self.kwargs, self.args_ref, self.kwargs_ref)

class Print(Call):
    __slots__ = (
        "newLine",
        "dest"
    )

    def __init__(self, dest, args, nl):
        self.newLine = nl and True or False
        self.dest = dest;
        Call.__init__(self, Identifier("print" + (self.newLine and "nl" or "")), args, None, None, None)

    def __repr__(self):
        return "<Print %s, %s>" % (Call.__repr__(self), self.dest)

class Return(Statement):
    __slots__ = (
        "expr"
    )

    def __init__(self, expr):
        Statement.__init__(self)
        self.expr = expr

    def __repr__(self):
        return "<Return %s>" % self.expr

class Delete(Statement):
    __slots__ = (
        "targets"
    )

    def __init__(self, targets):
        Statement.__init__(self)
        self.targets = targets

    def __repr__(self):
        return "<Delete %s>" % self.targets

#===============================================================================
# OPERATORS
#===============================================================================
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

# dummy
class ScriptContainer(ScriptElement, HasChildren):
    def __init__(self):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)