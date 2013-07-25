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
from src.errors.incorrrecttypeerror import IncorrrectTypeError
import pkg_resources


class VersionUtils(object):
    '''
    Provides params.Version related services
    '''

    @staticmethod
    def equals(first, other):
        """
        Compares two params.Version objects

        @param first: version first to compare
        @param other: version two to compare
        
        @return: 0 if equals
                -1 if first > other
                 1 if first < other
        """

        if VersionUtils.__isVersionObject(first) and \
            VersionUtils.__isVersionObject(other):

            left = pkg_resources.parse_version(
                             VersionUtils.__toString(first)
                 )
            right = pkg_resources.parse_version(
                             VersionUtils.__toString(other)
                 )

            if left == right: return 0
            if left > right: return -1
            return 1

    @staticmethod
    def __isVersionObject(version, raise_error=True):
        """
        Checks if version is instanceof params.Version
        
        @param raise_error: disables raise of IncorrrectTypeError
        
        @raise IncorrrectTypeError: if type(params.Version) != type(version)
        
        @return: true/false
        """
        if not isinstance(version, params.Version):
            if not raise_error: return False
            raise IncorrrectTypeError(
                      type(params.Version).__name__,
                      type(version).__name__
                  )
        return True


    @staticmethod
    def __toString(version):
        """
        Parse params.Version to string representation
        
        @version: version object to parse
        
        @return: string representation of version
        """
        if not isinstance(version, params.Version):
            raise IncorrrectTypeError(
                      type(params.Version).__name__,
                      type(version).__name__
                  )

        return str(version.get_major()) + "." + \
               str(version.get_minor()) + "." + \
               str(version.get_build()) + "." + \
               str(version.get_revision())
