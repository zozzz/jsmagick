'''
Created on 2011.05.17.

@author: Zozzz
'''

#from jsmagick._parser import SymbolTable
from jsmagick._parser import PathResolver
from jsmagick._parser import ImportModule
from jsmagick._parser import ImportDefinition
from jsmagick._parser import Parser

class Builtins:
    MODULES = []

    @classmethod
    def addModule(cls, importName, moduleName):
        cls.MODULES.append((importName, PathResolver.getFilePathFromModuleName(moduleName)))

    @classmethod
    def loadAll(cls):
        for name, file in cls.MODULES:
            module = Parser.parseFile(file)
            module.builtin = True
            module.name = name

    @classmethod
    def getFiles(cls):
        ret = []
        for name, file in cls.MODULES:
            ret.append(file)
        return ret

    @classmethod
    def initModule(cls, module):
        if module.builtin:
            return

        for name, file in reversed(cls.MODULES):

            builtin = Parser.parseFile(file)
            builtin.name = name
            builtin.builtin = True

            imp1 = ImportModule(builtin, name, name)
            imp2 = ImportDefinition(builtin, name, '*', '*')
            module.children.insert(0, imp1)
            module.children.insert(0, imp2)
            imp1.parent = module
            imp2.parent = module