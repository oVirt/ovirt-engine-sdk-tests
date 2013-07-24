'''
Created on May 1, 2013

@author: mpastern
'''

from ovirtsdk.xml import params
from src.resource.abstractresourcemanager import AbstractResourceManager
from src.resource.resourcefactory import ResourceFactory
from src.utils.statusutils import StatusUtils

class DataCenterResourceManager(AbstractResourceManager):
    '''
    DataCenter ResourceManager providing resource construction,
    location and manipulation services
    '''

    def __init__(self):
        super(DataCenterResourceManager, self).__init__(params.DataCenter)

    # abstract impl
    def get(self, get_only=False, **kwargs):
        """
        Fetches given resource
        
        @param get_only: do not create on absence
        @param kwargs: list args 
        """
        if not kwargs:
            kwargs = {'name': self.getName()}

        resource = self.__doGet(**kwargs)
        if not resource and not get_only:
            if self.isCreateOnDemand():
                return self.add()
            else:
                self.raiseNotFoundError()
        return resource

    def __doGet(self, **kwargs):
        return self.getResourceManager() \
                   .getSdk() \
                   .datacenters.get(**kwargs)

    # abstract impl
    def list(self, **kwargs):
        """
        Lists available datacenters
        
        @param kwargs: list args 
        """
        return self.getResourceManager() \
                   .getSdk() \
                   .datacenters.list(**kwargs)

    # abstract impl
    def add(self, **kwargs):
        """
        Adds new datacenters
        
        @param kwargs: list args 
        """

        dc = self.get(get_only=True)
        if not dc:
            return self.getResourceManager() \
                       .getSdk() \
                       .datacenters.add(
                              ResourceFactory.create(
                                         self.getType(),
                                         **kwargs)
        )
        return dc

    # abstract impl
    def update(self, **kwargs):
        resource = self.get()
        if not resource:
            self.raiseNotFoundError()
        return resource.update(**kwargs)

    # abstract impl
    def remove(self, **kwargs):
        resource = self.get()
        if not resource:
            self.raiseNotFoundError()

        # delete
        response = resource.delete()

        # wait till gone
        StatusUtils.waitRemoved(self.get)

        return response
