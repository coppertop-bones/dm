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

# functions the dm.core is providing for bones to use


import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from dm.core.types import bool

# @coppertop(bname='ifFalse:')
# def _ifFalse(res, block) -> bool:
#     if not res: block()

# @coppertop(bname='ifTrue:')
# def _ifTrue(res, block) -> bool:
#     if res: block()

# @coppertop(bname='ifTrue:')
# def _ifTrueifFalse(res, trueBlock, falseBlock) -> bool:
#     if res: trueBlock()
#     else: falseBlock()

@coppertop(style=binary, bname='!=')
def different(a, b) -> bool:
    return a != b

@coppertop(style=binary, bname='!=')
def different(a:matrix&darray, b:matrix&darray) -> bool:
    return bool((a != b).any())

@coppertop(style=binary, dispatchEvenIfAllTypes=True, bname='==')
def equals(a, b) -> bool:
    return a == b

@coppertop(style=binary, dispatchEvenIfAllTypes=True, bname='==')
def equals(a:matrix&darray, b:matrix&darray) -> bool:
    return bool((a == b).all())

@coppertop(style=binary, bname='>=')
def ge(a, b) -> bool:
    return a >= b

@coppertop(style=binary, bname='>')
def gt(a, b) -> bool:
    return a > b

@coppertop(style=binary, bname='<')
def le(a, b) -> bool:
    return a <= b

@coppertop(style=binary, bname='<=')
def lt(a, b) -> bool:
    return a < b
