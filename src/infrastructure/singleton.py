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


class Singleton(object):
    """
    Singleton design pattern, extending any class with this one,
    will make sure that no more than single instance of extending
    class will be created.
    """

    _instances = {}

    def __new__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = \
                super(Singleton, self).__new__(self, *args, **kwargs)
        return self._instances[self]
# def singleton(cls):
#     instances = {}
#     def getinstance():
#         if cls not in instances:
#             instances[cls] = cls()
#         return instances[cls]
#     return getinstance
