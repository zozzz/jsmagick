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
        "name",
        "builtin"
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
        self.builtin = False

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
        ret = []
        ret.append('/*%s*/' % self.file)
        ret.append("function " + self.jsName() + "()")
        ret.append("{")
        ret.append('\tvar __name__ = "' + self.name + '";')
        ret.append('\tfunction %s(){ return %s; };' % (self.js_accessSymbol(None), self.js_accessSymbol(None)))

        for child in self.children:
            ret.append(child.toJavaScript())

        ret.append("};")
        return ret

    def js_defineSymbol(self, name):
        if '.' in name:
            names = name.split('.')
            defs = [self.js_accessSymbol(None)]
            ret = []
            while True:
                curr = names.pop(0)
                ret.append("if( !('%s' in %s) )" % (curr, ".".join(defs)))
                defs.append(curr)
                ret.append("%s={};" % (".".join(defs)))
                if len(names) == 1:
                    defs.append(names.pop(0))
                    break
            ret.append(".".join(defs))
            return " ".join(ret)
        return "%s.%s" % (self.js_accessSymbol(None), name)

    def js_accessSymbol(self, name):
        if name is None:
            return "globals"
        return "%s.%s" % (self.js_accessSymbol(None), name)

    @memoize
    def jsName(self):
        return 'm_' + md5(self._file).hexdigest()


class ImportModule(ScriptElement):
    __slots__ = (
        "moduleName",
        "alias",
        "_module"
    )

    class module(Property):
        def fget(self):
            #if not self._module:
            #    self._module = self._loadModule()
            #    self._module.name = self.moduleName
            return self._module

    def __init__(self, module, moduleName, alias):
        ScriptElement.__init__(self)
        self._module = module
        self.alias = alias
        self.moduleName = moduleName

    def matchId(self, id):
        if self.alias == id:
            return self.module
        return None

    #def _loadModule(self):
    #    pass

    def __repr__(self):
        return "<ImportModule %s, %s>" % (self.alias, self.module)

    def __js__(self):
        ret = [self.parent.js_defineSymbol(self.alias) + " = " + self.module.jsName() + ";"]
        return ret

class ImportDefinition(ImportModule):
    __slots__ = (
        "definition",
        "defAlias"
    )

    def __init__(self, module, alias, definition, defAlias):
        ImportModule.__init__(self, module, alias, alias)
        self.definition = definition
        self.defAlias = defAlias

    def matchId(self, id):
        if self.defAlias == "*":
            pass
        elif self.defAlias == id:
            return self.module.lookupId(self.definition)
        return None

    def __repr__(self):
        return "<ImportDefinition %s.%s, %s>" % (self.alias, self.defAlias, self.module)

    def __js__(self):
        if self.defAlias == "*":
            return [self.module.jsName() + ".importAll(" + self.scope.js_accessSymbol(None) + ")"]
        else:
            return [self.scope.js_defineSymbol(self.defAlias) + "=" + self.module.jsName() + "." + self.definition]

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

    def __js__(self):
        return ["%s" % self.qname]