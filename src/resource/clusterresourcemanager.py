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
        Fetches default Cluster (creates it if not exist)

        @param get_only: do not create on absence
        @param kwargs: keyword args

        @return: Cluster
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
                   .clusters.get(**kwargs)

    # abstract impl
    def list(self, **kwargs):
        """
        Lists all available Clusters according
        to keyword agrs

        @param kwargs: keyword args

        @return: Clusters
        """

        return self.getResourceManager() \
                   .getSdk() \
                   .clusters.list(**kwargs)

    # abstract impl
    @requires.resources([params.DataCenter])
    def add(self, **kwargs):
        """
        Adds default Cluster according to default configuration
        and/or new/overrides defaults according to keyword args  

        @param kwargs: keyword args

        @return: Cluster
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
        """
        Updates default Cluster according to keyword args  

        @param kwargs: keyword args

        @return: Cluster
        """

        cluster = self.get()
        if not cluster:
            self.raiseNotFoundError()
        return cluster.update(**kwargs)

    # abstract impl
    def remove(self, **kwargs):
        """
        Removes default Cluster according to keyword args  

        @param kwargs: keyword args

        @return: Response
        """

        cluster = self.get()
        if not cluster:
            self.raiseNotFoundError()

        # delete
        response = cluster.delete()

        # wait till gone
        StatusUtils.waitRemoved(self.get)

        return response

