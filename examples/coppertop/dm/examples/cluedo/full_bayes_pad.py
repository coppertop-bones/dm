# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

import numpy as np, time
from coppertop.pipe import *
from bones.core.sentinels import Missing
from coppertop.dm.core.types import pylist, num
from coppertop.dm.examples.cluedo.core import *
from coppertop.dm.examples.cluedo.core import HasOne, NS_TO_S
from coppertop.dm.examples.cluedo.utils import cardIds
from coppertop.dm.core import without, count, collect, inject, minus, sort, zipAll, unpack, nPartitions, join, sum, allPartitionsInto
from coppertop.dm.pp import PP



partitionsTime = None

@coppertop
def indexesOfTruth(a:np.ndarray):
    return np.where(a)[0]

@coppertop(style=binary)
def rowsWithAll(A:np.ndarray, vs:pylist) -> np.ndarray:
    allTruths = None
    for v in vs:
        truths = (A == v).any(axis=1)
        allTruths = (allTruths & truths) if allTruths is not None else truths
    return allTruths

@coppertop(style=binary)
def rowsWithAny(A:np.ndarray, vs:pylist) -> np.ndarray:
    allTruths = None
    for v in vs:
        truths = (A == v).any(axis=1)
        allTruths = (allTruths | truths) if allTruths is not None else truths
    return allTruths

@coppertop(style=binary)
def rowsWithNone(A:np.ndarray, vs:pylist) -> np.ndarray:
    allTruths = None
    for v in vs:
        truths = ~((A == v).any(axis=1))
        allTruths = (allTruths & truths) if allTruths is not None else truths
    return allTruths

@coppertop
def calcPad(l, poss, ps, ws, rs, ss):
    pad = np.zeros((1 + len(ss), len(ps) + len(ws) + len(rs)))
    things = ps + ws + rs
    total = np.sum(l)

    # TBI
    offset1 = len(ps)
    offset2 = len(ps) + len(ws)
    for j, pe in enumerate(ps):
        truths = (poss[:, 0] == pe.value).astype(float)
        truths *= l
        pad[0, j] = np.sum(truths) / total
    for j, we in enumerate(ws):
        truths = (poss[:, 1] == we.value).astype(float)
        truths *= l
        pad[0, j + offset1] = np.sum(truths) / total
    for j, ro in enumerate(rs):
        truths = (poss[:, 2] == ro.value).astype(float)
        truths *= l.astype(float)
        pad[0, j + offset2] = np.sum(truths) / total

    # players
    for i, s in enumerate(ss):
        for j, thing in enumerate(things):
            truths = ((poss[:, s] == thing.value).any(axis=1)).astype(float)
            truths *= l
            pad[i + 1, j] = np.sum(truths) / total

    return pad


@coppertop
def printPad(pad, things, pl):
    width = 7
    titles = ' ' * len(pl[0]) + '   '
    for thing in things:
        titles += repr(thing).ljust(width)
    titles >> PP
    for i, title in enumerate(pl):
        row = title
        for j, what in enumerate(people + weapons + rooms):
            cell = f'{pad[i, j]:>{width}.1%}'
            if pad[i, j] == 0:
                row += '    -  '
            else:
                row += cell
        row >> PP

@coppertop
def PPA(x: np.ndarray):
    with np.printoptions(threshold=np.inf):
        x >> PP

