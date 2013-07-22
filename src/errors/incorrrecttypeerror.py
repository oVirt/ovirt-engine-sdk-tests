'''
Created on May 26, 2013

@author: mpastern
'''

from src.errors.testerror import TestError

class IncorrrectTypeError(TestError):

    def __init__(self, dstType, producedType):
        '''
        @param dstType: the destination type of the object
        @param producedType: the actual type of the object
        '''
        Exception.__init__(
               self,
               'Destination "%s" type does not match to produced one "%s".' \
               % (dstType, producedType)
        )
