'''
Created on May 26, 2013

@author: mpastern
'''

from src.errors.testerror import TestError

class NotFoundError(TestError):

    def __init__(self, typ, name):
        '''
        @param typ: the type of the object
        @param name: the name of the object  
        '''
        Exception.__init__(self, '%s %s is not found' % (typ, name))
