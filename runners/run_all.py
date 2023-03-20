# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

import sys, time
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from bones.core.context import context



def main():
    # groot_test - must be run before other modules load up the groot namespace
    import coppertop.tests.test_groot
    coppertop.tests.test_groot.main()

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