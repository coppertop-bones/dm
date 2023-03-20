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

from .core import *


@coppertop
def getTupleType(x):
    return x.phrases[0][0].tupleType


def test():
    context.testcase = 'null tuple'
    '()' >> group >> check >> getTupleType >> equals >> TUPLE_NULL \
        >> check >> bb >> equals >> '()'
    

    context.testcase = 'tuple or paren'
    '(1 * 2)' >> group >> check >> getTupleType >> equals >> TUPLE_OR_PAREN \
        >> check >> bb >> equals >> '(l o l)'


    context.testcase = '0 emtpy slots'
    '(1 ! 2, 2*3)' >> group >> check >> getTupleType >> equals >> TUPLE_0_EMPTY \
        >> check >> bb >> equals >> '(l o l, l o l)'


    context.testcase = '2D tuple'
    '(1 ! 2; 2*3)' >> group >> check >> getTupleType >> equals >> TUPLE_2D \
        >> check >> bb >> equals >> '(l o l; l o l)'


    context.testcase = '1 empty slot'
    '(1 ! 2,)' >> group >> check >> getTupleType >> equals >> TUPLE_1_EMPTY \
        >> check >> bb >> equals >> '(l o l, )'


    context.testcase = '2 empty slots'
    '(1 ! 2,,)' >> group >> check >> getTupleType >> equals >> TUPLE_2_EMPTY \
        >> check >> bb >> equals >> '(l o l, , )'


    context.testcase = '3 empty slots'
    '(,1 ! 2,,)' >> group >> check >> getTupleType >> equals >> TUPLE_3_EMPTY \
        >> check >> bb >> equals >> '(, l o l, , )'


    context.testcase = '4 plus empty slots'
    '(,,1 ! 2,,)' >> group >> check >> getTupleType >> equals >> TUPLE_4_PLUS_EMPTY \
        >> check >> bb >> equals >> '(, , l o l, , )'


