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


from src.config.configmanager import ConfigManager
from src.infrastructure.singleton import Singleton

from ovirtsdk.api import API

import threading
from src.infrastructure.reflectionhelper import ReflectionHelper

# @singleton
class ResourceManager(Singleton):
    '''
    ResourceManager providing resource construction
    and location services
    '''

    __sdk = None
    __cm = ConfigManager()
    __lock = threading.RLock()
    __mombers_map = {}

    ########### infra ##############

    @staticmethod
    def getConfigManager():
        """
        @return: ConfigManager
        """

        return ResourceManager.__cm

    @staticmethod
    def getSdk():
        """
        @return: oVirt SDK instance
        """

        if not ResourceManager.__sdk:
            with ResourceManager.__lock:
                if not ResourceManager.__sdk:
                    sdk_config = ResourceManager.getConfigManager().get(
                                    'sdk',
                                    exclude=ConfigManager.INTERNAL_PROPERIES
                    )
                    ResourceManager.__sdk = API(**sdk_config)
                    # FIXME: remove INTERNAL_PROPERIES internally
        return ResourceManager.__sdk

    @staticmethod
    def getResourceManager(resource):
        """
        @return: ResourceManager
        """

        if resource.lower() not in ResourceManager.__mombers_map.keys():
            with ResourceManager.__lock:
                if resource.lower() not in ResourceManager.__mombers_map.keys():
                    clazz = ReflectionHelper.getClass(
                                  "src.resource." +
                                  resource.lower() +
                                  "." +
                                  resource
                    )
                    ResourceManager.__mombers_map[
                              resource.lower()
                    ] = clazz
        return ResourceManager.__mombers_map[resource.lower()]
