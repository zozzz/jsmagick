'''
Created on 2011.05.12.

@author: Zozzz
'''

from hashlib import md5

from base import ScriptElement
from base import HasChildren
from base import Property
from base import Scope
from statement import Statement
from statement import Return
from jsmagick._util.decors import memoize

class Module(ScriptElement, HasChildren, Scope):
    __slots__ = (
        "_file",
        "doc",
        "name"
    )

    class file(Property):
        def fget(self):
            return self._file

    class module(Property):
        def fget(self):
            return self

    def __init__(self, file, name=None):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)
        Scope.__init__(self)
        self._file = file
        self.isScope = True

        if name:
            self.name = name
        else:
            self.name = "main"

    def getParentScope(self, type=None):
        return None

    def __repr__(self):
        return "<Module file=%s>" % (self.file)

    def __js__(self):
        print self.symTable
        ret = ["function " + self.jsName() + "()"]
        ret.append("{")
        ret.append('\tvar __name__ = "' + self.name + '";')
        ret.append('\tfunction globals(){ return globals; };')

        #for child in self.children:
        #    ret.append(child.toJavaScript())

        ret.append("};")
        return ret

    @memoize
    def jsName(self):
        return 'm_' + md5(self._file).hexdigest()


class ImportModule(ScriptElement):
    __slots__ = (
        "file",
        "moduleName",
        "alias",
        "_module"
    )

    class module(Property):
        def fget(self):
            if not self._module:
                self._module = self._loadModule()
                self._module.name = self.moduleName
            return self._module

    def __init__(self, file, moduleName, alias):
        ScriptElement.__init__(self)
        self.file = file
        self.alias = alias
        self.moduleName = moduleName
        self._module = None

    def matchId(self, id):
        if self.alias == id:
            return self.module
        return None

    def _loadModule(self):
        pass

    def __repr__(self):
        return "<ImportModule %s, %s>" % (self.alias, self.file)

    def __js__(self):
        ret = ["globals." + self.alias + " = " + self.module.jsName() + ";"]
        return ret

class ImportDefinition(ImportModule):
    __slots__ = (
        "definition",
        "defAlias"
    )

    def __init__(self, file, alias, definition, defAlias):
        ImportModule.__init__(self, file, alias, alias)
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

class Class(Statement, HasChildren, Scope):
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
        self.isScope = True
        Statement.__init__(self)
        HasChildren.__init__(self)
        Scope.__init__(self)

    def matchId(self, id):
        if self.name == id:
            return self
        return None

    def __repr__(self):
        return "<Class %s(%s)>" % (self.name, self.base)

class Function(Statement, HasChildren, Scope):
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
        Scope.__init__(self)
        self.name = name
        self.args = args
        self.decors = decors
        self.locals = []
        self.isScope = True
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