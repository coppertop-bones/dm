# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

import numpy as np
from coppertop.pipe import *
from dm.testing import check, equals
from dm._core.structs import tvarray
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



