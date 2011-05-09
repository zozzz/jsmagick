'''
Created on 2011.05.06.

@author: Zozzz
'''

from jsmagick._util import Singleton, memoize

class CodeContext(object):
    __slots__ = (
        "type",
        "node"
    )

    class Type:
        CLASS = 1
        FUNCTION = 2
        MODULE = 4
        GLOBAL = 8

    def __init__(self, t):
        self.type = t

    def getCtx(self, type):
        if self.type == type:
            return self
        else:
            return self.node.ctx.getCtx(type)

    def getDefinitionByName(self, qname):
        return self.lookupQName(qname.split("."))

    def lookupQName(self, parts):
        current = parts.pop(0)
        node = self._lookupId(current)
        if node:
            if len(parts) > 0:
                return node.ctx.lookupQName(parts)
            else:
                return node
        else:
            tmp = [current]
            while len(parts) != 0:
                tmp.append(parts.pop(0))
                ret = self._lookupId(".".join(tmp))
                if ret:
                    if len(parts) > 0:
                        return ret.ctx.lookupQName(parts)
                    else:
                        return ret
        return None

    def _lookupId(self, id):
        return self.node.lookupId(id)


@Singleton
class GlobalContext(CodeContext):
    __slots__ = (

    )

    def __init__(self):
        self.node = True
        CodeContext.__init__(self, CodeContext.Type.GLOBAL)

    def addModule(self, module):
        pass

class ModuleContext(CodeContext):
    __slots__ = (

    )

    def __init__(self, node):
        CodeContext.__init__(self, CodeContext.Type.MODULE)
        self.node = node
        GlobalContext().addModule(self)

class ClassContext(CodeContext):
    __slots__ = (

    )

    def __init__(self):
        CodeContext.__init__(self, CodeContext.Type.CLASS)

class FunctionContext(CodeContext):
    def __init__(self):
        CodeContext.__init__(self, CodeContext.Type.FUNCTION)

class Reference(object):
    __slots__ = (

    )

    def __init__(self):
        pass

class ClassReference(Reference):
    __slots__ = (

    )

    def __init__(self):
        Reference.__init__(self)

import sys, imp
from os import path

class PathResolver(object):

    __path__ = []

    @classmethod
    def addSearchPath(cls, path):
        cls.__path__.append(path)

    @classmethod
    def getFilePathFromModuleName(cls, name, inModule=None):
        try:
            module = sys.modules[name]
            return module.__file__
        except KeyError:
            pass
        except AttributeError:
            pass

        try:
            fp, pathname, desc = imp.find_module(name)
            if fp:
                return pathname
        except ImportError:
            pass


        if inModule:
            cls.__path__.append(path.dirname(inModule))

        pathname = cls.__findPathOrFile(name)
        res = None
        if pathname:
            if path.isfile(pathname + ".py"):
                res = pathname + ".py"
            else:
                _init_ = path.normpath(pathname + "/__init__.py")
                if path.isfile(_init_):
                    res = _init_

        if inModule:
            cls.__path__.pop()

        return res


    @classmethod
    def __findPathOrFile(cls, name):
        parts = name.split(".")
        pl = len(parts)

        for p in cls.__path__:
            np = path.normpath(p + "/" + parts[0])
            if path.isdir(np):
                if pl > 1:
                    sp = np
                    for i in range(1, pl):
                        sp = path.normpath(sp + "/" + parts[i])
                        if not path.isdir(sp) and not path.isfile(sp + ".py"):
                            break
                        if i == pl - 1:
                            return sp
                else:
                    return np
            elif path.isfile(np + ".py"):
                return np
