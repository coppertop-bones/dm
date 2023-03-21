# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************

BONES_NS = ''

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


EPS = 7.105427357601E-15      # i.e. double precision


import builtins, numpy as np, math

from bones.core.errors import NotYetImplemented
from coppertop.pipe import *
from dm.core.types import T1, T2, pylist, N, num, matrix, t, pyset, pytuple
from dm._core.structs import tvarray

import itertools, scipy

array_ = (N**num)&tvarray
matrix_ = matrix&tvarray



# **********************************************************************************************************************
# permutations (arrangements) and combinations
# perms and combs are such useful variable names so use fuller name in fn
# **********************************************************************************************************************

@coppertop(style=binary)
def permutations(xs, k):
    return tuple(itertools.permutations(xs, k))

@coppertop(style=binary)
def nPermutations(n, k):
    return math.perm(n, k)

@coppertop(style=binary)
def permutationsR(xs, k):
    return tuple(itertools.product(*([xs]*k)))

@coppertop(style=binary)
def nPermutationsR(n, k):
    return n ** k

@coppertop(style=binary)
def combinations(xs, k):
    return tuple(itertools.combinations(xs, k))

@coppertop(style=binary)
def nCombinations(n, k):
    return math.comb(n, k)

@coppertop(style=binary)
def combinationsR(xs, k):
    return tuple(itertools.combinations_with_replacement(xs, k))

@coppertop(style=binary)
def nCombinationsR(n, k):
    return scipy.special.comb(n, k, exact=True)


# **********************************************************************************************************************
# comparison
# **********************************************************************************************************************

@coppertop
def within(x, a, b):
    # answers true if x is in the closed interval [a, b]
    return (a <= x) and (x <= b)


# **********************************************************************************************************************
# functions
# **********************************************************************************************************************

@coppertop
def log(v:array_) -> array_:
    return np.log(v)

@coppertop
def sqrt(x):
    return np.sqrt(x)   # answers a nan rather than throwing


# **********************************************************************************************************************
# stats
# **********************************************************************************************************************

@coppertop
def cov(A:matrix&tvarray) -> matrix&tvarray:
    return (matrix&tvarray)(np.cov(A))

@coppertop
def max(x:matrix&tvarray):
    return np.max(x)

@coppertop
def max(x):
    return builtins.max(x)

@coppertop
def mean(ndOrPy):
    return np.mean(ndOrPy)

@coppertop
def min(x:matrix&tvarray):
    return np.min(x)

@coppertop
def min(x):
    return builtins.min(x)

@coppertop
def product(x:pylist+pyset+pytuple) -> num + t.count:
    return math.product(x)

@coppertop
def std(ndOrPy):
    return np.std(ndOrPy, 0)

@coppertop
def std(ndOrPy, dof):
    return np.std(ndOrPy, dof)

@coppertop
def sum(x):
    return builtins.sum(x)

@coppertop
def sum(x:(N**T1)[pylist][T2]) -> num:
    return builtins.sum(x._v)

@coppertop
def sum(x:(N**T1)[pylist]) -> num:
    return builtins.sum(x._v)


# **********************************************************************************************************************
# rounding
# **********************************************************************************************************************

@coppertop
def roundDown(x):
    # i.e. [roundDown(-2.9), roundDown(2.9,0)] == [-3, 2]
    return math.floor(x)

@coppertop
def roundUp(x):
    # i.e. [roundUp(-2.9), roundUp(2.9,0)] == [-2, 3]
    return math.ceil(x)

@coppertop
def roundHalfToZero(x):
    # i.e. [round(-2.5,0), round(2.5,0)] == [-2.0, 2.0]
    return round(x)

@coppertop
def roundHalfFromZero(x):
    raise NotYetImplemented()

@coppertop
def roundHalfToNeg(x):
    raise NotYetImplemented()

@coppertop
def roundHalfToPos(x):
    raise NotYetImplemented()

@coppertop
def round(xs:matrix&tvarray, figs:t.count) -> matrix&tvarray:
    return (matrix&tvarray)(np.round(xs, figs))

@coppertop
def round(xs:array_, figs:t.count) -> array_:
    return (array_)(np.round(xs, figs))
