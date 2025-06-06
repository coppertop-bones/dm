# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

import pytest
bones_lang = pytest.mark.bones_lang
xfail = pytest.mark.xfail
skip = pytest.mark.skip


from coppertop.pipe import *
from bones.core.sentinels import Missing
from bones.kernel import psm
from bones.kernel.bones import BonesKernel
from bones.lang.core import GLOBAL, SCRATCH
from bones.lang.symbol_table import SymTab
import bones.lang.symbol_table
from bones.lang.lex import LINE_COMMENT, BREAKOUT
from bones.lang.execute import TCInterpreter
from bones.lang.infer import InferenceLogger
from bones.lang._testing_.utils import stripSrc, pace as _pace, newKernel
from bones.ts.metatypes import BType


from coppertop.dm.testing import check, equals, raises
from coppertop.dm.core import startsWith, underride, withCtx, drop
from coppertop.dm.core.types import litint, littxt, void, litnum, num, index, txt, T1, T2, T3, T4, T5, bool, count, pylist
from coppertop.dm.pp import PP


bones.lang.symbol_table.PYCHARM = True


@bones_lang
def test_MAndMs(**ctx):
    k = newKernel()
    pace = _pace(k, _, _)

    src = r'''
        load coppertop.dm._stdlib.ops, coppertop.dm.pmf
        from coppertop.dm._stdlib.ops import *
        from coppertop.dm.pmf import to, PMF, L, normalise, PP, *
        
        bag1994: {Brown:30, Yellow:20, Red:20, Green:10, Orange:10, Tan:10}
        bag1996: {Brown:13, Yellow:14, Red:13, Green:20, Orange:16, Blue:24}
        
        prior: {hypA:0.5, hypB:0.5} to <:PMF> PP
        likelihood: {
            hypA:bag1994.Yellow * bag1996.Green, 
            hypB:bag1994.Green * bag1996.Yellow
        } to <:L> PP
        
        post: prior * likelihood normalise PP
    ''' >> stripSrc

    # OPEN: what's the best way to overload mul(name='*') - insist that python name and bones name pairs must be consistent?

    with context(**ctx):
        res = pace(src, 3)
        if res.error: raise res.error

        DF = BType('DF')
        res.result >> typeOf >> fitsWithin >> DF



@pytest.fixture(scope='module')
def ctx():
    return {}



def main():
    debug = dict(showSrc=True, showGroups=False, showTc=True, RESTRICT_NOTES=False, ALL=False, tt=InferenceLogger())
    debugNoRun = dict(showSrc=True, showGroups=False, showTc=True, RESTRICT_NOTES=False, ALL=False, run=False, tt=InferenceLogger())
    test_MAndMs(**debug)


if __name__ == '__main__':
    main()
    print('pass')
