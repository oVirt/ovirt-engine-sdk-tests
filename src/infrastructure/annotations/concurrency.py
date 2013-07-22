'''
Created on Jun 19, 2013

@author: mpastern
'''

def synchronized(lock):
    """ Synchronization decorator """
    def decorator(f):
        def nf(*args, **kw):
            with lock:
                return f(*args, **kw)
        return nf
    return decorator
