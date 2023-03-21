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


@coppertop(style=binary)
# def partitions_(es:N**T, sizes:N**index) -> N**N**N**T:
def partitions(es, sizes: pylist):
    sizes >> sum >> check >> equals >> (es >> count)
    return list(es) >> _partitions(_, es >> count, sizes)


@coppertop
# def _partitions2(es:N**T, n:index, sizes:N**index) -> N**N**(N**T):
def _partitions(es: pylist, n: index, sizes: pylist) -> pylist:
    if not sizes: return [[]]
    return es >> _combRest2(_, n, sizes >> first) \
        >> collect >> ((lambda x, y:
            y >> _partitions(_, n - (sizes >> first), sizes >> drop >> 1)
                >> collect >> (lambda partitions:
                    x >> prependTo >> partitions
                )
        ) >> unpack) \
        >> joinAll


@coppertop
# def _combRest2(es:N**T, n:index, m:index) -> N**( (N**T)*(N**T) ):
def _combRest2(es: pylist, n: index, m: index) -> pylist:
    '''answer [m items chosen from n items, the rest]'''
    if m == 0: return [([], es)]
    if m == n: return [(es, [])]
    return \
        es >> drop >> 1 >> _combRest2(_, n - 1, m - 1) >> collect >> (unpack >> (lambda x, y: (es >> take >> 1 >> join >> x, y))) \
        >> join >> (
        es >> drop >> 1 >> _combRest2(_, n - 1, m) >> collect >> (unpack >> (lambda x, y: (x, es >> take >> 1 >> join >> y)))
        )


@coppertop
def unpack(f):
    return lambda xy: f(xy[0], xy[1])  # needs to return a pipeable?

#%timeit range(13) >> partitions2_ >> [5,4,4] >> count >> PP
# 18 s ± 93.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
