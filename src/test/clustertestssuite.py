
from src.test.abstractovirttestssuite import AbstractOvirtTestsSuite
from src.resource.clusterresourcemanager import ClusterResourceManager
from ovirtsdk.xml import params
from src.infrastructure.annotations import requires, conflicts, invoke


class ClusterTestsSuite(AbstractOvirtTestsSuite):

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


    @conflicts.resources([params.Cluster])
    @invoke.prerun([])
    @invoke.postrun([])
    def testCreate(self):

        # verify add() response
        new_cluster = self.getClusterResourceManager().add()
        self.assertNotEqual(new_cluster, None, 'Cluster create has failed!')

        # verify get of newly created cluster
        cluster = ClusterTestsSuite.__clusterResourceManager.get()
        self.assertNotEqual(cluster, None, 'Fetch of cluster post create has failed!')

    def testCreateWithUserConfig(self):

        # verify add() response
        new_cluster = self.getClusterResourceManager().add(name="foo")
        self.assertNotEqual(new_cluster, None, 'Cluster create has failed!')

        # verify get of newly created cluster
        cluster = self.getClusterResourceManager().get(name="foo")
        self.assertNotEqual(cluster, None, 'Fetch of cluster post create has failed!')

    @requires.resources([params.Cluster])
    def testUpdate(self):

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
        cluster = self.getClusterResourceManager().get()

        cluster.delete()

        cluster = self.getClusterResourceManager().get(get_only=True)
        self.assertEqual(cluster, None, "cluster.delete() has failed")
