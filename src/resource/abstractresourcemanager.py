'''    
Created on May 26, 2013

@author: mpastern
'''

from src.resource.resourcemanager import ResourceManager
from abc import ABCMeta, abstractmethod
import threading
from ovirtsdk.xml import params
from src.config.configmanager import ConfigManager
from src.infrastructure.singleton import Singleton
from src.errors.notfounderror import NotFoundError
from src.errors.notcreatederror import NotCreatedError

class AbstractResourceManager(Singleton):

    __metaclass__ = ABCMeta

    def __init__(self, resourceType):

        assert resourceType != None

        self.__rm = ResourceManager()
        self.__lock = threading.RLock()
        self.__resourceType = resourceType

        self.__resource = None

    def getResourceManager(self):
        return self.__rm

    def getName(self):
        return self.getResourceConfig().get_name()

    def getType(self):
        return self.__resourceType

    def getTypeName(self):
        return self.getType().__name__.lower()

    def getResourceConfig(self):
        if not self.__resource:
            with self.__lock:
                if not self.__resource:
                    self.__resource = self.__doGetResourceConfig()
        return self.__resource

    def __doGetResourceConfig(self):
        return params.parseString(
                 ConfigManager
                     .get(self.__resourceType.__name__.lower())
                     .get('resource'))


    def raiseNotFoundError(self):
        raise NotFoundError(self.getType(), self.getName())

    def raiseNotCreatedError(self):
        raise NotCreatedError(self.getType(), self.getName())

    def injectExpectParam(self, kwargs):
        if not kwargs:
            kwargs = {}
        kwargs['expect'] = '201-created'

    def isCreateOnDemand(self):
        """
        Creates the resource on demand if it's enabled in the resource config
        """
        return ConfigManager.get(self.getTypeName()).get('create_on_demand')

    @abstractmethod
    def get(self, get_only=False, **kwargs):
        pass

    @abstractmethod
    def list(self, **kwargs):
        pass

    @abstractmethod
    def add(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def remove(self, **kwargs):
        pass
