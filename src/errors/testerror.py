'''
Created on May 26, 2013

@author: mpastern
'''

class TestError(Exception):
    def __init__(self, msg):
        '''
        @param msg: the error message
        '''
        Exception.__init__(self, msg)

