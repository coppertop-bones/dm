# **********************************************************************************************************************
# Copyright (c) 2021-2022 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

import sys, time
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from bones.core.context import context



def main():

    # coppertop tests
    import coppertop.tests.run_all
    coppertop.tests.run_all.main()

    # dm tests
    import dm.tests.run_all
    import dm.examples.run_all
    dm.tests.run_all.main()
    dm.examples.run_all.main()

    # bones tests
    import bones.tests.run_all
    bones.tests.run_all.main()


def addendum():
    # bones tests
    import bones.tests.run_all
    bones.tests.run_all.addendum()


if __name__ == '__main__':
    t1 = time.perf_counter_ns()
    # with context(EE=lambda x: x, PP=lambda x: x):
    # with context(EE=lambda x: x):
    # with context(PP=lambda x: x):
    with context():
        main()
        addendum()
    t2 = time.perf_counter_ns()

    from bones.lang import metatypes
    from dm.core.aggman import count
    from bones.core.sentinels import Missing

    numBTypes = [t for t in metatypes._BTypeById if t is not Missing] >> count
    numCacheQueries = len(metatypes._fitsCache)

    msg = f'\n' \
        f'\npass - {(t2 - t1) / 1000_000:.1f}ms' \
        f', {numBTypes} BTypes, {numCacheQueries} cached fitsWithin queries'

    print(msg)