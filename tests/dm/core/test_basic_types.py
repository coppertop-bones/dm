# **********************************************************************************************************************
# Copyright  (c) 2025 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************


# map, seq are abstract?
# pydict, pylist, pyset, pytuple are

from coppertop.pipe import *
from bones.lang.metatypes import BType
from dm.core.types import txt, num, count, index, offset, dmap, dseq

from dm.core.aggman import join
from dm.testing import check, equals, different


def test_txt():
    txt('hello') >> join >> ' world' >> check >> equals >> 'hello world'
    ('hello' | txt) >> check >> equals >> 'hello'
    'hello' >> typeOf >> check >> fitsWithin >> txt

    # the intersection safetxt will use the txt coercer / construction
    safetxt = BType('safetxt: safetxt & txt in mem')
    safetxt('hello') >> join >> safetxt(' world') >> check >> equals >> 'hello world'
    'hello world' >> check >> different >> safetxt('hello world')



