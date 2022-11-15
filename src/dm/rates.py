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

import builtins, polars as pl
from coppertop.pipe import *
from bones.core.errors import NotYetImplemented, ProgrammerError
from bones.core.sentinels import Missing
from dm.core.types import pylist, pytuple, pydict_keys, pydict_values, pyset, txt, t, offset, date, num
from dm.core.datetime import addMonths

import math

ACT365Q = 1
ACT365 = 2
ACT360 = 3
_30360 = 4


@coppertop(style=nullary)
def tau(d1, d2, dct):
    if dct == ACT365Q:
        return (d2 - d1).days / 365.25
    elif dct == ACT365:
        return (d2 - d1).days / 365.0
    elif dct == ACT360:
        return (d2 - d1).days / 360.0
    else:
        raise ProgrammerError()


@coppertop
def df(cc:num, tau:num) -> num:
    return math.exp(-cc * tau)


@coppertop
def cc(df:num, tau:num) -> num:
    return math.log(df) / -tau


class Curve(object):
    def __init__(self):
        self.d1 = []
        self.d2 = []
        self.rates = Missing
        self.cumdf = Missing


@coppertop
def df(curve:Curve, o:offset, d:date) -> num:
    return curve.cumdf[o] * df(curve.rates[o], (d - curve.d1[o]) / 365.25)


@coppertop
def startEnds(todayDate, tenorInMonths, freqInMonths):
    answer = []
    start = todayDate
    for o in range(int(tenorInMonths / freqInMonths)):
        end = todayDate >> addMonths >> (o + 1) * freqInMonths
        answer.append((start, end))
        start = end
    return answer

