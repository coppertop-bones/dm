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

import scipy.linalg, numpy as np, numpy.linalg

from coppertop.pipe import *
from dm._core.structs import tvarray
from dm.core.types import matrix, N, num, T
from dm.linalg.types import orth, right, upper, lower, Cholesky, QR, SVD, left
import dm.linalg.orient

from groot import dm


array_ = (N**num)[tvarray]
matrix_ = matrix[tvarray]


# NB a 1x1 matrix is assumed to be a scalar, e.g. https://®®en.wikipedia.org/wiki/Dot_product#Algebraic_definition


@coppertop(module='dm.linalg.np')
def inv(A:matrix_) -> matrix_:
    return np.linalg.inv(A)

@coppertop(module='dm.linalg.np')
def qr(A:matrix_) -> QR:
    Q, R = np.linalg.qr(A)            # via householder?
    q = matrix_(Q) | +orth
    r = matrix_(R) | +right
    return QR(q, r)

@coppertop(module='dm.linalg.np')
def cholesky(A:matrix_) -> matrix_&Cholesky:
    # use np since in scipy.linalg.cho_factor "The returned matrix also contains random data in the entries not
    # used by the Cholesky decomposition. If you need to zero these entries, use the function cholesky instead."
    return matrix_(np.linalg.cholesky(A)) | +Cholesky

@coppertop(module='dm.linalg.np')
def svd(A:matrix_) -> SVD:
    u, s, vT = np.linalg.svd(A)
    return SVD(matrix_(u), array_(s), matrix_(vT))



# https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_triangular.html

@coppertop(style=binary)
def solve(U:(upper&matrix_)+(right&matrix_), b:matrix_[T]) -> matrix_:
    """Returns the solution x of Ux = b where U is upper triangular"""
    return scipy.linalg.solve_triangular(U, b, lower=False).view(tvarray) | matrix_


@coppertop(style=binary)
def solve(L:(lower&matrix_)+(left&matrix_), b:matrix_[T]) -> matrix_:
    """Returns the solution x of Lx = b where U is lower triangular"""
    return scipy.linalg.solve_triangular(L, b, lower=True).view(tvarray) | matrix_


@coppertop(style=binary)
def solve(c:Cholesky&matrix, b:matrix_[T]) -> matrix_:
    """Returns the solution x of Ax = b given the Cholesky decomposition of A"""
    return matrix_(scipy.linalg.cho_solve(c, b))


@coppertop(style=binary)
def solve(qr:QR, b:matrix_[T]) -> matrix_:
    """Returns the solution x of Ax = b given a QR decomposition of A"""
    return scipy.linalg.solve_triangular(qr.r, qr.T @ b, lower=False).view(tvarray) | matrix_


@coppertop(style=binary)
def solve(svd:SVD, b:matrix_[T]) -> matrix_:
    """Returns the solution x of Ax = b given the SVD of A"""
    raise NotYetImplemented()


@coppertop
def pca(panel:matrix&tvarray):
    u, s, vh = dm.linalg.np.svd(panel)
    vor, e, sfv, thetas, sorts = dm.linalg.orientEigenvectors(vh.T, s)
    return vor, s

