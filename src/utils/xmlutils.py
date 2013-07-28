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


from xml.etree import ElementTree as et
from src.utils.fileutils import FileUtils
from copy import deepcopy

class XmlUtils(object):
    '''
    Provides XML related services
    '''

    @staticmethod
    def combine(files):
        """
        Combines XML files
        
        @param files: list of xml files to combine
        @return: combined XML 
        """

        combined = []

        if files and len(files) >= 2:
            elements = [et.parse(f).getroot() for f in files]
            for r in elements[1:]:
                for child in r._children:
                    root_copy = deepcopy(elements[0])
                    XmlUtils.__combineElement(root_copy, child)
                    xml_str = et.tostring(root_copy, encoding='utf8', method='xml')
                    combined.append(xml_str)
            return combined
        elif len(files) == 1:
            return FileUtils.getContent(files[0])

    @staticmethod
    def __combineElement(one, other):
        """
        Recursively updates either the text or the children
        of an element if another element is found in `one`, or adds it
        from `other` if not found.
        """
        mapping = {el.tag: el for el in one}
        for el in other:
            if len(el) == 0:
                try:
                    mapping[el.tag].text = el.text
                except KeyError:
                    mapping[el.tag] = el
                    one.append(el)
            else:
                try:
                    XmlUtils.__combineElement(mapping[el.tag], el)
                except KeyError:
                    mapping[el.tag] = el
                    one.append(el)
