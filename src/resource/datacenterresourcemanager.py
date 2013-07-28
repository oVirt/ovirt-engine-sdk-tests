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

        return self._doGet(
                       self.getResourceManager().getSdk().datacenters,
                       get_only=get_only,
                       **kwargs
        )

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
                   .datacenters \
                   .list(**kwargs)

    # abstract impl
    def add(self, **kwargs):
        """
        Adds default DataCenter/s according to the default configuration/s
        (default configuration can be overridden with custom config
        via keyword args)  

        @param kwargs: keyword args

        @return: DataCenter
        """

        return self._doAdd(
              self.getResourceManager().getSdk().datacenters,
              **kwargs
        )

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
