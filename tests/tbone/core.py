# **********************************************************************************************************************
# Copyright (c) 2022 David Briant. All rights reserved.
# This file is part of py-bones. For licensing contact David Briant.
# **********************************************************************************************************************

import builtins

from coppertop.pipe import *
from bones.lang.structs import tv
from dm.core.types import num, index, txt, bool, litint, litdec, littxt, T1, T2, N

true = tv(bool, True)
false = tv(bool, False)

@coppertop(name='id')
def ID(x:T1) -> T1:
    return x

@coppertop(style=ternary, name='ifTrue:ifFalse:')
def ifTrueIfFalse(cond:bool, x:T1, y:T2) -> T1 + T2:
    if cond:
        return x
    else:
        return y

@coppertop
def isString(a:txt) -> bool:
    return True

@coppertop
def isString(a:index) -> bool:
    return False

@coppertop
def addOne(a:index) -> index:
    return a + 1

@coppertop
def addOne(a:txt) -> txt:
    return a + "One"


# @coppertop(style=ternary, name='ifTrue:ifFalse:')
# def collect(cond:bool, x:T1, y:T2) -> T1 | T2:
#     if cond:
#         return x
#     else:
#         return y


@coppertop(style=binary, name='+')
def add(a:num, b:num) -> num:
    return a + b

@coppertop(style=binary, name='+')
def add(a:index, b:index) -> index:
    return a + b

@coppertop(style=binary, name='+')
def add(a:litint, b:litint) -> litint:
    return a + b

@coppertop(style=binary, name='+')
def add(a:litdec, b:litdec) -> litdec:
    return a + b



@coppertop(style=binary, name='-')
def sub(a:num, b:num) -> num:
    return a - b



@coppertop(style=binary, name='*')
def mul(a:num, b:num) -> num:
    return a * b

@coppertop(style=binary, name='*')
def mul(a:index, b:index) -> index:
    return a * b

@coppertop(style=binary, name='*')
def mul(a:litint, b:litint) -> litint:
    return a * b

@coppertop(style=binary, name='*')
def mul(a:litdec, b:litdec) -> litdec:
    return a * b



@coppertop(style=binary, name='/')
def div(a:num, b:num) -> num:
    return a / b



@coppertop(style=binary, name='==')
def eq(a:num, b:num) -> bool:
    return a == b

@coppertop(style=binary, name='==')
def eq(a:index, b:index) -> bool:
    return a == b

@coppertop(style=binary, name='==')
def eq(a:txt, b:txt) -> bool:
    return a == b

@coppertop(style=binary, name='==')
def eq(a:bool, b:bool) -> bool:
    return a == b

@coppertop(style=binary, name='==')
def eq(a:litint, b:litint) -> bool:
    return a == b

@coppertop(style=binary, name='==')
def eq(a:litdec, b:litdec) -> bool:
    return a == b




@coppertop(style=binary, name='<')
def lt(a:num, b:num) -> bool:
    return a < b

@coppertop(style=binary, name='-')
def sub(a:index, b:index) -> index:
    return a - b

@coppertop(style=binary)
def join(a:txt, b:txt) -> txt:
    return a + b

@coppertop
def count(a:txt) -> num:
    return len(a)

@coppertop
def toBool(a:txt) -> bool:
    return builtins.bool(a) | bool

@coppertop
def toTxt(a:litint) -> txt:
    return str(a) | txt

@coppertop
def toTxt(a:littxt) -> txt:
    return a

@coppertop
def toIndex(a:litint) -> index:
    return a | index

@coppertop
def PP(x:txt) -> txt:
    print(x)
    return x

@coppertop
def PP(x:num) -> num:
    print(x)
    return x

@coppertop
def PP(x:index) -> index:
    print(x)
    return x

@coppertop(style=binary)
def arrayJoin(a:N**T1, b:N**T1) -> N**T1:
    return a + b