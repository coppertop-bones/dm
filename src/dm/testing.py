# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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


from bones import jones
from coppertop.pipe import *
from dm.core.types import bool, matrix, pytuple
from dm._core.structs import tvarray
from dm.core.maths import EPS
from bones.core.errors import NotYetImplemented
from bones.core.sentinels import function


# OPEN: allow nullary >> unary etc

@coppertop(style=ternary)
def check(actual, fn, expected):
    fnName = fn.name if hasattr(fn, 'name') else (fn.d.name if isinstance(fn, jones._fn) else fn.__name__)
    with context(showFullType=False):
        isPartial = isinstance(fn, jones._pfn)
        isPyFuncWithSoleArg = False
        expectedIsFn = isinstance(expected, (function, jones._fn, jones._pfn))
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
def startsWith(a, b) -> bool:
    return a.startswith(b)

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def endsWith(a, b) -> bool:
    return a.endswith(b)

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def equals(a, b) -> bool:
    return a == b

@coppertop(style=binary)
def gt(a, b) -> bool:
    return a > b

@coppertop(style=binary)
def ge(a, b) -> bool:
    return a >= b

@coppertop(style=binary)
def lt(a, b) -> bool:
    return a < b

@coppertop(style=binary)
def le(a, b) -> bool:
    return a <= b

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def equals(a:matrix&tvarray, b:matrix&tvarray) -> bool:
    return bool((a == b).all())

@coppertop(style=binary)
def different(a, b) -> bool:
    return a != b

@coppertop(style=binary)
def different(a:matrix&tvarray, b:matrix&tvarray) -> bool:
    return bool((a != b).any())


