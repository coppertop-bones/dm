# **********************************************************************************************************************
# Copyright (c) 2019-2022 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

from bones.lang.tests.test_parse_groups import test_frame
from bones.lang.tests.test_parse_groups import test_load
from bones.lang.tests.test_parse_groups import test_misc
from bones.lang.tests.test_parse_groups import test_tuple_type

from bones.lang.tests.utils import *


def main():
    with context(testcase=Missing):
        test_frame.test()
        test_load.test()
        test_misc.test()
        test_tuple_type.test()


if __name__ == '__main__':
    main()
    print('pass')
