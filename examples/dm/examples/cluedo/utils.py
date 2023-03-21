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

from coppertop.pipe import *
from bones.lang.metatypes import BTAtom
from dm.core.types import txt, N, index, pylist, pytuple, T, pydict, dseq, dstruct
from dm.core.aggman import count, collect
from dm.testing import check, equals
from dm.core.maths import max, nCombinations, sum
from dm.core.text import pad
from dm.pp import PP

tPair = BTAtom.ensure('pair')

display_table = (N**txt)[dseq][BTAtom.ensure('table')].setCoercer(dseq)

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
def nHandCombinations(handSizes):
    nCards = handSizes >> sum
    total = 1
    for hs in handSizes:
        total = total * (nCards >> nCombinations >> hs)
        nCards -= hs
    return total

@coppertop(style=binary)
def partitions(xs:pylist+pytuple, sizes:pylist+pytuple) -> N**N**N**T:
    sizes >> sum >> check >> equals >> (xs >> count)
    return _partitions(list(xs), xs >> count, sizes)

def _partitions(xs:N**T, n:index, sizes:N**index) -> N**N**N**T:
    if sizes:
        answer = []
        for comb, rest in _combRest(xs, n, sizes[0]):
            for partitions in _partitions(rest, n - sizes[0], sizes[1:]):
                answer.append([comb] + partitions)
        return answer
    else:
        return [[]]

def _combRest(xs:N**T, n:index, m:index) -> N**( (N**T)*(N**T) ):
    '''answer [m items chosen from n items, the rest]'''
    if m == 0:
        return [([], xs)]
    elif m == n:
        return [(xs, [])]
    else:
        firstPart = [ (xs[0:1] + x, y) for x, y in _combRest(xs[1:], n - 1, m - 1)]
        secondPart = [ (x, xs[0:1] + y) for x, y in _combRest(xs[1:], n - 1, m)]
        return firstPart + secondPart

# %timeit partitions_(range(13), [5,4,4]) >> count >> PP
# 166 ms ± 2.01 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


@coppertop(style=binary, module=GROOT_NS)
def to(p:tPair, t:pydict) -> pydict:
    return dict(zip(p.a, p.b))

@coppertop(style=binary)
def pair(a, b):
    return dstruct(tPair[dstruct], a=a, b=b)
