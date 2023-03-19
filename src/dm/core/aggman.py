# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#    disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#    This product includes software developed by the copyright holders.
#
# 4. Neither the name of the copyright holder nor the names of the  contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# **********************************************************************************************************************

BONES_NS = ''

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


# manipulation of these aggregation classes:
# txt, sym, dtup, dstruct, dseq, dmap, pylist, pydict, pytup, pyset, dframe, nd, (N**num)&tvarray, matrix&tvarray
#
#
# NOTES
# dmap is order preserving (may add a fasthash that isn't)
# decide how to handle lazy / out-of-order aggregates
# do we need merge and underride (only difference is order of keys)



import builtins, numpy as np

from coppertop.pipe import *

from bones.core.errors import NotYetImplemented, ProgrammerError
from bones.lang.metatypes import hasT, cacheAndUpdate, fitsWithin
from bones.lang.structs import tv
from bones.core.sentinels import Void

from dm.core.types import pylist, pydict, pytuple, pydict_keys, pydict_items, pydict_values, pyfunc, pyset, T, \
    T1, T2, T3, T4, T5, T6, txt, t, index, offset, N, dstruct, dtup, dseq, void, dmap, dframe, matrix, num, py
from dm._core.structs import tvarray

dict_keys = type({}.keys())
dict_values = type({}.values())

def _fitsWithin(a, b):
    doesFit, ignore, ignore = cacheAndUpdate(fitsWithin(a, b), {})
    return doesFit


array_ = (N**num) & tvarray
matrix_ = matrix & tvarray


# **********************************************************************************************************************
# append
# **********************************************************************************************************************

@coppertop(style=binary)
def append(l:pylist, element) -> pylist:
    l = list(l)
    l.append(element)
    return l

@coppertop(style=binary)
def append(l:dseq&(N**T1), element:T1) -> dseq&(N**T1):
    l = dseq(l)
    l.append(element)
    return l


# **********************************************************************************************************************
# appendTo
# **********************************************************************************************************************

@coppertop(style=binary)
def appendTo(element, l:pylist) -> pylist:
    l = list(l)
    l.insert(0, element)
    return l

@coppertop(style=binary)
def appendTo(element, l:dseq&(N**T1)) -> dseq&(N**T1):
    l = dseq(l)
    l.insert(0, element)
    return l


# **********************************************************************************************************************
# at - if the selector is N** then this means a depth access - use atAll for breadth
# **********************************************************************************************************************

# @coppertop(style=binary)
# def at(xs, selector):
#     return xs[selector]

@coppertop(style=binary)
def at(xs:dseq+pylist+pytuple, o:offset) -> py:
    return xs[o]

@coppertop(style=binary)
def at(xs:dseq+pylist+pytuple, i:index):
    return xs[i - 1]

@coppertop(style=binary)
def at(s:dstruct+pydict+dmap, k:txt):
    return s[k]

@coppertop(style=binary)
def at(s:py, k:txt):
    return s[k]

@coppertop(style=binary)
def at(s:dstruct+pydict+dmap, ks:pylist):
    for k in ks:
        s = s[k]
    return s

@coppertop(style=binary)
def at(xs:pylist+pytuple, os:pylist):
    print('A WARNING')
    answer = []
    for o in os:
        answer.append(xs[o])
    return answer

@coppertop(style=binary)
def at(xs:pylist, s1:offset, s2: offset):
    return xs[s1:s2]

@coppertop(style=binary)
def at(a:dframe, f:txt) -> (N**T)&tvarray:
    return a[f]

@coppertop(style=binary)
def at(a:(N**T1)[dframe], f:txt) -> (N**N**T2)[tvarray]:
    # T2 is a column in  the struct T1
    return a[f]

@coppertop(style=binary)
def at(a:dframe, o:offset) -> dstruct:
    items = [(f, a[f][o]) for f in a._keys()]
    return dstruct(items)

@coppertop(style=binary)
def at(a:dframe, i:index) -> dstruct:
    items = [(f, a[f][i-1]) for f in a._keys()]
    return dstruct(items)

@coppertop(style=binary)
def at(a:(N**T)[dframe], o:offset):  # -> T:
    # answers a struct if o is an offset or an array if o is a name
    raise NotYetImplemented('(a, o) -> T')

@coppertop(style=binary)
def at(a:dframe, os:pylist+pytuple) -> dframe:
    items = [(f, a[f][os]) for f in a._keys()]
    return dstruct(items)

@coppertop(style=binary)
def at(xs:(N**T)&tvarray, o:t.offset) -> T:
    return xs[o]

@coppertop(style=binary)
def at(xs:(N**T)&tvarray, i:t.index) -> T:
    return xs[i-1]

@coppertop(style=binary)
def at(xs:(N**T)&tvarray, os:pylist) -> (N**T)&tvarray:
    return xs[os]


# **********************************************************************************************************************
# atAll - breadth access
# **********************************************************************************************************************

@coppertop(style=binary)
def atAll(xs:pydict, os:pylist+pytuple):
    answer = []
    for o in os:
        answer.append(xs[o])
    return answer


# **********************************************************************************************************************
# atAll - breadth access
# **********************************************************************************************************************

@coppertop(style=ternary)
def atAllPut(xs:pydict, ks:pylist+pytuple, vs:pylist+pytuple) -> pydict:
    raise NotYetImplemented()


# **********************************************************************************************************************
# atCol
# A atCol 1
# **********************************************************************************************************************

@coppertop(style=binary)
def atCol(a: matrix & tvarray, o:offset) -> matrix & tvarray:
    return a[:, [o]]

@coppertop(style=binary)
def atCol(a: matrix & tvarray, i:index) -> matrix & tvarray:
    return a[:, [i - 1]]


# **********************************************************************************************************************
# atColPut
# A atColPut 1 (1,2,3)
# **********************************************************************************************************************

@coppertop(style=ternary)
def atColPut(m, i, v):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atIfNone
# map at: `fred ifNone: missing
# **********************************************************************************************************************

@coppertop(style=ternary)
def atIfNone(m, k, default):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atIfNonePut
# map at: `fred ifNonePut: default
# **********************************************************************************************************************

