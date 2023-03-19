# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

from coppertop.pipe import *
from groot import to, shape
from bones.core.utils import assertRaises
from dm.core.types import matrix
from dm._core.structs import tvarray
from dm.testing import check, equals
from dm.core.conv import to
from dm.pp import PP


def test():
    A = [[1, 2], [3, 5]] >> to >> (matrix&tvarray)
    b = [1, 2] >> to >> (matrix&tvarray) >> PP
    A @ b >> shape >> check >> equals >> (2,1)
    with assertRaises(Exception) as e:
        b @ A



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')
