# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************


import sys         
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from coppertop.pipe import *
from bones.lang.metatypes import S
from dm.core.types import T1, T2, tvfloat, pyfunc
from dm.finance.types import ccy, fx
from dm.testing import check, raises, equals


# <:fx:fx_&{{domestic:_ccy&T1,_ccy&T2}}>
#
# <:GBP:_ccy&"GBP">
# <:USD:_ccy&"USD">
#
# <:GBPUSD:fx(GBP,USD)>
#
# <:ccy:_ccy&num>
#
# <:rat:()

GBP = ccy['GBP'][tvfloat].setCoercer(tvfloat)
USD = ccy['USD'][tvfloat].setCoercer(tvfloat)
tvccy = ccy & tvfloat

GBPUSD = fx[S(domestic=GBP, foreign=USD)].nameAs('GBPUSD')[tvfloat].setCoercer(tvfloat)
fxT1T2 = fx[S(domestic=tvccy[T1], foreign=tvccy[T2])] & tvfloat


@coppertop(style=binary)
def addccy(a:tvccy[T1], b:tvccy[T1]) -> tvccy[T1]:
    return (a + b) | a._t

@coppertop(style=binary)
def addccy_(a, b) -> pyfunc:
    return lambda : (addccy(a, b))

@coppertop(style=binary)
def mul(dom:tvccy[T1], fx:fxT1T2, tByT) -> tvccy[T2]:
    assert dom._t == tvccy[tByT[T1]]
    return (dom * fx) | tvccy[tByT[T2]]

@coppertop(style=binary)
def mul(dom:tvccy[T2], fx:fxT1T2, tByT) -> tvccy[T1]:
    assert dom._t == tvccy[tByT[T2]]
    return (dom / fx) | tvccy[tByT[T1]]


def testFx():
    cacheId1, fits1, tByT1, distance1 = fitsWithin_(GBP, tvccy[T1])
    cacheId2, fits2, tByT2, distance2 = fitsWithin_(GBPUSD, fxT1T2)

    (100|GBP) >> mul >> (1.3|GBPUSD) >> addccy >> (20|USD) >> check >> equals >> (150|USD)
    (130|USD) >> mul >> (1.3|GBPUSD) >> check >> equals >> (100|GBP)


    (100|GBP) >> addccy_ >> (100|USD) >> check >> raises >> TypeError

    assert (100|GBP) >> addccy >> (100|GBP) == (200|GBP)




def main():
    testFx()


if __name__ == '__main__':
    main()
    print('pass')
