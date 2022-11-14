# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
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

# SHOULDDO handle locales


import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import datetime
from bones.core.sentinels import Missing
from coppertop.pipe import *
from dm.core.types import txt, index, date, offset


@coppertop
def year(x):
    return x.year

@coppertop
def month(x):
    return x.month

@coppertop
def day(x):
    return x.day

@coppertop
def hour(x):
    return x.hour

@coppertop
def minute(x):
    return x.minute

@coppertop
def second(x):
    return x.second

@coppertop
def weekday(x):
    return x.weekday()

@coppertop
def weekdayName(x):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x]

@coppertop
def weekdayName(x, locale):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x]

@coppertop
def weekdayLongName(x):
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x]

@coppertop
def weekdayLongName(x, locale):
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x]

@coppertop
def monthName(month):
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month - 1]

@coppertop
def monthName(month, locale):
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month - 1]

@coppertop
def monthLongName(month):
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month - 1]

@coppertop
def monthLongName(month, locale):
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month - 1]

@coppertop
def toCTimeFormat(simpleFormat:txt) -> txt:

    # a little care is needed here to avoid clashes between formats
    answer = simpleFormat
    answer = answer.replace('DDDD', '%A')
    answer = answer.replace('DDD', '%a')
    answer = answer.replace('DD', '%d')
    answer = answer.replace('D', '%e')

    answer = answer.replace('YYYY', '%Y')
    answer = answer.replace('YY', '%y')

    answer = answer.replace('ms', '%f')                             # Microsecond as a decimal number, zero-padded to 6 digits
    answer = answer.replace('us', '%f')

    answer = answer.replace('mm', '%M')
    answer = answer.replace('m', '%-M')

    answer = answer.replace('ms', '%f')                             # Microsecond as a decimal number, zero-padded to 6 digits
    answer = answer.replace('us', '%f')

    answer = answer.replace('ss', '%S')
    answer = answer.replace('s', '%<single-digit-second>')

    answer = answer.replace('MMMM', '%B')                           # Month as locale’s full name
    answer = answer.replace('MMM', '%b')                            # Month as locale’s abbreviated name
    answer = answer.replace('MM', '%m')                             # Month as a zero-padded decimal number
    answer = answer.replace('M', '%<single-digit-month>')
    answer = answer.replace('%%<single-digit-month>', '%M')
    answer = answer.replace('%-%<single-digit-month>', '%-M')

    answer = answer.replace('hh', '%H')                             # 0 padded 12 hour
    answer = answer.replace('h', '%-H')
    answer = answer.replace('HH', '%I')                             # 0 padded 24 hour
    answer = answer.replace('H', '%-I')
    answer = answer.replace('%%-I', '%H')
    answer = answer.replace('%-%-I', '%-H')

    answer = answer.replace('TT', '%p')                             # Locale’s equivalent of either AM or PM

    answer = answer.replace('city', '%<city>')
    answer = answer.replace('z/z', '%<IANA>')
    answer = answer.replace('z', '%Z')                              # Time zone name (empty string if the object is naive)
    return answer


@coppertop(style=binary)
def addDays(d:date, n) -> date:
    return d + datetime.timedelta(n)


MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6


@coppertop(style=binary)
def dateOnOrAfter(d: date, weekday: offset) -> date:
    wd = d.weekday()
    if wd == weekday:
        return d
    else:
        return d >> addDays >> ((weekday - wd) % 7)


@coppertop
def firstOfMonth(d: date) -> date:
    return d >> addDays >> -(d.day - 1)


@coppertop
def thirdWednesday(d: date) -> date:
    return d >> firstOfMonth >> dateOnOrAfter >> WED >> addDays >> 14


@coppertop
def firstThursday(d):
    return d >> firstOfMonth >> dateOnOrAfter >> THU


@coppertop
def thirdWednesdayOnOrAfter(d: date) -> date:
    fom = d >> firstOfMonth
    thirdWed = fom >> dateOnOrAfter >> WED >> addDays >> 14
    if thirdWed >= d:
        return thirdWed
    else:
        return fom >> addMonths >> 1 >> dateOnOrAfter >> WED >> addDays >> 14


@coppertop(style=binary)
def addMonths(d: date, months) -> date:
    # I can't think of a situation where we mindlessly add months - i.e. we have to think about how to handle dates after the 28
    # thus we allow an error if the day is invalid as it means the client code needs a bit more thinking through
    m = d.month + months
    if m > 12:
        m, yInc = m % 12, m // 12
        return datetime.date(d.year + yInc, m, d.day)
    else:
        return datetime.date(d.year, m, d.day)


@coppertop
def nextIMM(d: date) -> date:
    m = d >> month
    if m in (3, 6, 9, 12):
        nextIMM = d >> thirdWednesdayOnOrAfter
        if d < nextIMM:
            return nextIMM
        else:
            return d >> firstOfMonth >> addMonths >> 3 >> dateOnOrAfter >> WED >> addDays >> 14
    elif m in (1, 4, 7, 10):
        return d >> firstOfMonth >> addMonths >> 2 >> dateOnOrAfter >> WED >> addDays >> 14
    else:
        return d >> firstOfMonth >> addMonths >> 1 >> dateOnOrAfter >> WED >> addDays >> 14


_monthFromFuturesCode = dict(F=1, G=2, H=3, J=4, K=5, M=6, N=7, Q=8, U=9, V=10, X=11, Z=12)
_futuresCodeFromMonth = ("F", "G", "H", "J", "K", "M", "N", "Q", "U", "V" ,"X", "Z")

@coppertop
def monthFromFutureCode(monthCode:txt):
    return _monthFromFuturesCode[monthCode]

@coppertop
def futuresCodeFromMonth(m) -> txt:
    return _futuresCodeFromMonth[m - 1]


