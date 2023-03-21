# **********************************************************************************************************************
# Copyright (c) 2021-2022 David Briant. All rights reserved.
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


# coppertop tests
import coppertop.tests.test_anon_and_partial
import coppertop.tests.test_misc
import coppertop.tests.test_modules
import coppertop.tests.test_pipeable
import coppertop.tests.test_cow_scope
import coppertop.tests.test_styles



def main():
    coppertop.tests.test_anon_and_partial.main()
    coppertop.tests.test_misc.main()
    coppertop.tests.test_modules.main()
    coppertop.tests.test_pipeable.main()
    coppertop.tests.test_cow_scope.main()
    coppertop.tests.test_styles.main()


if __name__ == '__main__':
    main()
    print('pass')

