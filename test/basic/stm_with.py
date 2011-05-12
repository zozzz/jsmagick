'''
Created on 2011.05.10.

@author: Zozzz
'''

class Cube:
    def __enter__(self):
        return 10, 20, 30

    def __exit__(self, type, value, trace):
        print type, value, trace
        return isinstance(value, RuntimeError)

with Cube() as (x, y, z):
    raise RuntimeError
    print x, y, z