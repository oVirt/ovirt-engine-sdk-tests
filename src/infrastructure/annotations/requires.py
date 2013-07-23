'''
Created on Jun 19, 2013

@author: mpastern
'''
from src.resource.resourcemanager import ResourceManager
from src.errors.resourcemanagernotfounderror import ResourceManagerNotFoundError

class resources(object):
    def __init__(self, params):
        self.params = params
    def __call__(self, original_func):
        decorator_self = self
        def wrappee(*args, **kwargs):
            for resource in decorator_self.params:
                rm = (resource.__name__ + 'ResourceManager')
                rm_class = ResourceManager.getResourceManager(rm)
                if rm_class:
                    rm_instance = rm_class()
                    if not rm_instance.get(get_only=True):
                        rm_instance.add(**kwargs)
                        # TODO: use **kwargs for private init
                else:
                    raise ResourceManagerNotFoundError(rm)
            return original_func(*args, **kwargs)
        return wrappee
