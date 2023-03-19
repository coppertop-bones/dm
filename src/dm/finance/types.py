# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************

BONES_NS = 'dm'

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from bones.lang.metatypes import BTAtom as _BTAtom


ccy = _BTAtom.ensure('ccy').setExplicit
fx = _BTAtom.ensure('fx').setExplicit



if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
