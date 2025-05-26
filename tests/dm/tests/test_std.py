# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

import operator
from coppertop.pipe import *
from dm.core.types import offset, index, N, count, dseq
from dm.core.aggman import inject, collect, drop, at
from dm.testing import check, equals
from dm.wip import eachAsArgs

def test_inject():
    [1,2,3] >> inject(_,0,_) >> (lambda a,b: a + b) >> check >> equals >> 6


def test_stuff():

    @coppertop
    def squareIt(x):
        return x * x

    @coppertop(style=binary)
    def add(x, y):
        return x + y

    [1,2,3] >> collect >> squareIt >> inject(_, 0, _) >> add >> check >> equals >> 14

    [[1,2], [2,3], [3,4]] >> eachAsArgs >> add >> check >> equals >> [3, 5, 7]
    [[1, 2], [2, 3], [3, 4]] >> eachAsArgs >> operator.add >> check >> equals >> [3, 5, 7]

def test_at():
    [1,2,3] >> at >> 0 >> check >> equals >> 1
    [1,2,3] >> at >> (0 | offset) >> check >> equals >> 1
    [1,2,3] >> at >> (1 | index) >> check >> equals >> 1
    dseq((N**index)[dseq], [1 | index, 2 | index, 3 | index]) >> at >> (1 | index) >> check >> typeOf >> index

def test_drop():
    dseq((N**str)[dseq], ['a','b','c']) >> drop >> (2 | count) >> check >> typeOf >> (N**str)[dseq]

def main():
    test_at()
    test_inject()
    test_stuff()
    # test_drop()


if __name__ == '__main__':
    main()
    print('pass')

