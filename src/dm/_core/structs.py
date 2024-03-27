# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
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

import abc, numpy as np
from collections import UserList, UserDict

from bones.core.errors import NotYetImplemented, ProgrammerError, PathNotTested
from bones.core.sentinels import Missing, Void
from bones.lang.metatypes import BType, fitsWithin, cacheAndUpdate
from bones.lang.utils import Constructors


__all__ = ['tvarray', 'tvseq', 'tvmap']




# see https://en.wikipedia.org/wiki/Tensor
# https://medium.com/@quantumsteinke/whats-the-difference-between-a-matrix-and-a-tensor-4505fbdc576c

# tvarray is not a tensor - see Dan Fleisch - https://www.youtube.com/watch?v=f5liqUk0ZTw&t=447s
# I understand a tensor to be a n dimensional matrix of coefficients with each coefficient corresponding to m vectors in and

# tensors are combination of components and basis vectors

# a scalar is a tensor of rank 0 - size is 1 x 1 x 1 etc

# a vector is a tensor of rank 1 - size is rank x dimensions,
# e.g for 3 dimensions
# [Ax,           (0,0,1)
#  Ab,           (0,1,0)
#  Ac]           (1,0,0)

# a matrix is a tensor of rank 2 - size is n x n for n dimensions
# e.g. for 2 dimensions
# [Axx, Axy;           (0,1)&(0,1), (0,1)&(1,0)
#  Ayx, Ayy]           (1,0)&(0,1), (1,0)&(1,0)

# a tensor is therefore not a data structure but a data structure with a context

class nd_(np.ndarray):
    def __rrshift__(self, arg):  # so doesn't get in the way of arg >> func
        return NotImplemented

    def __rshift__(self, arg):  # so doesn't get in the way of func >> arg
        return NotImplemented


class tvarray(nd_):

    def __new__(cls, *args_, **kwargs):
        constr, args = (args_[0][0], args_[1:]) if args_ and isinstance(args_[0], Constructors) else (Missing, args_)
        if len(args) == 0:
            # we have a null tuple
            raise NotYetImplemented()
        elif len(args) == 1:
            if constr:
                instance = np.asarray(args[0], **kwargs).view(cls)
                instance._t_ = constr
            else:
                raise SyntaxError()
        elif len(args) == 2:
            arg1, arg2 = args
            if isinstance(arg1, BType):
                # tvarray(t, iterable)
                try:
                    instance = np.asarray(arg2, **kwargs).view(cls)
                    instance._t_ = arg1
                except Exception as ex:
                    print(f'{arg1}    {arg2} {ex}')
                    raise ex
            else:
                raise SyntaxError()
        else:
            raise SyntaxError()
        return instance

    def __array_finalize__(self, instance):
        # see - https://numpy.org/doc/stable/user/basics.subclassing.html
        if instance is None: return
        self._t_ = getattr(instance, '_t_', tvarray)

    @property
    def _v(self):
        return self

    @property
    def _t(self):
        return self._t_

    def _asT(self, t):
        self._t_ = t
        return self

    def __or__(self, arg):  # so doesn't get in the way of arg | type
        return NotImplemented

    def __ror__(self, arg):  # disabled so don't get confusing error messages for type | arg (we want a doesNotUnderstand)
        return NotImplemented

    def __repr__(self):
        if type(self._t) is type:
            typename = self._t.__name__
        else:
            typename = str(self._t)
        return f'{self._t}({np.array2string(self)})'


class tvseq(UserList):
    def __init__(self, *args_):
        constr, args = (args_[0][0], args_[1:]) if args_ and isinstance(args_[0], Constructors) else (Missing, args_)
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, tvseq):
                # tvseq(tvseq)
                super().__init__(arg._v)
                self._t = arg._t
            elif isinstance(arg, BType):
                # tvseq(<BType>)
                super().__init__()
                self._t = arg
            else:
                raise TypeError("Can't create tvseq without type information")
        elif len(args) == 2:
            # tvseq(t, iterable)
            arg1, arg2 = args
            super().__init__(arg2)
            self._t = arg1
        elif len(args) == 3:
            # tvseq(dseq, t, iterable)
            arg1, arg2, arg3 = args
            assert isinstance(arg1, Constructors)
            super().__init__(arg3)
            self._t = arg2
        else:
            raise TypeError("Invalid arguments to tvseq constructor")

    @property
    def _v(self):
        return self.data

    def _asT(self, t):
        self._t = t
        return self

    def __repr__(self):
        itemStrings = (f"{str(e)}" for e in self.data)
        t = self._t
        if type(t) is abc.ABCMeta or t is tvseq:
            name = self._t.__name__
        else:
            name = str(self._t)
        rep = f'{name}({", ".join(itemStrings)})'
        return rep

    def __eq__(self, other):
        if isinstance(other, tvseq):
            return self._t == other._t and self.data == other.data
        else:
            return False

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self._t, self.data[i])
        else:
            return self.data[i]


class tvmap(UserDict):
    __slots__ = ['_t', 'data']

    def __new__(cls, *args_, **kwargs):
        constr, args = (args_[0][0], args_[1:]) if args_ and isinstance(args_[0], Constructors) else (Missing, args_)
        if len(args) == 0:
            if not kwargs:
                # tvmap()
                instance = super().__new__(cls)
                instance.data = {}
                instance._t = constr  # maybe use TBI in the future
            else:
                # tvmap(a=1, b=2)
                instance = super().__new__(cls)
                instance.data = {}
                instance._t = constr  # maybe use TBI in the future
                instance.update(kwargs)
                # raise PathNotTested()
        elif len(args) == 1:
            arg1 = args[0]
            if not kwargs:
                if isinstance(arg1, BType):
                    # tvmap(t)
                    instance = super().__new__(cls)
                    instance.data = {}
                    instance._t = arg1
                    raise PathNotTested()
                else:
                    # assume arg1 can be used as a dictionary
                    instance = super().__new__(cls)
                    instance.data = {}
                    instance._t = constr  # maybe use TBI in the future
                    instance.update(arg1)
            else:
                if isinstance(arg1, BType):
                    # tvmap(t, a=1, b=2)
                    instance = super().__new__(cls)
                    instance.data = {}
                    instance._t = arg1
                    instance.update(kwargs)
                else:
                    raise PathNotTested()
                    raise SyntaxError(
                        f"if kwargs are given and just one arg then it must be a BType - got {arg1} instead")
        elif len(args) == 2:
            arg1, arg2 = args
            if not kwargs:
                if isinstance(arg1, BType):
                    # assume arg2 can be used to construct a dictionary
                    instance = super().__new__(cls)
                    instance.data = {}
                    instance._t = arg1
                    instance.update(arg2)
                    raise PathNotTested()
                else:
                    raise PathNotTested()
                    raise SyntaxError("do a better error message")
            else:
                raise NotYetImplemented("getting bored!")
        else:
            # too many args
            raise PathNotTested()
            raise SyntaxError("too many args")
        return instance

    def __init__(self, *args, **kwargs):
        pass  # we handle construction in __new__

    @property
    def _v(self):
        return self.data

    def _asT(self, t):
        self._t = t
        return self
