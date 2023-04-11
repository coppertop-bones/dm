# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import csv, numpy as np, collections

from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from bones.core.sentinels import Missing, function
from dm.core.types import dframe, txt, pydict, dtup, t, N, num, pylist, pytuple, pydict_keys, pydict_values, matrix, \
    offset, pyfunc
from dm._core.structs import tvarray
from dm.core.aggman import count

MODULE_NS = GROOT


# sql style
# f >> by_(...) >> collect_(...) >> where(...) >> orderBy(...)   - sortBy, xasc, keyBy

ByRow = collections.namedtuple('ByRow', ['x'])
FrameGroups = collections.namedtuple('FrameGroups', ['x'])

DefBy = collections.namedtuple('DefBy', ['x'])
DefCollect = collections.namedtuple('DefCollect', ['x'])
DefWhere = collections.namedtuple('DefWhere', ['x'])

DefCount = collections.namedtuple('DefCount', ['col_name'])
DefFirst = collections.namedtuple('DefFirst', ['col_name'])
DefLast = collections.namedtuple('DefLast', ['col_name'])
DefMean = collections.namedtuple('DefMean', ['col_name'])
DefRange = collections.namedtuple('DefRange', ['col_name'])
DefTotal = collections.namedtuple('DefTotal', ['col_name'])



# **********************************************************************************************************************
# aj
# **********************************************************************************************************************

