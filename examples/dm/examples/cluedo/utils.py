# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************
import time


import numpy as np
from coppertop.pipe import *
from bones.lang.metatypes import BTAtom
from bones.core.sentinels import Missing
from dm.core.types import txt, N, index, pylist, pytuple, T, pydict, dseq, dstruct, t, pyfunc
from dm.core.aggman import count, collect, inject, zipAll, minus, without, join, sort
from dm.testing import check, equals
from dm.core.maths import max, nCombinations, sum
# from dm.core.text import pad
from dm.pp import PP
from groot import pad

from dm.examples.cluedo.types import display_table, tPair



BONES_NS = GROOT_NS


@coppertop
def PP(t:display_table) -> display_table:
    for string in t:
        string >> PP
    return t

@coppertop(style=binary)
def hjoin(a:display_table, b:display_table) -> display_table:
    return hjoin(a, b, {})

@coppertop(style=binary)
def hjoin(a:display_table, b:display_table, options:pydict) -> display_table:
    assert (a >> count) == (b >> count)
    answer = dseq(display_table, [])
    for i in range(len(a)):
        answer.append(a[i] + options.get('sep', '') + b[i])
    return answer

@coppertop(style=binary)
def join(a:display_table, b:display_table) -> display_table:
    return dseq(display_table, a.data + b.data) >> ljust

@coppertop
def ljust(rows:display_table) -> display_table:
    return ljust(rows, {})

@coppertop
def ljust(rows:display_table, options:pydict) -> display_table:
    maxLength = rows >> collect >> count >> max
    options_ = dict(left=max((maxLength, options.get('width',0))), pad=options.get('fillchar', ' '))
    return rows >> collect >> pad(_, options_) | display_table

@coppertop(style=binary)
def add(rows:display_table, row:txt) -> display_table:
    rows.append(row)
    return rows >> ljust

@coppertop
def nPartitions(sizes:pylist) -> t.count:
    num = 1
    n = sizes >> sum
    for k in sizes:
        num *= n >> nCombinations >> k
        n -= k
    return num | t.count

@coppertop(style=binary)
def allPartitionsInto(xs:pylist+pytuple, sizes:pylist+pytuple) -> pylist: #N**N**N**T:
    sizes >> sum >> check >> equals >> (xs >> count)
    return _partitions(list(xs), sizes)

def _partitions(xs:N**T, sizes:N**t.count) -> pylist: #N**N**N**T:
    if sizes:
        answer = []
        for comb, rest in _combRest(xs, sizes[0]):
            for e in _partitions(rest, sizes[1:]):
                answer.append(comb + e)
        return answer
    else:
        return [[]]

def _combRest(xs:N**T, m:count) -> pylist: #N**( (N**T)*(N**T) ):
    '''answer [m items chosen from n items, the rest]'''
    if m == 0:
        return [([], xs)]
    elif m == len(xs):
        return [(xs, [])]
    else:
        firstOne, remainder = xs[0:1], xs[1:]
        firstPart = [ (firstOne + x, y) for x, y in _combRest(remainder, m - 1)]
        secondPart = [ (x, firstOne + y) for x, y in _combRest(remainder, m)]
        return firstPart + secondPart

# %%timeit
# x = list(range(13)) >> allPartitionsInto >> [5,4,4]
# 115 ms ± 3.49 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


@coppertop
def shape(x: np.ndarray) -> pytuple:
    return x.shape

@coppertop(style=binary)
def take(x: np.ndarray, n: t.count) -> np.ndarray:
    if n > 0:
        return x[:n]
    else:
        return x[n:]

@coppertop(style=binary)
def takeRows(x: np.ndarray, n: t.count) -> np.ndarray:
    if n > 0:
        return x[:n, :]
    else:
        return x[n:, :]

@coppertop
def sum(x: np.ndarray):
    return np.sum(x)

@coppertop
def unpackArgs(f:pyfunc) -> pyfunc:
    return lambda args: f(*args)

