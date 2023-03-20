# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

# this file must be run before other modules load up the groot namespace


import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


def main():
    import types
    from coppertop._groot import BModule
    import coppertop.pipe
    import groot

    assert groot
    assert 'PP' not in dir(groot)

    import dm.pp
    assert groot.PP

    import dm.linalg.core
    assert groot.dm.linalg.np.qr

    assert 'PP' not in locals()
    from groot import PP
    assert 'PP' in locals()
    assert PP

    assert type(dm) is types.ModuleType
    from groot import dm
    assert type(dm) is BModule

    assert dm.linalg.np.qr

    from groot.dm.linalg.np import qr


if __name__ == '__main__':
    main()
    print('pass')