@coppertop(style=ternary)
def atIfNonePut(m, k, default):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atPut
# **********************************************************************************************************************

@coppertop(style=ternary)
def atPut(s:dstruct, name:txt, value) -> dstruct:
    s = dstruct(s)
    s[name] = value
    return s

@coppertop(style=ternary)
def atPut(m:(T2**T1)[dstruct][T3], ks:(N**T1)[pylist], v:T2) -> (T2**T1)[dstruct][T3]:
    for k in ks._v:
        m[k] = v
    return m

@coppertop(style=ternary)
def atPut(a:dframe, o:offset, row:dstruct) -> dframe:
    raise NotYetImplemented()

@coppertop(style=ternary)
def atPut(a:dframe, f:txt, col:(N**T1)[tvarray]) -> dframe:
    a[f] = col
    return a

@coppertop(style=ternary)
def atPut(m:pydict, k:T1, v:T2) -> pydict:
    m = dict(m)
    m[k] = v
    return m

@coppertop(style=ternary)
def atPut(m:dmap, k, v) -> dmap:
    raise NotYetImplemented()
    m[k] = v
    return m

@coppertop(style=ternary)
def atPut(xs:pylist, iOrIs, yOrYs) -> pylist:
    # immutable??
    # xs = list(xs)
    if isinstance(iOrIs, (list, tuple)):
        for fromI, toI in enumerate(iOrIs):
            xs[toI] = yOrYs[fromI]
    else:
        xs[iOrIs] = yOrYs
    return xs


# **********************************************************************************************************************
# atRemain
# **********************************************************************************************************************

@coppertop(style=binary)
def atRemain(m, o:offset):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atRow
# **********************************************************************************************************************

@coppertop(style=binary)
def atRow(m, o:offset):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atRowPut
# **********************************************************************************************************************

@coppertop(style=ternary)
def atRowPut(m, o:offset, row):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atSlice
# (1,2,3)(0:1) == (1)   // in bones:
# (`a,`b,`c) 1 == `a    // in bones
# so we don't want to reuse at
# **********************************************************************************************************************

@coppertop(style=binary)
def atSlice(m, s):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atSlicePut
# **********************************************************************************************************************

@coppertop(style=binary)
def atSlicePut(m, s, y):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atSlices
# **********************************************************************************************************************

@coppertop(style=binary)
def atSlices(m, ss):
    raise NotYetImplemented()


# **********************************************************************************************************************
# atSlicesPut
# **********************************************************************************************************************

@coppertop(style=binary)
def atSlicesPut(m, ss, y):
    raise NotYetImplemented()


# **********************************************************************************************************************
# both
# **********************************************************************************************************************

@coppertop(style=ternary)
def both(a:pylist+pydict_items, f:pyfunc, b:pylist+pydict_items) -> pylist:
    return [f(x, y) for (x, y) in builtins.zip(a, b)]

@coppertop(style=ternary)
def both(a:pydict, f:pyfunc, b:pydict) -> pylist:
    answer = []
    for (ak, av), (bk, bv) in zip((a.items(), b.items())):
        answer.append(f(ak, av, bk, bv))
    return answer

@coppertop(style=ternary)
def both(a:(T1 ** T2)[dstruct], fn, b:(T1 ** T2)[dstruct]) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:dstruct, fn, b:dstruct) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:(T1 ** T2)[dstruct][T3], fn, b:(T1 ** T2)[dstruct][T3]) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:dstruct[T], fn, b:dstruct[T]) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:(T1 ** T2)[dstruct][T3], fn:pyfunc, b:(T4 ** T5)[dstruct][T6]) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a: matrix&tvarray, f, b:matrix&tvarray) -> matrix&tvarray:
    with np.nditer([a, b, None]) as it:
        for x, y, z in it:
            z[...] = f(x,y)
        return it.operands[2].view(matrix&tvarray)


# **********************************************************************************************************************
# centerCols
# **********************************************************************************************************************

@coppertop
def centerCols(panel:matrix&tvarray) -> matrix&tvarray:
    return panel - np.mean(panel, 0).reshape((1, panel.shape[1]))


# **********************************************************************************************************************
# collect
# **********************************************************************************************************************

@coppertop(style=binary)
def collect(xs, f) -> pylist:
    return [f(x) for x in xs]

@coppertop(style=binary)
def collect(xs:pylist+pydict_keys+pydict_values+pytuple, f) -> pylist:
    return [f(x) for x in xs]

@coppertop(style=binary)
def collect(xs:pyset, f) -> pyset:
    return set([f(x) for x in xs])

@coppertop(style=binary)
def collect(a:dmap, fn2) -> dmap:
    answer = dmap()
    for f, v in a._kvs():
        answer[f] = fn2(f, v)
    return answer

@coppertop(style=binary)
def collect(a:dframe, fn1):
    inputsAndOutput = [x for x in a._values()] + [None]
    with np.nditer(inputsAndOutput) as it:
        for vars in it:
            vars[-1][...] = fn1(*vars[:-1])
        return it.operands[len(inputsAndOutput) - 1].view(dtup)

@coppertop(style=binary)
def collect(xs: pydict_items, f) -> pylist:
    return [f(k, v) for k, v in xs]

def _collectHelper(xs:(N**T1)[dseq], f:T1^T2, tByT) -> dict:
    t1 = tByT[T1]
    fn, tByT_f, hasValue = f.d.selectFn((t1,))
    t2 = fn.tRet
    if hasT(t2):
        raise NotYetImplemented()
    answer = dict(tByT)
    answer[T2] = t2
    return answer

@coppertop(style=binary, typeHelper=_collectHelper)
def collect(xs:(N**T1)[dseq], f:T1^T2, tByT) -> (N**T2)[dseq]:
    return dseq((N**tByT[T2])[dseq], [f(x) for x in xs])

@coppertop(style=binary, typeHelper=_collectHelper)
def collect(xs:(N**T1)[dseq, T3], f:T1^T2, tByT) -> (N**T2)[dseq, T3]:
    fxs = [f(x) for x in xs]
    return dseq((N**tByT[T2])[dseq, tByT[T3]], fxs)


# **********************************************************************************************************************
# collectV
# **********************************************************************************************************************

