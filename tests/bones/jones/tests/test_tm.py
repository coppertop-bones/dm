# **********************************************************************************************************************
# Copyright (c) 2023-2025 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

import sys, traceback
from bones import jones
from bones.core.sentinels import Missing
from bones.jones import BTypeError
from bones.lang.type_lang import TypeLangInterpreter
from bones.lang._type_lang.py_type_manager import PyTypeManager
from bones.lang._type_lang.jones_type_manager import JonesTypeManager
from bones.lang.core import TLError, bmtnul, bmtatm, bmtint, bmtuni, bmttup, bmtstr, bmtrec, bmtseq, bmtmap, bmtfnc, bmtsvr


# TODO
#   once all types can be created rework bones.lang.metatypes
#   create the null tuple for functions that take no arguments

# OPEN:
#   - intersections of unions
#   - handle recursion in PP
#   - check every valid arg in constructor can handle recursion (fiddly)
#   - handle tm.minus(t1, tm.intersection(t1, t2)) == tm.intersection(t1, tm.exclusion(t2))? currently consider it
#     hard to reason about so probably not
#   - sizes



def test_atom(TM):
    tli = TypeLangInterpreter(tm := TM())
    t = tm['sally']
    assert t.id == 0
    t = tli.parse('sally: atom')

    assert tm['sally'].id == t.id
    assert tm.bmtid(t) == bmtatm
    assert tm.name(t) == 'sally'

    assert t == tli.parse('sally')
    assert t is tm['sally']

    return "test_atom passed"


def test_intersection(TM):
    tli = TypeLangInterpreter(tm := TM())

    mem = tli.parse('mem: atom')
    ccy = tli.parse('ccy: atom')

    t = tli.parse('ccy & (_GBP: atom)')
    assert t == tm.intersection([tm['_GBP'], ccy])

    i1 = tm.intersection([mem, t])
    i2 = tm.intersection([mem, tm['_GBP'], mem, ccy, t])
    assert i1 == i2

    for t in tm.intersectionTl(i1):
        assert t in [ccy, mem, tm['_GBP']]

    # OPEN: test create recursive intersection

    return "test_intersection passed"


def test_union(TM):
    tli = TypeLangInterpreter(tm := TM())

    tli.parse('u32: err: txt: atom')
    u32, err, txt = tm.get('u32'), tm.get('err'), tm.get('txt')

    assert tli.parse('u32 + err') == tli.parse('err + u32'), f"{tli.parse('u32 + err')} != {tli.parse('err + u32')}"
    assert tli.parse('u32 + err + u32') == tli.parse('err + u32 + err')
    assert tli.parse('(u32 + err) + u32') == tli.parse('err + (err + u32)')

    tl = tm.unionTl(tli.parse('(u32 + err) + u32').types)
    assert tl == (err, u32)       # err is created before u32 above

    # with assertRaises(Exception):
    mut = tm.reserve(space=err)
    mut = tm.union(u32, err, txt, self=mut)

    # fred: tbc
    # fred: f64 + {lhs:fred, rhs:fred}

    return "test_union passed"


def test_tuple(TM):
    tli = TypeLangInterpreter(tm := TM())

    t1 = tm.atom('u32')
    t2 = tm.atom('err')

    assert tm.tuple(t1, t2) == tm.tuple(t1, t2)
    assert tm.tuple(t1, t2) != tm.tuple(t2, t1)

    return "test_tuple passed"


def test_struct(TM):
    tli = TypeLangInterpreter(tm := TM())

    t1 = tm.atom('f64')
    t2 = tm.atom('txt')

    assert tm.struct(('x', 'y'), (t1, t2)) == tm.struct(('x', 'y'), (t1, t2))
    assert tm.struct(('x', 'y'), (t1, t2)) != tm.struct(('y', 'x'), (t1, t2))

    return "test_struct passed"


def test_sequence(TM):
    tli = TypeLangInterpreter(tm := TM())

    t1 = tm.union([tm.atom('u32'), tm.atom('err')])
    assert tm.seq(t1) == tm.seq(t1)
    assert tm.seqT(tm.seq(t1)) == t1

    return "test_sequence passed"


def test_map(TM):
    tli = TypeLangInterpreter(tm := TM())

    t1 = tm.atom('txt')
    t2 = tm.atom('f64')
    assert tm.map(t1, t2) == tm.map(t1, t2)
    assert tm.mapTK(tm.map(t1, t2)) == t1
    assert tm.mapTV(tm.map(t1, t2)) == t2

    return "test_map passed"


def test_function(TM):
    tli = TypeLangInterpreter(tm := TM())

    t1 = tm.atom('u32')
    t2 = tm.union(t1, tm.atom('err'))
    assert tm.fn((t1, t1), t2) == tm.fn((t1, t1), t2)
    assert tm.tupleTl(tm.fnTArgs(tm.fn((t1, t1), t2)))[0] == t1
    assert tm.tupleTl(tm.fnTArgs(tm.fn((t1, t1), t2)))[1] == t1
    assert tm.fnTRet(tm.fn((t1, t1), t2)) == t2

    return "test_function passed"


