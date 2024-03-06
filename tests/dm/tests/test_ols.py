# **********************************************************************************************************************
# Copyright  (c) 2021 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

import numpy as np
from coppertop.pipe import *
from dm.testing import check, equals
from dm.core.structs import tvarray
from dm.core.types import bool, matrix
from dm.ols import ols, tStats


# utility fns
@coppertop(style=binary)
def to(v, t:matrix&tvarray) -> matrix&tvarray:
    return (matrix&tvarray)(t,v)

@coppertop(style=binary)
def equal(a:matrix&tvarray, b:matrix&tvarray) -> bool:
    return bool((a == b).all())


# domain functions
@coppertop
def T(A:matrix&tvarray) -> matrix&tvarray:
    return A.T



def test1():
    A = [[1, 2], [3, 4]] >> to >> matrix[tvarray]
    AT = A >> T
    B = ([[1,3], [2,4]] >> to >> (matrix&tvarray))
    AT >> check >> equals >> B



def testOLS():
    x = (matrix&tvarray)([1, 2.5, 3.5, 4, 5, 7, 8.5]).reshape(7,1)
    Y = (matrix&tvarray)([0.3, 1.1, 1.5, 2.0, 3.2, 6.6, 8.6]).reshape(7,1)
    X = x ** [0, 2]
    lm = ols(Y, X)
    lm >> tStats


def main():
    test1()
    testOLS()



if __name__ == '__main__':
    main()
    print('pass')



