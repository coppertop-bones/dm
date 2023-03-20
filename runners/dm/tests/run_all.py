# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import dm.tests.test_ols
import dm.tests.test_pmf
import dm.tests.test_linealg
# from dm.core.tests import test_agg
import dm.tests.test_misc
import dm.tests.test_range
import dm.tests.test_std


def main():
    dm.tests.test_ols.main()
    dm.tests.test_pmf.main()
    dm.tests.test_linealg.main()
    # test_agg.main()

    dm.tests.test_misc.main()
    dm.tests.test_range.main()
    dm.tests.test_std.main()


if __name__ == '__main__':
    main()
    print('pass')