def test_schemavar(TM):
    tli = TypeLangInterpreter(tm := TM())

    assert tm['T1'].id == 0
    t = tm.schemavar('T1')
    assert tm.get('T1') == t
    assert tm.name(t) == 'T1'

    return "test_schemavar passed"


def test_assign(TM):
    tli = TypeLangInterpreter(tm := TM())

    mem = tm.atom('mem')

    tCcy = tm.atom('f8', self=tm.reserve(space=mem))
    GBP = tm.intersection(tCcy, tm.atom('_GBP'))

    # test nameAs
    assert tm.name(GBP) != 'GBP'
    t = tm.bind('GBP', GBP)
    assert GBP == t
    assert tm.name(GBP) == 'GBP'

    return "test_assign passed"


def test_orthogonal_spaces(TM):
    tli = TypeLangInterpreter(tm := TM())

    ccyfx = tm.atom('ccyfx')

    opts = tm.reserve()
    assert opts is not None

    opts = tm.reserve(space=ccyfx)
    assert tm.space(opts) == ccyfx

    ccy = tm.atom('ccy', self=tm.reserve(space=ccyfx))
    assert ccy == tm.atom('ccy')

    # let's try to reconstruct ccy however if we decide that ccy2 is ccy then we have the throw away opts as they are
    # preallocated
    opts = tm.reserve(space=ccyfx)
    assert opts != ccy
    with assertRaises(BTypeError):
        ccy2 = tm.atom('ccy', self=opts)

    if tm.get('fx').id == 0:
        fx = tm.atom('fx', self=tm.reserve(space=ccyfx))

    assert tm.space(ccy) == ccyfx
    assert tm.rootspace(fx) == ccyfx

    with assertRaises(BTypeError):
        t = tm.intersection(ccy, fx)

    mem = tm.atom('mem')         # mem is a builtin type
    py = tm.atom('py')           # to indicate Python types
    null = tm.atom('null')

    sz = tm.atom('sz')
    m64 = tm.atom('m64', self=tm.reserve(space=sz))

    # C style const
    # mut: tbc
    # const: atom in const implicitly mut
    # mut: mut & const in const
    mut = tm.reserve()
    const = tm.reserve()
    const = tm.atom('const', self=const, space=const, implicitly=mut)
    mut = tm.bind('mut', tm.intersection(const, mut, self=mut, space=const))

    f64 = tm.reserve(name='f64')
    f64 = tm.intersection(f64, m64, self=f64, space=mem)

    GBP = tm.reserve(name='GBP')
    GBP = tm.intersection(GBP, f64, ccy, self=GBP, space=ccy)         # intersection of GBP, f64 and ccy in the ccy space

    USD = tm.reserve(name='USD')
    USD = tm.intersection(USD, f64, ccy, self=USD, space=ccy)

    assert tm.isRecursive(GBP)
    with assertRaises(BTypeError):
        tm.intersection(GBP, USD)


    # recursive types do not need to be named
    f64Tree = tm.reserve()
    tLhs = tm.union(f64Tree, f64, null)
    tRhs = tm.union(f64Tree, f64, null)
    f64Tree = tm.struct(('lhs', 'rhs'), (tLhs, tRhs), self=f64Tree)

    assert tm.isRecursive(f64Tree) and not tm.isRecursive(tLhs) and not tm.isRecursive(tRhs)


    pylist = tm.intersection(tm.reserve(name='pylist'), space=py)
    pytup = tm.intersection(tm.reserve(name='pytup'), space=py)

    # pyToBones[list] = pylist
    # pyToBones[tuple] = pytup

    lit = tm.atom('lit')
    littxt = tm.intersection(tm.reserve(name='littxt'), space=lit)


    return "test_orthogonal passed"


def test_minus(TM):
    tli = TypeLangInterpreter(tm := TM())

    t3 = tm.atom('GBP')     # deliberately in reverse order
    t2 = tm.atom('ccy')
    t1 = tm.atom('f64')
    t4 = tm.atom('u32')

    # intersections
    assert tm.minus(tm.intersection(t1, t2, t3), t2) == tm.intersection(t1, t3)
    assert tm.minus(tm.intersection(t1, t2, t3), tm.intersection(t1, t3)) == t2
    with assertRaises(BTypeError):
        tm.minus(t1, t1)
    with assertRaises(BTypeError):
        tm.minus(t1, t2)
    with assertRaises(BTypeError):
        tm.minus(tm.intersection(t1, t2, t3), t4)
    with assertRaises(BTypeError):
        tm.minus(tm.intersection(t1, t2, t3), tm.intersection(t1, t3, t4))

    # unions
    assert tm.minus(tm.union(t1, t2, t3), t2) == tm.union(t1, t3)
    assert tm.minus(tm.union(t1, t2, t3), tm.union(t1, t3)) == t2
    with assertRaises(BTypeError):
        tm.minus(tm.union(t1, t2, t3), t4)
    with assertRaises(BTypeError):
        tm.minus(tm.union(t1, t2, t3), tm.union(t1, t3, t4))

    return "test_minus passed"


