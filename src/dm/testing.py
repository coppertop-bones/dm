# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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


import builtins
from bones import jones
from coppertop.pipe import *
from dm.core.types import dmap, T1, T2, T3, T4, T5, T6, bool, pydict, dstruct, matrix, txt, pytuple
from dm._core.structs import tvarray
from bones.core.errors import NotYetImplemented
from bones.lang.metatypes import fitsWithin as _fitsWithin, cacheAndUpdate

_EPS = 7.105427357601E-15      # i.e. double precision



@coppertop(style=ternary)
def check(actual, fn, expected):
    fnName = fn.name if hasattr(fn, 'name') else (fn.d.name if isinstance(fn, jones._fn) else '')
    with context(showFullType=False):
        # OPEN add isinstance
        if fn is builtins.type or fnName == 'typeOf':
            res = fn(actual)
            if res is not expected:
                msg = f"{_getTestTitle()}\n'{fn.name}' failed the following\nactual:   {fn(actual)}\nexpected: {expected}"
                # assert res == expected, f'Expected type <{expected}> but got type <{fn(actual)}>'
                raise AssertionError(msg)
        else:
            if isinstance(fn, jones._unary):
                raise NotYetImplemented()
            elif isinstance(fn, jones._binary):
                try:
                    if fnName == 'fitsWithin':
                        actual, passed, ppAct, ppExp = _localFitsWithin(actual, expected)
                    else:
                        actual, passed, ppAct, ppExp = fn(actual, expected)
                except Exception as ex:
                    # replicated so can put breakpoint here
                    if fnName == 'fitsWithin':
                        actual, passed, ppAct, ppExp = _localFitsWithin(actual, expected)
                    else:
                        actual, passed, ppAct, ppExp = fn(actual, expected)
                    raise
                if not passed:
                    msg = f"{_getTestTitle()}\n'{fn.name}' failed the following\nactual:   {ppAct}\nexpected: {ppExp}"
                    raise AssertionError(msg)
            elif isinstance(fn, jones._ternary):
                return actual >> _finishCheckWhenTernary(_, fn, expected, _)
    return actual

def _getTestTitle():
    return f'\ntestcase: {context.testcase}' if context.testcase else ''

@coppertop(style=binary)
def _finishCheckWhenTernary(actual, ternary, arg2, expected):
    actual, passed, ppAct, ppExp = actual >> ternary >> arg2 >> expected
    if not passed:
        msg = f"{_getTestTitle()}\n'{ternary.name} >> {arg2.name}' failed the following\nactual:   {ppAct}\nexpected: {ppExp}"
        raise AssertionError(msg)
    return actual

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def raises(fn0, exceptionType) -> pytuple:
    try:
        actual = fn0()
        return actual, False, repr(actual), exceptionType.__name__
    except Exception as ex:
        return ex, isinstance(ex, exceptionType), type(ex).__name__, exceptionType.__name__

def _localFitsWithin(a, b):
    doesFit, tByT, distances = cacheAndUpdate(_fitsWithin(a, b), {})
    return a, doesFit, repr(a), repr(b)

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def doesNotFitWithin(a, b):
    doesFit, tByT, distances = cacheAndUpdate(_fitsWithin(a, b), {})
    return a, not doesFit, repr(a), repr(b)

@coppertop(style=binary)
def closeTo(a, b):
    return closeTo(a, b, _EPS)

@coppertop(style=binary)
def closeTo(a, b, tol):
    if abs(a) < tol:
        return a, abs(b) < tol, repr(a), repr(b)
    else:
        return a, abs(a - b) / abs(a) < tol, repr(a), repr(b)

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def equals(a, b) -> pytuple:
    return a, a == b, repr(a), repr(b)

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def equals(a:matrix&tvarray, b:matrix&tvarray) -> pytuple:
    return a, bool((a == b).all()), repr(a), repr(b)

@coppertop(style=binary)
def different(a, b) -> pytuple:
    return a, a != b, repr(a), repr(b)

@coppertop(style=binary)
def different(a:matrix&tvarray, b:matrix&tvarray) -> pytuple:
    return a, bool((a != b).any()), repr(a), repr(b)

@coppertop(style=ternary)
def same(a, fn1, b):
    actual, expected = fn1(a), fn1(b)
    return actual, actual == expected, repr(actual), repr(expected)

@coppertop(style=binary)
def lenAs(a, b):
    return a, len(a) == len(b), repr(a), repr(b)

@coppertop(style=binary)
def sameShape(a, b):
    return a, a.shape == b.shape, repr(a), repr(b)


# **********************************************************************************************************************
# sameNames
# **********************************************************************************************************************

@coppertop(style=binary)
def sameKeys(a:pydict, b:pydict) -> pytuple:
    return a, a.keys() == b.keys(), repr(a), repr(b)

@coppertop(style=binary)
def sameNames(a:dmap, b:dmap) -> pytuple:
    return a, a._keys() == b._keys(), repr(a), repr(b)

# some adhoc are defined like this (num ** account)[dstruct]["positions"]
@coppertop(style=binary)
def sameNames(a:(T1 ** T2)[dstruct][T3], b:(T4 ** T2)[dstruct][T5]) -> pytuple:
    return a, a._keys() == b._keys(), repr(a), repr(b)


@coppertop(style=binary)
def sameNames(a:(T1 ** T2)[dstruct][T3], b:(T5 ** T4)[dstruct][T6]) -> pytuple:
    assert a._keys() != b._keys()
    return a, False, repr(a), repr(b)

# many structs should be typed (BTStruct)[dstruct] and possibly (BTStruct)[dstruct][T]   e.g. xy in pixels and xy in data

# if we can figure how to divide up the dispatch space (or even indicate it) this would be cool
# the total space below is T1[BTStruct][dstruct] * T2[BTStruct][dstruct] with
# T1[BTStruct][dstruct] * T1[BTStruct][dstruct] as a subspace / set
# can dispatch to the total space and then to the specific subset - with one as default
# @coppertop(style=binary)
# def sameNames(a:T1[BTStruct][dstruct], b:T2[BTStruct][dstruct]) -> bool:
#     assert a._keys() != b._keys()
#     return False
#
# #@coppertop(style=binary, memberOf=(T1[BTStruct][dstruct]) * (T2[BTStruct][dstruct])))
# @coppertop(style=binary)
# def sameNames(a:T1[BTStruct][dstruct], b:T1[BTStruct][dstruct]) -> bool:
#     assert a._keys() == b._keys()
#     return True

# any should really be unhandles or alt or others or not default