@coppertop
def updateSuggest(sPl, suggest, l, poss, l0, l1, l2, l3):
    truthsPe = poss[:, sPl] >> rowsWithAll >> ([suggest[0]] >> cardIds)
    truthsWe = poss[:, sPl] >> rowsWithAll >> ([suggest[1]] >> cardIds)
    truthsRo = poss[:, sPl] >> rowsWithAll >> ([suggest[2]] >> cardIds)
    truthsPeWe = poss[:, sPl] >> rowsWithAll >> ([suggest[0], suggest[1]] >> cardIds)
    truthsPeRo = poss[:, sPl] >> rowsWithAll >> ([suggest[0], suggest[2]] >> cardIds)
    truthsWeRo = poss[:, sPl] >> rowsWithAll >> ([suggest[1], suggest[2]] >> cardIds)
    truthsPeWeRo = poss[:, sPl] >> rowsWithAll >> (suggest >> cardIds)

    # wasting 3 guesses
    truths = truthsPeWeRo
    n3 = truths >> sum
    l[truths >> indexesOfTruth] *= l3

    # wasting 2 guesses

    truths1 = truthsPeWe & ~truthsRo
    truths2 = truthsPeRo & ~truthsWe
    truths3 = truthsWeRo & ~truthsPe
    truths = truths1 | truths2 | truths3
    n2 = truths >> sum
    l[truths >> indexesOfTruth] *= l2

    # wasting 1 guesses
    truths1 = truthsPe & ~truthsWeRo
    truths2 = truthsWe & ~truthsPeRo
    truths3 = truthsRo & ~truthsPeWe
    truths = truths1 | truths2 | truths3
    n1 = truths >> sum
    l[truths >> indexesOfTruth] *= l1

    # none of the cards
    truths = ~(truthsPe | truthsWe | truthsRo)
    n0 = truths >> sum
    l[truths >> indexesOfTruth] *= l0

    if _.DEBUG: f'0: {n0},  1: {n1},  2: {n2},  3: {n3}' >> PP
    return l

@coppertop
def updateNone(sPl, suggest, l, poss):
    truths = poss[:, sPl] >> rowsWithAny >> (suggest >> cardIds)
    if _.DEBUG: truths >> sum >> PP
    l[truths >> indexesOfTruth] = 0
    return l

@coppertop
def updateOne(sPl, suggest, l, poss, knownCards):
    # check that the one card isn't a known card (which may have been eliminated as a possibility)
    for c in suggest:
        if c in knownCards:
            return l
    truthsAny = poss[:, sPl] >> rowsWithAny >> (suggest >> cardIds)
    truths = ~truthsAny
    if _.DEBUG: truths >> sum >> PP
    l[truths >> indexesOfTruth] = 0
    return l

@coppertop(style=binary)
def updateCard(sPl, c, l, poss, ss):
    totalDropped = 0
    for s in ss >> without >> sPl:
        truths = poss[:, s] >> rowsWithAny >> [c.value]
        totalDropped += truths >> sum
        l[truths >> indexesOfTruth] = 0
    if _.DEBUG: totalDropped >> PP
    return l

@coppertop
def trimPoss(l, poss):
    impossibilities = (l == 0)
    if sum(impossibilities) > 0:
        if _.DEBUG: f'old: {(l >> count)}, {(l >> count) * 16 / 1_000_000:,.1f} MB' >> PP
        l = l[~impossibilities >> indexesOfTruth]
        poss = np.asfortranarray(poss[~impossibilities >> indexesOfTruth,:])
        if _.DEBUG: f'new: {(l >> count)}, {(l >> count) * 16 / 1_000_000:,.1f} MB' >> PP
    else:
        if _.DEBUG: f'unchanged: {(l >> count)}, {(l >> count) * 16 / 1_000_000:,.1f} MB' >> PP
    return l, poss

@coppertop
def processEvents(events: pylist, s0: num, s1: num, s2: num, s3: num):
    # expect events to be a super set of _.events
    for i, (a, b) in enumerate(zip(_.events, events)):
        if a != b: raise Exception(i)
    for ev in events[len(_.events):]:
        if isinstance(ev, int) and type(ev) is not Card:
            t1 = time.perf_counter_ns()
            _.pads[ev] = calcPad(_.l, _.poss, people, weapons, rooms, _.otherPlayers >> collect >> (lambda x: _.ss[x]))
            t2 = time.perf_counter_ns()
            if _.DEBUG: f'calcPad: #{ev}, {(t2 - t1) / 1_000_000:,.1f}ms' >> PP
        elif isinstance(ev, list):
            s = _.ss.get(ev[0], Missing)
            if len(ev) == 4:
                suggest = ev[1:]
                if s:
                    _.l = updateSuggest(s, suggest, _.l, _.poss, s0, s1, s2, s3)
            elif len(ev) == 2:
                if s:
                    _.l = updateCard(s, ev[1], _.l, _.poss, ([TBI] + _.otherPlayers) >> collect >> (lambda x: _.ss[x]))
            else:
                raise Exception('list is wrong length')
        elif ev >> typeOf == HasOne:
            if _.DEBUG: f'update: {ev} has one of {suggest}   (already has {_.knownCards[ev.handId]})' >> PP
            _.l = updateOne(_.ss[ev.handId], suggest, _.l, _.poss, _.knownCards[ev.handId])
        else:
            s = _.ss.get(ev, Missing)
            if s:
                _.l = updateNone(s, suggest, _.l, _.poss)
        _.events.append(ev)
        _.l, _.poss = trimPoss(_.l, _.poss)