@coppertop(style=binary)
def collectV(a:dmap, fn1) -> pylist:
    answer = list()
    for v in a._values():
        answer.append(fn1(v))
    return answer


# **********************************************************************************************************************
# count
# **********************************************************************************************************************

@coppertop
def count(x:dstruct) -> t.count:
    return len(x._keys())

@coppertop
def count(x) -> t.count:
    return len(x)

@coppertop
def count(x:txt+pylist+pytuple+pyset+pydict_keys+pydict_values) -> t.count:
    return len(x)

@coppertop
def count(m:matrix&tvarray) -> t.count:
    nr, nc = m.shape
    return nr

@coppertop
def count(a:array_) -> t.count:
    assert a.ndim == 1
    return a.shape[0] | t.count


# **********************************************************************************************************************
# countIf
# **********************************************************************************************************************

@coppertop(style=binary)
def countIf(xs:pylist+pytuple+pyset+pydict_keys+pydict_values, fn:pyfunc) -> t.count:
    c = 0
    for x in xs:
        c += fn(x)
    return c | t.count


# **********************************************************************************************************************
# diff
# **********************************************************************************************************************

@coppertop
def diff(a:array_):
    assert a.ndim == 1
    return np.diff(a)


# **********************************************************************************************************************
# diffCols
# **********************************************************************************************************************

@coppertop
def diffCols(p:matrix):
    return np.diff(p,axis=1)


# **********************************************************************************************************************
# diffRows
# **********************************************************************************************************************

@coppertop
def diffRows(p:matrix):
    return np.diff(p,axis=0)


# **********************************************************************************************************************
# distinct
# **********************************************************************************************************************

@coppertop
def distinct(x:pylist) -> pyset:
    return set(x)


# **********************************************************************************************************************
# do
# **********************************************************************************************************************

@coppertop(style=binary)
def do(xs:pylist+pydict_keys+pydict_values+pytuple, f) -> void:
    [f(x) for x in xs]
    return Void


# **********************************************************************************************************************
# drop - drops elements from a N**T2 or a T1**T2
#        three cases of overload 1) drop count, 2) drop N/T1 or Ns/T1s 3) drop T2 or T2s
#        this becomes ambiguous when T1 == T2 and in python we have to peek into the args :(, in bones we don't :)
#        we could distinguish by having dropV as a companion - something to think about
# **********************************************************************************************************************

@coppertop(style=binary)
def drop(xs:(N**T)[pylist], ks:(N**T)[pylist]) -> (N**T)[pylist]:
    raise ProgrammerError("Don't need to box pylist now we have dseq")
    # answer = []
    # for x in xs._v:
    #     if x not in ks._v:
    #         answer.append(x)
    # return tv(xs._t, answer)

@coppertop(style=binary)
def drop(xs:pylist+pydict_keys, ks:pylist) -> pylist:
    answer = []
    if isinstance(ks[0], (builtins.str, txt)):
        for x in xs:
            if x not in ks:
                answer.append(x)
    elif isinstance(ks[0], int):
        for o, e in enumerate(xs):
            if o not in ks:
                answer.append(e)
    else:
        raise NotYetImplemented()
    return answer

@coppertop(style=binary)
def drop(xs:pylist+pydict_keys+pydict_values, e) -> pylist:    #(N**T1, T1)-> N**T1
    answer = []
    for x in xs:
        if x != e:
            answer.append(x)
    return answer

@coppertop(style=binary)
def drop(xs:pylist, n:t.count) -> pylist:    #(N**T(im), count)-> N**T(im)
    if n > 0:
        return xs[n:]
    else:
        raise NotYetImplemented('drop(xs:txt, n:count) -> txt')

@coppertop(style=binary)
def drop(xs:pytuple, n:t.count) -> pytuple:    #(N**T(im), count)-> N**T(im)
    if n > 0:
        return xs[n:]
    else:
        raise NotYetImplemented('drop(xs:txt, n:count) -> txt')

@coppertop(style=binary)
def drop(xs:pydict_keys+pydict_values, n:t.count) -> pylist:    #(N**T(im), count)-> N**T(im)
    if n > 0:
        return list(xs)[n:]
    else:
        raise NotYetImplemented('drop(xs:txt, n:count) -> txt')

@coppertop(style=binary)
def drop(xs:txt, n:t.count) -> txt:     #(N**T(txt), count)-> N**T(txt)
    if n > 0:
        return xs[n:]
    else:
        raise NotYetImplemented('drop(xs:txt, n:count) -> txt')

@coppertop(style=binary)
def drop(xs:pylist, ss:pytuple) -> pylist:
    s1, s2 = ss
    if s1 is Ellipsis:
        if s2 is Ellipsis:
            return []
        else:
            return xs[s2:]
    else:
        if s2 is Ellipsis:
            return xs[:s1]
        else:
            raise NotYetImplemented()

@coppertop(style=binary)
def drop(d:pydict, ks: pylist) -> pydict:
    return {k:d[k] for k in d.keys() if k not in ks}

@coppertop(style=binary)
def drop(d:pydict, k:txt) -> pydict:
    return {k2:d[k2] for k2 in d.keys() if k2 != k}

@coppertop(style=binary)
def drop(s:dmap, keys:pylist) -> dmap:
    # keys may be a list[str] or list[int]
    answer = dmap(s)
    if not keys: return answer
    if type(keys[0]) is builtins.str:
        for k in keys:
            del answer[k]
    elif type(keys[0]) is int:
        raise NotImplementedError()
    else:
        raise TypeError(f'Unhandled type list[{str(type(keys[0]))}]')
    return answer

@coppertop(style=binary)
def drop(s:dmap, name:txt) -> dmap:
    answer = dmap(s)
    del answer[name]
    return answer

@coppertop(style=binary)
def drop(s:dstruct, name:txt) -> dstruct:
    answer = dstruct(s)
    del answer[name]
    return answer

@coppertop(style=binary)
def drop(f:dframe, k:txt) -> dframe:
    return dframe({k_:f[k_] for k_ in f >> keys >> drop >> k})

