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
from src.infrastructure.annotations import requires, conflicts, invoke, run
from src.infrastructure.test.abstractovirttestssuite import AbstractOvirtTestsSuite
from src.resource.resourcemanagerscontainer import ResourceManagersContainer


class ClusterTestsSuite(AbstractOvirtTestsSuite):

    """
    Cluster TestsSuite
    """

    @run.ifGrateOrEqual(params.Version(major=3, minor=3, build_=0, revision=0))
    @conflicts.resources([params.Host, params.Cluster])
    def testCreate(self):
        """"
        Validates the cluster creation
        """

        # manual cluster create
        new_cluster = ResourceManagersContainer\
                                .getClusterResourceManager()\
                                .add()

        # verify response
        self.assertNotEqual(
                        new_cluster,
                        None,
                        'Cluster create has failed!'
        )

        # fetch newly created cluster
        cluster = ResourceManagersContainer\
                                .getClusterResourceManager()\
                                .getOnly()

        # verify existance
        self.assertNotEqual(
                        cluster,
                        None,
                        'Fetch of cluster post create has failed!'
        )

    def testCreateWithUserConfig(self):
        """"
        Validates the cluster with custom config creation
        """

        # create custom cluster
        new_cluster = ResourceManagersContainer\
                            .getClusterResourceManager()\
                            .add(name="foo")

        # verify response
        self.assertNotEqual(
                        new_cluster,
                        None,
                        'Cluster create has failed!'
        )

        # fetch new cluster
        cluster = ResourceManagersContainer\
                            .getClusterResourceManager()\
                            .getOnly(name="foo")

        # verify existence
        self.assertNotEqual(
                        cluster,
                        None,
                        'Fetch of cluster post create has failed!'
        )

    @requires.resources([params.Cluster])
    def testUpdate(self):
        """"
        Validates the cluster update
        """

        # fetch resource
        cluster = ResourceManagersContainer\
                            .getClusterResourceManager()\
                            .getOnly()

        # update
        cluster.set_description("TEST")
        cluster.update()

        # fetch updated cluster
        updated_cluster = ResourceManagersContainer\
                            .getClusterResourceManager()\
                            .getOnly()

        # verify update
        self.assertEqual(
             updated_cluster.get_description(),
             "TEST",
             "cluster.update() has failed"
         )

    def testDelete(self):
        """"
        Validates the cluster delete
        """

        cluster = ResourceManagersContainer.getClusterResourceManager().get()

        cluster.delete()

        cluster = ResourceManagersContainer.getClusterResourceManager().getOnly()
        self.assertEqual(cluster, None, "cluster.delete() has failed")
