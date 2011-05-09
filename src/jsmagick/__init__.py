
__version__ = 1.0
__author__ = "Zozzz"

from _tree.ctx import PathResolver
from _tree.parser import Parser



def compile(file):
    Parser.parseFile(file)