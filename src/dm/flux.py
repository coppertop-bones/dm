# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
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


from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from dm.core.types import pylist, T1, N, bseq



# **********************************************************************************************************************
# add
# **********************************************************************************************************************

@coppertop(style=binary)
def add(xs:pylist, x) -> pylist:
    return xs + [x]         # this is immutable

@coppertop(style=binary)
def add(xs:(N**T1)[bseq], x:T1) -> (N**T1)[bseq]:
    xs = bseq(xs)
    xs.append(x)
    return xs


# **********************************************************************************************************************
# append
# **********************************************************************************************************************

@coppertop(style=binary)
def append(xs:pylist, x) -> pylist:
    return xs + [x]         # this is immutable


# **********************************************************************************************************************
# appendTo
# **********************************************************************************************************************

@coppertop(style=binary)
def appendTo(x, xs:pylist) -> pylist:
    return xs + [x]         # this is immutable


# **********************************************************************************************************************
# drop
# **********************************************************************************************************************

# @coppertop(style=binary)
# def drop(xs:(T2**T1)[pylist], ks:(T2**T1)[pylist]) -> (T2**T1)[pylist]:
#     answer = []
#     for x in xs:
#         if x not in ks:
#             answer.append(x)
#     return answer


# **********************************************************************************************************************
# prepend
# **********************************************************************************************************************

@coppertop(style=binary)
def prepend(xs:pylist, x) -> pylist:
    return [x] + xs         # this is immutable


# **********************************************************************************************************************
# prependTo
# **********************************************************************************************************************

@coppertop(style=binary)
def prependTo(x, xs:pylist) -> pylist:
    return [x] + xs         # this is immutable


# **********************************************************************************************************************
# postAdd
# **********************************************************************************************************************

@coppertop(style=ternary)
def postAdd(c, i, v):
    raise NotYetImplemented()


# **********************************************************************************************************************
# postAddCol
# **********************************************************************************************************************

@coppertop(style=ternary)
def postAddCol(c, i, v):
    raise NotYetImplemented()


# **********************************************************************************************************************
# postAddRow
# **********************************************************************************************************************

@coppertop(style=ternary)
def postAddRow(c, i, v):
    raise NotYetImplemented()


# **********************************************************************************************************************
# preAdd
# **********************************************************************************************************************

@coppertop(style=ternary)
def preAdd(c, i, v):
    raise NotYetImplemented()


# **********************************************************************************************************************
# preAddCol
# **********************************************************************************************************************

@coppertop(style=ternary)
def preAddCol(c, i, v):
    raise NotYetImplemented()


# **********************************************************************************************************************
# preAddRow
# **********************************************************************************************************************

@coppertop(style=ternary)
def preAddRow(c, i, v):
    raise NotYetImplemented()


