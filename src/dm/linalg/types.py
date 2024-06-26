# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************

import numpy as np
from coppertop.pipe import *
from bones.lang.metatypes import BTNom, BTStruct
from dm.core.types import matrix, N, num, pytuple, dstruct
from dm.core.structs import tvarray


# NB a 1x1 matrix is assumed to be a scalar, e.g. https://®®en.wikipedia.org/wiki/Dot_product#Algebraic_definition


I = BTNom.define('I')
square = BTNom.define('square')
right = BTNom.define('right')
left = BTNom.define('left')
upper = BTNom.define('upper')
lower = BTNom.define('lower')
orth = BTNom.define('orth')
diag = BTNom.define('diag')
tri = BTNom.define('tri')
cov = BTNom.define('cov')
colvec = BTNom.define('colvec')
rowvec = BTNom.define('rowvec')

Cholesky = BTNom.ensure('Cholesky')


matrix_ = matrix & tvarray
array_ = (N**num) & tvarray


QR = BTStruct(qT=matrix, r=matrix&right)
@coppertop(style=nullary, local=True)
def _makeQR(ts, q:matrix_, r:matrix_):
    return dstruct(QR&dstruct, q=q, r=r)
@coppertop(style=nullary, local=True)
def _makeQR(ts, qr:pytuple):
    return dstruct(QR&dstruct, q=matrix_(qr[0]), r=matrix_(qr[1]))
QR.setConstructor(_makeQR)


SVD = BTStruct(u=matrix, s=N**num, vt=matrix)
@coppertop(style=nullary, local=True)
def _makeSVD(ts, u:matrix_, s:array_, vT:matrix_) -> SVD&dstruct:
    return dstruct(SVD&dstruct, u=u, s=s, vT=vT)
SVD.setConstructor(_makeSVD)
