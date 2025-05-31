# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# see https://kotlinlang.org/docs/sequences.html#sequence

from coppertop.pipe import *
from coppertop.dm.core.types import bool, index

class IInputRange:
    @property
    def empty(self) -> bool:
        raise NotImplementedError()
    @property
    def front(self):
        raise NotImplementedError()
    def popFront(self):
        raise NotImplementedError()
    def moveFront(self):
        raise NotImplementedError()

    # assignable
    @front.setter
    def front(self, value):
        raise NotImplementedError()

    # python iterator interface - so we can use ranges in list comprehensions and for loops!!! ugh
    # this is convenient but possibly too convenient and it may muddy things hence the ugly name
    @property
    def _getIRIter(self):
        return IInputRange._Iter(self)

    class _Iter:
        def __init__(self, r):
            self.r = r
        def __iter__(self):
            return self
        def __next__(self):
            if self.r.empty: raise StopIteration
            answer = self.r.front
            self.r.popFront()
            return answer

@coppertop
def getIRIter(r):
    # the name is deliberately semi-ugly to discourage but not prevent usage - see comment above
    return r._getIRIter


class IForwardRange(IInputRange):
    def save(self):
        raise NotImplementedError()


class IBidirectionalRange(IForwardRange):
    @property
    def back(self):
        raise NotImplementedError()
    def moveBack(self):
        raise NotImplementedError()
    def popBack(self):
        raise NotImplementedError()

    # assignable
    @back.setter
    def back(self, value):
        raise NotImplementedError()


class IRandomAccessFinite(IBidirectionalRange):
    def moveAt(self, i: int):
        raise NotImplementedError()
    def __getitem__(self, i: index+slice):
        raise NotImplementedError()
    @property
    def length(self) -> index:
        raise NotImplementedError()

    # assignable
    def __setitem__(self, i: int, value):
        raise NotImplementedError()


class IRandomAccessInfinite(IForwardRange):
    def moveAt(self, i: int):
        raise NotImplementedError()

    def __getitem__(self, i: int):
        """Answers an element"""
        raise NotImplementedError()


class IOutputRange:
    def put(self, value):
        """Answers void"""
        raise NotImplementedError()