@coppertop(style=binary)
def drop(f:dframe, n:t.count) -> dframe:
    if n >= 0:
        return dframe({k:f[k][n:] for k in f._keys()})
    else:
        firstCol = None
        for firstCol in f._values():
            break
        s1 = firstCol.shape[0] - n
        return dframe({k:f[k][s1:] for k in f._keys()})

@coppertop(style=binary)
def drop(f:dframe, isOrKs:pylist) -> dframe:
    if not isOrKs:
        return f
    elif isinstance(isOrKs[0], str):
        # sequence( of strings
        ks = [k for k in f._keys() if k not in isOrKs]
        return dframe({k:f[k] for k in ks})
    elif isinstance(isOrKs[0], int):
        raise NotYetImplemented()
    else:
        raise TypeError()

@coppertop(style=binary)
def drop(f:dframe, ss:pytuple) -> dframe:
    raise NotYetImplemented()

@coppertop(style=binary)
def drop(xs:(N**T1)&tvarray, c:t.count) -> (N**T1)&tvarray:
    return xs[c:]


# **********************************************************************************************************************
# dropCol
# A dropCol 1
# **********************************************************************************************************************

@coppertop(style=binary)
def dropCol(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# dropColRemain
# A dropColRemain 1
# **********************************************************************************************************************

@coppertop(style=binary)
def dropColRemain(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# dropCols
# **********************************************************************************************************************

@coppertop(style=binary)
def dropCols(m:matrix&tvarray, n:t.count):
    return m[:,n:]


# **********************************************************************************************************************
# dropRow
# A dropRow 1
# **********************************************************************************************************************

@coppertop(style=binary)
def dropRow(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# dropRemain
# A dropRemain 1
# **********************************************************************************************************************

@coppertop(style=binary)
def dropRemain(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# dropRowRemain
# A dropRowRemain 1
# **********************************************************************************************************************

@coppertop(style=binary)
def dropRowRemain(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# dropRows
# **********************************************************************************************************************

@coppertop(style=binary)
def dropRows(m:matrix&tvarray, n:t.count):
    if n >= 0:
        return m[n:,:]
    else:
        raise NotYetImplemented()


# **********************************************************************************************************************
# eachCol_
# TODO use sequence instead
# **********************************************************************************************************************

@coppertop
def eachCol_(m: matrix & tvarray) -> pylist:
    answer = []
    nr, nc = m.shape
    for i in range(nc):
        answer.append(m[:,[i]])
    return answer


# **********************************************************************************************************************
# eachRow_
# TODO use sequence instead
# **********************************************************************************************************************

@coppertop
def eachRow_(m: matrix & tvarray) -> pylist:
    answer = []
    nr, nc = m.shape
    for i in range(nc):
        answer.append(m[[i],:])
    return answer


# **********************************************************************************************************************
# first
# **********************************************************************************************************************

@coppertop
def first(a:array_) -> num:
    return float(a[0])

@coppertop
def first(a:dframe) -> dframe:
    # answers first row
    raise NotYetImplemented()

@coppertop
def first(x:pylist+pytuple):
    return x[0]

@coppertop
def first(xs:pydict_values+pydict_keys):
    # https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
    for x in xs:
        return x

@coppertop
def first(f:dframe) -> dframe:
    return dframe({k:f[k][[0]] for k in f._keys()})


# **********************************************************************************************************************
# firstLast
# **********************************************************************************************************************

@coppertop
def firstLast(a:dframe) -> dframe:
    # answers first row
    raise NotYetImplemented()

@coppertop
def firstLast(x:pylist+pytuple) -> pytuple:
    return x[0], x[-1]

@coppertop
def firstLast(x:(N**T)&tvarray) -> (N**T)&tvarray:
    return x[[0,-1]]


# **********************************************************************************************************************
# hjoin
# A hjoin B
# **********************************************************************************************************************

@coppertop(style=binary)
def hjoin(a:tvarray&matrix, b:tvarray&matrix) -> tvarray&matrix:
    aShape = a.shape; bShape = b.shape
    if aShape[0] != bShape[0]: raise ValueError('A and B are different heights!')
    return (tvarray&matrix)(np.append(a, b, axis=1))


# **********************************************************************************************************************
# hjoinAll
# A hjoinAll
# **********************************************************************************************************************

@coppertop
def hjoinAll(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# icollect
# **********************************************************************************************************************

@coppertop(style=binary)
def icollect(xs:pylist, f2) -> pylist:
    return [f2(i, x) for (i, x) in enumerate(xs)]


# **********************************************************************************************************************
# indexOf
# **********************************************************************************************************************

@coppertop
def indexOf(xs, x):
    raise NotYetImplemented()


# **********************************************************************************************************************
# indexesOf
# **********************************************************************************************************************

@coppertop
def indexesOf(xs, x):
    answer = []
    for i, e in enumerate(xs):
        if x == e:
            answer.append(i)
    return answer


# **********************************************************************************************************************
# inject
# **********************************************************************************************************************

@coppertop(style=binary)
def inject(xs:pylist, seed, f2):
    prior = seed
    for x in xs:
        prior = f2(prior, x)
    return prior

@coppertop(style=binary)
def inject(s:dmap, seed, f3):
    prior = seed
    for f, v in s._kvs():
        prior = f3(prior, f, v)
    return prior


# **********************************************************************************************************************
# interleave
# **********************************************************************************************************************

@coppertop(style=binary)
def interleave(xs:pylist+pytuple, b) -> pylist:
    answer = xs[0]
    for x in xs[1:]:
        answer = answer >> join >> b >> join >> x
    return answer

@coppertop(style=binary)
def interleave(a:(N**T1)[dseq], b: T1) -> (N**T1)[dseq]:
    raise NotYetImplemented()

@coppertop(style=binary)
def interleave(a:(N**T1)[dseq], b: (N**T1)[dseq]) -> (N**T1)[dseq]:
    raise NotYetImplemented()

@coppertop(style=binary)
def interleave(xs:N**txt, sep:txt) -> txt:
    # ['hello', 'world'] >> joinAll(_,' ')
    return sep.join(xs)

@coppertop(style=binary)
def interleave(xs:pylist+pytuple, sep:txt) -> txt:
    return sep.join(xs)


# **********************************************************************************************************************
# intersects
# **********************************************************************************************************************

@coppertop(style=binary)
def intersects(a, b):
    if not isinstance(a, (list, tuple, set, dict_keys, dict_values)):
        if not isinstance(b, (list, tuple, set, dict_keys, dict_values)):
            return a == b
        else:
            return a in b
    else:
        if not isinstance(b, (list, tuple, set, dict_keys, dict_values)):
            return b in a
        else:
            for e in a:
                if e in b:
                    return True
            return False


# **********************************************************************************************************************
# join
# **********************************************************************************************************************

@coppertop(style=binary)
def join(xs:pylist, ys:pylist) -> pylist:
    return xs + ys

@coppertop(style=binary)
def join(s1:txt, s2:txt) -> txt:
    return s1 + s2

@coppertop(style=binary)
def join(d1:pydict, d2:pydict) -> pydict:
    answer = dict(d1)
    for k, v in d2.items():
        if k in answer:
            raise KeyError(f'{k} already exists in d1 - use underride or override to merge (rather than join) two pydicts')
        answer[k] = v
    return answer

@coppertop(style=binary)
def join(xs:pylist, ys:pydict_keys) -> pylist:
    return xs + list(ys)

@coppertop(style=binary)
def join(xs:(N**T1)[dseq], ys:(N**T1)[dseq], tByT) -> (N**T1)[dseq]:
    return dseq((N**(tByT[T1]))[dseq], xs.data + ys.data)


# **********************************************************************************************************************
# joinAll
# **********************************************************************************************************************

@coppertop
def joinAll(xs:N**txt) -> txt:
    return ''.join(xs)

@coppertop
def joinAll(xs:pylist+pytuple) -> txt + ((N**T1)[dseq]) + pylist + pytuple:
    # could be a list of strings or a list of (N**T1) & dseq
    # answer a string if no elements
    if not xs:
        return ''
    typeOfFirst = typeOf(xs[0])
    if _fitsWithin(typeOfFirst, txt):
        return ''.join(xs)
    elif _fitsWithin(typeOfFirst, (N**T1)[dseq]):
        elements = []
        for x in xs:
            # could check the type of each list using metatypes.fitsWithin
            elements.extend(x.data)
        return dseq(xs[0]._t, elements)
    elif _fitsWithin(typeOfFirst, pylist):
        answer = []
        for e in xs:
            answer += e
        return answer
    elif _fitsWithin(typeOfFirst, pytuple):
        answer = ()
        for e in xs:
            answer += e
        return answer


# **********************************************************************************************************************
# keys
# **********************************************************************************************************************

@coppertop
def keys(d:pydict) -> pylist:     # (T1**T2)&map -> (N**T1)&pylist
    return list(d.keys())

@coppertop
def keys(x:(T1**T2)[dmap][T3]) -> (N**T1)[pylist]:
    return tv(
        (N**x._t.parent.parent.indexType)[pylist],
        list(x._keys())
    )

@coppertop
def keys(m:dmap) -> pylist:
    return list(m.keys())

@coppertop
def keys(f:dframe) -> pylist:
    return list(f._keys())

@coppertop
def keys(s:(dstruct & T1)+dstruct) -> list: #(N**txt)[pydict_keys]: needs a tvdict_keys!!!
    return list(s._keys())


# **********************************************************************************************************************
# keys_
# **********************************************************************************************************************

@coppertop
def keys_(d:pydict) -> pydict_keys:     # (T2**T1)(map) -> (N**T1)(iter)
    return d.keys()

@coppertop
def keys_(s:dmap) -> pydict_keys:
    return s._keys()


# **********************************************************************************************************************
# kvs
# **********************************************************************************************************************

@coppertop
def kvs(x:dmap) -> pydict_items:
    return x._kvs()

@coppertop
def kvs(x:dmap) -> pydict_items:
    return x._kvs()

@coppertop
def kvs(x:(T1**T2)[dstruct][T]) -> pydict_items:
    return x._v._kvs()

@coppertop
def kvs(x:(T1**T2)[dstruct][T]) -> pydict_items:
    return x._v._kvs()

@coppertop
def kvs(x:pydict) -> pydict_items:
    return x.items()


# **********************************************************************************************************************
# last
# **********************************************************************************************************************

@coppertop
def last(f:dframe) -> dframe:
    return dframe({k:f[k][[-1]] for k in f._keys()})

@coppertop
def last(x:pylist+pytuple):
    return x[-1]


# **********************************************************************************************************************
# merge - answers all of A and all of B raising an error if any keys are in common - see also underride and override
# **********************************************************************************************************************

@coppertop(style=binary)
def merge(a:pydict, b:pydict) -> pydict:
    answer = dict(a)
    for k, v in b.items():
        if k in answer:
            raise RuntimeError(f"{k} is already in a")
        else:
            answer[k] = v
    return answer

@coppertop(style=binary)
def merge(a:pydict, b:dstruct) -> pydict:
    answer = dict(a)
    for k, v in b._kvs():
        if k in answer:
            raise RuntimeError(f"{k} is already in a")
        else:
            answer[k] = v
    return answer

@coppertop(style=binary)
def merge(a:dmap, b:dmap) -> dmap:
    answer = dmap(a)
    for k, v in b._kvs():
        if k in answer:
            raise RuntimeError(f"{k} is already in a")
        else:
            answer[k] = v
    return answer

@coppertop(style=binary)
def merge(a:dstruct, b:dstruct) -> dstruct:
    answer = dstruct(a)
    for k, v in b._kvs():
        if k in answer:
            raise RuntimeError(f"{k} is already in a")
        else:
            answer[k] = v
    return answer

@coppertop(style=binary)
def merge(a:dstruct, b:pydict) -> dstruct:
    answer = dstruct(a)
    for k, v in b.keys():
        if k in answer:
            raise RuntimeError(f"{k} is already in a")
        else:
            answer[k] = v
    return answer


# **********************************************************************************************************************
# minus
# **********************************************************************************************************************

@coppertop(style=binary)
def minus(a:pyset, b:pyset+pylist+pydict_keys+pydict_values) -> pyset:
    return a.difference(b)

@coppertop(style=binary)
def minus(a:pylist+pytuple, b:pyset+pylist+pydict_keys+pydict_values) -> pyset:
    return set(a).difference(b)


# **********************************************************************************************************************
# numCols
# **********************************************************************************************************************

@coppertop
def numCols(f: dframe) -> t.count:
    return len(f._keys())

@coppertop
def numCols(x:matrix&tvarray) -> t.count:
    return x.shape[1] | t.count

@coppertop
def numCols(x:np.ndarray) -> t.count:
    return x.shape[1] | t.count


# **********************************************************************************************************************
# numRows
# **********************************************************************************************************************

@coppertop
def numRows(f: dframe) -> t.count:
    firstCol = None
    for firstCol in f._values():
        break
    return firstCol.shape[0]

@coppertop
def numRows(x:matrix&tvarray) -> t.count:
    return x.shape[0] | t.count

@coppertop
def numRows(x:np.ndarray) -> t.count:
    return x.shape[0] | t.count


# **********************************************************************************************************************
# override - for each in A replace with the one in B if it exists
# **********************************************************************************************************************

@coppertop(style=binary)
def override(a:dstruct, b:dstruct) -> dstruct:
    answer = dstruct(a)
    for k, v in b._kvs():
        if k in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer


# **********************************************************************************************************************
# prepend
# **********************************************************************************************************************

@coppertop(style=binary)
def prepend(l:pylist, element) -> pylist:
    l = list(l)
    l.insert(0, element)
    return l

@coppertop(style=binary)
def prepend(l:(N**T1)&dseq, element:T1) -> (N**T1)&dseq:
    l = dseq(l)
    l.insert(0, element)
    return l


# **********************************************************************************************************************
# prependTo
# **********************************************************************************************************************

@coppertop(style=binary)
def prependTo(element, l:pylist) -> pylist:
    l = list(l)
    l.insert(0, element)
    return l

@coppertop(style=binary)
def prependTo(element:T1, l:(N**T1)&dseq) -> (N**T1)&dseq:
    l = dseq(l)
    l.insert(0, element)
    return l


# **********************************************************************************************************************
# rename
# **********************************************************************************************************************

@coppertop(style=ternary)
def rename(d:pydict, old, new):
    d = dict(d)
    d[new] = d.pop(old)
    return d

@coppertop(style=ternary)
def rename(d:dmap, old, new):
    d = dmap(d)
    d[new] = d._pop(old)
    return d


# **********************************************************************************************************************
# replace
# **********************************************************************************************************************

@coppertop(style=ternary)
def replace(d:dmap, f:txt, new):
    d = dmap(d)
    d[f] = new
    return d

@coppertop(style=ternary)
def replace(d:pydict, f:txt, new):
    d = dict(d)
    d[f] = new
    return d


# **********************************************************************************************************************
# scalarProduct aka innerProduct, dotProduct - scalarProduct is selected here as it conveys return type
# **********************************************************************************************************************

@coppertop(style=binary)
def scalarProduct(A:matrix&tvarray, B:matrix&tvarray) -> num:
    return float(np.dot(A, B))


# **********************************************************************************************************************
# select - https://en.wikipedia.org/wiki/Filter_(higher-order_function)
# **********************************************************************************************************************

@coppertop(style=binary)
def select(d:pydict, f2) -> pydict:
    filteredKVs = []
    for k, v in d.items():
        if f2(k, v): filteredKVs.append((k,v))
    return dict(filteredKVs)

@coppertop(style=binary)
def select(d:dmap, f2) -> dmap:
    filteredKVs = []
    for k, v in d._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return dmap(filteredKVs)

@coppertop(style=binary)
def select(pm:dstruct, f2) -> dstruct:
    filteredKVs = []
    for k, v in pm._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return dstruct(pm._t, filteredKVs)

@coppertop(style=binary)
def select(pm:(T1**T2)[dstruct], f2) -> (T1**T2)[dstruct]:
    filteredKVs = []
    for k, v in pm._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return dstruct(pm._t, filteredKVs)

@coppertop(style=binary)
def select(pm:(T1**T2)[dstruct][T3], f2) -> (T1**T2)[dstruct][T3]:
    filteredKVs = []
    for k, v in pm._v._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return dstruct(pm._t, filteredKVs)

@coppertop(style=binary)
def select(xs:pylist+pydict_keys+pydict_values, f) -> pylist:
    return [x for x in xs if f(x)]

@coppertop(style=binary)
def select(xs:pytuple, f) -> pytuple:
    return tuple(x for x in xs if f(x))

@coppertop(style=binary)
def select(a:dframe, fn1) -> dframe:
    fs = a._keys()
    cols = [c for c in a._values()] #a >> values >> std.collect >> partial(lambda c: c)
    # collate the offsets that fn1 answers true
    os = []
    for o in range(cols[0].shape[0]):
        r = dstruct(builtins.zip(fs, [c[o] for c in cols]))
        if fn1(r): os.append(o)
    # create new cols from the old cols and the offsets
    newCols = [c[os] for c in cols]
    return dframe(builtins.zip(fs, newCols))

@coppertop(style=binary)
def select(z:builtins.zip, f:pyfunc):
    answer = []
    for e in z:
        if f(*e): answer.append(e)
    return answer


# **********************************************************************************************************************
# setOrder - reorders the keyed collection a with the keys in ks - keeping the order of any missing at the end
# **********************************************************************************************************************

@coppertop(style=binary)
def setOrder(a, ks):
    raise NotYetImplemented()


# **********************************************************************************************************************
# shape
# **********************************************************************************************************************

@coppertop
def shape(x:matrix&tvarray) -> pytuple:
    return x.shape

@coppertop
def shape(f:dframe) -> pytuple:
    firstCol = None
    for firstCol in f._values():
        break
    return (firstCol.shape[0], len(f._keys()))


# **********************************************************************************************************************
# shift
# **********************************************************************************************************************

@coppertop(style=binary)
def shift(m:array_, n:t.count) -> array_:
    if n == 0:
        return m
    elif n > 0:
        answer = np.roll(m, n)
        answer[0:n] = 0
        return answer
    else:
        raise NotYetImplemented()


# **********************************************************************************************************************
# shuffleColsInPlace
# **********************************************************************************************************************

@coppertop
def shuffleColsInPlace(panel:matrix&tvarray) -> matrix&tvarray:
    for i in range(panel >> numCols):
        ix = np.arange(panel >> numRows)
        np.random.shuffle(ix)      # destructive
        panel[:,i] = panel[:,i][ix]
    return panel


# **********************************************************************************************************************
# soleElement
# **********************************************************************************************************************

@coppertop
def soleElement(a:pyset):
    # https://stackoverflow.com/questions/1619514/how-to-extract-the-member-from-single-member-set-in-python
    answer, = a
    return answer


# **********************************************************************************************************************
# sort
# **********************************************************************************************************************

@coppertop
def sort(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=False))

@coppertop
def sort(x:dstruct) -> dstruct:
    return dstruct(sorted(x._kvs(), key=None, reverse=False))

@coppertop
def sort(x:dmap) -> dmap:
    return dmap(sorted(x._kvs(), key=None, reverse=False))

@coppertop
def sort(x:pylist+pyset) -> pylist:
    return sorted(x, key=None, reverse=False)


# **********************************************************************************************************************
# sortRev
# **********************************************************************************************************************

@coppertop
def sortRev(x:pylist+pyset) -> pylist:
    return sorted(x, key=None, reverse=True)

@coppertop
def sortRev(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=True))

@coppertop
def sortRev(x:dmap) -> dmap:
    raise NotYetImplemented()

@coppertop
def sortRev(x:dstruct) -> dstruct:
    raise NotYetImplemented()


# **********************************************************************************************************************
# sortRevUsing
# **********************************************************************************************************************

@coppertop(style=binary)
def sortRevUsing(x:pylist+pyset, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=True)

@coppertop(style=binary)
def sortRevUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=True))


# **********************************************************************************************************************
# sortUsing
# **********************************************************************************************************************

@coppertop(style=binary)
def sortUsing(x:pylist+pyset, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=False)

@coppertop(style=binary)
def sortUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=False))

