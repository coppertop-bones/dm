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

from coppertop.pipe import *
from bones.core.utils import assertRaises
from dm.testing import check, equals
from dm.core.types import txt, num

from coppertop.tests.int_adders import addOne, eachAddOne, eachAddTwo


# test that functions can be patched in a module more than once
@coppertop(module='tests.adders')
def addTwo(x:txt) -> txt:
    return x + 'Three'

with context(halt=True):
    @coppertop(module='tests.adders')
    def addTwo(x:txt) -> txt:
        return x + 'Two'


# test that functions can be redefined in "main"
with context(halt=True):
    @coppertop
    def fred(x):
        pass

with context(halt=True):
    @coppertop
    def fred(x):
        pass




def test_addOneEtc():
    1 >> addOne >> check >> equals >> 2
    [1, 2] >> eachAddOne >> check >> equals >> [2, 3]


def test_updatingAddOne():

    # now we want to use it with strings
    @coppertop
    def addOne(x:txt) -> txt:
        return x + 'One'

    # and floats
    @coppertop
    def addOne(x:num) -> num:
        return x + 1.0

    # check our new implementation
    1 >> addOne >> check >> equals >> 2
    'Two' >> addOne >> check >> equals >> 'TwoOne'
    1.0 >> addOne >> check >> equals >> 2.0

    # but
    with assertRaises(Exception) as ex:
        a = ['Two'] >> eachAddOne >> check >> equals >> ['TwoOne']
    # which is to be expected since the above are local (defined in a function)

    b = ['One'] >> eachAddTwo >> check >> equals >> ['OneTwo']


    # # test that redefining a function in either a different python module or a different bone module without the patch
    # # argument throws an error
    # with assertRaises(CoppertopError) as ex:
    #     from coppertop.tests.int_adders2 import addOne



def main():
    test_addOneEtc()
    test_updatingAddOne()



if __name__ == '__main__':
    main()
    print('pass')

