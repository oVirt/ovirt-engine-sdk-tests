
from ovirtsdk.xml import params
from src.infrastructure.annotations import conflicts
from src.resource.storagedomainresourcemanager import StorageDomainResourceManager
from src.test.suites.abstractovirttestssuite import AbstractOvirtTestsSuite


class StorageDomainTestsSuite(AbstractOvirtTestsSuite):

    __StorageDomainResourceManager = StorageDomainResourceManager()

    def getStorageDomainResourceManager(self):
        return StorageDomainTestsSuite.__StorageDomainResourceManager

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


    @conflicts.resources([params.StorageDomain])
    def testCreate(self):

        # verify add() response
        new_storagedomain = self.getStorageDomainResourceManager().add()
        self.assertNotEqual(new_storagedomain, None, 'StorageDomain create has failed!')

        # verify get of newly created cluster
        storagedomain = self.getStorageDomainResourceManager().get(get_only=True)
        self.assertNotEqual(storagedomain, None, 'StorageDomain of host post create has failed!')
