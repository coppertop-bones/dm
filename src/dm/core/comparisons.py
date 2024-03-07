# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2024 David Briant. All rights reserved.
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

from coppertop.pipe import *
from dm.core.types import bool, matrix
from dm.core.structs import tvarray
from dm.core.maths import EPS

@coppertop(style=binary)
def closeTo(a, b) -> bool:
    return closeTo(a, b, EPS)

@coppertop(style=binary)
def closeTo(a, b, tol) -> bool:
    if abs(a) < tol:
        return abs(b) < tol
    else:
        return abs(a - b) / abs(a) < tol

@coppertop(style=binary, name='!=')
def different(a, b) -> bool:
    return a != b

@coppertop(style=binary, name='!=')
def different(a:matrix&tvarray, b:matrix&tvarray) -> bool:
    return bool((a != b).any())

@coppertop(style=binary, dispatchEvenIfAllTypes=True)
def doesNotFitWithin(a, b) -> bool:
    return not fitsWithin(a, b)

@coppertop(style=binary, dispatchEvenIfAllTypes=True, name='==')
def equals(a, b) -> bool:
    return a == b

@coppertop(style=binary, dispatchEvenIfAllTypes=True, name="==")
def equals(a:matrix&tvarray, b:matrix&tvarray) -> bool:
    return bool((a == b).all())

@coppertop(style=binary, name='>=')
def ge(a, b) -> bool:
    return a >= b

@coppertop(style=binary, name='>')
def gt(a, b) -> bool:
    return a > b

@coppertop
def isEmpty(x) -> bool:
    return len(x) == 0

@coppertop(style=binary, name='<=')
def le(a, b) -> bool:
    return a <= b

@coppertop(style=binary, name='<')
def lt(a, b) -> bool:
    return a < b