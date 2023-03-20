# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from dm.examples import ex_count_lines_jsp
# from dm.examples import ex_deferred
# from dm.examples import ex_format
from dm.examples import ex_format_calendar
from dm.examples import ex_lazy_vs_eager
# from dm.examples import ex_linalg
from dm.examples import ex_misc
# from dm.examples import ex_raiseLess
from dm.examples import ex_spaceships
from dm.examples import ex_ytm_cov
from dm.examples.cluedo.tests import test_cluedo



def main():
    ex_count_lines_jsp.main()
    # ex_deferred.main()
    # ex_format.main()
    ex_format_calendar.main()
    ex_lazy_vs_eager.main()
    # ex_linalg.main()
    ex_misc.main()
    # ex_raiseLess.main()/
    ex_spaceships.main()
    # ex_ytm_cov.main()
    test_cluedo.main()


if __name__ == '__main__':
    main()
    print('pass')
