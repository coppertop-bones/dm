# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
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


import builtins, numpy as np

from coppertop.pipe import *
from bones.core.sentinels import Missing, dict_keys, dict_values, dict_items, function
from bones.core.errors import NotYetImplemented
from bones.lang.metatypes import cacheAndUpdate, fitsWithin as _fitsWithin, BTAtom as _BTAtom
from dm.core.aggman import inject
from bones.lang.structs import tv
from dm.core.types import T, pylist, txt, pydict


_SBT = _BTAtom.define('ShouldBeTyped')      # temporary type to allow"  'DE000762534' >> box | tISIN - i.e. make the box then type it

@coppertop
def box(v) -> _SBT:
    return tv(_SBT, v)

@coppertop
def box(v, t:T) -> T:
    return tv(t, v)

@coppertop
def getAttr(x, name):
    return getattr(x, name)

@coppertop
def compose(x, fs):
    return fs >> inject(_, x, _) >> (lambda x, f: f(x))

def not_(b):
    return False if b else True
Not = coppertop(name='Not')(not_)
not_ = coppertop(name='not_')(not_)

repr = coppertop(name='repr', dispatchEvenIfAllTypes=True)(builtins.repr)

@coppertop
def _t(x):
    return x._t

@coppertop
def _v(x):
    return x._v

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def fitsWithin(a, b):
    doesFit, dummy, distances = cacheAndUpdate(_fitsWithin(a, b), {})
    return doesFit

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def doesNotFitWithin(a, b):
    does = a >> fitsWithin >> b
    return does >> not_

@coppertop(style=nullary)
def sequence(p1, p2):
    first , last = p1, p2
    return list(range(first, last+1, 1))

@coppertop(style=nullary)
def sequence(p1, p2, n, sigmas):
    mu, sigma = p1, p2
    low = mu - sigmas * sigma
    high = mu + sigmas * sigma
    return sequence(low, high, n=n)

@coppertop(style=nullary)
def sequence(p1, p2, n):
    first , last = p1, p2
    return list(np.linspace(first, last, n))

@coppertop(style=nullary)
def sequenceStep(p1, p2, step):
    first , last = p1, p2
    return list(np.arange(first, last + step, step))

@coppertop
def gather(x:function):
    return x()

@coppertop
def gather(x:dict_keys) -> pylist:
    return list(x)

@coppertop
def gather(x:dict_values) -> pylist:
    return list(x)

@coppertop
def gather(x:dict_items) -> pylist:
    return list(x)

@coppertop
def pyeval_(src:txt):
    return lambda : eval(src)

@coppertop
def pyeval_(src:txt, ctx:pydict):
    return lambda : eval(src, ctx)
