# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
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

import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from coppertop.pipe import *
from bones.core.utils import assertRaises
from bones.lang.metatypes import BTAtom, BType, BTSeq, BTMap, BTFn, S, isT
from dm.testing import check, equals
from dm.core.aggman import collect, joinAll, sortUsing
from dm.core.conv import to
from dm.core.misc import box

from dm.core.types import index, count, offset, num, txt, N, null, T, T1, bstruct



tFred = BTAtom.ensure('fred')
tJoe = BTAtom.ensure('joe')
tSally = BTAtom.ensure('sally')



def testNominalAndAtoms():
    assert repr(tFred) == 'fred'
    assert tFred == BType('fred')
    assert tFred is BType('fred')

    x = 'hello' >> box | tFred
    assert isinstance(x, tFred)
    assert x._v == 'hello'

    i1 = 1 | index
    assert i1._t == index
    c1 = 1 | count
    assert c1._t == count
    o1 = 1 | offset
    assert o1._t == offset
    n1 = 1 | num
    assert n1._t == num


def testBTUnion():
    s = tFred+tJoe

    assert (repr(s) == 'fred+joe') or (repr(s) == 'joe+fred')
    assert tFred in s
    assert tSally not in s
    assert tJoe+tFred == s   # summing is commutative

    assert isinstance('hello' >> box | tFred, s)


def testBTTuple():
    p1 = tFred*tJoe
    assert repr(p1) == 'fred*joe'
    assert p1 != tJoe*tFred              # the product is not commutative
    assert p1 == tFred*tJoe


def testBTSeq():
    tArr = N ** (num+null)
    repr(tArr) >> check >> equals >> f'N**{num+null}'
    assert isinstance(tArr, BTSeq)


def testBTMap():
    tMap = index ** (num+null)
    repr(tMap) >> check >> equals >> f'index**({num+null})'
    assert isinstance(tMap, BTMap)


def testBTFn():
    fn = (tSally+null) ^ (tFred*tJoe)
    rep = [tSally, null] \
        >> sortUsing >> (lambda x: x.id) \
        >> collect >> (lambda x: x >> to >> txt) \
        >> joinAll(_, ' + ')
    repr(fn) >> check >> equals >> f'(({rep}) -> (fred * joe))'
    assert isinstance(fn, BTFn)


def testStructCreation():
    label = BTAtom.ensure('label').setConstructor(bstruct)
    title = label(text='My cool Tufte-compliant scatter graph')
    title._keys() == ['text']


def test_hasT():
    assert isT(T)
    assert isT(T1)

    matrix = BTAtom.ensure('matrix2')
    inout = BTAtom.ensure('inout')
    out = BTAtom.ensure('out')
    assert matrix[inout, T1].hasT

    ccy = BType('ccy')
    fx = BType('fx')
    GBP = ccy['GBP']
    USD = ccy['USD']
    assert fx[S(domestic=GBP, foreign=T1)].hasT

    N = BType('N')
    assert (N**T).hasT
    assert ((T*num)^num).hasT
    assert ((num*num)^T).hasT

    assert S(name=T, age=num).hasT
    assert (T**num).hasT
    assert (num**T).hasT
    assert (num**T).hasT

    with assertRaises(TypeError):
        1 | T


def testNaming():
    tUnusualThing = (num+txt).nameAs('tUnusualThing')
    assert BType('tUnusualThing') == tUnusualThing



def main():
    testNominalAndAtoms()
    testBTUnion()
    testBTTuple()
    testBTSeq()
    testBTMap()
    # testBTFn()
    test_hasT()
    testStructCreation()
    testNaming()


if __name__ == '__main__':
    main()
    print('pass')
