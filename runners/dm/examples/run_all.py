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
