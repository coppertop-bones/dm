# **********************************************************************************************************************
# Copyright (c) 2019-2022 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

from .core import *


def test():
    context.testcase = 'frame - missing comma'
    '''
        ([]
            s0: (0.95;0.2) <:probs>                 // missing comma
            s1: (0.05;0.8) <:probs>
        )
    ''' >> group_ >> check >> raises >> GroupError

    context.testcase = 'frame'
    '''
        ([]
            s0: (0.95;0.2) <:probs>,
            s1: (0.05;0.8) <:probs>
        )
    ''' >> group >> bb >> check >> equals >> '([] (l; l) t {:s0}, (l; l) t {:s1})'

    context.testcase = 'keyed frame - missing comma'
    '''
        (
            [G:`gA`gB`gC`gA`gB`gC L:`l0`l0`l0`l1`l1`l1]   // missing comma, should be `gC, L:`l0
            P: (0.10;0.40;0.99;0.90;0.60;0.01)<:probs>
        )
    ''' >> group_ >> check >> raises >> GroupError

    context.testcase = 'example frame no keys'
    '''
        (
            [G:`gA`gB`gC`gA`gB`gC, L:`l0`l0`l0`l1`l1`l1] 
            P: (0.10;0.40;0.99;0.90;0.60;0.01)<:probs>
        )
    ''' >> group >> bb >> check >> equals >> '([l {:G}, l {:L}] (l; l; l; l; l; l) t {:P})'

    context.testcase = "frame"
    '''
        ([]
            s0: (0.95;0.2) <:probs>,
            s1: (0.05;0.8) <:probs>
        )
    ''' >> group >> bb >> check >> equals >> '([] (l; l) t {:s0}, (l; l) t {:s1})'

    context.testcase = "keyed frame"
    '''
        ([int: `i0`i1]
            s0: (0.95;0.2) <:probs>,
            s1: (0.05;0.8) <:probs>
        )
    ''' >> group >> bb >> check >> equals >> '([l {:int}] (l; l) t {:s0}, (l; l) t {:s1})'