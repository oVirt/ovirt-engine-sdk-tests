'''
Created on Jun 17, 2013

@author: mpastern
'''

class DictUtils(object):
    '''
    Provides dict services
    '''

    @staticmethod
    def exclude(dct, keys=[]):
        if dct:
            for key in keys:
                if dct.has_key(key):
                    dct.pop(key)
