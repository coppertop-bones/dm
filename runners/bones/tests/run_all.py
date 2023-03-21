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

from dm.pp import PP

# core tests
import bones.core.tests.test_context
import bones.core.tests.test_utils

# kernel tests
import bones.kernel.tests.test_site
import bones.kernel.tests.test_sym

# lang tests - types and selection
import bones.lang.tests.test_metatypes.test_constructors
import bones.lang.tests.test_metatypes.test_decomposition
import bones.lang.tests.test_metatypes.test_fitsWithin

import bones.lang.tests.test_parse_groups.test_all


def main():
    # core tests
    bones.core.tests.test_context.main()

    # kernel tests
    bones.kernel.tests.test_site.main()
    bones.kernel.tests.test_sym.main()

    # lang tests - types and selection
    bones.lang.tests.test_metatypes.test_constructors.main()
    bones.lang.tests.test_metatypes.test_decomposition.main()
    bones.lang.tests.test_metatypes.test_fitsWithin.main()

    # lang tests - PACE
    bones.lang.tests.test_parse_groups.test_all.main()


def addendum():
    import bones.lang.tests.test_lex.test_canon
    import bones.lang.tests.test_parse_groups.test_canon

    '\nlexing canon' >> PP
    bones.lang.tests.test_lex.test_canon.main()
    '\ngrouping canon' >> PP
    bones.lang.tests.test_parse_groups.test_canon.main()


if __name__ == '__main__':
    main()
    addendum()
    '\npass' >> PP


