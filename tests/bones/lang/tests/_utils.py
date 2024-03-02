# **********************************************************************************************************************
# Copyright (c) 2022-2024 David Briant. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************


from coppertop.pipe import *
from bones.core.sentinels import Missing
from bones.kernel import psm
from bones.kernel.bones import BonesKernel
from bones.lang.core import GLOBAL, SCRATCH
from bones.lang.ctx import Ctx
import bones.lang.ctx
from bones.lang.lex import LINE_COMMENT, BREAKOUT
from bones.lang.execute import TCInterpreter
from bones.lang.infer import InferenceLogger



@coppertop
def dropFirstNL(s):
    return s[1:] if s[0:1] == '\n' else s


def _newKernel():
    sm = psm.PythonStorageManager()
    k = BonesKernel(sm)
    k.ctxs[GLOBAL] = Ctx(k, Missing, Missing, Missing, Missing, GLOBAL)
    k.ctxs[SCRATCH] = scratchCtx = Ctx(k, Missing, Missing, Missing, k.ctxs[GLOBAL], SCRATCH)
    k.scratch = scratchCtx
    k.tcrunner = TCInterpreter(k, scratchCtx)
    sm.frameForCtx(k.ctxs[GLOBAL])
    sm.frameForCtx(k.ctxs[SCRATCH])
    return k

class Res(object): pass

@coppertop
def evalPyInComments(res):
    commentTypes = []
    for token in res.tokens:
        if token.tag == LINE_COMMENT:
            pysrc = token.src[2:].strip()
            try:
                t = eval(pysrc)
                commentTypes.append(t)
            except Exception as ex:
                commentTypes.append(ex)
    res2 = Res()
    res2.tokens = res.tokens
    res2.types = res.types
    res2.result = res.result
    res2.error = res.error
    res2.commentTypes = commentTypes
    return res2

@coppertop
def errorMsg(res):
    return res.error.args[0]

@coppertop
def pace(k, src):
    return k.pace(src)

@coppertop
def pace_(k, src):
    return lambda : k.pace(src)