@coppertop
def printBayesPad(id):
    (_.pads[id] if id >= 0 else list(_.pads.values())[id]) >> printPad(_, people + weapons + rooms, _.rowTitles)

def createPossibilities(ps, ws, rs, handSizes, handKnowns):
    global partitionsTime
    partitionsTime = 0
    t1 = time.perf_counter_ns()
    mTBI = 0
    hkIds = handKnowns >> collect >> (lambda hand: hand >> collect >> (lambda c: c.value))

    pRemain = ps >> collect >> (lambda c: c.value) >> inject(hkIds, _, _) >> (lambda p, e: p >> minus >> e) >> sort
    pRemain, mTBI = (pRemain, mTBI + 1) if pRemain else ([Missing], mTBI)
    wRemain = ws >> collect >> (lambda c: c.value) >> inject(hkIds, _, _) >> (lambda p, e: p >> minus >> e) >> sort
    wRemain, mTBI = (wRemain, mTBI + 1) if wRemain else ([Missing], mTBI)
    rRemain = rs >> collect >> (lambda c: c.value) >> inject(hkIds, _, _) >> (lambda p, e: p >> minus >> e) >> sort
    rRemain, mTBI = (rRemain, mTBI + 1) if rRemain else ([Missing], mTBI)

    sizes = [handSizes, hkIds] >> zipAll >> collect >> unpack(lambda hs, hk: hs - (hk >> count))
    nzSizes = sizes >> without >> [0]
    nEachSet = nzSizes >> nPartitions
    nTBI = (pRemain >> count) * (wRemain >> count) * (rRemain >> count)
    nCols = mTBI + (nzSizes >> sum)

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
    master[:,:] = 255
    p = pRemain[0]
    w = wRemain[0]
    r = rRemain[0]
    ocol = 0
    remain = []
    if p:
        master[:, ocol] = 90
        ocol += 1
        remain = remain >> join >> (pRemain >> without >> p)
    if w:
        master[:, ocol] = 91
        ocol += 1
        remain = remain >> join >> (wRemain >> without >> w)
    if r:
        master[:, ocol] = 92
        ocol += 1
        remain = remain >> join >> (rRemain >> without >> r)
    TBISize = ocol
    res = list(range(101, 101 + len(remain))) >> allPartitionsInto >> nzSizes
    master[:, ocol:] = res
    if np.any(master == 255): raise Exception()

    slices = [slice(0, TBISize)]
    s1 = TBISize
    for size in sizes:
        s2 = s1 + size
        slices.append(slice(s1, s2))
        s1 = s2

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
                if np.any(res > 21): raise Exception()
                t3 = time.perf_counter_ns()
                answer[srow1:srow2, :] = res
                t4 = time.perf_counter_ns()
                partitionsTimes.append(t3 - t2)
                assignTimes.append(t4 - t3)
                msg = f'{(time.perf_counter_ns() - t1) * NS_TO_S:>7.1f} tbi: {oTBI + 1:>4} of {nTBI}  '
                msg += f'({repr(p)}, {repr(w)}, {repr(r)}) {srow1}:{srow2}  {res.shape}  '
                msg += f'partition: {np.average(partitionsTimes) * NS_TO_S:>3.3f} '
                msg += f'assign: {np.average(assignTimes) * NS_TO_S:>3.3f}'
                msg >> PP
                partitionsTime += t4 - t2
                oTBI += 1

    return answer, slices



if __name__ == '__main__':

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


