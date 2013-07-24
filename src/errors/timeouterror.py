'''
Created on May 26, 2013

@author: mpastern
'''

from src.errors.testerror import TestError

class TimeoutError(TestError):
    def __init__(self, ttl):
        '''
        @param ttl: the ttl that caused timeout
        '''
        Exception.__init__(self, "TTL {0} has expired".format(ttl))
