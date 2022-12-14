# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2022 David Briant. All rights reserved.
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

import operator, random
import numpy as np
import scipy.stats

from coppertop.pipe import *
from dm.core.aggman import both, zip, values, keys, merge, select, sort
from dm.core.conv import to
from dm.core.misc import sequence
from dm.core.types import T, T1, T2, pylist, index, pytuple, num, bstruct, matrix, obj
from bones.lang.metatypes import BTAtom
from bones.lang.structs import tvarray



# Ideally PMF should be somewhat typeable in bones. This can't work for numerical pmf but can for categorical pmfs
# and tags. For example:

# numkeys = BTAtom('numkeys')
# structWithNKs = S(T)[bstruct] + (S(T) & numkeys)[bstruct] + numkeys & (num**num)[bmap]
# PMF = structWithNKs['PMF']
# L = structWithNKs['L']

# for the moment we won't add typing

numkeys = BTAtom.ensure('numkeys')
structWithNKs = bstruct & numkeys

PMF = structWithNKs['PMF'].setPP('PMF')
L = structWithNKs['L'].setPP('L')
CMF = structWithNKs['CMF'].setPP('CMF')

def _makePmf(*args, **kwargs):
    answer = bstruct(*args, **kwargs)
    if answer:
        _normaliseInPlaceBstruct(answer)
    return answer | PMF


structWithNKs.setConstructor(bstruct)
PMF.setConstructor(_makePmf)
L.setConstructor(structWithNKs)
CMF.setConstructor(structWithNKs)




@coppertop
def kvs(x: structWithNKs[T]) -> pylist:
    return list(x._kvs())

@coppertop
def values(x: structWithNKs[T]) -> pylist:
    return list(x._values())

@coppertop
def keys(x: structWithNKs[T]) -> pylist:
    return list(x._keys())




@coppertop
def normalise(swnk:structWithNKs) -> PMF:
    dup = bstruct(swnk)
    return _normaliseInPlaceBstruct(dup) | PMF

def _normaliseInPlaceBstruct(swnk):
    # mutable - asssumes non-numeric values are tags and all numeric values are part of swnk
    total = 0
    for k, v in swnk._kvs():
        if isinstance(v, (float, int)):
            total += v
    factor = 1.0 / total
    for k, v in swnk._kvs():
        if isinstance(v, (float, int)):
            swnk[k] = v * factor
    return swnk


@coppertop
def uniform(nOrXs:pylist) -> PMF:
    '''Makes a uniform PMF. xs can be sequence of values or [length]'''
    # if a single int it is a count else there must be many xs
    answer = PMF()
    if len(nOrXs) == 1:
        if isinstance(nOrXs[0], int):
            n = nOrXs[0]
            p = 1.0 / n
            for x in sequence(0, n-1):
                answer[float(x)] = p
            return answer
    p = 1.0 / len(nOrXs)
    for x in nOrXs:
        answer[float(x)] = p
    return answer


@coppertop
def mix(args:pylist) -> PMF:
    """answer a mixture pmf, each arg is (beta, pmf) or pmf"""
    t = {}
    for arg in args:
        beta, pmf = arg if isinstance(arg, (tuple, list)) else (1.0, arg)
        for x, p in pmf._kvs():
            t[x] = t.setdefault(x, 0) + beta * p
    return PMF(t >> sort)


@coppertop
def mean(pmf:PMF) -> num:
    fs = pmf >> keys
    ws = pmf >> values
    try:
        return np.average(fs, weights=ws) >> to >> num
    except TypeError:
        fs, ws = list([fs, ws] >> zip) >> select >> (lambda fv: not isinstance(fv[0], str)) >> zip
        return np.average(fs, weights=ws) >> to >> num
    # if pmf:
    #     answer = 0
    #     for x, p in pmf >> kvs:
    #         answer += x * p
    #     return answer
    # else:
    #     return np.nan


@coppertop
def gaussian_kde(data) -> scipy.stats.kde.gaussian_kde:
    return scipy.stats.gaussian_kde(data)


