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
from src.resource.storagedomainresourcemanager import StorageDomainResourceManager
from src.test.suites.abstractovirttestssuite import AbstractOvirtTestsSuite


class StorageDomainTestsSuite(AbstractOvirtTestsSuite):

    """
    StorageDomain TestsSuite
    """

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

        """
        Validates the StorageDomain creation
        """

        # verify add() response
        new_storagedomain = self.getStorageDomainResourceManager().add()
        self.assertNotEqual(new_storagedomain, None, 'StorageDomain create has failed!')

        # verify get of newly created cluster
        storagedomain = self.getStorageDomainResourceManager().getOnly()
        self.assertNotEqual(storagedomain, None, 'StorageDomain of host post create has failed!')
