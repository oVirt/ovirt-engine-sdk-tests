'''
Created on May 1, 2013

@author: mpastern
'''

from ovirtsdk.xml import params
from src.resource.abstractresourcemanager import AbstractResourceManager
from src.resource.resourcefactory import ResourceFactory
from src.infrastructure.annotations import requires
from src.utils.statusutils import StatusUtils

class HostResourceManager(AbstractResourceManager):
    '''
    Host ResourceManager provides host construction,
    location and manipulation services.
    '''

    def __init__(self):
        super(HostResourceManager, self).__init__(params.Host)

    # abstract impl
    def get(self, get_only=False, **kwargs):
        """
        Fetches given host
        
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
                   .hosts \
                   .get(**kwargs)

    # abstract impl
    def list(self, **kwargs):
        """
        Lists available hosts
        
        @param kwargs: list args 
        """
        return self.getResourceManager() \
                   .getSdk() \
                   .hosts \
                   .list(**kwargs)

    # abstract impl
    @requires.resources([params.Cluster])
    def add(self, **kwargs):
        """
        Adds new host
        
        @param kwargs: keyword args 
        """
        host = self.get(get_only=True)
        if not host:
            self.injectExpectParam(kwargs)
            host = self.getResourceManager() \
                       .getSdk() \
                       .hosts.add(
                             ResourceFactory.create(
                                        self.getType(),
                                        **kwargs)
                      )
            if not host:
                self.raiseNotCreatedError()

            # wait till ready
            StatusUtils.wait(self.get, 'up')

            return host
        return host

    # abstract impl
    def update(self, **kwargs):
        host = self.get()
        if not host:
            self.raiseNotFoundError()
        return host.update(**kwargs)

    # abstract impl
    def remove(self, **kwargs):
        host = self.get()
        if not host:
            self.raiseNotFoundError()

        if host.status.state != 'maintenance':
            host.deactivate()
            StatusUtils.wait(self.get, 'maintenance')

        # delete
        response = host.delete()

        # wait till gone
        StatusUtils.waitRemoved(self.get)

        return response
