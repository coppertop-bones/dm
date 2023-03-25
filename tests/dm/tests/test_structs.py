# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

from coppertop.pipe import *
from dm.testing import check, equals
from dm.core.aggman import append, prepend, prependTo, appendTo, join, drop, at, keys, sort
from dm.core.misc import _v, box
from dm.core.conv import to
from dm.pp import PP

from dm.core.types import N, num, index, txt, litint, pydict, pylist, dtup, dstruct, dseq, dmap, dframe
# def to(xs:N**T, t:N**(T)) -> N**(T):



def test_dtup():
    # inferred type one level and 1D only
    # dtup() >> typeOf >> check >> equals >> null

    dtup((1,2,"hello"))

    # with assertRaises(NotYetImplemented):
    #     # inferring type of more than 2d is ambiguous - should a nested list be a subarray or a pylist?
    #     dtup(((1, 2), "hello"))

    fred = dtup(str**(str*index), [[1,2]])


def test_dstruct():
    fred = dstruct(str**(str*index), [[1,2]])
    fred.a = 1
    fred.b = 2
    fred['a'] >> PP
    fred['a'] = 5
    fred._fred = 1
    fred = fred | str**(str*index)
    fred._fred >> PP
    repr(fred) >> PP
    str(fred) >> PP
    for k, v in fred._kvs():
        f'{(k, v)}' >> PP


def test_dseq():
    fred = dseq((N**litint)[dseq], [1, 2])
    fred >> _v >> check >> equals >> [1, 2]
    fred >> check >> typeOf >> (N**litint)[dseq]
    fred = fred >> append >> 3
    fred = 0 >> prependTo >> fred
    fred = fred >> join >> dseq((N**litint)[dseq], [4, 5])
    fred >> _v >> check >> equals >> [0, 1, 2, 3, 4, 5]
    repr(fred) >> PP
    str(fred) >> PP


def test_dmap():
    dmap()
    # we can either specify a bones type or infer types on construction - need to write an inference function and
    # decide on mapping from python types to bones types, e.g. is a pyint a litint or an index, we can stop at pylist
    # etc so we end up with strongly typed outer with dynamic inner. obviously calling from python to bones is always
    # a full selection

    # + t1&err was meant so could pass any error to + e.g. `txt("nan")&err + 1 -> txt&err` so an intersection with
    # a T can't really be statically inferred?'

    # https://discourse.julialang.org/t/union-types-good-or-bad/46255

    # txt&err < T1 & err  => T1 = txt

    dmap((txt**litint)[dmap], a=1, b=2, c=3) >> drop >> ['a', 'b'] >> to >> pydict >> check >> equals >> dict(c=3)
    [dict(a=1)] >> at >> 0 >> at >> "a" >> check >> equals >> 1
    dict(b=1, a=2) >> keys >> to >> pylist >> sort


def test_me():
    rx = "rx"; oe = "oe"
    bf1 = dframe(date=[1, 2, 3, 1, 2, 3], asset=[rx, rx, rx, oe, oe, oe])
    bf2 = dframe(date=[1, 2, 3, 1, 2, 3], asset=[rx, rx, rx, oe, oe, oe])




import numpy as np


class nd_(np.ndarray):
    def __rrshift__(self, arg):  # so doesn't get in the way of arg >> func
        return NotImplemented

    def __rshift__(self, arg):  # so doesn't get in the way of func >> arg
        return NotImplemented

    def __array_finalize__(self, instance):
        # see - https://numpy.org/doc/stable/user/basics.subclassing.html
        if instance is None: return
        #self._t_ = getattr(instance, '_t_', tvarray)

    def __new__(cls, *args, **kwargs):
        instance = np.asarray(args[0], **kwargs).view(cls)
        return instance


@coppertop
def T(A:nd_):
    return A.T

@coppertop
def allTrue(A:nd_):
    return bool(A.all())


def test_nd_():
    assert ((nd_([[1, 2], [3, 4]]) >> T >> T) == (nd_([[1, 3], [2, 4]]) >> T >> T >> T)) >> allTrue




def main():
    test_dtup()
    test_dstruct()
    # test_dseq()
    test_dmap()
    test_me()
    test_nd_()


if __name__ == '__main__':
    main()
    print('pass')




