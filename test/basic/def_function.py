'''
Created on 2011.05.07.

@author: Zozzz
'''

def test():
    return 10

def test2(arg1, arg2=None, arg3=False, arg4=test):
    return 10, 20

def test3(*args):
    pass

def test4(**kwargs):
    pass

def test5(test, *args, **kwargs):
    pass

def test6(x=10, y= -2.2, label="Button"):
    pass