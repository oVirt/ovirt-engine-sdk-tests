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

from src.errors.testerror import TestError

class IncorrrectTypeError(TestError):
    """
    IncorrrectType is raised when types mismatch has occurred
    """

    def __init__(self, dstType, producedType):
        '''
        @param dstType: the destination type of the object
        @param producedType: the actual type of the object
        '''
        Exception.__init__(
               self,
               'Required type "%s" while accepted "%s".' \
               % (dstType, producedType)
        )
