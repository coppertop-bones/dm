# **********************************************************************************************************************
# Copyright (c) 2024 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************


from coppertop.pipe import *
from bones.core.sentinels import Missing
from bones.lang.ctx import Ctx
import bones.lang.ctx
from bones.lang.infer import InferenceLogger

from bones.lang.tests._utils import dropFirstNL, pace, evalPyInComments, errorMsg, pace_, _newKernel


import dm.pp, dm.testing
from dm.core import PP, check, equals, startsWith, underride, withCtx, raises, drop
from dm.core.types import litint, littxt, void, litdec, num, index, txt, T1, T2, T3, T4, T5, bool, count, pylist


bones.lang.ctx.PYCHARM = True




def test_partition(**ctx):
    k = _newKernel()

    src = r'''
        load dm.core, dm.testing
        from dm.core import check, equals, sum
        
        partitions: {{[xs, sizes]
            sizes sum check equals (xs count)
            xs _partitions(, xs count, sizes)
        }}
        
        _partitions: {[xs, n, sizes]
            sizes isEmpty ifTrue: [^ (())]
            xs _combRest(, n, sizes first) each {[a, b]
                _partitions(b, .n - (.sizes first), .sizes drop 1) each {
                    .a prependTo r
                }
            } joinAll
        }
        
        _combRest: {[xs, n, m]
            m == 0 ifTrue: [^ ( ((), xs) ) to <:N**T1>]
            m == n ifTrue: [^ ( (xs, ()) ) to <:N**T1>]
            (s1, s2): xs takeDrop 1
            _combRest(s2, s2 count, m - 1) each { (.s1 join a, b) }    // #1
              join
              _combRest(s2, s2 count, m) each { (a, .s1 join b) }      // #2
        }
    ''' >> dropFirstNL

    if context.analyse:
        context.testcase = 'overload fail - static'
        res = src >> withCtx >> ctx >> pace(k,_) >> evalPyInComments
        res \
            >> check >> errorMsg >> startsWith >> 'cannot constrain {littxt} <:' \
            >> check >> (lambda x: [e[1] for e in x.types]) >> drop >> 2 >> equals >> res.commentTypes
    else:
        context.testcase = 'run partitions'
        src >> pace(k, _)
        src >> withCtx >> ctx >> check >> pace_(k, _)
        #>> raises >> TypeError




def main():

    debug = dict(showSrc=True, showGroups=False, showTc=True, RESTRICT_NOTES=False, ALL=False, tt=InferenceLogger())
    debugNoRun = dict(showSrc=True, showGroups=False, showTc=True, RESTRICT_NOTES=False, ALL=False, run=False, tt=InferenceLogger())

    test_partition()




if __name__ == '__main__':
    main()
    print('pass')