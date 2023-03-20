# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2022 David Briant. All rights reserved.
#
# This file is part of coppertop-bones.
#
# coppertop-bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General 
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# coppertop-bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License 
# for more details.
#
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

from bones.lang.tests.test_parse_groups import test_frame
from bones.lang.tests.test_parse_groups import test_load
from bones.lang.tests.test_parse_groups import test_misc
from bones.lang.tests.test_parse_groups import test_tuple_type

from .core import *


def main():
    with context(testcase=Missing):
        test_frame.test()
        test_load.test()
        test_misc.test()
        test_tuple_type.test()


if __name__ == '__main__':
    main()
    print('pass')
