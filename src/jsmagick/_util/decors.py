'''
Created on 2011.05.06.

@author: Zozzz
'''
import functools

class MetaProperty(type):

    def __new__(meta, class_name, bases, new_attrs): #@NoSelf
        if bases == (object,):
            # The property class itself
            return type.__new__(meta, class_name, bases, new_attrs)
        fget = new_attrs.get('fget')
        fset = new_attrs.get('fset')
        fdel = new_attrs.get('fdel')
        fdoc = new_attrs.get('__doc__')
        return property(fget, fset, fdel, fdoc)

class Property(object):

    __metaclass__ = MetaProperty

    def __new__(cls, fget=None, fset=None, fdel=None, fdoc=None):
        if fdoc is None and fget is not None:
            fdoc = fget.__doc__
        return property(fget, fset, fdel, fdoc)

class Singleton:
    __instance__ = None

    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        if self.__instance__ is None:
            self.__instance__ = self.cls(*args, **kwargs)
        return self.__instance__

    def __getattr__(self, name):
        return getattr(self.cls, name)

class memoize(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)

class JavaScript:

    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)
