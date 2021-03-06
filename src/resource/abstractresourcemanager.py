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


from src.resource.resourcemanager import ResourceManager
from abc import ABCMeta, abstractmethod
import threading
from ovirtsdk.xml import params
from src.config.configmanager import ConfigManager
from src.infrastructure.singleton import Singleton
from src.errors.notfounderror import NotFoundError
from src.errors.notcreatederror import NotCreatedError
import types
from src.resource.resourcefactory import ResourceFactory

class AbstractResourceManager(Singleton):
    """
    Abstract ResourceManager
    """

    __metaclass__ = ABCMeta

    def __init__(self, resourceType):

        assert resourceType != None

        self.__rm = ResourceManager()
        self.__lock = threading.RLock()
        self.__resourceType = resourceType

        self.__resource = None

    def getResourceManager(self):
        """
        @return: ResourceManager
        """

        return self.__rm

    def getName(self):
        """
        @return: Resource name as it defined at resource config
        """

        configs = self.getResourceConfig()
        if isinstance(configs, types.ListType):
            return configs[0].get_name()
        return configs.get_name()

    def getType(self):
        """
        @return: Resource type
        """

        return self.__resourceType

    def getTypeName(self):
        """
        @return: Resource type name
        """

        return self.getType().__name__.lower()

    def getResourceConfig(self):
        """
        @return: Resource ResourceConfig
        """

        if not self.__resource:
            with self.__lock:
                if not self.__resource:
                    self.__resource = self.__doGetResourceConfig()
        return self.__resource

    def __doGetResourceConfig(self):
        configs = ConfigManager \
                     .get(self.__resourceType.__name__.lower()) \
                     .get('resource')

        if isinstance(configs, types.ListType):
            config_items = []
            i = 1
            for item in configs:
                item_param = params.parseString(item)
                if len(configs) > 1:
                    item_param.set_name(item_param.get_name() + str(i))
                    # TODO: implement creation params strategy
                config_items.append(item_param)
                i += 1
            return config_items
        return params.parseString(configs)

    def _doAdd(self, collection, **kwargs):
        """
        Adds default resource/s according to the default configuration/s
        (default configuration can be overridden with custom config
        via keyword args)  

        @param collection: the collection to invoke .add() on
        @param kwargs: keyword args

        @return: DataCenter
        """

        resource = self.getOnly(**kwargs)
        if not resource:
            params_holders = ResourceFactory.create(
                                        self.getType(),
                                        **kwargs
            )

            if isinstance(params_holders, types.ListType):
                create_responses = []

                for params_holder in params_holders:
                    create_responses.append(
                        collection.add(params_holder)
                    )
                return create_responses
            else:
                return collection.add(params_holders)
        return resource

    def _doGet(self, collection, get_only=False, **kwargs):
        """
        Fetches default resource
        (creates it if not exist if configured to create_on_demand)

        @param get_only: do not create on absence
        @param kwargs: keyword args

        @return: Cluster
        """

        if not kwargs or not kwargs.has_key("name"):
            kwargs = {'name': self.getName()}

        resource = collection.get(**kwargs)

        if not resource and not get_only:
            if self.isCreateOnDemand():
                result = self.add()
                if result and isinstance(result, types.ListType):
                    return result[0]
                return result
            else:
                self.raiseNotFoundError()
        return resource

    def raiseNotFoundError(self):
        """
        @raise NotFoundError: when entity is not found
        """
        raise NotFoundError(self.getType(), self.getName())

    def raiseNotCreatedError(self):
        """
        @raise NotCreatedError: when entity was not created
        """

        raise NotCreatedError(self.getType(), self.getName())

    def injectExpectParam(self, kwargs):
        """
        Injects in to kwarg args an 'expect'
        
        @return: updated kwargs
        """

        if not kwargs:
            kwargs = {}
        kwargs['expect'] = '201-created'
        return kwargs

    def isCreateOnDemand(self):
        """
        Checks if the resource should be created on
        demand according to the resource config
        """
        return ConfigManager.get(self.getTypeName()).get('create_on_demand')

    def getOnly(self, **kwargs):
        """
        Fetches default Resource

        @param kwargs: keyword args

        @return: default Resource
        """

        return self.get(get_only=True, **kwargs)

    @abstractmethod
    def get(self, get_only=False, **kwargs):
        """
        Abstract method used to fetches the default resource
        """
        pass

    @abstractmethod
    def list(self, **kwargs):
        """
        Abstract method used to list all resources
        """
        pass

    @abstractmethod
    def add(self, **kwargs):
        """
        Abstract method used to create the default/custom resource
        """
        pass

    @abstractmethod
    def update(self, **kwargs):
        """
        Abstract method used to update the default resource
        """
        pass

    @abstractmethod
    def remove(self, **kwargs):
        """
        Abstract method used to remove the default resource
        """
        pass
