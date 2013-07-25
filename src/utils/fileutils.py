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


class FileUtils(object):
    '''
    Provides file related services
    '''


    @staticmethod
    def getContent(fname, mode='r'):
        """
        Fetches file content
        
        @param file: the file path
        @param mode: file open mode (default 'r')
        
        @return: file content
        """
        fo = None
        try:
            fo = open(fname, mode)
            return fo.read()
        finally:
            if fo: fo.close()
