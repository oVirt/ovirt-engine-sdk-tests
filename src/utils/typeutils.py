'''
Created on Jun 17, 2013

@author: mpastern
'''

class TypeUtils(object):
    '''
    Provides type related services
    '''

    @staticmethod
    def str2bool(string):
        return string.lower() in ("True", "true", "yes")
