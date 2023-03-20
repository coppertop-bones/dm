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


from bones import jones
from coppertop.pipe import *
from dm.core.types import bool, matrix, pytuple
from dm._core.structs import tvarray
from dm.core.maths import EPS
from bones.core.errors import NotYetImplemented
from bones.core.sentinels import function


# OPEN: allow nullary >> unary etc

_PARTIAL_FN_CLASS = (jones._pnullary, jones._punary, jones._pbinary, jones._pternary)
_ANY_FUNCTION_CLASS = (function, jones._fn)

@coppertop(style=ternary)
def check(actual, fn, expected):
    fnName = fn.name if hasattr(fn, 'name') else (fn.d.name if isinstance(fn, jones._fn) else fn.__name__)
    with context(showFullType=False):
        isPartial = isinstance(fn, _PARTIAL_FN_CLASS)
        isPyFuncWithSoleArg = False
        expectedIsFn = isinstance(expected, _ANY_FUNCTION_CLASS)
        # could check that the partial isn't piping
        if (fnName in ('type', 'typeOf')) or (isPartial and fn.o_tbc == 1 and not expectedIsFn) or isPyFuncWithSoleArg:
            # fn is an F1
            res = fn(actual)
            passed, ppAct, ppExp = res == expected, repr(res), repr(expected)
        elif not isPartial and isinstance(fn, jones._ternary):
            # needs 3 arguments - pipe in the first 2 and the third will be piped later
            return actual >> _finishCheckWhenTernary(_, fn, expected, _)
        else:
            if expectedIsFn:
                # assume fn is an F1, and expected is an F2
                # e.g. res >> check >> errorMsg >> startsWith >> 'cannot constrain {littxt} <:'
                return actual >> _finishCheckWhenF2(_, fn(actual), expected, _)
            else:
                if fn in (raises, ):
                    actual, passed, ppAct, ppExp = fn(actual, expected)
                else:
                    passed, ppAct, ppExp = fn(actual, expected), repr(actual), repr(expected)
        if not passed:
            msg = f"{_getTestTitle()}\n'{fnName}' failed the following\nactual:   {ppAct}\nexpected: {ppExp}"
            raise AssertionError(msg)
    return actual

def _getTestTitle():
    return f'\ntestcase: {context.testcase}' if context.testcase else ''

@coppertop(style=binary)
def _finishCheckWhenF2(rootActual, actual, f2, expected):
    passed, ppAct, ppExp = f2(actual, expected), repr(actual), repr(expected)
    if not passed:
        f2Name = f2.name if hasattr(f2, 'name') else (f2.d.name if isinstance(f2, jones._fn) else f2.__name__)
        msg = f"{_getTestTitle()}\n'{f2Name}' failed the following\nactual:   {ppAct}\nexpected: {ppExp}"
        raise AssertionError(msg)
    return rootActual

@coppertop(style=binary)
def _finishCheckWhenTernary(actual, ternary, arg2, expected):
    actual, passed, ppAct, ppExp = actual >> ternary >> arg2 >> expected
    if not passed:
        msg = f"{_getTestTitle()}\n'{ternary.name} >> {arg2.name}' failed the following\nactual:   {ppAct}\nexpected: {ppExp}"
        raise AssertionError(msg)
    return actual


# **********************************************************************************************************************
# raises known by check and required to return a tuple (act, pass, PP1, PP2)
# **********************************************************************************************************************

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def raises(fn0, exceptionType) -> pytuple:
    try:
        actual = fn0()
        return actual, False, repr(actual), exceptionType.__name__
    except Exception as ex:
        return ex, isinstance(ex, exceptionType), type(ex).__name__, exceptionType.__name__


# **********************************************************************************************************************
# same is a ternary which is required by check to return a tuple (act, pass, PP1, PP2)
# **********************************************************************************************************************

@coppertop(style=ternary)
def same(a, fn1, b) -> pytuple:
    actual, expected = fn1(a), fn1(b)
    return actual, actual == expected, repr(actual), repr(expected)


# **********************************************************************************************************************
# some binary comparison fns
# **********************************************************************************************************************

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def doesNotFitWithin(a, b) -> bool:
    return not fitsWithin(a, b)

@coppertop(style=binary)
def closeTo(a, b) -> bool:
    return closeTo(a, b, EPS)

@coppertop(style=binary)
def closeTo(a, b, tol) -> bool:
    if abs(a) < tol:
        return abs(b) < tol
    else:
        return abs(a - b) / abs(a) < tol

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def equals(a, b) -> bool:
    return a == b

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def equals(a:matrix&tvarray, b:matrix&tvarray) -> bool:
    return bool((a == b).all())

@coppertop(style=binary)
def different(a, b) -> bool:
    return a != b

@coppertop(style=binary)
def different(a:matrix&tvarray, b:matrix&tvarray) -> bool:
    return bool((a != b).any())

