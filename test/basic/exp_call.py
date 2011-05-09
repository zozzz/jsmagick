'''
Created on 2011.05.09.

@author: Zozzz
'''

from def_function import *

test()

test2(1, 2, 3, arg4=3)

kw = {"arg2":333, "arg3":444, test:"alma"}
test2(1, **kw)

_args = [1, 2, 3, 4, 5, 6, 7, 8, 9]
test3(*_args)