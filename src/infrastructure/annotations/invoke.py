'''
Created on Jun 19, 2013

@author: mpastern
'''
class postrun(object):
    def __init__(self, params):
        self.params = params
    def __call__(self, original_func):
        decorator_self = self
        def wrappee(*args, **kwargs):
            return original_func(*args, **kwargs)
            for method in decorator_self.params:
                method()
        return wrappee

class prerun(object):
    def __init__(self, params):
        self.params = params
    def __call__(self, original_func):
        decorator_self = self
        def wrappee(*args, **kwargs):
            for method in decorator_self.params:
                method()
            return original_func(*args, **kwargs)
        return wrappee
