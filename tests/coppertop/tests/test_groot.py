# **********************************************************************************************************************
# Copyright (c) 2021 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
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

