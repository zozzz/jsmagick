'''
Created on 2011.05.12.

@author: Zozzz
'''

TOP_LEVEL = "TOP_LEVEL"

def test():
    global TEST
    TEST = "NOOOO"
    LOCAL = "LOCAL"
    TOP_LEVEL = LOCAL
    print TOP_LEVEL

class Test:

    CLASS_LEVEL = "CLASS_LEVEL"

    def __init__(self, arg):
        print self.CLASS_LEVEL

    def glob(self):
        global TOP_LEVEL
        TOP_LEVEL += " added this from class"
        print TOP_LEVEL

    def err(self):
        TOP_LEVEL = "haha"
        print TOP_LEVEL

TEST = "TEST"

print TOP_LEVEL

test()

print TOP_LEVEL, TEST

T = Test(1)
T.glob()
T.err()

print TOP_LEVEL

import scope_sub