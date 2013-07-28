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


import os
import types
import threading

from ovirtsdk.utils.ordereddict import OrderedDict
from src.infrastructure.singleton import Singleton
from ConfigParser import ConfigParser
from src.errors.confignotfounderror import ConfigNotFoundError
from src.utils.typeutils import TypeUtils
from src.utils.dictutils import DictUtils
from src.utils.fileutils import FileUtils
from src.errors.notfoundresourceconfigerror import NotFoundResourceConfigError
from src.utils.xmlutils import XmlUtils
# from src.infrastructure.singleton import singleton

# @singleton
class ConfigManager(Singleton):
    """
    ConfigManager managing test suite config
    """

    __dict = None
    __custom_dict = None
    __lock = threading.RLock()

    INTERNAL_PROPERIES = ['__name__', 'create_on_demand']
    INTERNAL_SECTIONS = ['sdk', 'tests']

    # FIXME: fetch slash for platform
    CONFIG_DIR = os.getcwd() + os.sep + "src" + os.sep + "config" + os.sep + "system" + os.sep + "ini"
    CUSTOM_CONFIG_DIR = os.getcwd() + os.sep + "src" + os.sep + "config" + os.sep + "custom" + os.sep + "ini"

    RESOURCES_CONFIG_DIR = os.getcwd() + os.sep + "src" + os.sep + "config" + os.sep + "system" + os.sep + "resources"
    CUSTOM_RESOURCES_CONFIG_DIR = os.getcwd() + os.sep + "src" + os.sep + "config" + os.sep + "custom" + os.sep + "resources"

    CONFIG_FILE = "config.ini"
    CUSTOM_CONFIG_FILE = "custom_config.ini"

    @staticmethod
    def __loadConfigFile(fname, error_on_not_found=True):
        """
        Load default values from the configuration file.

        @param fname: file name
        @param error_on_not_found: raise error if not found

        @raise ConfigNotFoundError: when file not found and 
                                    error_on_not_found=True (default)

        @return: ConfigParser sections
        """

        cp = ConfigParser()
        if cp.read(fname):
            ConfigManager.__normalalaizeParams(cp._sections)
            ConfigManager.__injectResources(cp._sections)
            return cp._sections
        if error_on_not_found:
            raise ConfigNotFoundError(fname)

    @staticmethod
    def get(key, failobj=None, exclude=None):
        """
        Fetches the value of ConfigManager according to key
        
        @param key: the key of value to fetch
        @param failobj: object to be returned in case of failure
                        (key not in ConfigManager)
        @param exclude: items to exclude
        
        @return: ConfigManager[key] or failobj
        """

        if exclude:
            res = ConfigManager.__getDict().get(key, failobj)
            if isinstance(res, types.DictType):
                DictUtils.exclude(
                          res,
                          exclude
                )
            return res
        return ConfigManager.__getDict().get(key, failobj)

    @staticmethod
    def hasKey(key):
        """
        Checks if given key is exist in the ConfigManager
        
        @param key: key to check
        
        @return: true/false
        """

        return ConfigManager.__getDict().__dict.has_key(key)

    @staticmethod
    def __getDict():
        """
        Combines the dect of configuration from both default
        and custom config files
        
        @return: dict
        """

        config_fname = ConfigManager.CONFIG_DIR + '/' + ConfigManager.CONFIG_FILE
        custom_config_fname = ConfigManager.CUSTOM_CONFIG_DIR + '/' + ConfigManager.CUSTOM_CONFIG_FILE

        if not ConfigManager.__dict:
            with ConfigManager.__lock:
                if not ConfigManager.__dict:
                    config = OrderedDict(
                                         ConfigManager.__loadConfigFile(
                                                        fname=config_fname
                                                        )
                                         )
                    custom_config = OrderedDict(
                                        ConfigManager.__loadConfigFile(
                                                       fname=custom_config_fname,
                                                       error_on_not_found=False
                                                       )
                                    )
                    if config and custom_config:
                        config.update(custom_config)
                    ConfigManager.__dict = config

        return ConfigManager.__dict


    @staticmethod
    def __normalalaizeParams(sections):
        """
        Formats string/NoneType to the python types 
        """

        for section in sections:
            for key in sections[section]:
                if not key.startswith("__"):
                    if sections[section][key] == 'None':
                        sections[section][key] = None
                    elif sections[section][key] in ['true', 'True', 'false', 'False']:
                        sections[section][key] = TypeUtils.str2bool(sections[section][key])

    @staticmethod
    def __injectResources(sections):
        """
        Updates ConfigManager with actual resources
        configuration
        """

        for section in sections:
            if section not in ConfigManager.INTERNAL_SECTIONS:
                resource = ConfigManager.__loadResource(section)
                sections[section]['resource'] = resource

    @staticmethod
    def __loadResource(resource):
        """
        Loads resources configuration from the default
        and custom config files
        
        @param resource: resource to fetch the config for
        
        @return: resources XML representation 
        """

        default_resourece = ConfigManager.RESOURCES_CONFIG_DIR + os.sep + resource + ".xml"
        custom_resourece = ConfigManager.CUSTOM_RESOURCES_CONFIG_DIR + os.sep + resource + ".xml"

        if os.path.exists(default_resourece) and os.path.isfile(default_resourece):
            if os.path.exists(custom_resourece) and os.path.isfile(custom_resourece):
                return XmlUtils.combine([default_resourece, custom_resourece])
            return FileUtils.getContent(default_resourece)
        else:
            raise NotFoundResourceConfigError(resource)
