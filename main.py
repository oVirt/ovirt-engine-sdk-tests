#!/usr/bin/python
#
# Copyright (c) 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writingprint '%r executed in %2.2f sec' % (original_func.__name__, te - ts)print '%r executed in %2.2f sec' % (original_func.__name__, te - ts), software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest
from src.test.clustertestssuite import ClusterTestsSuite

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ClusterTestsSuite)
    unittest.TextTestRunner(verbosity=2).run(suite)
