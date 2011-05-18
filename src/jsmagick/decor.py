'''
Created on 2011.05.17.

@author: Zozzz
'''

class JavaScript:

    def __init__(self, doc=False):
        self.doc = doc

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)