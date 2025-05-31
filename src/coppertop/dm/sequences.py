# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# https://kotlinlang.org/docs/sequences.html#construct


import sys, types

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from coppertop.dm._irange import IInputRange, IRandomAccessInfinite
from coppertop.dm._range import EachFR, ChainAsSingleFR, UntilFR, FileLineIR, ListOR, toIndexableFR, \
    ChunkUsingSubRangeGeneratorFR, RaggedZipIR, FnAdapterFR, ChunkFROnChangeOf, EMPTY
from coppertop.dm._range import getIRIter
from coppertop.dm.core.types import pytuple


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - imports done')


@coppertop
def rZip(r):
    raise NotYetImplemented()

@coppertop
def rInject(r, seed, f):
    raise NotYetImplemented()

@coppertop
def rFilter(r, f):
    raise NotYetImplemented()

@coppertop
def rTakeBack(r, n):
    raise NotYetImplemented()

@coppertop
def rDropBack(r, n):
    raise NotYetImplemented()

@coppertop
def rFind(r, value):
    while not r.empty:
        if r.front == value:
            break
        r.popFront()
    return r

@coppertop
def put(r, x):
    return r.put(x)

@coppertop
def front(r):
    return r.front

@coppertop
def back(r):
    return r.back

@coppertop
def empty(r):
    return r.empty

@coppertop
def popFront(r):
    r.popFront()
    return r

@coppertop
def popBack(r):
    r.popBack()
    return r


each_ = coppertop(style=binary, name='each_')(EachFR)
rChain = coppertop(name='rChain')(ChainAsSingleFR)
rUntil = coppertop(style=binary, name='rUntil')(UntilFR)


@coppertop
def fileLineIR(f):
    return FileLineIR(f)

@coppertop
def listOR(l):
    return ListOR(l)

@coppertop
def chunkUsingSubRangeGeneratorFR(r, f):
    return ChunkUsingSubRangeGeneratorFR(r, f)

@coppertop
def raggedZipIR(r):
    return RaggedZipIR(r)

@coppertop
def fnAdapterFR(r):
    return FnAdapterFR(r)

@coppertop
def chunkFROnChangeOf(r, f):
    return ChunkFROnChangeOf(r, f)

@coppertop
def fnAdapterEager(f):
    answer = []
    i = 0
    while (x := f(i)) != EMPTY:
        answer.append(x)
        i += 1
    return answer

@coppertop
def replaceWith(haystack, needle, replacement):
    return haystack >> each_ >> (lambda e: replacement if e == needle else e)

@coppertop(style=binary)
def pushAllTo(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return outR

def _materialise(r):
    answer = list()
    while not r.empty:
        e = r.front
        if isinstance(e, IInputRange) and not isinstance(e, IRandomAccessInfinite):
            answer.append(_materialise(e))
            if not r.empty:  # the sub range may exhaust this range
                r.popFront()
        else:
            answer.append(e)
            r.popFront()
    return answer

@coppertop
def materialise(r):
    return _materialise(r)


# **********************************************************************************************************************
# buffer
# **********************************************************************************************************************

@coppertop
def buffer(iter) -> pytuple:
    return tuple(iter)



if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
