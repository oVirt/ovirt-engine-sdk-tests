'''
Created on May 26, 2013

@author: mpastern
'''

from src.errors.testerror import TestError

class NotFoundResourceConfigError(TestError):

    def __init__(self, resource):
        '''
        @param resource: the resource name  
        '''
        Exception.__init__(self, 'resource %s configuration is not found' % resource)
