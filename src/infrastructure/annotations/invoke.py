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


class postrun(object):
    """
    'invoke.postrun' annotation, invokes specified method after
    the given method was executed

    @param params: list of methods to invoke
    """

    def __init__(self, params):
        """
        'invoke.postrun' annotation, invokes specified method after
        the given method was executed

        @param params: list of methods to invoke
        """

        self.params = params

    def __call__(self, original_func):
        decorator_self = self
        def wrappee(*args, **kwargs):
            return original_func(*args, **kwargs)
            for method in decorator_self.params:
                method()
        return wrappee

class prerun(object):
    """
    'invoke.prerun' annotation, invokes specified method before
    the given method is being executed

    @param params: list of methods to invoke
    """

    def __init__(self, params):
        """
        'invoke.prerun' annotation, invokes specified method before
        the given method is being executed

        @param params: list of methods to invoke
        """

        self.params = params

    def __call__(self, original_func):
        decorator_self = self
        def wrappee(*args, **kwargs):
            for method in decorator_self.params:
                method()
            return original_func(*args, **kwargs)
        return wrappee
