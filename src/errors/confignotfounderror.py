'''
Created on May 26, 2013

@author: mpastern
'''

from src.errors.testerror import TestError


class ConfigNotFoundError(TestError):

    def __init__(self, cFile):
        '''
        @param cFile: config file
        '''
        Exception.__init__(
           self,
           'Configuration file "%s" was not found.' \
           % (cFile)
        )
