'''
Created on 2011.05.17.

@author: Zozzz
'''

from _parser.parser import Parser
from _builtins.builtins import Builtins

class ConfigError(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class Compiler:
    CACHE_DIR = ""
    OUTPUT_DIR = ""

    _builtinsInited = False

    class Config:
        EOL = "\r\n"

    @classmethod
    def compile(cls, file):

        if not cls.CACHE_DIR:
            raise ConfigError("Compiler::CACHE_DIR not defined!")

        if not cls.OUTPUT_DIR:
            raise ConfigError("Compiler::OUTPUT_DIR not defined!")

        cls.initBuiltins()

        sess = CompileSession()

        Parser.setSession(sess)
        Parser.parseFile(file)

        for module in sess.modules:
            if not module.compiled:
                Builtins.initModule(module)
            print module.toJavaScript(Compiler.Config)

    @classmethod
    def initBuiltins(cls):
        if cls._builtinsInited:
            return

        Builtins.addModule("__builtins__", "jsmagick._builtins.py")

        cls._builtinsInited = True

class CompileSession:

    def __init__(self):
        self.modules = []

    def addModule(self, module):
        self.modules.append(module)