# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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

import os, os.path, json, itertools, builtins, numpy as np

from io import TextIOWrapper
from coppertop.pipe import *
from dm.core.types import txt, pylist, bframe, bmap, pytuple, pyfunc, btup, pydict, t as bt
from dm.core.text import strip
from dm.core.aggman import collect
from bones.core.errors import NotYetImplemented
from bones.core.sentinels import Missing
from dm.core.conv import to
from dm.core.aggman import zip



class OStreamWrapper(object):
    def __init__(self, sGetter):
        self._sGetter = sGetter
    def __lshift__(self, other):
        # self << other
        self._sGetter().write(other)      # done as a function call so it plays nicely with HookStdOutErrToLines
        return self

stdout = OStreamWrapper(lambda : sys.stdout)
stderr = OStreamWrapper(lambda : sys.stderr)



# **********************************************************************************************************************
# chunkBy
# **********************************************************************************************************************

@coppertop
def chunkBy(a:bframe, keys):
    "answers a range of range of row"
    raise NotYetImplemented()


# **********************************************************************************************************************
# chunkUsing
# **********************************************************************************************************************

@coppertop(style=binary)
def chunkUsing(iter, fn2):
    answer = []
    i0 = 0
    for i1, (a, b) in enumerate(_pairwise(iter)):
        if not fn2(a, b):
            answer += [iter[i0:i1+1]]
            i0 = i1 + 1
    answer += [iter[i0:]]
    return answer
def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return builtins.zip(a, b)


# **********************************************************************************************************************
# groupBy
# **********************************************************************************************************************

@coppertop
def groupBy(a:bframe, keys):
    "answers a collection of groups"
    raise NotYetImplemented()

@coppertop
def groupBy(a:bframe, keys, directions):
    "answers a collection of groups"
    raise NotYetImplemented()


getCwd = coppertop(style=nullary, name='getCwd')(os.getcwd)
isFile = coppertop(name='isFile')(os.path.isfile)
isDir = coppertop(name='isDir')(os.path.isdir)
dirEntries = coppertop(style=nullary, name='dirEntries')(lambda path: os.listdir(path))

@coppertop(style=binary)
def joinPath(a, b):
    return os.path.join(a, *(b if isinstance(b, (list, tuple)) else [b]))

@coppertop
def readlines(f:TextIOWrapper) -> pylist:
    return f.readlines()

@coppertop
def linesOf(pfn:txt):
    with open(pfn) as f:
        return f >> readlines >> collect >> strip(_,'\\n')

@coppertop(style=binary)
def copyTo(src, dest):
    raise NotImplementedError()

@coppertop
def readJson(pfn:txt):
    with open(pfn) as f:
        return json.load(f)

@coppertop
def readJson(f:TextIOWrapper):
    return json.load(f)

@coppertop(style=binary, module='bmap')
def ksJoinVs(ks, vs) -> bmap:
    return [ks, vs] >> zip >> to >> bmap
bmap.ksJoinVs = ksJoinVs

@coppertop(style=binary, module='pydict')
def ksJoinVs(ks, vs) -> pydict:
    return [ks, vs] >> zip >> to >> pydict
pydict.ksJoinVs = ksJoinVs


def sequence(p1, p2, n=Missing, step=Missing, sigmas=Missing):
    requiredType = bt.count
    if step is not Missing and n is not Missing:
        raise TypeError('Must only specify either n or step')
    if step is Missing and n is Missing:
        first , last = p1, p2
        return [e | requiredType for e in range(first, last+1, 1)]
    elif n is not Missing and sigmas is not Missing:
        mu, sigma = p1, p2
        low = mu - sigmas * sigma
        high = mu + sigmas * sigma
        first, last = high, low
        return [e | requiredType for e in np.linspace(first, last, n)]
    elif n is not Missing and sigmas is Missing:
        first, last = p1, p2
        return [e | requiredType for e in np.linspace(first, last, n)]
    elif n is Missing and step is not Missing:
        first, last = p1, p2
        return [e | requiredType for e in np.arange(first, last + step, step)]
    else:
        raise NotImplementedError('Unhandled case')
bt.count.sequence = sequence

def sequence(p1, p2, n=Missing, step=Missing, sigmas=Missing):
    requiredType = bt.offset
    if step is not Missing and n is not Missing:
        raise TypeError('Must only specify either n or step')
    if step is Missing and n is Missing:
        first , last = p1, p2
        return [e | requiredType for e in range(first, last+1, 1)]
    elif n is not Missing and sigmas is not Missing:
        mu, sigma = p1, p2
        low = mu - sigmas * sigma
        high = mu + sigmas * sigma
        first, last = high, low
        return [e | requiredType for e in np.linspace(first, last, n)]
    elif n is not Missing and sigmas is Missing:
        first, last = p1, p2
        return [e | requiredType for e in np.linspace(first, last, n)]
    elif n is Missing and step is not Missing:
        first, last = p1, p2
        return [e | requiredType for e in np.arange(first, last + step, step)]
    else:
        raise NotImplementedError('Unhandled case')
bt.offset.sequence = sequence
@coppertop
def sequence_(n:bt.count):
    return range(n)
bt.offset.sequence_ = sequence_

def sequence(p1, p2, n=Missing, step=Missing, sigmas=Missing):
    requiredType = bt.index
    if step is not Missing and n is not Missing:
        raise TypeError('Must only specify either n or step')
    if step is Missing and n is Missing:
        first , last = p1, p2
        return [e | requiredType for e in range(first, last+1, 1)]
    elif n is not Missing and sigmas is not Missing:
        mu, sigma = p1, p2
        low = mu - sigmas * sigma
        high = mu + sigmas * sigma
        first, last = high, low
        return [e | requiredType for e in np.linspace(first, last, n)]
    elif n is not Missing and sigmas is Missing:
        first, last = p1, p2
        return [e | requiredType for e in np.linspace(first, last, n)]
    elif n is Missing and step is not Missing:
        first, last = p1, p2
        return [e | requiredType for e in np.arange(first, last + step, step)]
    else:
        raise NotImplementedError('Unhandled case')
bt.index.sequence = sequence

@coppertop(style=binary)
def takeUntil(iter, fn):
    items = []
    if isinstance(iter, dict):
        for k, v in iter.items():
            if fn(k, v):
                break
            else:
                items.append([k,v])
        return dict(items)
    else:
        raise NotYetImplemented()

@coppertop
def replaceAll(xs, old, new):
    assert isinstance(xs, pytuple)
    return (new if x == old else x for x in xs)

@coppertop
def fromto(x, s1):
    return x[s1:None]

@coppertop
def fromto(x, s1, s2):
    return x[s1:s2]

@coppertop(style=binary)
def where(s:bmap, bools) -> bmap:
    assert isinstance(s, bmap)
    answer = bmap(s)
    for f, v in s._kvs():
        answer[f] = v[bools].view(btup)
    return answer

@coppertop
def wrapInList(x):
    l = list()
    l.append(x)
    return l

@coppertop(style=binary)
def eachAsArgs(listOfArgs, f):
    """eachAsArgs(f, listOfArgs)
    Answers [f(*args) for args in listOfArgs]"""
    return [f(*args) for args in listOfArgs]

@coppertop(style=binary)
def subset(a:bmap, f2:pyfunc) -> pytuple:
    A, B = bmap(), bmap()
    for k, v in a._kvs():
        if f2(k, v):
            A[k] = v
        else:
            B[k] = v
    return A, B

