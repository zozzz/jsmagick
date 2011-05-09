'''
Created on 2011.05.09.

@author: Zozzz
'''

l = [1, 2, 3, 4, 5]

for x in l:
    print x
    print x ** 2

l = {
    "key1": "val1",
    "key2": "val2",
    "key3": "val3",
    "key4": "val4"
}

for x in l:
    print x

for (k, v) in l.iteritems():
    print "%s: %s" % (k, v)

for k in []:
    pass
else:
    print "EMPTY"