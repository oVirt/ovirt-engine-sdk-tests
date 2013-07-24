
from ovirtsdk.xml import params
from src.infrastructure.annotations import conflicts
from src.resource.hostresourcemanager import HostResourceManager
from src.test.suites.abstractovirttestssuite import AbstractOvirtTestsSuite


class HostTestsSuite(AbstractOvirtTestsSuite):

    __hostResourceManager = HostResourceManager()

    def getHostResourceManager(self):
        return HostTestsSuite.__hostResourceManager

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


    @conflicts.resources([params.Host])
    def testCreate(self):

        # verify add() response
        new_host = self.getHostResourceManager().add()
        self.assertNotEqual(new_host, None, 'Host create has failed!')

        # verify get of newly created cluster
        host = self.getHostResourceManager().get(get_only=True)
        self.assertNotEqual(host, None, 'Fetch of host post create has failed!')
