'''
Created on 2011.05.12.

@author: Zozzz
'''

from base import ScriptElement
from base import HasChildren
from base import Property
from statement import Statement
from statement import Return

class Module(ScriptElement, HasChildren):
    __slots__ = (
        "_file",
        "doc"
    )

    class file(Property):
        def fget(self):
            return self._file

    class module(Property):
        def fget(self):
            return self

    def __init__(self, file):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)
        self._file = file

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

class Lambda(Function):

    def __init__(self, args, ret):
        Function.__init__(self, "", args, None)
        self.addChild(Return(ret))

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

    def matchId(self, id):
        if self.qname == id:
            return self
        return None

    def __repr__(self):
        return "<Identifier %s:%s>" % (self.qname, self.getType())