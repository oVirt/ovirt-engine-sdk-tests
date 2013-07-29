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
from src.infrastructure.annotations import conflicts
from src.infrastructure.test.abstractovirttestssuite import AbstractOvirtTestsSuite
from src.resource.resourcemanagerscontainer import ResourceManagersContainer


class HostTestsSuite(AbstractOvirtTestsSuite):

    """
    Host TestsSuite
    """

    @conflicts.resources([params.Host])
    def testCreate(self):
        """
        Validates the host creation
        """

        # verify add() response
        new_host = ResourceManagersContainer.getHostResourceManager().add()
        self.assertNotEqual(new_host, None, 'Host create has failed!')

        # verify get of newly created cluster
        host = ResourceManagersContainer.getHostResourceManager().getOnly()
        self.assertNotEqual(host, None, 'Fetch of host post create has failed!')
