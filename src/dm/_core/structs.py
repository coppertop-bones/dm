# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
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

import sys

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import abc, numpy as np
from typing import Iterable
from collections import UserList, UserDict

from bones.core.errors import NotYetImplemented, ProgrammerError, PathNotTested
from bones.core.sentinels import Missing, Void
from bones.lang.metatypes import BType, fitsWithin, cacheAndUpdate
from bones.lang.utils import Constructors


__all__ = ['tvtuple', 'tvstruct', 'tvarray', 'tvlist', 'tvdict']

class tvtuple(object):
    def __init__(self):
        raise NotYetImplemented

class tvstruct(object):
    __slots__ = ['_pub', '_pvt']

    def __init__(self, *args_, **kwargs):
        super().__init__()
        super().__setattr__('_pvt', {})
        super().__setattr__('_pub', {})
        super().__getattribute__('_pvt')['_t'] = type(self)
        super().__getattribute__('_pvt')['_v'] = self

        constr, args = (args_[0][0], args_[1:]) if args_ and isinstance(args_[0], Constructors) else (Missing, args_)
        if len(args) == 0:
            # tvstruct(), tvstruct(**kwargs)
            if constr:
                super().__getattribute__('_pvt')['_t'] = constr
            if kwargs:
                super().__getattribute__('_pub').update(kwargs)
        elif len(args) == 1:
            # tvstruct(tvstruct), tvstruct(dictEtc)
            arg1 = args[0]
            if isinstance(arg1, tvstruct):
                # tvstruct(tvstruct)
                super().__getattribute__('_pvt')['_t'] = arg1._t
                super().__getattribute__('_pub').update(arg1._pub)
            elif isinstance(arg1, (dict, list, tuple, zip)):
                # tvstruct(dictEtc)
                super().__getattribute__('_pub').update(arg1)
                if constr:
                    super().__getattribute__('_pvt')['_t'] = constr
            else:
                # tvstruct(t), tvstruct(t, **kwargs)
                super().__getattribute__('_pvt')['_t'] = arg1
                if kwargs:
                    # tvstruct(t, **kwargs)
                    super().__getattribute__('_pub').update(kwargs)
        elif len(args) == 2:
            # tvstruct(t, tvstruct), tvstruct(t, dictEtc)
            arg1, arg2 = args
            if kwargs:
                # this needs sorting but I don't have time right now
                # came up for `PMF(Brown=30, Yellow=20, Red=20, Green=10, Orange=10, Tan=10)`
                # having two types (PMF and then dstruct do the construction so args is (dstruct, PMF)
                super().__getattribute__('_pvt')['_t'] = arg2
                super().__getattribute__('_pub').update(kwargs)
                # raise TypeError('No kwargs allowed when 2 args are provided')
                return None
            super().__getattribute__('_pvt')['_t'] = arg1
            if isinstance(arg2, tvstruct):
                # tvstruct(t, tvstruct)
                super().__getattribute__('_pub').update(arg2._pub)
            else:
                # tvstruct(t, dictEtc)
                super().__getattribute__('_pub').update(arg2)
        else:
            raise TypeError(
                'tvstruct(...) must be of form tvstruct(), tvstruct(**kwargs), tvstruct(tvstruct), tvstruct(dictEtc), ' +
                'tvstruct(t), tvstruct(t, **kwargs), tvstruct(t, tvstruct), tvstruct(t, dictEtc), '
            )

    def __asT__(self, t):
        super().__getattribute__('_pvt')['_t'] = t
        return self

    def __copy__(self):
        return tvstruct(self)

    def __getattribute__(self, f):
        if f[0:2] == '__':
            try:
                answer = super().__getattribute__(f)
            except AttributeError as e:
                answer = super().__getattribute__('_pvt').get(f, Missing)
            if answer is Missing:
                if f in ('__class__', '__len__', '__members__', '__getstate__'):
                    # don't change behaviour
                    raise AttributeError()
            return answer

        if f[0:1] == "_":
            if f == '_pvt': return super().__getattribute__('_pvt')
            if f == '_pub': return super().__getattribute__('_pub')
            if f == '_asT': return super().__getattribute__('__asT__')
            if f == '_t': return super().__getattribute__('_pvt')['_t']
            if f == '_v': return super().__getattribute__('_pvt')['_v']
            # if f == '_asT': return super().__getattribute__('_asT')
            if f == '_keys': return super().__getattribute__('_pub').keys
            if f == '_kvs': return super().__getattribute__('_pub').items
            if f == '_values': return super().__getattribute__('_pub').values
            if f == '_update': return super().__getattribute__('_pub').update
            if f == '_get': return super().__getattribute__('_pub').get
            # if names have been added e.g. by self['_10y'] allow access as long as not double entered
            pub = super().__getattribute__('_pub').get(f, Missing)
            pvt = super().__getattribute__('_pvt').get(f, Missing)
            if pub is Missing: return pvt
            if pvt is Missing: return pub
            raise AttributeError(f'public and private entries exist for {f}')
        # print(f)
        # I think we can get away without doing the following
        # if f == 'items':
        #     # for pycharm :(   - pycharm knows we are a subclass of dict so is inspecting us via items
        #     # longer term we may return a BTStruct instead of struct in response to __class__
        #     return {}.items
        v = super().__getattribute__('_pub').get(f, Missing)
        if v is Missing:
            raise AttributeError(f'{f} is Missing')
        else:
            return v

    def __setattr__(self, f, v):
        if f[0:1] == "_":
            if f == '_t_': return super().__getattribute__('_pvt').__setitem__('_t', v)
            # if f in ('_t', '_v', '_pvt', '_pub'): raise AttributeError(f"Can't set {f} on tvstruct")
            if f in ('_pvt', '_pub'): raise AttributeError(f"Can't set {f} on tvstruct")
            return super().__getattribute__('_pvt').__setitem__(f, v)
        return super().__getattribute__('_pub').__setitem__(f, v)

    def __getitem__(self, fOrFs):
        if isinstance(fOrFs, (list, tuple)):
            kvs = {f: self[f] for f in fOrFs}
            return tvstruct(self._t, kvs)
        else:
            return super().__getattribute__('_pub').__getitem__(fOrFs)

    def __setitem__(self, f, v):
        if isinstance(f, str):
            if f[0:1] == "_":
                if f in ('_pvt', '_pub', '_keys', '_kvs', '_values', '_update', '_get'):
                    raise AttributeError(f'name {f} is reserved for use by tvstruct')
                # if f in super().__getattribute__('_pvt'):
                #     raise AttributeError(f'name {f} is already in pvt use')
        super().__getattribute__('_pub').__setitem__(f, v)

    def __delitem__(self, fOrFs):
        if isinstance(fOrFs, (list, tuple)):
            for f in fOrFs:
                super().__getattribute__('_pub').__delitem__(f)
        else:
            super().__getattribute__('_pub').__delitem__(fOrFs)

    def __contains__(self, f):
        return super().__getattribute__('_pub').__contains__(f)

    def __call__(self, **kwargs):
        _pub = super().__getattribute__('_pub')
        for f, v in kwargs.items():
            _pub.__setitem__(f, v)
        return self

    def __dir__(self) -> Iterable[str]:
        # return super().__getattribute__('_pub').keys()
        return [k for k in super().__getattribute__('_pub').keys() if isinstance(k, str)]

    def __repr__(self):
        _pub = super().__getattribute__('_pub')
        _t = super().__getattribute__('_pvt')['_t']
        itemStrings = (f"{str(k)}={repr(v)}" for k, v in _pub.items())

        if type(_t) is abc.ABCMeta or _t is tvstruct:
            name = _t.__name__
        else:
            name = str(self._t)
        rep = f'{name}({", ".join(itemStrings)})'
        return rep

    def __len__(self):
        return len(super().__getattribute__('_pub'))

    def __eq__(self, rhs):  # self == rhs
        if isinstance(rhs, dict):
            raise NotYetImplemented()
        elif isinstance(rhs, tvstruct):
            return self._kvs() == rhs._kvs()
        else:
            return False

    def __iter__(self):
        return iter(super().__getattribute__('_pub').values())



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

    def __ror__(self,
                arg):  # disabled so don't get confusing error messages for type | arg (we want a doesNotUnderstand)
        return NotImplemented

    def __repr__(self):
        if type(self._t) is type:
            typename = self._t.__name__
        else:
            typename = str(self._t)
        return f'{self._t}({np.array2string(self)})'


