'''
Created on 2011.05.10.

@author: Zozzz
'''

g1_test, g2_test = 2, 3

def ttt():
    global g1_test
    print g1_test

    for x in [g1_test, g2_test]:
        print x
        break

    for x in range(1, 10):
        if x > 4:
            continue
        print x