@coppertop(style=binary)
def sortUsing(soa, f):
    raise NotYetImplemented()


# **********************************************************************************************************************
# split - splits collection a at all the points in b
# [1, 2, 3] >> split >> 1 == [[1], [2], [3]]
# [1, 2, 3] >> split >> 0 == [[], [1], [2, 3]]
# **********************************************************************************************************************

@coppertop(style=binary)
def split(a, b):
    raise NotYetImplemented()


# **********************************************************************************************************************
# splitCol - splits matrix a at all the points in b
# **********************************************************************************************************************

@coppertop(style=binary)
def splitCol(a, b):
    raise NotYetImplemented()


# **********************************************************************************************************************
# splitOn - splits collection a at every point value v is found
# "fred.joe" >> splitOn >> '.' == ['fred', 'joe']  (the '.' is implicit)
# **********************************************************************************************************************

@coppertop(style=binary)
def splitOn(a, v):
    raise NotYetImplemented()


# **********************************************************************************************************************
# splitRow - splits matrix a at all the points in b
# **********************************************************************************************************************

@coppertop(style=binary)
def splitRow(a, b):
    raise NotYetImplemented()


# **********************************************************************************************************************
# subsetOf
# **********************************************************************************************************************

@coppertop(style=binary)
def subsetOf(a, b):
    if not isinstance(a, (list, set, tuple, dict_keys, dict_values)):
        if not isinstance(b, (list, set, tuple, dict_keys, dict_values)):
            # 1, 1
            return a == b
        else:
            # 1, 1+
            return a in b
    else:
        if not isinstance(b, (list, set, tuple, dict_keys, dict_values)):
            # 1+, 1
            return False
        else:
            # 1+, 1+
            for e in a:
                if e not in b:
                    return False
            return True


