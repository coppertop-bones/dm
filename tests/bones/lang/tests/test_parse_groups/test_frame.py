# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2022 David Briant. All rights reserved.
#
# This file is part of coppertop-bones.
#
# coppertop-bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# coppertop-bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
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