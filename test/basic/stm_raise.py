'''
Created on 2011.05.10.

@author: Zozzz
'''

class MyEx:

    def __init__(self, code=0, msg=None):
        self.code = code
        self.msg = msg

class MyEx2:
    pass

try:
    raise MyEx
except MyEx as x:
    pass
except (MyEx, MyEx2) as (x1, x2):
    pass
except:
    raise
else:
    print 2
    print 3
    print 4

try:
    raise MyEx(10)
finally:
    print "Final"

try:
    raise MyEx(11, "Hello")
except MyEx2:
    pass
else:
    print "Else"
finally:
    print "Final"
