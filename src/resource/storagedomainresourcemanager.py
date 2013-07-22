'''
Created on May 1, 2013

@author: mpastern
'''

from ovirtsdk.xml import params
from src.resource.abstractresourcemanager import AbstractResourceManager
from src.resource.resourcefactory import ResourceFactory
from src.infrastructure.annotations import requires
from src.resource.datacenterresourcemanager import DataCenterResourceManager

class StorageDomainResourceManager(AbstractResourceManager):
    '''
    StorageDomain ResourceManager provides StorageDomain construction,
    location and manipulation services.
    '''

    def __init__(self):
        super(StorageDomainResourceManager, self).__init__(params.StorageDomain)
        self.dataCenterResourceManager = DataCenterResourceManager()

    # abstract impl
    def get(self, get_only=False, **kwargs):
        """
        Fetches given StorageDomain
        
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
                   .storagedomains \
                   .get(**kwargs)

    # abstract impl
    def list(self, **kwargs):
        """
        Lists available storagedomains
        
        @param kwargs: list args 
        """
        return self.getResourceManager() \
                   .getSdk() \
                   .storagedomains \
                   .list(**kwargs)

    # abstract impl
    @requires.resources([params.DataCenter, params.Host])
    def add(self, **kwargs):
        """
        Adds new storagedomain
        
        @param kwargs: keyword args 
        """

        storagedomain = self.get(get_only=True)
        if not storagedomain:
            # create storage domain
            self.injectExpectParam(kwargs)
            storagedomain = self.getResourceManager() \
                                .getSdk() \
                                .storagedomains.add(
                                      ResourceFactory.create(
                                                 self.getType(),
                                                 **kwargs)
                                )
            if storagedomain:
                # attach storage domain
                datacenter = self.dataCenterResourceManager.get(storagedomain)
                return datacenter.storagedomains.add(**kwargs)
            else:
                self.raiseNotCreatedError()
        return storagedomain

    # abstract impl
    def update(self, **kwargs):
        storagedomain = self.get()
        if not storagedomain:
            self.raiseNotFoundError()
        return storagedomain.update(**kwargs)

    # abstract impl
    def remove(self, **kwargs):
        storagedomain = self.get()
        if not storagedomain:
            self.raiseNotFoundError()
        return storagedomain.delete()
