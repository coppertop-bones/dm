# **********************************************************************************************************************
# Copyright (c) 2021 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import dm.tests.test_structs
import dm.tests.test_ols
import dm.tests.test_pmf
import dm.tests.test_linealg
# from dm.core.tests import test_frame
import dm.tests.test_misc
import dm.tests.test_range
import dm.tests.test_std
import dm.tests.test_testing


def main():
    dm.tests.test_structs.main()
    dm.tests.test_ols.main()
    dm.tests.test_pmf.main()
    dm.tests.test_linealg.main()
    # test_frame.main()

    dm.tests.test_misc.main()
    dm.tests.test_range.main()
    dm.tests.test_std.main()
    dm.tests.test_testing.main()


if __name__ == '__main__':
    main()
    print('pass')

