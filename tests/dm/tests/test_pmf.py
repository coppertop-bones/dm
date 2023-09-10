# **********************************************************************************************************************
# Copyright  (c) 2017-2020 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from dm.testing import check, equals, closeTo
from dm.core.misc import sequence
from dm.pmf import uniform, rvAdd, mix, toXsPs, PMF, toCmf, pmfMul, normalise, L


def test_pmf():
    d4 = uniform(sequence(1, 4))
    d6 = uniform(sequence(1, 6))
    rv = d4 >> rvAdd >> d4
    rv[2] >> check >> equals >> 1/16

    d4d6 = [d4, d6] >> mix
    result = d4d6[1]
    expected = (1/4 + 1/6) / (4 * (1/4 + 1/6) + 2 * 1/6)
    assert closeTo(result, expected, 0.00001), '%s != %s' % (result, expected)

    (d4 >> toXsPs)[0] >> check >> equals >> (1.0, 2.0, 3.0, 4.0)


def test_MMs():
    bag1994 = PMF(Brown=30, Yellow=20, Red=20, Green=10, Orange=10, Tan=10)
    bag1994.Brown >> check >> closeTo >> 0.3
    bag1996 = PMF(Brown=13, Yellow=14, Red=13, Green=20, Orange=16, Blue=24)

def test_cmf():
    d6 = uniform(sequence(1, 6))
    cmf = d6 >> toCmf
    cmf >> percentile(_, 0.5) >> check >> equals >> 3

def test_MM():
    bag1994 = PMF(Brown=30, Yellow=20, Red=20, Green=10, Orange=10, Tan=10)
    bag1996 = PMF(Brown=13, Yellow=14, Red=13, Green=20, Orange=16, Blue=24)
    prior = PMF(hypA=0.5, hypB=0.5)
    likelihood = L(
        hypA=bag1994.Yellow * bag1996.Green,
        hypB=bag1994.Green * bag1996.Yellow
    )
    post = prior >> pmfMul >> likelihood >> normalise
    post.hypA >> check >> closeTo >> 20/27

def test_monty():
    prior = PMF(A=1, B=1, C=1)
    likelihood = L(  # i.e. likelihood of monty opening B given that the car is behind each, i.e. p(data|hyp)
        A=0.5,  # prob of opening B if behind A - he can choose at random so 50:50
        B=0,  # prob of opening B if behind B - Monty can't open B else he'd reveal the car, so cannot open B => 0%
        C=1,  # prob of opening B if behind C - Monty can't open C else he'd reveal the car, so must open B => 100%
    )
    posterior = prior >> pmfMul >> likelihood >> normalise
    posterior.C >> check >> closeTo(_,_,0.001) >> 0.667


def main():
    test_MM()
    test_monty()
    test_pmf()
    test_MMs()
    # test_cmf()


if __name__ == '__main__':
    main()
    print('pass')

