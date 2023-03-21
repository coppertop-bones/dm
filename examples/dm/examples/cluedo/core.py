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

from bones.lang.metatypes import BTAtom, S
from bones.core.sentinels import Missing
from dm.core.types import pydict, count, txt, dstruct


card = BTAtom.ensure('card')
handId = BTAtom.ensure('handId')
ndmap = BTAtom.ensure('ndmap')
pad_element = S(has=txt, suggestions=count, like=count)
cluedo_pad = ((card*handId)**pad_element)[ndmap] & BTAtom.ensure('cluedo_pad')
cluedo_pad = pydict #& BTAtom.ensure('cluedo_pad') once we have tvmap we can do this
cluedo_bag = (dstruct & BTAtom.ensure('_cluedo_bag')).nameAs('cluedo_bag')


YES = 'X'
NO = '-'
MAYBE = '?'

class HasOne(object):
    def __init__(self, handId=Missing):
        self.handId = handId
    def __rsub__(self, handId):     # handId / has
        assert self.handId == Missing, 'Already noted a handId'
        return HasOne(handId)
one = HasOne()
