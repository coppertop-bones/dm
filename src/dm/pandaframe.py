# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import numpy as np, csv, pandas as pd, polars as pl

from coppertop.pipe import *
from dm.core.types import dframe, void, pydict
from dm.core.aggman import array_
from dm.core.conv import to
from bones.core.sentinels import Void


pandaframe = pd.DataFrame
polarframe = pl.DataFrame


# **********************************************************************************************************************
# to
# **********************************************************************************************************************

@coppertop(style=binary)
def to(bf:dframe, t:pandaframe) -> pandaframe:
    df = pd.DataFrame()
    for f, d in bf._kvs():
        df[f] = d >> to >> array_
    return df

@coppertop(style=binary)
def to(f:polarframe, t:pandaframe) -> pandaframe:
    return f.to_pandas()

@coppertop(style=binary)
def to(f:pandaframe, t:polarframe) -> polarframe:
    return pl.from_pandas(f)



