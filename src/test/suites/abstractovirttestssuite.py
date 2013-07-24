'''
Created on May 1, 2013

@author: mpastern
'''

import abc
import unittest
import logging
from src.infrastructure.annotations import measure

# from src.test.runnable import Runnable

class AbstractOvirtTestsSuite(unittest.TestCase):
    '''
    Abstract Test class
    '''
#     def __init__(self, *args, **kwargs):
#         unittest.TestCase.__init__(self, *args, **kwargs)

    __metaclass__ = abc.ABCMeta

#     def __init__(self, *args, **kwargs):
# #         unittest.TestCase.__init__(self, *args, **kwargs)
#         self.log = logging.getLogger(self.__class__.__name__)

#     @classmethod
#     def tearDownClass(cls):
#         OvirtTestsSuite.__initResourceManagers()
#
#     @staticmethod
#     def __initResourceManagers():
#         pass


#     @measure.time
    def run(self, result=None):
        super(AbstractOvirtTestsSuite, self).run(result)
