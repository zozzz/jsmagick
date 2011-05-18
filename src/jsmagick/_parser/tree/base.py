'''
Created on 2011.05.12.

@author: Zozzz
'''

from jsmagick._util import Property
from jsmagick._util import memoize

class ScriptElement(object):
    __slots__ = (
        "parent",
        "isScope",
        "_astNode",
        "_ctx",
        "_cfg",
        "compiled",
        "compiledSource"
    )

    class astNode(Property):
        def fset(self, val):
            self._astNode = val

    class module(Property):
        @memoize
        def fget(self):
            return self.parent.module

    class config(Property):
        @memoize
        def fget(self):
            if self._cfg:
                return self._cfg
            else:
                return self.parent.config

    class level(Property):
        @memoize
        def fget(self):
            if not self.parent:
                return 0
            else:
                return self.parent.level + 1

    def __init__(self):
        self.parent = None
        self.isScope = False
        self.compiled = False
        self._cfg = None

    def matchId(self, id):
        raise NotImplementedError("ScriptElement::matchId in %s" % self.__class__.__name__)

    def getType(self):
        raise NotImplementedError("ScriptElement::getType in %s" % self.__class__.__name__)

    @memoize
    def getParentScope(self, type=None):
        if isinstance(self.parent, Scope) is False:
            return self.parent.getParentScope(type)
        elif type:
            if isinstance(self.parent, type):
                return self.parent
        else:
            return self.parent
        return None

    def dump(self, indent=0):
        print ("\t" * indent) + self.__repr__()
        if hasattr(self, "children"):
            for child in getattr(self, "children"):
                child.dump(indent + 1)

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def toJavaScript(self, cfg=None):
        if self.compiled is False:
            if cfg:
                self._cfg = cfg
            arr = self.__js__()
            self.compiledSource = ""
            for line in arr:
                self.compiledSource += ("\t" * self.level) + line + self.config.EOL

            self.compiled = True
        return self.compiledSource

    def __js__(self):
        raise NotImplementedError("ScriptElement::__js__ in %s" % self.__class__.__name__)

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

    def findDefinition(self, name):
        pass

    def lookupId(self, id):
        res = None
        for child in self.children:
            m = child.matchId(id)
            if m: res = m

        return res

class CodeBlock(ScriptElement, HasChildren):
    def __init__(self):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)

    def __repr__(self):
        return "<CodeBlock %s>" % (self.children)

class ScriptContainer(ScriptElement, HasChildren):
    def __init__(self):
        ScriptElement.__init__(self)
        HasChildren.__init__(self)

class SymbolTable(object):
    __slots__ = (
        "symbols"
    )

    def __init__(self):
        self.symbols = {}

    def add(self, sym):
        self.symbols[sym.name] = sym

    def get(self, name):
        return self.symbols.get(name, None)

    def extend(self, symTable):
        pass

    def clone(self):
        pass

    def __repr__(self):
        ret = []
        for (k, v) in self.symbols.iteritems():
            ret.append("%s = %s" % (k, v))
        return "\n".join(ret)

class Symbol(object):
    __slots__ = (
        "scope",
        "name",
        "reference"
    )

    def __init__(self, name, reference, scope):
        self.name = name
        self.reference = reference
        self.scope = scope

    def __repr__(self):
        return "<Symbol for=%s>" % self.reference

class Scope:
    # ez csak a parsolaskor kell
    CURRENT = None

    __slots__ = (
        "symTable"
    )

    def __init__(self):
        self.symTable = SymbolTable()

    def addSymbol(self, name, reference):
        self.symTable.add(Symbol(name, reference, self))

    def findSymbol(self, name, allowGlobal=False):
        sym = self.symTable.get(name)
        if not sym and allowGlobal:
            sym = self.module.findSymbol(name, allowGlobal)
        return sym


# self.test.x.y.z
# self => Refrence(id=Identifier(self), scope=Class)
# self.test => Reference(id=Identifier(test), scope=Reference(self))
#class Reference(ScriptElement, HasChildren):
#    __slots__ = (
#        "id"
#    )
#
#    def __init__(self, id):
#        ScriptElement.__init__(self)
#        HasChildren.__init__(self)
#        self.id = id
#
#    def findDefinition(self, name):
#        return self.id.findDefinition(name)
#
#    def matchId(self, id):
#        if self.id.name == id:
#            return self.id
#        return None