@coppertop(style=binary)
def to(xs:pylist, t:PMF, kde:scipy.stats.kde.gaussian_kde) -> PMF:
    answer = PMF()
    answer._kde = kde
    for x in xs:
        answer[x] = kde.evaluate(x)[0]
    return _normaliseInPlaceBstruct(answer)

@coppertop
def toCmf(pmf:PMF) -> CMF:
    running = 0.0
    answer = CMF()
    answer2 = dict()
    for k, v in pmf._kvs():
        if isinstance(v, (float, int)):
            running += v
            answer[k] = running
        else:
            answer2[k] = v
    cmf = np.array(list(answer._kvs()))
#    cmf[:, 1] = np.cumsum(cmf[:, 1])
    answer = answer >> merge >> answer2
    answer['_cmf'] = cmf
    return answer

@coppertop(style=binary)
def merge(a:structWithNKs[T1], b:bstruct&T2, tByT) -> structWithNKs[T1]:
    answer = bstruct(tByT[T1], a)
    answer._update(b._kvs())
    return answer

@coppertop(style=binary)
def sample(cmf:CMF, n:index) -> matrix[tvarray]:
    vals = []
    sortedCmf = cmf['_cmf']
    for _ in range(n):
        p = random.random()
        i = np.searchsorted(sortedCmf[:, 1], p, side='left')
        vals.append(sortedCmf[i, 0])
    return matrix[tvarray](vals)

@coppertop(style=binary)
def sample(kde:scipy.stats.kde.gaussian_kde, n:index) -> matrix[tvarray]:
    return kde.resample(n).flatten()

@coppertop(style=binary)
def pmfMul(lhs:structWithNKs[T1], rhs:structWithNKs[T2]) -> structWithNKs:
    # lhs kvs both {(x.k, x.v*(y.v)} (rhs kvs) normalise <:pmf>
    return structWithNKs(
        lhs >> both >> (lambda kLhs, vLhs, kRhs, vRhs: (kLhs, vLhs * vRhs)) >> rhs
    )

@coppertop(style=binary)
def rvAdd(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.add)

@coppertop(style=binary)
def rvSub(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.sub)

@coppertop(style=binary)
def rvMul(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.mul)

@coppertop(style=binary)
def rvDiv(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.truediv)

@coppertop(style=binary)
def rvMax(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, max)

def _rvOp(lhs, rhs, op):
    xps = {}
    for x1, p1 in lhs._kvs():
        for x2, p2 in rhs._kvs():
            x = op(x1, x2)
            xps[x] = xps.setdefault(x, 0.0) + p1 * p2
    return PMF(
        sorted(
            xps.items(),
            key=lambda xp: xp[0]
        )
    )


@coppertop
def toXsPs(pmf:PMF) -> pytuple:
    return tuple(zip(pmf._kvs()))

@coppertop(style=unary)
def percentile(pmf:PMF, percentage:num):
    total = 0
    for k, v in pmf._kvs():
        total += v
        if total >= percentage:
            return k

@coppertop(style=unary)
def percentile(cmf:CMF, percentage:num):
    for k, v in cmf._kvs():
        if v >= percentage:
            return k


@coppertop
def toSteps(s:PMF+bstruct) -> pytuple:
    return _asSteps(s >> keys, s >> values)

@coppertop
def toSteps(s:PMF+bstruct, kwargs) -> pytuple:
    return _asSteps(s >> keys, s >> values, **kwargs)

def _asSteps(xs:pylist, ys:pylist, align='center', width=None):
    #xMin, xMax = min(xs), max(xs)
    if width is None:
        width = np.diff(xs).min()
    points = []
    lastx = np.nan
    lasty = np.nan
    for x, y in [xs, ys] >> zip:
        if (x - lastx) > 1e-5:
            points.append((lastx, 0))
            points.append((x, 0))
        if not np.isnan(lasty):
            points.append((x, lasty))
        points.append((x, y))
        points.append((x + width, y))
        lastx = x + width
        lasty = y
    points.append((lastx, lasty))
    pxs, pys = points >> zip
    if align == 'center':
        pxs = np.array(pxs) - width / 2.0
    elif align == 'right':
        pxs = np.array(pxs) - width
    return pxs, np.array(pys)
