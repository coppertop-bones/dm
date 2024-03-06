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

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import builtins, numpy as np

from coppertop.pipe import *
from dm.core.types import T1, T2, pylist, N, num, matrix
from dm.core.structs import tvarray



array_ = (N**num)&tvarray
matrix_ = matrix&tvarray



# **********************************************************************************************************************
# stats
# **********************************************************************************************************************

@coppertop
def cov(A:matrix_) -> matrix&tvarray:
    return (matrix&tvarray)(np.cov(A))

@coppertop
def max(x:matrix_):
    return np.max(x)

@coppertop
def max(x):
    return builtins.max(x)

@coppertop
def mean(ndOrPy):
    return np.mean(ndOrPy)

@coppertop
def min(x:matrix_):
    return np.min(x)

@coppertop
def min(x):
    return builtins.min(x)


# **********************************************************************************************************************
# sum - is okay as same interface as Python
# **********************************************************************************************************************

@coppertop
def std(ndOrPy):
    return np.std(ndOrPy, 0)

@coppertop
def std(ndOrPy, dof):
    return np.std(ndOrPy, dof)


# **********************************************************************************************************************
# sum - is okay as same interface as Python
# **********************************************************************************************************************

@coppertop
def sum(x):
    return builtins.sum(x)

@coppertop
def sum(x:(N**T1)[pylist][T2]) -> num:
    return builtins.sum(x._v)

@coppertop
def sum(x:(N**T1)[pylist]) -> num:
    return builtins.sum(x._v)

