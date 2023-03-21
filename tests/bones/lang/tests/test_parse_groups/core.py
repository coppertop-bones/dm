# **********************************************************************************************************************
# Copyright (c) 2019-2022 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

from coppertop.pipe import *
from dm.testing import check, equals, raises, same
from dm.pp import PP, TT, DD, HH
from dm.core.types import txt
from bones.lang import lex
from bones.core.errors import GroupError
from bones.lang.parse_groups import parseStructure, TUPLE_NULL, TUPLE_OR_PAREN, TUPLE_2D, TUPLE_0_EMPTY, TUPLE_1_EMPTY, \
    TUPLE_2_EMPTY, TUPLE_3_EMPTY, TUPLE_4_PLUS_EMPTY, SnippetGroup
from bones.core.sentinels import function, Missing

@coppertop
def group(src:txt):
    tokens, lines = lex.lexBonesSrc(0, src)
    return parseStructure(tokens)

@coppertop
def group_(src:txt) -> function:
    return lambda : src >> group

@coppertop
def bb(g:SnippetGroup) -> txt:
    return g.PPGroup

@coppertop
def stripSpace(x):
    return x.replace(' ', '')
