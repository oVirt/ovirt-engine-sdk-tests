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


from ovirtsdk.xml import params
from src.errors.notfounderror import NotFoundError
from src.config.configmanager import ConfigManager
from src.infrastructure.singleton import Singleton
from src.errors.incorrrecttypeerror import IncorrrectTypeError
import types
# from src.infrastructure.singleton import singleton


# @singleton
class ResourceFactory(Singleton):
    '''
    Resource factory provides resources
    construction capabilities
    '''

    __cm = ConfigManager()

    @staticmethod
    def getConfigManager():
        """
        @return: ConfigManager
        """
        return ResourceFactory.__cm

    @staticmethod
    def create(typ, **kwargs):
        """
        Creates params holder from default config
        and overrides/set properties according to kwargs

        @param kwargs: keyword args

        @return: params holder
        """

        params_holders = []

        clazz = getattr(params, typ.__name__)
        if not clazz:
            raise NotFoundError(typ, 'type')

        data = ResourceFactory.getConfigManager()\
                                 .get(typ.__name__.lower())\
                                 .get('resource')

        if isinstance(data, types.ListType):
            i = 1
            for item in data:
                params_holder = ResourceFactory.__produceParamsHolder(typ, item, **kwargs)
                # TODO: implement creation strategy
                if len(data) > 1:
                    params_holder.set_name(params_holder.get_name() + str(i))
                    i += 1
                params_holders.append(params_holder)
            return params_holders
        else:
            return ResourceFactory.__produceParamsHolder(typ, data, **kwargs)

    @staticmethod
    def __produceParamsHolder(typ, item, **kwargs):
        """
        Produces ParamsHolder and injects custom data

        @param item: item to process
        @param kwargs: keyword args

        @return: params holder
        """
        params_holder = params.parseString(item)

        if type(params_holder) != typ:
            raise IncorrrectTypeError(
                      typ.__name__,
                      type(params_holder).__name__
        )

        # TODO: revisit
        if kwargs:
            for name, value in kwargs.items():
                if name not in ConfigManager.INTERNAL_PROPERIES:
                    setattr(params_holder, name, value)

        return params_holder
