# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#    disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#    This product includes software developed by the copyright holders.
#
# 4. Neither the name of the copyright holder nor the names of the  contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# **********************************************************************************************************************

BONES_NS = 'dm.linalg'

import numpy as np
from coppertop.pipe import *
from bones.lang.metatypes import BTAtom, BTStruct
from dm.core.types import matrix, N, num, pytuple
from bones.lang.structs import tvarray, bstruct


# NB a 1x1 matrix is assumed to be a scalar, e.g. https://®®en.wikipedia.org/wiki/Dot_product#Algebraic_definition


I = BTAtom.define('I')
square = BTAtom.define('square')
right = BTAtom.define('right')
left = BTAtom.define('left')
upper = BTAtom.define('upper')
lower = BTAtom.define('lower')
orth = BTAtom.define('orth')
diag = BTAtom.define('diag')
tri = BTAtom.define('tri')
cov = BTAtom.define('cov')
colvec = BTAtom.define('colvec')
rowvec = BTAtom.define('rowvec')

Cholesky = BTAtom.ensure('Cholesky')


matrix_ = matrix & tvarray
array_ = (N**num) & tvarray


QR = BTStruct(qT=matrix, r=matrix&right)
@coppertop(style=nullary, module='pvt')
def _makeQR(ts, q:matrix_, r:matrix_):
    return bstruct(QR&bstruct, q=q, r=r)
@coppertop(style=nullary, module='pvt')
def _makeQR(ts, qr:pytuple):
    return bstruct(QR&bstruct, q=matrix_(qr[0]), r=matrix_(qr[1]))
QR.setConstructor(_makeQR)


SVD = BTStruct(u=matrix, s=N**num, vt=matrix)
@coppertop(style=nullary, module='pvt')
def _makeSVD(ts, u:matrix_, s:array_, vT:matrix_) -> SVD&bstruct:
    return bstruct(SVD&bstruct, u=u, s=s, vT=vT)
SVD.setConstructor(_makeSVD)
