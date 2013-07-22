#!/usr/bin/python
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
#

from ovirtsdk.utils.ordereddict import OrderedDict
from src.infrastructure.singleton import Singleton
from ConfigParser import ConfigParser
import os
import threading
from src.errors.confignotfounderror import ConfigNotFoundError
from src.utils.typeutils import TypeUtils
from src.utils.dictutils import DictUtils
import types
# from src.infrastructure.singleton import singleton

# @singleton
class ConfigManager(Singleton):

    __dict = None
    __lock = threading.RLock()

    INTERNAL_PROPERIES = ['__name__', 'create_on_demand']
    INTERNAL_SECTIONS = ['sdk', 'tests']

    # FIXME: fetch slash for platform
    CONFIG_DIR = os.getcwd() + "/src/config/ini"
    RESOURCES_CONFIG_DIR = os.getcwd() + "/src/config/resources"
    CONFIG_FILE = "config.ini"

    @staticmethod
    def __loadConfigFile():
            """
            Load default values from a configuration file.
            """

            fname = ConfigManager.CONFIG_DIR + \
                    '/' + \
                    ConfigManager.CONFIG_FILE

            cp = ConfigParser()
            if cp.read(fname):
                ConfigManager.__normalalaizeParams(cp._sections)
                ConfigManager.__injectResources(cp._sections)
                return cp._sections
            raise ConfigNotFoundError(
                          ConfigManager.CONFIG_DIR,
                          ConfigManager.CONFIG_FILE
                  )

    @staticmethod
    def get(key, failobj=None, exclude=None):
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
        return ConfigManager.__getDict().__dict.has_key(key)

    @staticmethod
    def __getDict():
        if not ConfigManager.__dict:
            with ConfigManager.__lock:
                if not ConfigManager.__dict:
                    ConfigManager.__dict = \
                        OrderedDict(ConfigManager.__loadConfigFile())
        return ConfigManager.__dict


    @staticmethod
    def __normalalaizeParams(sections):
        for section in sections:
            for key in sections[section]:
                if not key.startswith("__"):
                    if sections[section][key] == 'None':
                        sections[section][key] = None
                    elif sections[section][key] in ['true', 'True', 'false', 'False']:
                        sections[section][key] = TypeUtils.str2bool(sections[section][key])

    @staticmethod
    def __injectResources(sections):
        for section in sections:
            if section not in ConfigManager.INTERNAL_SECTIONS:
                resource = ConfigManager.__loadResource(section)
                sections[section]['resource'] = resource

    @staticmethod
    def __loadResource(section):
        fo = None
        try:
            # FIXME: fetch slash for platform
            fo = open(
                  ConfigManager.RESOURCES_CONFIG_DIR +
                      "/" + section + ".xml",
                  "r"
            )
            return fo.read()
        finally:
            if fo: fo.close()
