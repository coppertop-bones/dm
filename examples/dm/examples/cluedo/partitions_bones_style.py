# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************


from coppertop.pipe import *
from dm.core.types import pylist, index
from dm.testing import check, equals
from groot import first, count, drop, collect, prependTo, join, joinAll, take, sum


#%timeit range(13) >> partitions2 >> [5,4,4] >> count >> PP
# 6.15 s ± 89.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

@coppertop(style=binary)
# def partitions_(es:N**T, sizes:N**index) -> N**N**N**T:
def partitions2(es, sizes: pylist) -> pylist:
    sizes >> sum >> check >> equals >> (es >> count)
    return _partitions2(list(es), es >> count, sizes)

@coppertop
# def _partitions2(es:N**T, n:index, sizes:N**index) -> N**N**(N**T):
def _partitions2(es: pylist, n: index, sizes: pylist) -> pylist:
    if not sizes: return [[]]
    return es >> _combRest2(_, n, sizes >> first) \
        >> collect >> (unpack(lambda x, y:
            _partitions2(y, n - (sizes >> first), sizes >> drop >> 1)
                >> collect >> (lambda partitions:
                    x >> prependTo >> partitions
                )
        )) \
        >> joinAll

@coppertop
# def _combRest2(es:N**T, n:index, m:index) -> N**( (N**T)*(N**T) ):
def _combRest2(es: pylist, n: index, m: index) -> pylist:
    '''answer [m items chosen from n items, the rest]'''
    if m == 0: return [([], es)]
    if m == n: return [(es, [])]
    return \
        (es >> drop >> 1 >> _combRest2(_, n - 1, m - 1) >> collect >> unpack(lambda x, y: (es >> take >> 1 >> join >> x, y))) \
        >> join >> \
        (es >> drop >> 1 >> _combRest2(_, n - 1, m) >> collect >> unpack(lambda x, y: (x, es >> take >> 1 >> join >> y)))


#%timeit range(13) >> partitions3 >> [5,4,4] >> count >> PP
# 2.49 s ± 11.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

@coppertop(style=binary)
def partitions3(xs, sizes: pylist) -> pylist:
    sizes >> sum >> check >> equals >> (xs >> count)
    return _partitions3(list(xs), xs >> count, sizes)

@coppertop
def _partitions3(xs: pylist, n: index, sizes: pylist) -> pylist:
    if not sizes: return [[]]
    return _combRest3(xs, n, sizes[0]) \
        >> collect >> (unpack(lambda comb, rest:
            _partitions3(rest, n - sizes[0], sizes[1:])
                >> collect >> (lambda partitions:
                    [comb] + partitions
                )
        )) \
        >> joinAll

@coppertop
def _combRest3(xs: pylist, n: index, m: index) -> pylist:
    '''answer [m items chosen from n items, the rest]'''
    if m == 0: return [([], xs)]
    if m == n: return [(xs, [])]
    return \
        (_combRest3(xs[1:], n - 1, m - 1) >> collect >> (lambda xy: (xs[0:1] + xy[0], xy[1]))) + \
        (_combRest3(xs[1:], n - 1, m) >> collect >> (lambda xy: (xy[0], xs[0:1] + xy[1])))



