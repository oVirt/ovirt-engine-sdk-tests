'''
Created on May 1, 2013

@author: mpastern
'''
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
        return ResourceManager.__cm

    @staticmethod
    def getSdk():
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
