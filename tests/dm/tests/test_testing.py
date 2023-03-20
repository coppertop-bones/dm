# **********************************************************************************************************************
#
#                           Copyright (c) 2017-2022 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************


import dm.core, dm.testing
from groot import check, same, count, raises, pyeval_, equals


def test_testing():
    [1,2,3] >> check >> same >> len >> {'a':1,'b':2,'c':3}
    '1/0' >> pyeval_ >> check >> raises >> ZeroDivisionError
    10 >> check >> equals >> 100 / 10


def main():
    test_testing()


if __name__ == '__main__':
    main()
    print('pass')

