'''
Created on 2011.05.12.

@author: Zozzz
'''

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
