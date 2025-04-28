# **********************************************************************************************************************
# Copyright (c) 2019-2021 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

from coppertop.pipe import *
from bones.lang.metatypes import BType, BTAtom, S, weaken, cacheAndUpdate, fitsWithin as _fitsWithin
import bones.lang.metatypes
from dm.testing import check, fitsWithin, doesNotFitWithin
from dm.core.types import index, count, num, txt, N,  T, T1, T2, T3, num, pylist, pydict, litdec
from dm.finance.types import ccy


oldWeakenings = bones.lang.metatypes._weakenings

weaken(index, num)

tFred = BTAtom('fred')
tJoe = BTAtom('joe')
tSally = BTAtom('sally')





def testSimple():
    # exact
    num >> check >> fitsWithin >> num
    num+txt >> check >> fitsWithin >> num+txt

    # T
    num >> check >> fitsWithin >> T
    num+txt >> check >> fitsWithin >> T
    num**num >> check >> fitsWithin >> T

    # union
    num >> check >> fitsWithin >> txt+num
    txt+num >> check >> doesNotFitWithin >> num

    # coercion via rules
    index >> check >> fitsWithin >> num
    index >> check >> fitsWithin >> index
    count >> check >> doesNotFitWithin >> index
    num >> check >> doesNotFitWithin >> index
    count >> check >> doesNotFitWithin >> num
    litdec >> check >> fitsWithin >> num
    # float >> check >> fitsWithin >> num


def testNested():
    GBP = ccy['GBP']
    USD = ccy['USD']
    weaken((index, num, index, num), (ccy[T], GBP, USD))

    index >> check >> fitsWithin >> GBP
    GBP >> check >> doesNotFitWithin >> index
    index >> check >> doesNotFitWithin >> ccy
    num >> check >> fitsWithin >> ccy[T]

    num*txt >> check >> fitsWithin >> (num+index)*(txt+GBP)
    S(a=num, b=num) >> check >> fitsWithin >> S(a=num)


def testTemplates():
    fred = BTAtom('fred')
    num*fred >> check >> fitsWithin >> T*fred
    index*fred >> check >> fitsWithin >> T1*T2

    # simple wildcards
    (N ** fred)[pylist] >> check >> fitsWithin >> (N ** T1)[T2]
    (N ** fred)[pylist] >> check >> doesNotFitWithin >> (N ** T)[pydict]
    (txt ** fred)[pylist] >> check >> doesNotFitWithin >> (N ** T1)[pylist]
    (fred ** txt)[pylist] >> check >> fitsWithin >> (T1 ** T2)[pylist]
    (fred ** txt)[pylist] >> check >> fitsWithin >> (T1 ** T2)[T3]
    (fred ** txt)[pylist] >> check >> doesNotFitWithin >> (T1 ** T2)[pydict]
    (fred ** txt)[pylist] >> check >> doesNotFitWithin >> (T1 ** T1)[pylist]


def testTemplates2():

    account = txt['account']
    weaken(txt, account)

    dstruct = txt['tvstruct2']
    pylist = txt['pylist2']
    positions = (num ** account)[dstruct]['positions']

    t1 = positions
    t2 = (N**account)[pylist]
    t3 = index

    tByT = {}
    r1, tByT, distances = cacheAndUpdate(_fitsWithin(t1, (T2**T1)[dstruct][T3]), tByT)
    r2, tByT, distances = cacheAndUpdate(_fitsWithin(t2, (N**T1)[pylist]), tByT)
    r3, tByT, distances = cacheAndUpdate(_fitsWithin(t3, T2), tByT)

    assert r1 and r2 and r3

    # dispatch._fitsCache = {}
    tByT = {}
    r4, tByT, distances = cacheAndUpdate(_fitsWithin(t3, T2), tByT)
    r5, tByT, distances = cacheAndUpdate(_fitsWithin(t2, (N**T1)[pylist]), tByT)
    r6, tByT, distances = cacheAndUpdate(_fitsWithin(t1, (T2**T1)[dstruct][T3]), tByT)

    assert r4 and r5 and r6

    t2 = txt
    t3 = index

    tByT = {}
    r9, tByT, distances = cacheAndUpdate(_fitsWithin(t3, T2, tByT), tByT)
    r8, tByT, distances = cacheAndUpdate(_fitsWithin(t2, T1, tByT), tByT)
    r7, tByT, distances = cacheAndUpdate(_fitsWithin(t1, (T2**T1)[dstruct][T3], tByT), tByT)

    assert r7
    assert r8
    assert r9



def main():
    testSimple()
    testNested()
    testTemplates()
    testTemplates2()


if __name__ == '__main__':
    main()
    print('pass')

bones.lang.metatypes._weakenings = oldWeakenings
