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
    context.testcase = 'load'
    '''
    load 
        dm.core
    ''' >> group >> bb >> check >> equals >> '{L}'
    
    
    context.testcase = 'load #2'
    '''
        load a
        load a
        5
    ''' >> group >> bb >> check >> equals >> '{L}. {L}. l'
    
    
    context.testcase = 'load #3'
    '''
        load a, fred.sally,
          joe,
          arthur. load stuff,
                      nancy,
                    sid
        load a, b. load c, d.e
        5
    ''' >> group >> bb >> check >> equals >> '{L}. {L}. {L}. {L}. l'
    
    
    context.testcase = 'missing name'
    '''
    load
        dm.core,
    fred
    ''' >> group_ >> check >> raises >> GroupError
    
    
    context.testcase = 'nothing specified to load in the phrase'
    'load' >> group_ >> check >> raises >> GroupError
    
    
    context.testcase = 'trailing comma causes the error in load #1'
    '''
        load 
            dm.core,        // the trailing comma causes the error
    ''' >> group_ >> check >> raises >> GroupError
    
    
    context.testcase = 'load #4'
    '''
        from x import y
        difficulty: 1
    ''' >> group >> bb >> check >> equals >> '{FI}. l {:difficulty}'
    
    
    context.testcase = 'trailing comma causes the error in load #2'
    '''
        load 
            my_first_bones.conversions, 
            constants             // constants added to stretch the load parsing
        from my_first_bones.lang import ...       // defines op+, op-, op*, op/, tNum, tStr, fUnary, fBinary in global scope
        from std_bones.bones.stdio import stdout :cout, cerr: stderr
        stdout << "Hello " "world!"
        a: 1
        2 :b + a my_first_bones.conversions.intToStr :c
        stdout << c

        stderr << (1.0 :fred / constants.zero)          // what are we going to do about this?
    ''' >> group >> bb >> check >> equals >> '{L}. {FI}. {FI}. n o l l. l {:a}. l {:b} o n n {:c}. n o n. n o (l {:fred} o n)'
