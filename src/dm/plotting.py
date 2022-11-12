# **********************************************************************************************************************
#
#                             Copyright (c) 2022 David Briant. All rights reserved.
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

BONES_NS = 'dm.plot'

import plotnine, numpy as np, statsmodels.api as sm

from coppertop.pipe import *
from dm.pandaframe import pandaframe
from dm.p9 import P9
from dm.core.aggman import atCol
from dm.core.types import matrix, N, num, void
from bones.lang.structs import tvarray
from bones.core.sentinels import Void
from dm.core.conv import to


array_ = (N**num)&tvarray
matrix_ = matrix&tvarray

@coppertop
def scatter(F:matrix_) -> P9:
    df = pandaframe({
        'X':  F >> atCol >> 0 >> to >> array_,
        'Y':  F >> atCol >> 1 >> to >> array_
    })
    p = plotnine.ggplot(df, plotnine.aes(x='X', y='Y')) + plotnine.geom_point()
    return p | P9


@coppertop
def qq(res:array_) -> void:
    sm.qqplot(res / np.std(res) >> to >> np.ndarray, line ='45')
    return Void

