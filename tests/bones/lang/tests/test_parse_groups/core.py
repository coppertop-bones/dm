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
