'''
Created on May 1, 2013

@author: mpastern
'''

from ovirtsdk.xml import params
from src.resource.abstractresourcemanager import AbstractResourceManager
from src.resource.resourcefactory import ResourceFactory
from src.infrastructure.annotations import requires
from src.resource.datacenterresourcemanager import DataCenterResourceManager
from src.utils.statusutils import StatusUtils
from src.resource.hostresourcemanager import HostResourceManager

class StorageDomainResourceManager(AbstractResourceManager):
    '''
    StorageDomain ResourceManager provides StorageDomain construction,
    location and manipulation services.
    '''

    def __init__(self):
        super(StorageDomainResourceManager, self).__init__(params.StorageDomain)
        self.dataCenterResourceManager = DataCenterResourceManager()
        self.hostResourceManager = HostResourceManager()

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
    @requires.resources([params.Host])
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
                                .storagedomains \
                                .add(ResourceFactory.create(
                                          self.getType(),
                                          **kwargs
                                    )
                            )
            if storagedomain:
                # wait till ready
                StatusUtils.wait(self.get, 'unattached')
                # attach storage domain
                datacenter = self.getDataCenter()
                attached_storagedomain = datacenter.storagedomains.add(storagedomain)
                # wait till it got active
                try:
                    StatusUtils.wait(self.getAttachedStorageDomain, 'active')
                except:
                    pass

                # if it's not went up, try activate manually
                if attached_storagedomain.status.state != 'active':
                    # activate SD
                    attached_storagedomain.activate()
                    # wait till ready
                    StatusUtils.wait(self.getAttachedStorageDomain, 'active')

                return attached_storagedomain
            else:
                self.raiseNotCreatedError()
        return storagedomain

    # abstract impl
    def update(self, **kwargs):
        storagedomain = self.get()
        if not storagedomain:
            self.raiseNotFoundError()
        return storagedomain.update(**kwargs)

    def getAttachedStorageDomain(self, get_only=True):
        storagedomain = self.get(get_only=get_only)
        if not storagedomain:
            self.raiseNotFoundError()

        # attach storage domain
        datacenter = self.getDataCenter()
        return  datacenter.storagedomains.get(id=storagedomain.id)

    def getDataCenter(self, get_only=True):
        return self.dataCenterResourceManager.get(get_only=get_only)

    def getHost(self, get_only=True):
        return self.dataCenterResourceManager.get(get_only=get_only)

    # abstract impl
    def remove(self, **kwargs):
        storagedomain = self.get(get_only=True)
        if not storagedomain:
            return

        # get attached storage domain
        attached_storagedomain = self.getAttachedStorageDomain()

        if attached_storagedomain.status.state != 'maintenance':

            # move to maintenance
            attached_storagedomain.deactivate()

            # wait till ready
            StatusUtils.wait(self.getAttachedStorageDomain, 'maintenance')

        # delete DC
        datacenter = self.getDataCenter()
        datacenter.delete()
        # wait till gone
        StatusUtils.waitRemoved(self.getDataCenter)

        # delete
        response = storagedomain.delete(
                            storagedomain=params.StorageDomain(
                                           host=self.hostResourceManager.get()
                                           )
                            )
        # wait till gone
        StatusUtils.waitRemoved(self.get)


        return response