@coppertop
def cardIds(cards):
    return [c.value for c in cards]


partitionsTime = 0
NS_TO_S = 1 / 1_000_000_000

def createPossibilities(ps, ws, rs, handSizes, handKnowns):
    global partitionsTime
    t1 = time.perf_counter_ns()
    mTBI = 0
    hkIds = handKnowns >> collect >> (lambda hand: hand >> collect >> (lambda c: c.value))

    pRemain = ps >> collect >> (lambda c: c.value) >> inject(hkIds, _, _) >> (lambda p, e: p >> minus >> e) >> sort
    pRemain, mTBI = (pRemain, mTBI + 1) if pRemain else ([Missing], mTBI)
    wRemain = ws >> collect >> (lambda c: c.value) >> inject(hkIds, _, _) >> (lambda p, e: p >> minus >> e) >> sort
    wRemain, mTBI = (wRemain, mTBI + 1) if wRemain else ([Missing], mTBI)
    rRemain = rs >> collect >> (lambda c: c.value) >> inject(hkIds, _, _) >> (lambda p, e: p >> minus >> e) >> sort
    rRemain, mTBI = (rRemain, mTBI + 1) if rRemain else ([Missing], mTBI)

    sizes = [handSizes, hkIds] >> zipAll >> collect >> unpackArgs(lambda hs, hk: hs - (hk >> count)) >> without >> [0]
    nEachSet = sizes >> nPartitions
    nTBI = (pRemain >> count) * (wRemain >> count) * (rRemain >> count)
    nCols = mTBI + (sizes >> sum)

    f'nTBI:  {nTBI}  nEachSet:  {nEachSet}   nCols:  {nCols}  ' + \
    f'mem:  {(nTBI * nEachSet) * (nCols) / 1_000_000}MB' >> PP

    t2 = time.perf_counter_ns()
    answer = np.zeros((nTBI * nEachSet, nCols), np.uint8, order="F")
    t3 = time.perf_counter_ns()
    answer[:,:] = 0
    t4 = time.perf_counter_ns()
    f'zeros: {(t3-t2) * NS_TO_S}  =0:  {(t4-t3) * NS_TO_S}' >> PP
    partitionsTimes = []
    assignTimes = []

    # assuming replacing ids in numpy array is quicker than regenerating the partitions each time:
    # create master
    # copy master
    # for each id in copy replace with the needed value
    # assign copy to answer

    master = np.zeros((nEachSet, nCols), np.uint8, order="F")
    p = pRemain[0]
    w = wRemain[0]
    r = rRemain[0]
    ocol = 0
    remain = []
    if p:
        ocol += 1
        remain = remain >> join >> (pRemain >> without >> p)
    if w:
        ocol += 1
        remain = remain >> join >> (wRemain >> without >> w)
    if r:
        ocol += 1
        remain = remain >> join >> (rRemain >> without >> r)
    res = list(range(101, 101 + len(remain))) >> allPartitionsInto >> sizes
    master[:, ocol:] = res

    oTBI = 0
    for p in pRemain:
        for w in wRemain:
            for r in rRemain:
                t2 = time.perf_counter_ns()
                srow1, srow2 = oTBI * nEachSet, (oTBI + 1) * nEachSet
                ocol = 0
                remain = []
                res = np.copy(master)
                if p:
                    res[:, ocol] = p
                    ocol += 1
                    remain = remain >> join >> (pRemain >> without >> p)
                if w:
                    res[:, ocol] = w
                    ocol += 1
                    remain = remain >> join >> (wRemain >> without >> w)
                if r:
                    res[:, ocol] = r
                    ocol += 1
                    remain = remain >> join >> (rRemain >> without >> r)
                for f, t in zip(range(101, 101 + len(remain)), remain):
                    res[res == f] = t
                t3 = time.perf_counter_ns()
                answer[srow1:srow2, :] = res
                t4 = time.perf_counter_ns()
                partitionsTimes.append(t3 - t2)
                assignTimes.append(t4 - t3)
                f'{(time.perf_counter_ns() - t1) * NS_TO_S:>7.1f} tbi: {oTBI + 1:>4} of {nTBI}  ' + \
                f'partition: {np.average(partitionsTimes) * NS_TO_S:>3.3f} ' + \
                f'assign: {np.average(assignTimes) * NS_TO_S:>3.3f}'>> PP
                partitionsTime += t4 - t2
                oTBI += 1

    # oTBI = 0
    # for p in pRemain:
    #     for w in wRemain:
    #         for r in rRemain:
    #             srow1, srow2 = oTBI * nEachSet, (oTBI + 1) * nEachSet
    #             ocol = 0
    #             remain = []
    #             if p:
    #                 answer[srow1:srow2, ocol] = p
    #                 ocol += 1
    #                 remain = remain >> join >> (pRemain >> without >> p)
    #             if w:
    #                 answer[srow1:srow2, ocol] = w
    #                 ocol += 1
    #                 remain = remain >> join >> (wRemain >> without >> w)
    #             if r:
    #                 answer[srow1:srow2, ocol] = r
    #                 ocol += 1
    #                 remain = remain >> join >> (rRemain >> without >> r)
    #             t2 = time.perf_counter_ns()
    #             res = remain >> allPartitionsInto >> sizes
    #             t3 = time.perf_counter_ns()
    #             answer[srow1:srow2, ocol:] = res
    #             t4 = time.perf_counter_ns()
    #             partitionsTimes.append(t3 - t2)
    #             assignTimes.append(t4 - t3)
    #             f'{(time.perf_counter_ns() - t1) * NS_TO_S:>7.1f} tbi: {oTBI + 1:>4} of {nTBI}  ' + \
    #             f'partition: {np.average(partitionsTimes) * NS_TO_S:>3.3f} ' + \
    #             f'assign: {np.average(assignTimes) * NS_TO_S:>3.3f}'>> PP
    #             partitionsTime += t4 - t2
    #             oTBI += 1
    return answer


