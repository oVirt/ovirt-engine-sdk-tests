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
from src.resource.abstractresourcemanager import AbstractResourceManager
from src.infrastructure.annotations import requires
from src.resource.datacenterresourcemanager import DataCenterResourceManager
from src.utils.statusutils import StatusUtils
from src.resource.hostresourcemanager import HostResourceManager
import types

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
        Fetches default StorageDomain (creates it if not exist)

        @param get_only: do not create on absence
        @param kwargs: keyword args

        @return: StorageDomain
        """

        return self._doGet(
                       self.getResourceManager().getSdk().storagedomains,
                       get_only=get_only,
                       **kwargs
        )

    # abstract impl
    def list(self, **kwargs):
        """
        Lists all available StorageDomains according
        to keyword agrs

        @param kwargs: keyword args

        @return: StorageDomains
        """

        return self.getResourceManager() \
                   .getSdk() \
                   .storagedomains \
                   .list(**kwargs)

    # abstract impl
    @requires.resources([params.Host])
    def add(self, **kwargs):
        """
        Adds default StorageDomain/s according to the default configuration/s
        (default configuration can be overridden with custom config
        via keyword args)  

        @param kwargs: keyword args

        @return: StorageDomain
        """

        storagedomain = self.get(get_only=True)
        if not storagedomain:
            # wait for host to become ready
            StatusUtils.wait(self.getHost, 'up')

            # create storage domain
            self.injectExpectParam(kwargs)

            created_storagedomains = self._doAdd(
                  self.getResourceManager().getSdk().storagedomains,
                  **kwargs
            )
            if created_storagedomains:
                if isinstance(created_storagedomains, types.ListType):
                    attach_responses = []
                    for item in created_storagedomains:
                        attach_responses.append(self._attach(item))
                    return attach_responses[0]
                else:
                    return self._attach(created_storagedomains)
            else:
                self.raiseNotCreatedError()
        return storagedomain

    def _attach(self, storagedomain):
        """
        Attaches StorageDomain to DC
        
        @param storagedomain: The StorageDomain to attach
        """
        if storagedomain:
            # wait till ready
            StatusUtils.waitBrutal(self.get, 'unattached', name=storagedomain.name)
            # attach storage domain
            datacenter = self.getDataCenter()
            attached_storagedomain = datacenter.storagedomains.add(storagedomain)

            # wait till it got active
            try:
                StatusUtils.wait(
                     self.getAttachedStorageDomain,
                     'active'
                )
            except:
                pass

            # if it's not went up, try activate manually
            if attached_storagedomain.status.state != 'active':
                # activate SD
                attached_storagedomain.activate()
                # wait till ready
                StatusUtils.wait(
                     self.getAttachedStorageDomain,
                     'active'
                )
            return attached_storagedomain

    # abstract impl
    def update(self, **kwargs):
        """
        Updates default StorageDomain according to keyword args  

        @param kwargs: keyword args

        @return: StorageDomain
        """

        storagedomain = self.get()
        if not storagedomain:
            self.raiseNotFoundError()
        return storagedomain.update(**kwargs)

    def getAttachedStorageDomain(self, get_only=True):
        """
        Fetches attached StorageDomain by default DC

        @param get_only: do not create on demand

        @return: StorageDomain
        """

        storagedomain = self.get(get_only=get_only)
        if not storagedomain:
            self.raiseNotFoundError()

        # attach storage domain
        datacenter = self.getDataCenter()
        return  datacenter.storagedomains.get(id=storagedomain.id)

    def getDataCenter(self, get_only=True):
        """
        Fetches default DataCenter

        @param get_only: do not create on demand

        @return: DataCenter
        """

        return self.dataCenterResourceManager.get(get_only=get_only)

    def getHost(self, get_only=True):
        """
        Fetches default Host

        @param get_only: do not create on demand

        @return: Host
        """

        return self.hostResourceManager.get(get_only=get_only)

    # abstract impl
    def remove(self, **kwargs):
        """
        Removes default StorageDomain according to keyword args  

        @param kwargs: keyword args

        @return: Response
        """

        storagedomain = self.get(get_only=True)
        if not storagedomain:
            return

        # get attached storage domain
        attached_storagedomain = self.getAttachedStorageDomain()

        if attached_storagedomain and attached_storagedomain.status and \
           attached_storagedomain.status.state and \
           attached_storagedomain.status.state != 'maintenance':

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
