'''
Created on 2011.05.18.

@author: Zozzz
'''

class A:
    A = 1

class B(A):
    def printA(self):
        print self.A

a = A()
print a.A

b = B()
b.printA()
A.A = 3
b.printA()