@coppertop(style=binary, module=GROOT_NS)
def to(p:tPair, t:pydict) -> pydict:
    return dict(zip(p.a, p.b))

@coppertop(style=binary)
def pair(a, b) -> tPair[dstruct]:
    return dstruct(tPair[dstruct], a=a, b=b)

@coppertop(style=binary)
def bucket(t, n):
    return _bucket(t, t, n)

def _bucket(t, r, n):
    if n == 1:
        return [[r]]
    else:
        answer = []
        for numGive in range(r + 1):
            others = _bucket(t, numGive, n-1)
            for other in others:
                answer.append( [r - numGive] + other)
    return answer



if __name__ == '__main__':

    from dm.examples.cluedo.types import *
    # ps = [Gr, Mu, Or, Pe, Pl, Sc]
    # ws = [Da, Le]
    # rs = []
    # ps1, pk1 = 2, [Gr]
    # ps2, pk2 = 2, [Sc]
    # ps3, pk3 = 2, []
    # x = createPossibilities(ps, ws, rs, [ps1, ps2, ps3], [pk1, pk2, pk3])
    # x >> PP

    # game 6
    people = [Gr, Mu, Or, Pe, Pl, Sc]
    weapons = [Ca, Da, Le, Re, Ro, Wr]
    rooms = [Ba, Bi, Co, Di, Ha, Ki, Li, Lo, St]

    ps0, pk0 = 5, [Li, Di, Co, Wr, Ro]
    ps1, pk1 = 5, []
    ps2, pk2 = 4, []
    ps3, pk3 = 4, []

    t1 = time.perf_counter_ns()
    x = createPossibilities(people, weapons, rooms, [ps0, ps1, ps2, ps3], [pk0, pk1, pk2, pk3])
    # (16, 11351340)
    t2 = time.perf_counter_ns()
    f'total: {(t2-t1)/1_000_000}   partition: {partitionsTime/1_000_000}' >> PP
    x.shape >> PP