# **********************************************************************************************************************
# T
# **********************************************************************************************************************

@coppertop
def T(A:matrix&tvarray) -> matrix&tvarray:
    return A.T


# **********************************************************************************************************************
# take - for type analysis / issues see drop
# **********************************************************************************************************************

@coppertop(style=binary)
def take(a:dframe, k:txt) -> dframe:
    return dframe({k:a[k]})

@coppertop(style=binary)
def take(a:dframe, isOrKs:pylist) -> dframe:
    if not isOrKs:
        return dframe
    elif isinstance(isOrKs[0], (builtins.str, str)):
        return dframe({k:a[k] for k in isOrKs})
    elif isinstance(isOrKs[0], int):
        raise NotYetImplemented()
    else:
        raise TypeError()

@coppertop(style=binary)
def take(a:dframe, ss:pytuple) -> dframe:
    raise NotYetImplemented()

@coppertop(style=binary)
def take(a:dframe, i:t.count) -> dframe:
    if i >= 0:
        return dframe({k:a[k][0:i] for k in a._keys()})
    else:
        return dframe({k:a[k][i:] for k in a._keys()})

@coppertop(style=binary)
def take(a:dframe, isOrKs:pylist) -> dframe:
    if not isOrKs:
        return dframe()
    elif isinstance(isOrKs[0], (str, txt)):
        # sequence( of strings
        return dframe({k:a[k] for k in isOrKs})
    elif isinstance(isOrKs[0], (int, offset)):
        # sequence( of offets
        return dframe({k:at(a[k], isOrKs) for k in a._keys()})
    else:
        raise TypeError()

