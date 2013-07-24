'''
Created on May 1, 2013

@author: mpastern
'''

from ovirtsdk.xml import params
from src.resource.abstractresourcemanager import AbstractResourceManager
from src.resource.resourcefactory import ResourceFactory
from src.infrastructure.annotations import requires
from src.utils.statusutils import StatusUtils

class ClusterResourceManager(AbstractResourceManager):
    '''
    Cluster ResourceManager provides cluster construction,
    location and manipulation services.
    '''

    def __init__(self):
        super(ClusterResourceManager, self).__init__(params.Cluster)

    # abstract impl
    def get(self, get_only=False, **kwargs):
        """
        Fetches given cluster
        
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
                   .clusters.get(**kwargs)

    # abstract impl
    def list(self, **kwargs):
        """
        Lists available clusters
        
        @param kwargs: list args 
        """
        return self.getResourceManager() \
                   .getSdk() \
                   .clusters.list(**kwargs)

    # abstract impl
    @requires.resources([params.DataCenter])
    def add(self, **kwargs):
        """
        Adds new clusters
        
        @param kwargs: list args 
        """

        cluster = self.get(get_only=True)
        if not cluster:
            return self.getResourceManager() \
                       .getSdk() \
                       .clusters.add(
                             ResourceFactory.create(
                                        self.getType(),
                                        **kwargs)
        )
        return cluster

    # abstract impl
    def update(self, **kwargs):
        cluster = self.get()
        if not cluster:
            self.raiseNotFoundError()
        return cluster.update(**kwargs)

    # abstract impl
    def remove(self, **kwargs):
        cluster = self.get()
        if not cluster:
            self.raiseNotFoundError()

        # delete
        response = cluster.delete()

        # wait till gone
        StatusUtils.waitRemoved(self.get)

        return response

