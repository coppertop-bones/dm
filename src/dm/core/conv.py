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


import numpy as np, datetime, builtins
from _strptime import _strptime

from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from bones.lang.metatypes import BType
from dm.core.datetime import toCTimeFormat
from dm.core.types import dframe, dmap, txt, pylist, pydict, T1, N, pytuple, pydict_keys, pydict_values, date, index, \
    num, npfloat, dtup, dseq, matrix, t, darray


array_ = (N**num)&darray
matrix_ = matrix&darray

_defaultDateFmt = toCTimeFormat('YYYY.MM.DD')


# **********************************************************************************************************************
# to
# **********************************************************************************************************************

@coppertop(style=binary)
def to(x:pydict+pylist, t:dmap) -> dmap:
    return t(x)

@coppertop(style=binary)
def to(x, t):
    if isinstance(t, BType):
        return t(x)
    try:
        return t(x)
    except Exception as ex:
        raise TypeError(f'Catch all can\'t convert {repr(x)} to {repr(t)} - {ex}')

@coppertop(style=binary)
def to(x:pydict_keys+pydict_values, t:pylist) -> pylist:
    return list(x)

@coppertop(style=binary)
def to(x, t:pylist) -> pylist:
    return list(x)

@coppertop(style=binary)
def to(x:dmap, t:pydict) -> pydict:
    return dict(x.items())

@coppertop(style=binary)
def to(x, t:pydict) -> pydict:
    return dict(x)



@coppertop(style=binary)
def to(x:txt, t:date, f:txt) -> date:
    return parseDate(x, toCTimeFormat(f))

@coppertop(style=binary)
def to(x:txt, t:date) -> date:
    return parseDate(x, _defaultDateFmt)

@coppertop(style=binary)
def to(x:date, t:txt) -> txt:
    return x.strftime(_defaultDateFmt)

@coppertop(style=binary)
def to(d:date, t_:t.count) -> t.count:
    return d.toordinal() | t.count

@coppertop(style=binary)
def to(greg:t.count+index, t:date) -> date:
    return datetime.date.fromordinal(greg)



@coppertop(style=binary)
def to(x, t:txt) -> txt:
    return str(x)

@coppertop(style=binary)
def to(v:T1, t:T1) -> T1:
    return v

@coppertop(style=binary)
def to(x, t:index) -> index:
    return int(x)

@coppertop(style=binary)
def to(x, t:num) -> num:
    return float(x)

@coppertop(style=binary)
# def to(x:pylist, t:matrix&darray) -> matrix&darray:
def to(x:pylist, t:matrix&darray) -> matrix&darray:
    return (matrix&darray)(t, x)

@coppertop(style=binary)
def to(x:matrix&darray, t:array_) -> array_:
    return array_(x.reshape(max(x.shape)))

@coppertop(style=binary)
def to(x:pylist, t:np.ndarray) -> np.ndarray:
    return np.array(x)

@coppertop(style=binary)
def to(x:array_, t:np.ndarray) -> np.ndarray:
    return np.array(x)

def parseNum(x:txt) -> num:
    try:
        return float(x)
    except:
        return np.nan

@coppertop
def parseDate(x:txt, cFormat:txt) -> date:
    # rework to be more efficient in bulk by parsing format separately from x or handle x as an array / range
    dt, micro, _ = _strptime(x, cFormat)
    return datetime.date(dt[0], dt[1], dt[2])

@coppertop(style=binary)
def to(xs:pylist, t:array_) -> array_:
    return array_([parseNum(x) for x in xs])

@coppertop(style=binary)
def to(xs:pylist, t:(N**date)&darray, f:txt) -> (N**date)&darray:
    cFormat = toCTimeFormat(f)
    return darray((N**date)&darray, [parseDate(x, cFormat) for x in xs])

@coppertop
def toRow(xs:pylist) -> matrix&darray:
    if len(xs) == 0: raise ValueError("can't create an empty matrix")
    if isinstance(xs[0], str):
        raise NotYetImplemented()
    raise NotYetImplemented()
    cFormat = toCTimeFormat(f)
    return darray((N**date)&darray, [parseDate(x, cFormat) for x in xs])

@coppertop
def toCol(xs:pylist) -> matrix&darray:
    if len(xs) == 0: raise ValueError("can't create an empty matrix")
    if isinstance(xs[0], str):
        return darray(matrix&darray, [parseNum(x) for x in xs]).reshape(len(xs), 1)
    return darray(matrix&darray, xs).reshape(len(xs), 1)

@coppertop(style = binary)
def withKeys(vs, ks) -> pydict:
    return dict(builtins.zip(ks, vs))

@coppertop(style = binary)
def withValues(ks, vs) -> pydict:
    return dict(builtins.zip(ks, vs))