@coppertop(style=binary)
def take(a:dframe, ss:slice) -> dframe:
    return dframe({k:a[k][ss] for k in a._keys()})

@coppertop(style=binary)
def take(d:pydict, ks:pylist) -> pydict:
    return {k:d[k] for k in ks}

@coppertop(style=binary)
def take(d:pydict, k:txt) -> pydict:
    return {k:d[k]}

@coppertop(style=binary)
def take(d:dstruct, k:txt) -> dstruct:
    return d[k]

@coppertop(style=binary)
def take(xs:pylist, c:t.count) -> pylist:
    if c >= 0:
        return xs[0:c]
    else:
        return xs[c:]

@coppertop(style=binary)
def take(xs:pylist, os:pylist) -> pylist:
    return [xs[o] for o in os]

@coppertop(style=binary)
def take(xs:pylist, ss:pytuple) -> pylist:
    s1, s2 = ss
    if s1 is Ellipsis:
        if s2 is Ellipsis:
            return xs
        else:
            return xs[:s2]
    else:
        if s2 is Ellipsis:
            return xs[s1:]
        else:
            return xs[s1:s2]

@coppertop(style=binary)
def take(xs:(N**T1)&tvarray, c:t.count) -> (N**T1)&tvarray:
    if c >= 0:
        return xs[:c]
    else:
        return xs[c:]


