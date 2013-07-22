'''
Created on Jul 22, 2013

@author: mpastern
'''

class FileUtils(object):
    '''
    classdocs
    '''


    @staticmethod
    def getContent(fname, mode='r'):
        fo = None
        try:
            fo = open(fname, mode)
            return fo.read()
        finally:
            if fo: fo.close()
