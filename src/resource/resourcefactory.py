'''
Created on May 1, 2013

@author: mpastern
'''

from ovirtsdk.xml import params
from src.errors.notfounderror import NotFoundError
from src.config.configmanager import ConfigManager
# from src.infrastructure.singleton import singleton
from src.infrastructure.singleton import Singleton
from src.errors.incorrrecttypeerror import IncorrrectTypeError

# @singleton
class ResourceFactory(Singleton):
    '''
    ParamsHolder factory provides parameters holders
    construction capabilities
    '''

    __cm = ConfigManager()

    @staticmethod
    def getConfigManager():
        return ResourceFactory.__cm

    @staticmethod
    def create(typ, **kwargs):
        clazz = getattr(params, typ.__name__)
        if not clazz:
            raise NotFoundError(typ, 'type')
        xm_body = ResourceFactory.getConfigManager().get(typ.__name__.lower()).get('resource')
        params_holder = params.parseString(xm_body)

        if type(params_holder) != typ:
            raise IncorrrectTypeError(
                      typ.__name__,
                      type(params_holder).__name__
            )

        if kwargs:
            for name, value in kwargs.items():
                if name not in ConfigManager.INTERNAL_PROPERIES:
                    setattr(params_holder, name, value)
        return params_holder
