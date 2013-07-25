#
# Copyright (c) 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import abc
import unittest
from src.infrastructure.annotations import measure

# from src.test.runnable import Runnable

class AbstractOvirtTestsSuite(unittest.TestCase):
    '''
    Abstract Test class
    '''

    __metaclass__ = abc.ABCMeta

#     @measure.time
    def run(self, result=None):
        super(AbstractOvirtTestsSuite, self).run(result)
