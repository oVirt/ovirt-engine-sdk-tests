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


from src.resource.resourcemanager import ResourceManager
from src.errors.resourcemanagernotfounderror import ResourceManagerNotFoundError

class resources(object):
    """
    'requires.resources' annotation, verifies  resource/s existance
    in the system upon method execution

    @param params: list of resources
    """

    def __init__(self, params):
        """
        'requires.resources' annotation, verifies  resource/s existance
        in the system upon method execution

        @param params: list of resources
        """

        self.params = params

    def __call__(self, original_func):
        decorator_self = self
        def wrappee(*args, **kwargs):
            for resource in decorator_self.params:
                rm = (resource.__name__ + 'ResourceManager')
                rm_class = ResourceManager.getResourceManager(rm)
                if rm_class:
                    rm_instance = rm_class()
                    if not rm_instance.getOnly():
                        rm_instance.add(**kwargs)
                        # TODO: use **kwargs for private init
                else:
                    raise ResourceManagerNotFoundError(rm)
            return original_func(*args, **kwargs)
        return wrappee