class tvlist(UserList):
    def __init__(self, *args_):
        constr, args = (args_[0][0], args_[1:]) if args_ and isinstance(args_[0], Constructors) else (Missing, args_)
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, tvlist):
                # tvlist(tvlist)
                super().__init__(arg._v)
                self._t = arg._t
            elif isinstance(arg, BType):
                # tvlist(<BType>)
                super().__init__()
                self._t = arg
            else:
                raise TypeError("Can't create tvlist without type information")
        elif len(args) == 2:
            # tvlist(t, iterable)
            arg1, arg2 = args
            super().__init__(arg2)
            self._t = arg1
        elif len(args) == 3:
            # tvlist(dseq, t, iterable)
            arg1, arg2, arg3 = args
            assert isinstance(arg1, Constructors)
            super().__init__(arg3)
            self._t = arg2
        else:
            raise TypeError("Invalid arguments to tvlist constructor")

    @property
    def _v(self):
        return self.data

    def _asT(self, t):
        self._t = t
        return self

    def __repr__(self):
        itemStrings = (f"{str(e)}" for e in self.data)
        t = self._t
        if type(t) is abc.ABCMeta or t is tvlist:
            name = self._t.__name__
        else:
            name = str(self._t)
        rep = f'{name}({", ".join(itemStrings)})'
        return rep

    def __eq__(self, other):
        if isinstance(other, tvlist):
            return self._t == other._t and self.data == other.data
        else:
            return False

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self._t, self.data[i])
        else:
            return self.data[i]


class tvdict(UserDict):
    __slots__ = ['_t', 'data']

    def __new__(cls, *args_, **kwargs):
        constr, args = (args_[0][0], args_[1:]) if args_ and isinstance(args_[0], Constructors) else (Missing, args_)
        if len(args) == 0:
            if not kwargs:
                # tvdict()
                instance = super().__new__(cls)
                instance.data = {}
                instance._t = constr  # maybe use TBI in the future
            else:
                # tvdict(a=1, b=2)
                instance = super().__new__(cls)
                instance.data = {}
                instance._t = constr  # maybe use TBI in the future
                instance.update(kwargs)
                raise PathNotTested()
        elif len(args) == 1:
            arg1 = args[0]
            if not kwargs:
                if isinstance(arg1, BType):
                    # tvdict(t)
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
                    # tvdict(t, a=1, b=2)
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