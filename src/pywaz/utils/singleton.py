# -*- coding: utf-8 -*-
#
#    Created on 2011/02/11
#    Created by giginet
#
class Singleton(object):
    u"""Singleton Abstract class
    
    Usage:
        >>> class A(Singleton): pass
        >>> a1 = A()
        >>> a2 = A()
        >>> assert(a1 == a2)

    """
    def __new__(cls, *args, **kwargs):
        tmpInstance = None
        if not hasattr(cls, "_instanceDict"):
            cls._instanceDict = {}
            cls._instanceDict[str(hash(cls))] = super(Singleton, cls).__new__(cls)
            tmpInstance = cls._instanceDict[str(hash(cls))]
        elif not hasattr(cls._instanceDict, str(hash(cls))):
            cls._instanceDict[str(hash(cls))] = super(Singleton, cls).__new__(cls)
            tmpInstance = cls._instanceDict[str(hash(cls))]
        else:
            tmpInstance = cls._instanceDict[str(hash(cls))]
        return tmpInstance

    def __init__(self, *args, **kwargs): pass

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
