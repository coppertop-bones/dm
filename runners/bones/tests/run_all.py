# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
#
# This file is part of coppertop-bones.
#
# coppertop-bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General 
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# coppertop-bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License 
# for more details.
#
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
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


