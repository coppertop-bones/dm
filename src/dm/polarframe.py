# **********************************************************************************************************************
#
#                             Copyright (c) 2022 David Briant. All rights reserved.
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

import builtins, polars as pl, numpy as np
from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from dm.core.types import pylist, pytuple, pydict_keys, pydict_values, pyset, txt, t, offset, matrix
from dm._core.structs import tvarray



# **********************************************************************************************************************
# aj
# **********************************************************************************************************************

@coppertop(style=binary)
def aj(f1:pl.DataFrame, f2:pl.DataFrame, k:txt, direction:txt):
    return f1.join_asof(f2, on=k, strategy='backward' if direction == 'prior' else 'forward')

@coppertop(style=binary)
def aj(f1:pl.DataFrame, f2:pl.DataFrame, k1:txt, k2:txt, direction:txt):
    return f1.join_asof(f2, left_on=k1, right_on=k2, strategy='backward' if direction == 'prior' else 'forward')


# **********************************************************************************************************************
# asc
# **********************************************************************************************************************

@coppertop(style=unary)
def asc(f:pl.DataFrame) -> pl.DataFrame:
    return f.sort(by=f >> keys >> at >> 0)


# **********************************************************************************************************************
# at
# **********************************************************************************************************************

@coppertop(style = binary)
def at(df:pl.DataFrame, k:txt):
    return df.get_column(k)

@coppertop(style = binary)
def at(df:pl.DataFrame, o:offset):
    return df.row(o)


# **********************************************************************************************************************
# drop
# **********************************************************************************************************************

@coppertop(style=binary)
def drop(f: pl.DataFrame, n: t.count) -> pl.DataFrame:
    if n >= 0:
        return f[n:]
    else:
        return f[:n]

@coppertop(style=binary)
def drop(f: pl.DataFrame, k:txt) -> pl.DataFrame:
    return f.drop(k)

@coppertop(style=binary)
def drop(f: pl.DataFrame, k:txt) -> pl.DataFrame:
    return f.drop(k)

@coppertop(style=binary)
def drop(f: pl.DataFrame, ks:pylist) -> pl.DataFrame:
    return f.drop(ks)


# **********************************************************************************************************************
# first
# **********************************************************************************************************************

@coppertop
def first(f: pl.Series):
    return f[0]

@coppertop
def first(f: pl.DataFrame) -> pl.DataFrame:
    return f[:1]


# **********************************************************************************************************************
# firstLast
# **********************************************************************************************************************

@coppertop
def firstLast(f: pl.DataFrame) -> pl.DataFrame:
    return f[[1, -1]]


# **********************************************************************************************************************
# kays
# **********************************************************************************************************************

@coppertop
def keys(df:pl.DataFrame) -> pylist:
    return df.columns


# **********************************************************************************************************************
# last
# **********************************************************************************************************************

@coppertop
def last(f: pl.DataFrame) -> pl.DataFrame:
    return f[-1:]

@coppertop
def last(f: pl.Series):
    return f[-1]


# **********************************************************************************************************************
# lj
# **********************************************************************************************************************

@coppertop(style=binary)
def lj(f1:pl.DataFrame, f2:pl.DataFrame, k:txt):
    return f1.join(f2, on=k, how='left')

@coppertop(style=binary)
def lj(f1:pl.DataFrame, f2:pl.DataFrame, k1:txt, k2:txt):
    return f1.join(f2, left_on=k1, right_on=k2, how='left')


# **********************************************************************************************************************
# numCols
# **********************************************************************************************************************

@coppertop
def numCols(df:pl.DataFrame) -> t.count:
    return len(df.columns) | t.count


# **********************************************************************************************************************
# numRows
# **********************************************************************************************************************

@coppertop
def numRows(df:pl.DataFrame) -> t.count:
    return len(df) | t.count


# **********************************************************************************************************************
# read
# **********************************************************************************************************************

@coppertop(module='dm.polars.csv')
def read(path:txt) -> pl.DataFrame:
    return pl.read_csv(path, parse_dates=True)


# **********************************************************************************************************************
# rename
# **********************************************************************************************************************

@coppertop(style=ternary)
def rename(f:pl.DataFrame, old:pylist+pytuple+pydict_keys+pydict_values, new:pylist+pytuple+pydict_keys+pydict_values) -> pl.DataFrame:
    oldNew = dict(builtins.zip(old, new))
    return f.rename(oldNew)

@coppertop(style=ternary)
def rename(f:pl.DataFrame, old:txt, new:txt) -> pl.DataFrame:
    oldNew = {old:new}
    return f.rename(oldNew)


# **********************************************************************************************************************
# select
# **********************************************************************************************************************

@coppertop(style=binary)
def select(f:pl.DataFrame, pred:pl.Expr) -> pl.DataFrame:
    return f.filter(pred)


# **********************************************************************************************************************
# shape
# **********************************************************************************************************************

@coppertop
def shape(df:pl.DataFrame) -> pytuple:
    return df.shape #(len(df) | t.count, len(df.columns) | t.count)


# **********************************************************************************************************************
# take
# **********************************************************************************************************************

@coppertop(style=binary)
def take(f: pl.DataFrame, n: t.count) -> pl.DataFrame:
    if n >= 0:
        return f[:n]
    else:
        return f[n:]

@coppertop(style=binary)
def take(f: pl.DataFrame, ks: pylist+pyset) -> pl.DataFrame:
    return f.select(ks)

@coppertop(style=binary)
def take(f: pl.DataFrame, k: txt) -> pl.DataFrame:
    return f.select(k)


# **********************************************************************************************************************
# takePanel
# **********************************************************************************************************************

@coppertop
def takePanel(f: pl.DataFrame) -> matrix&tvarray:
    return (matrix&tvarray)(f.to_numpy())


# **********************************************************************************************************************
# xasc
# **********************************************************************************************************************

@coppertop(style=binary)
def xasc(f:pl.DataFrame, ks:pylist+pytuple) -> pl.DataFrame:
    return f.sort(by=ks)

@coppertop(style=binary)
def xasc(f:pl.DataFrame, k:txt) -> pl.DataFrame:
    return f.sort(by=k)

