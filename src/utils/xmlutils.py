'''
Created on Jul 23, 2013

@author: mpastern
'''

from xml.etree import ElementTree as et

class XmlUtils(object):
    '''
    Provides XML related services
    '''

    @staticmethod
    def combine(files):
        """
        Combines XML files
        """
        elements = [et.parse(f).getroot() for f in files]
        if elements and len(elements) >= 2:
            for r in elements[1:]:
                XmlUtils.__combineElement(elements[0], r)
            return et.tostring(elements[0])

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
