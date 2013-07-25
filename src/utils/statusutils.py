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


import time
from src.errors.notfounderror import NotFoundError
from src.errors.timeouterror import TimeoutError

class StatusUtils(object):
    '''
    Providing status related services
    '''

    @staticmethod
    def wait(method, status, ttl=240, sleep=2):
        """
        Waits for status condition
        
        @param method: the method to invoke in order to fetch the entity
        @param status: the status to wait for
        @param ttl: time to wait in seconds (default 240 seconds)
        @param sleep: check interval in seconds (default 2 seconds)
        
        @raise NotFoundError: when destination object not found
        @raise TimeoutError: after ttl expires
        """
        while ttl > 0:
            wait_object = method(get_only=True)
            if not wait_object:
                raise NotFoundError('type', 'defined for wait()')
            if wait_object.status.state and wait_object.status.state == status:
                return
            time.sleep(sleep)
            ttl -= sleep
        raise TimeoutError(ttl)

    @staticmethod
    def waitRemoved(method, ttl=240, sleep=2):
        """
        Waits for resource to being removed
        
        @param method: the method to invoke in order to fetch the entity
        @param ttl: time to wait in seconds (default 240 seconds)
        @param sleep: check interval in seconds (default 2 seconds)
        
        @raise TimeoutError: after ttl expires
        """
        while ttl > 0:
            wait_object = method(get_only=True)
            if not wait_object:
                return
            time.sleep(sleep)
            ttl -= sleep
        raise TimeoutError(ttl)
