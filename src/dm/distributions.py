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

MODULE_NS = ''

import math

from coppertop.pipe import *


@coppertop(module='dm.stats')
def logisticCDF(x, mu, s):
    return 1 / (1 + math.exp(-1 * (x - mu) / s))

@coppertop(module='dm.stats')
def logisticCDFInv(p, mu, s):
    return mu + -s * math.log(1 / p - 1)


## scipy.stats.f.cdf
## scipy.stats.t.cdf