# **********************************************************************************************************************
# takeCol
# A takeCol 1
# **********************************************************************************************************************

@coppertop(style=binary)
def takeCol(m:matrix&tvarray, i:offset):
    return m[:,[i]]


# **********************************************************************************************************************
# takeColRemain
# A takeColRemain 1
# **********************************************************************************************************************

@coppertop(style=binary)
def takeColRemain(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# takeCols
# **********************************************************************************************************************

@coppertop(style=binary)
def takeCols(m:matrix&tvarray, n:t.count) -> matrix&tvarray:
    if n >= 0:
        return m[:,0:n]
    else:
        raise NotYetImplemented()


# **********************************************************************************************************************
# takeDiag
# **********************************************************************************************************************

@coppertop
def takeDiag(m: matrix & tvarray) -> array_:
    return np.diag(m) | array_


# **********************************************************************************************************************
# takePanel
# **********************************************************************************************************************

@coppertop
def takePanel(f:dframe) -> matrix&tvarray:
    return (matrix&tvarray)(np.hstack(f >> values))


# **********************************************************************************************************************
# takeRemain
# A takeRemain 1
# **********************************************************************************************************************

@coppertop(style=binary)
def takeRemain(f:dframe, n:t.count):
    t, r = dframe(), dframe()
    for k, v in f._kvs():
        t[k] = v[:n]
        r[k] = v[n:]
    return t, r


# **********************************************************************************************************************
# takeRemainUsing
# **********************************************************************************************************************

@coppertop(style=binary)
def takeRemainUsing(xs:pytuple, f1):
    selected = []
    rejected = []
    for x in xs:
        if f1(x):
            selected.append(x)
        else:
            rejected.append(x)
    return tuple(selected), tuple(rejected)


# **********************************************************************************************************************
# takeRow
# A takeRow 1
# **********************************************************************************************************************

@coppertop(style=binary)
def takeRow(m, i):
    raise NotYetImplemented()


# **********************************************************************************************************************
# takeRowRemain
# A takeRowRemain 1
# **********************************************************************************************************************

@coppertop(style=binary)
def takeRowRemain(X:matrix&tvarray, i:offset) -> pytuple:
    remain = np.delete(X, i, axis=0)
    take = X[[i],:]
    return take, remain


# **********************************************************************************************************************
# takeRows
# **********************************************************************************************************************

@coppertop(style=binary)
def takeRows(m:matrix&tvarray, n:t.count) -> matrix&tvarray:
    if n >= 0:
        return m[:n, :]
    else:
        return m[n:, :]


# **********************************************************************************************************************
# toDiag
# **********************************************************************************************************************

@coppertop
def toDiag(m: array_) -> matrix & tvarray:
    return (matrix & tvarray)(np.diag(m))


# **********************************************************************************************************************
# underride
# **********************************************************************************************************************

@coppertop(style=binary)
def underride(a:dstruct, b:dstruct) -> dstruct:
    answer = dstruct(a)
    for k, v in b._kvs():
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer

@coppertop(style=binary)
def underride(a:dstruct, b:pydict) -> dstruct:
    answer = dstruct(a)
    for k, v in b.items():
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer

@coppertop(style=binary)
def underride(a:pydict, b:pydict) -> pydict:
    answer = dict(a)
    for k, v in b.items():
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer


# **********************************************************************************************************************
# values
# **********************************************************************************************************************

@coppertop
def values(x:(T1**T2)[dstruct][T3]) -> (N**T2)[pylist]:
    return tv(
        (N**x._t.parent.parent.mappedType)[pylist],
        list(x._values())
    )

@coppertop
def values(x:pydict) -> pytuple:
    return tuple(x.values())

@coppertop
def values_(x:pydict) -> pydict_values:
    return x.values()

@coppertop
def values(x:dmap) -> pytuple:
    return tuple(x._values())

@coppertop
def values_(x:dmap) -> pydict_values:
    return x._values()

@coppertop
def values(a:dframe) -> pytuple:
    return tuple(a._values())

@coppertop
def values_(a:dframe) -> pydict_values:
    return a._values()


# **********************************************************************************************************************
# [1,2,3,4] without [2,3] == [1,4]
# without as python can't easily distinguish drop(N**T1, N**N) from drop(N**T1, N**T1) :(
# **********************************************************************************************************************

@coppertop(style=binary)
def without(xs:pylist+pytuple+pyset, elements:pylist+pytuple+pyset) -> pylist:
    answer = []
    for x in xs:
        if x not in elements:
            answer.append(x)
    return answer

@coppertop(style=binary)
def without(xs:pylist+pytuple+pyset, element) -> pylist:
    answer = []
    for x in xs:
        if x != element:
            answer.append(x)
    return answer

@coppertop(style=binary)
def without(xs:(N**T1)[dseq], element:T1, tByT) -> (N**T1)[dseq]:
    answer = dseq((N**tByT[T1])[dseq])
    for e in xs:
        if e != element:
            answer.append(e)
    return answer


# **********************************************************************************************************************
# XTX
# **********************************************************************************************************************

@coppertop
def XTX(x:matrix&tvarray) -> matrix&tvarray:
    return x.T @ x


# **********************************************************************************************************************
# XXT
# **********************************************************************************************************************

@coppertop
def XXT(x:matrix&tvarray) -> matrix&tvarray:
    return x @ x.T


# **********************************************************************************************************************
# zipAll
# **********************************************************************************************************************

@coppertop
def zipAll(x:pylist+pytuple+pydict_keys+pydict_values+pydict_items):
    return builtins.zip(*x)
