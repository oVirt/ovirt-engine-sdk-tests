'''
Created on May 26, 2013

@author: mpastern
'''

from src.errors.testerror import TestError

class ConfigNotFoundError(TestError):

    def __init__(self, cDir, cFile):
        '''
        @param cDir: config dir
        @param cFile: config file
        '''
        Exception.__init__(
           self,
           'Configuration file %s is not found at %s.' \
           % (cFile, cDir)
        )
