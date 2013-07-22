'''
Created on May 26, 2013

@author: mpastern
'''

from src.errors.testerror import TestError

class ResourceManagerNotFoundError(TestError):

    def __init__(self, resourcemanager):
        '''
        @param typ: the type of the object
        @param name: the name of the object  
        '''
        TestError.__init__(self, 'ResourceManager "%s" is not found!' % (resourcemanager))
