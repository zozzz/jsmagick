'''
Created on 2011.05.09.

@author: Zozzz
'''

def test1():
    print "test1"

def test2(arg1, arg2=None):
    print "test2 %s, %s" % (arg1, arg2)

def test3(*args):
    print "test3 %s" % `args`

def test4(**kw):
    print "test4 %s" % kw

def test5(arg1, arg2=None, *args, **kw):
    print "test5 %s, %s, %s, %s" % (arg1, arg2, args, kw)


test1()
test2(1)
test2(1, 2)
test3(1, 2, 3)
test4(test=1, test2=2)
test5(1, test1=1, test2=2)
_args = (2, 3, 4, 5, 6)
_kw = {'ttt':4}
test5(1, *_args, test=3, **_kw)