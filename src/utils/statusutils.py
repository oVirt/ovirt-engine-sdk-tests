'''
Created on Jul 24, 2013

@author: mpastern
'''

import time
from src.errors.notfounderror import NotFoundError
from src.errors.timeouterror import TimeoutError

class StatusUtils(object):
    '''
    classdocs
    '''

    @staticmethod
    def wait(method, status, ttl=240):
        while ttl > 0:
            wait_object = method(get_only=True)
            if not wait_object:
                raise NotFoundError('type', 'defined for wait()')
            if wait_object.status.state and wait_object.status.state == status:
                return
            time.sleep(2)
            ttl -= 2
        raise TimeoutError(ttl)

    @staticmethod
    def waitRemoved(method, ttl=240):
        while ttl > 0:
            wait_object = method(get_only=True)
            if not wait_object:
                return
            time.sleep(2)
            ttl -= 2
        raise TimeoutError(ttl)
