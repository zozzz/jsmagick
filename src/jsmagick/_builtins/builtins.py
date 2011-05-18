'''
Created on 2011.05.17.

@author: Zozzz
'''

#from jsmagick._parser import SymbolTable
from jsmagick._parser import PathResolver
from jsmagick._parser import ImportModule

class Builtins:
    MODULES = []

    @classmethod
    def addModule(cls, importName, moduleName):
        cls.MODULES.append((importName, PathResolver.getFilePathFromModuleName(moduleName)))

    @classmethod
    def initModule(cls, module):
        if module.file in cls.MODULES:
            return

        for name, file in reversed(cls.MODULES):
            module.children.insert(0, ImportModule(file, name, name))