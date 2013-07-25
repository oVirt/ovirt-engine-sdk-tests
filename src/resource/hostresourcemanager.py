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
        Fetches default Host (creates it if not exist)

        @param get_only: do not create on absence
        @param kwargs: keyword args

        @return: Host
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
        """
        Performs actual get()
        """
        return self.getResourceManager() \
                   .getSdk() \
                   .hosts \
                   .get(**kwargs)

    # abstract impl
    def list(self, **kwargs):
        """
        Lists all available Hosts according
        to keyword agrs

        @param kwargs: keyword args

        @return: Hosts
        """

        return self.getResourceManager() \
                   .getSdk() \
                   .hosts \
                   .list(**kwargs)

    # abstract impl
    @requires.resources([params.Cluster])
    def add(self, **kwargs):
        """
        Adds default Host according to default configuration
        and/or new/overrides defaults according to keyword args  

        @param kwargs: keyword args

        @return: Host
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
        """
        Updates default Host according to keyword args  

        @param kwargs: keyword args

        @return: Host
        """

        host = self.get()
        if not host:
            self.raiseNotFoundError()
        return host.update(**kwargs)

    # abstract impl
    def remove(self, **kwargs):
        """
        Removes default host according to keyword args  

        @param kwargs: keyword args

        @return: Response
        """

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
