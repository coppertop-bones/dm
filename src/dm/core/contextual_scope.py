# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
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

BONES_NS = ''

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop._scopes import _ContextualScopeManager, _MutableContextualScope, _CoWScope, ANON_NAME
from coppertop.pipe import *
from bones.core.errors import NotYetImplemented, CPTBError
from bones.core.sentinels import Missing
from dm.core.types import txt


@coppertop
def push(underscore:_ContextualScopeManager):
    # create an anonymous scope and push it - cannot be switched only popped
    child = _MutableContextualScope(underscore, underscore._current)
    underscore._current = child
    return child


@coppertop
def pushCow(underscore:_ContextualScopeManager):
    raise NotYetImplemented()


@coppertop
def pop(underscore:_ContextualScopeManager):
    if underscore._current._name is Missing:
        raise CPTBError("Cannot pop a named context - use switch instead")
    underscore._current = underscore._current._parent
    return underscore._current


@coppertop(style=binary)
def new(underscore:_ContextualScopeManager, name:txt):
    # return a child scope that inherits from the current one without pushing it
    if (current := underscore._namedScopes.get(name, Missing)) is Missing:    # numpy overides pythons truth function in an odd way
        current = underscore._current = _MutableContextualScope(underscore._current._manager, underscore._current, name)
    return current


@coppertop(style=binary)
def newCow(underscore:_ContextualScopeManager, name:txt):
    # return a child cow scope that inherits from the current one without pushing it
    raise NotYetImplemented()


@coppertop(style=binary)
def switch(underscore:_ContextualScopeManager, contextualScopeOrName):
    if underscore._current._name is Missing:
        raise CPTBError("Cannot switch from an anonymous context - use pop instead")
    if isinstance(contextualScopeOrName, _MutableContextualScope):
        underscore._current = contextualScopeOrName
        return contextualScopeOrName
    else:
        underscore._current = underscore._namedScopes[contextualScopeOrName]
        return underscore._current


@coppertop
def root(underscore:_ContextualScopeManager):
    root = underscore._parent
    while root is not (root := root._parent): pass
    return root


@coppertop
def name(underscore:_ContextualScopeManager):
    current = underscore._current
    for k, v in underscore._namedScopes.items():
        if v is current:
            return k
    return ANON_NAME


@coppertop
def names(underscore:_ContextualScopeManager):
    return list(underscore._namedScopes.keys())
