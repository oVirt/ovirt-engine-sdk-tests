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


from src.resource.clusterresourcemanager import ClusterResourceManager
from ovirtsdk.xml import params
from src.infrastructure.annotations import requires, conflicts, invoke, run
from src.test.suites.abstractovirttestssuite import AbstractOvirtTestsSuite


class ClusterTestsSuite(AbstractOvirtTestsSuite):

    """
    Cluster TestsSuite
    """

    __clusterResourceManager = ClusterResourceManager()

    def getClusterResourceManager(self):
        return ClusterTestsSuite.__clusterResourceManager

####### pre/post test run #############

    def setUp(self):
        pass

    def tearDown(self):
        pass

######## pre/post class run #############

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

# ############### test/s ###############

    @run.ifGrateOrEqual(params.Version(major=3, minor=4, build_=0, revision=0))
    @conflicts.resources([params.Host, params.Cluster])
    @invoke.prerun([])
    @invoke.postrun([])
    def testCreate(self):
        """"
        Validates the cluster creation
        """
        # verify add() response
        new_cluster = self.getClusterResourceManager().add()
        self.assertNotEqual(new_cluster, None, 'Cluster create has failed!')

        # verify get of newly created cluster
        cluster = ClusterTestsSuite.__clusterResourceManager.get()
        self.assertNotEqual(cluster, None, 'Fetch of cluster post create has failed!')

    def testCreateWithUserConfig(self):
        """"
        Validates the cluster with custom config creation
        """

        # verify add() response
        new_cluster = self.getClusterResourceManager().add(name="foo")
        self.assertNotEqual(new_cluster, None, 'Cluster create has failed!')

        # verify get of newly created cluster
        cluster = self.getClusterResourceManager().get(name="foo")
        self.assertNotEqual(cluster, None, 'Fetch of cluster post create has failed!')

    @requires.resources([params.Cluster])
    def testUpdate(self):
        """"
        Validates the cluster update
        """

        cluster = self.getClusterResourceManager().get(get_only=True)

        cluster.set_description("TEST")
        cluster.update()

        updated_cluster = self.getClusterResourceManager().get()
        self.assertEqual(
             updated_cluster.get_description(),
             "TEST",
             "cluster.update() has failed"
         )

    def testDelete(self):
        """"
        Validates the cluster delete
        """

        cluster = self.getClusterResourceManager().get()

        cluster.delete()

        cluster = self.getClusterResourceManager().get(get_only=True)
        self.assertEqual(cluster, None, "cluster.delete() has failed")
