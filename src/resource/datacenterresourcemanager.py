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
        Fetches default DataCenter (creates it if not exist)

        @param get_only: do not create on absence
        @param kwargs: keyword args

        @return: DataCenter
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
                   .datacenters.get(**kwargs)

    # abstract impl
    def list(self, **kwargs):
        """
        Lists all available DataCenters according
        to keyword agrs

        @param kwargs: keyword args

        @return: DataCenters
        """
        return self.getResourceManager() \
                   .getSdk() \
                   .datacenters.list(**kwargs)

    # abstract impl
    def add(self, **kwargs):
        """
        Adds default DataCenter according to default configuration
        and/or new/overrides defaults according to keyword args  

        @param kwargs: keyword args

        @return: DataCenter
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
        """
        Updates default DataCenter according to keyword args  

        @param kwargs: keyword args

        @return: DataCenter
        """

        resource = self.get()
        if not resource:
            self.raiseNotFoundError()
        return resource.update(**kwargs)

    # abstract impl
    def remove(self, **kwargs):
        """
        Removes default DataCenter according to keyword args  

        @param kwargs: keyword args

        @return: Response
        """

        resource = self.get()
        if not resource:
            self.raiseNotFoundError()

        # delete
        response = resource.delete()

        # wait till gone
        StatusUtils.waitRemoved(self.get)

        return response
