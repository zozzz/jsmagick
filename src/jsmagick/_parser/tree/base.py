'''
Created on 2011.05.12.

@author: Zozzz
'''

from jsmagick._util import Property
from jsmagick._util import memoize

class ScriptElement(object):
    __slots__ = (
        "parent",
        "_astNode",
        "_ctx"
    )

    class ctx(Property):
        @memoize
        def fget(self):
            pass
            """if self._ctx:
                return self._ctx
            elif self.parent:
                return self.parent.ctx"""

        def fset(self, val):
            if val.node is None:
                val.node = self
            self._ctx = val

    class astNode(Property):
        def fset(self, val):
            self._astNode = val

    class module(Property):
        @memoize
        def fget(self):
            return self.parent.module

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


class Scope:
    __slots__ = (
        "_parent",
        "_chain"
    )

    @classmethod
    def current(cls):
        pass

    @classmethod
    def enter(cls, scope):
        pass

    @classmethod
    def exit(cls):
        pass

    def __init__(self, parent=None):
        self._parent = parent
        self._chain = []

# self.test.x.y.z
# self => Refrence(id=Identifier(self), scope=Class)
# self.test => Reference(id=Identifier(test), scope=Reference(self))
class Reference(ScriptElement, Scope):
    __slots__ = (
        "id"
    )

    def __init__(self, id, scope):
        ScriptElement.__init__(self)
        Scope.__init__(self, scope)
        self.id = id