@coppertop(style=binary)
def aj(f1:dframe, f2:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# at
# **********************************************************************************************************************

@coppertop(style=binary)
def at(f:dframe, k:txt) -> dframe:
    return f[k]

@coppertop(style=binary)
def at(f:dframe, o:offset) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# by
# **********************************************************************************************************************

@coppertop(style=binary)
def by(a:dframe, keys) -> FrameGroups:
    raise NotYetImplemented()


# **********************************************************************************************************************
# by_
# **********************************************************************************************************************

@coppertop(style=binary)
def by_(a:dframe, keys) -> DefBy:
    raise NotYetImplemented()


# **********************************************************************************************************************
# byRow
# **********************************************************************************************************************

@coppertop
def byRow(f:function) -> ByRow:
    raise NotYetImplemented()


# **********************************************************************************************************************
# collect
# **********************************************************************************************************************

@coppertop(style=binary)
def collect(a:dframe, collectors:pylist+pytuple) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# collect_
# **********************************************************************************************************************

@coppertop(style=binary)
def collect_(a:dframe, definitions) -> DefCollect:
    raise NotYetImplemented()


# **********************************************************************************************************************
# count_
# **********************************************************************************************************************

@coppertop
def count_(colName:txt) -> DefCount:
    raise NotYetImplemented()


# **********************************************************************************************************************
# drop
# **********************************************************************************************************************

@coppertop(style=binary)
def drop(f: dframe, n: t.count) -> dframe:
    raise NotYetImplemented()

@coppertop(style=binary)
def drop(f: dframe, k:txt) -> dframe:
    raise NotYetImplemented()

@coppertop(style=binary)
def drop(f: dframe, k:txt) -> dframe:
    raise NotYetImplemented()

@coppertop(style=binary)
def drop(f: dframe, ks:pylist) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# first
# **********************************************************************************************************************

@coppertop
def first(a:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# first_
# **********************************************************************************************************************

@coppertop
def first_(colName:txt) -> DefFirst:
    raise NotYetImplemented()


# **********************************************************************************************************************
# firstCol
# **********************************************************************************************************************

@coppertop
def firstCol(a:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# firstLast
# **********************************************************************************************************************

@coppertop
def firstLast(f:dframe) -> dframe:
    return dframe({k:f[k][[0,-1]] for k in f._keys()})

@coppertop
def firstLast(f:dframe, n:t.count) -> dframe:
    return dframe({k:(N**num)[tvarray](np.append(f[k][:n], f[k][-n:])) for k in f._keys()})


# **********************************************************************************************************************
# gather
# **********************************************************************************************************************

@coppertop
def gather(f:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# hj
# **********************************************************************************************************************

@coppertop(style=binary)
def hj(f1:dframe, f2:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# ij
# **********************************************************************************************************************

@coppertop(style=binary)
def ij(f1:dframe, f2:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# keyBy
# **********************************************************************************************************************

@coppertop(style=binary)
def keyBy(f:dframe, cols:pylist) -> pylist:
    raise NotYetImplemented()


# **********************************************************************************************************************
# keys
# **********************************************************************************************************************

@coppertop
def keys(f:dframe) -> pydict_keys:
    return f._keys()


# **********************************************************************************************************************
# last
# **********************************************************************************************************************

@coppertop
def last(a:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# last_
# **********************************************************************************************************************

@coppertop
def last_(colName:txt) -> DefLast:
    raise NotYetImplemented()


# **********************************************************************************************************************
# lastCol
# **********************************************************************************************************************

@coppertop
def lastCol(a:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# lj
# **********************************************************************************************************************

@coppertop(style=binary)
def lj(f1:dframe, f2:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# mean_
# **********************************************************************************************************************

@coppertop
def mean_(colName:txt) -> DefMean:
    raise NotYetImplemented()


# **********************************************************************************************************************
# numCols
# **********************************************************************************************************************

@coppertop
def numCols(f:dframe) -> t.count:
    raise NotYetImplemented()


# **********************************************************************************************************************
# numRows
# **********************************************************************************************************************

@coppertop
def numRows(f:dframe) -> t.count:
    raise NotYetImplemented()


# **********************************************************************************************************************
# pivot
# **********************************************************************************************************************

@coppertop
def pivot(f:dframe, index:txt+pylist, value:txt+pylist, agg:pyfunc+pylist, titles:txt+pylist) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# range_
# **********************************************************************************************************************

@coppertop
def range_(colName:txt) -> DefRange:
    raise NotYetImplemented()


# **********************************************************************************************************************
# read in dm.frame.fromCsv
# **********************************************************************************************************************

@coppertop(module='dm.frame.csv')
def read(pfn:txt, renames:pydict, conversions:pydict) -> dframe:
    with open(pfn, mode='r') as f:
        r = csv.DictReader(f)
        d = {}
        for name in r.fieldnames:
            d[name] = list()
        for cells in r:
            for k, v in cells.items():
                d[k].append(v)
        a = dframe()
        for k in d.keys():
            newk = renames.get(k, k)
            fn = conversions.get(newk, lambda l: dtup(l, Missing))     ## we could insist the conversions return dtup s
            a[newk] = fn(d[k])
    return a

@coppertop(module='dm.frame.csv')
def read(pfn:txt, renames:pydict, conversions:pydict, cachePath) -> dframe:
    with open(pfn, mode='r') as f:
        r = csv.DictReader(f)
        d = {}
        for name in r.fieldnames:
            d[name] = list()
        for cells in r:
            for k, v in cells.items():
                d[k].append(v)
        a = dframe()
        for k in d.keys():
            newk = renames.get(k, k)
            fn = conversions.get(newk, lambda l: dtup(l, Missing))     ## we could insist the conversions return dtup s
            a[newk] = fn(d[k])
    return a


# **********************************************************************************************************************
# rename
# **********************************************************************************************************************

@coppertop(style=ternary)
def rename(f:dframe, old:pylist+pytuple+pydict_keys+pydict_values, new:pylist+pytuple+pydict_keys+pydict_values) -> dframe:
    raise NotYetImplemented()

@coppertop(style=ternary)
def rename(f:dframe, old:txt, new:txt) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# reorder
# **********************************************************************************************************************

@coppertop(style=ternary)
def reorder(f:dframe, old:pylist+pytuple+pydict_keys+pydict_values, new:pylist+pytuple+pydict_keys+pydict_values) -> dframe:
    raise NotYetImplemented()

@coppertop(style=ternary)
def reorder(f:dframe, old:txt, new:txt) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# shape
# **********************************************************************************************************************

@coppertop
def shape(f:dframe) -> pytuple:
    ks = f >> keys
    return (f[ks >> first] >> count, ks >> count)


# **********************************************************************************************************************
# sortBy
# **********************************************************************************************************************

@coppertop
def sortBy(f:dframe, fields) -> dframe:
    raise NotYetImplemented()

@coppertop
def sortBy(f:dframe, fields, directions) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# take
# **********************************************************************************************************************

@coppertop(style=binary)
def take(f:dframe, fields) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# takePanel
# **********************************************************************************************************************

@coppertop
def takePanel(f: dframe) -> matrix&tvarray:
    raise NotYetImplemented()


# **********************************************************************************************************************
# total_
# **********************************************************************************************************************

@coppertop
def total_(colName:txt) -> DefTotal:
    raise NotYetImplemented()


# **********************************************************************************************************************
# uj
# **********************************************************************************************************************

@coppertop(style=binary)
def uj(f1:dframe, f2:dframe) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# where
# **********************************************************************************************************************

@coppertop(style=binary)
def where(f:dframe, includers) -> dframe:
    raise NotYetImplemented()


# **********************************************************************************************************************
# where_
# **********************************************************************************************************************

@coppertop(style=binary)
def where_(f:dframe, includers) -> DefWhere:
    raise NotYetImplemented()


