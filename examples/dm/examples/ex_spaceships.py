# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
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
from bones.core.sentinels import Null

from dm.core.types import txt, null
from dm.testing import check, equals
from dm.pp import PP


# Inspired by the wikipedia article on multi-dispatch - https://en.wikipedia.org/wiki/Multiple_dispatch
# Hopefully this is even more readable than Julia

tAsteroid = BTNom.ensure('asteroid').setCoercer(tv)
tShip = BTNom.ensure('ship').setCoercer(tv)
tEvent = BTNom.ensure('event').setCoercer(tv)


@coppertop
def collide(a:tAsteroid, b:tAsteroid) -> tEvent:
    return f'{a._v} split {b._v} (collide<:asteroid,asteroid:>)' | tEvent

@coppertop
def collide(a:tShip, b:tAsteroid) -> tEvent:
    return f'{a._v} tried to ram {b._v} (collide<:ship,asteroid:>)' | tEvent

@coppertop
def collide(a:tAsteroid, b:tShip) -> tEvent:
    return f'{a._v} destroyed {b._v} (collide<:asteroid,ship:>)' | tEvent

@coppertop
def collide(a:tShip, b:tShip) -> null:
    return Null
#    return f'{a} bounced {b} (collide<:ship,ship:>)' >> to >> tEvent

@coppertop
def process(e:tEvent) -> txt:
    return e._v

@coppertop
def process(e:null) -> txt:
    return 'nothing happened'

# @coppertop
# def process(e:tEvent+null) -> txt:
#     return 'nothing happened' if e._t == null else e._v


borg = tShip['borg'].setCoercer(tv)

@coppertop
def collide(a:borg, b:tShip) -> tEvent:
    return f'{a._v} subsumes {b._v} (collide<:borg,ship:>)' | tEvent

@coppertop
def collide(a:borg, b:borg) -> tEvent:
    return f'{a._v} merges with {b._v} (collide<:borg,big:>)' | tEvent



def testCollide():
    ship1 = 'ship1' | tShip
    ship2 = 'ship2' | tShip
    ast1 = 'big asteroid' | tAsteroid
    ast2 = 'small asteroid' | tAsteroid
    b = 'borg' | borg

    ship1 >> collide(_, ship2) >> process >> PP
    ship1 >> collide(_, ast1) >> process >> PP
    ship2 >> collide(ast2, _) >> process >> PP
    ast1 >> collide(_, ast2) >> process >> PP
    b >> collide(_, ship2) >> process >> PP
    b >> collide(_, ast1) >> process >> PP
    b >> collide(ast2, _) >> process >> PP
    ship1 >> collide(_, b) >> process >> PP
    b >> collide(_, b) >> process >> PP

    ship1 >> collide(_, ship2) >> process >> check >> equals >> 'nothing happened'
    # 'ship1 tried to ram big asteroid (collide<:ship,asteroid:>)'
    # 'small asteroid destroyed ship2 (collide<:asteroid,ship:>)'
    # 'big asteroid split small asteroid (collide<:asteroid,asteroid:>)'


def main():
    testCollide()


if __name__ == '__main__':
    testCollide()
    print('pass')
