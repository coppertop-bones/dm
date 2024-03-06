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

import plotnine, numpy as np, statsmodels.api as sm, seaborn as sns

from coppertop.pipe import *
from dm.pandaframe import pandaframe
from dm.p9 import P9
from dm.core.aggman import atCol
from dm.core.types import matrix, N, num, void, pydict
from dm.core.structs import tvarray
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

@coppertop
def correlogram(pdf:pandaframe) -> void:
    return _correlogram(pdf)

@coppertop
def correlogram(pdf:pandaframe, kwargs:pydict) -> void:
    return _correlogram(pdf, **kwargs)

def _correlogram(pdf:pandaframe, kind="reg", diag_kind='kde') -> void:
    sns.pairplot(
        pdf,
        kind="reg",
        diag_kind="kde"
    )
    return Void