def test_hasT(TM):
    tli = TypeLangInterpreter(tm := TM())

    t1 = tm.atom("u8")
    assert tm.hasT(t1) == False

    T1 = tm.schemavar('T1')
    assert tm.hasT(T1) == True

    assert tm.hasT(tm.intersection(t1, T1)) == True
    assert tm.hasT(tm.union(t1, T1)) == True
    assert tm.hasT(tm.tuple(t1, T1)) == True
    assert tm.hasT(tm.seq(T1)) == True
    assert tm.hasT(tm.map(t1, T1)) == True
    assert tm.hasT(tm.fn((t1, t1), T1)) == True
    assert tm.hasT(tm.struct(("x",), (T1,))) == True

    return "test_hasT passed"


def test_recursion(TM):
    tli = TypeLangInterpreter(tm := TM())

    u8 = tm.atom('u8')
    null = tm.atom('null')
    txt = tm.atom('txt')
    f64 = tm.atom('f64')

    # struct - linked list of u8
    tr1 = tm.reserve()
    tnode1 = tm.struct(('i', 'next'), (u8, tm.union(tr1, null)), self=tr1)
    assert tr1 == tnode1

    # check we can't use tr1 again
    with assertRaises(BTypeError):
        tm.tuple(u8, tm.union(tr1, null), self=tr1)

    # tuple - linked list of u8
    tr2 = tm.reserve()
    tnode2 = tm.tuple(u8, tm.union(tr2, null), self=tr2)
    assert tr2 == tnode2

    # seq - linked list of u8
    tr3 = tm.reserve()
    tnode3 = tm.seq(tm.union(u8, tr3, null), self=tr3)
    assert tr3 == tnode3

    # map - linked list of u8 - txt {"this", "next"} -> u8 + tr4 + null
    tr4 = tm.reserve()
    tnode4 = tm.map(txt, tm.union(u8, tr4, null), self=tr4)
    assert tr4 == tnode4

    # union
    tr5 = tm.reserve()
    tnode5 = tm.union(null, tm.tuple(u8, tr5), self=tr5)
    assert tr5 == tnode5

    # intersection
    tr6 = tm.reserve()
    GBP = tm.intersection(tr6, f64, self=tr6)
    tm.bind('GBP', GBP)

    return "test_recursion passed"


def test_offsets(TM):
    tli = TypeLangInterpreter(tm := TM())

    mem = tm.exclusionCat('mem')
    f64 = tm.exclusiveNominal('f64', mem, 8)
    u32 = tm.exclusiveNominal('f64', mem, 4)

    s1 = tm.struct(('t', 'x', 'y'), (u32, f64, f64))
    assert tm.sz(s1) == 24
    assert tm.align(s1) == 8
    assert tm.offsets(s1) == (0, 8, 16)

    s2 = tm.struct(('x', 'y', 't'), (f64, f64, u32))
    assert tm.sz(s2) == 20
    assert tm.align(s2) == 8
    assert tm.offsets(s2) == (0, 8, 16)

    s3 = tm.struct(('x', 'y', 't'), (u32, u32, u32))
    assert tm.sz(s3) == 12
    assert tm.align(s3) == 4
    assert tm.offsets(s3) == (0, 4, 8)

    return "test_offsets passed"




def main():

    fns = [
        # test_em,                       # not needed for dispatch
        test_atom,
        test_intersection,
        test_union,
        test_tuple,
        test_struct,
        test_sequence,
        test_map,
        test_function,
        test_schemavar,

        test_assign,
        test_orthogonal_spaces,

        test_minus,
        test_hasT,
        test_recursion,
        # test_offsets,            # needed for memory layout but not for dispatch
    ]

    for fn in fns:
        for TM in (PyTypeManager, JonesTypeManager):
            print(fn(TM))



class assertRaises:

    def __init__(self, expectedExceptionType):
        self.expectedExceptionType = expectedExceptionType
        self.exceptionType = None
        self.exceptionValue = None
        self.tb = None

    def __enter__(self):
        return self

    def __exit__(self, exceptionType, exceptionValue, tb):
        self.exceptionType = exceptionType
        self.exceptionValue = exceptionValue
        self.tb = tb
        if exceptionType is None:
            # no exception was raised
            raise AssertionError("No exception raised, %s expected." % self.expectedExceptionType)        # no error was raised
        elif not issubclass(exceptionType, self.expectedExceptionType):
            # the wrong exception was raised
            # print the tb to make it easier to figure why the test is failing
            traceback.print_tb(tb)
            raise AssertionError("%s raised. %s expected." % (exceptionType, self.expectedExceptionType))
        else:
            # the correct error was raised
            return True




if __name__ == '__main__':
    main()
    sys._k = None
    'passed'

