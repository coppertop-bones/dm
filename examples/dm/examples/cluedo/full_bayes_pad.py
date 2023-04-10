# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2023 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************

import numpy as np
from coppertop.pipe import *
from dm.core.types import pylist
from dm.examples.cluedo.types import people, weapons, rooms
from dm.examples.cluedo.utils import cardIds, sum
import dm.pp
from groot import PP, without, count

BONES_NS = GROOT_NS


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

    f'0: {n0},  1: {n1},  2: {n2},  3: {n3}' >> PP
    return l

@coppertop
def updateNone(sPl, suggest, l, poss):
    truths = poss[:, sPl] >> rowsWithAny >> (suggest >> cardIds)
    truths >> sum >> PP
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
    truths >> sum >> PP
    l[truths >> indexesOfTruth] = 0
    return l

@coppertop(style=binary)
def updateCard(sPl, c, l, poss, ss):
    totalDropped = 0
    for s in ss >> without >> sPl:
        truths = poss[:, s] >> rowsWithAny >> [c.value]
        totalDropped += truths >> sum
        l[truths >> indexesOfTruth] = 0
    totalDropped >> PP
    return l

@coppertop
def trimPoss(l, poss):
    impossibilities = (l == 0)
    if sum(impossibilities) > 0:
        f'old: {(l >> count)}, {(l >> count) * 16 / 1_000_000:,.1f} MB' >> PP
        l = l[~impossibilities >> indexesOfTruth]
        poss = np.asfortranarray(poss[~impossibilities >> indexesOfTruth,:])
        f'new: {(l >> count)}, {(l >> count) * 16 / 1_000_000:,.1f} MB' >> PP
    else:
        f'unchanged: {(l >> count)}, {(l >> count) * 16 / 1_000_000:,.1f} MB' >> PP
    return l, poss
