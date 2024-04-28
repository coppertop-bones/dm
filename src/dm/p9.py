# **********************************************************************************************************************
#
#                             Copyright (c) 2022 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************

from coppertop.pipe import *
from bones.lang.metatypes import BTNom
from bones.lang.structs import tv


P9 = BTNom.ensure('P9').setCoercer(tv)

@coppertop
def PP(p: P9) -> P9:
    fig = p._v.draw(show=True)
    return p
