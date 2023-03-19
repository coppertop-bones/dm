# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

from dm.core.misc import sequence
from dm.testing import check, equals


def test_misc():
    sequence(1, 10) >> check >> equals >> [1,2,3,4,5,6,7,8,9,10]


def main():
    test_misc()


if __name__ == '__main__':
    main()
    print('pass')
