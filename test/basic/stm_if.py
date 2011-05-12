'''
Created on 2011.05.10.

@author: Zozzz
'''

bool_ = True
x = 10
y = 11

if bool_: print "OK"

if x == y:
    print "EQ"
else:
    print "NEQ"

if x == y:
    print "EQ"
elif x + 1 == y:
    print "EQ x+1"
else:
    print "NEQ"