# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************



from coppertop.pipe import *
from bones.core.sentinels import Missing
from dm.testing import check, equals
from dm.core.frame import sortBy, collect, byRow, total_, mean_, first_, \
    last_, count_, by_, take, collect_, by, gather, where
from dm.core.types import dframe



def test_sortBy():
    a = dframe(a=[1,2,1,2,1,2],b=[2,2,2,1,1,1],c=['a','b','c','d','e','f'])
    r = a >> sortBy >> ['b', 'a']


def test_sql_style():
    context.testcase = 'collect using byRow and whole table'
    f = dframe(a=[1,2,1,2,1,2], b=[2,2,2,1,1,1], c=['a','b','c','d','e','f'])
    f >> collect >> [
        'a',
        'b',
        {'c' : (lambda r: r['a'] + r['b']) >> byRow,
         'd' :  lambda t: [a * b for (a,b) in zip(f['A'] + f['B'])]}
    ] >> check >> equals >> dframe(
        a=[1,2,1,2,1,2],
        b=[2,2,2,1,1,1],
        c=[3,4,3,3,2,3],
        d=[2,4,2,2,1,2]
    )

    context.testcase = 'by & collect, both eager and deferred with gather, and some deferred reducers'
    f >> by >> 'a' >> collect >> ['a', total_('a'), mean_('b'), first_('c'), last_('c'), count_('d')] \
        >> take >> 't1' >> check >> equals >> (f >> by_ >> 'a' >> collect_ >> total_('a') >> gather)


    context.testcase = 'where'
    f >> where >> byRow(lambda r: r['a'] == 1)




def main():
    with context(testcase=Missing):
        test_sql_style()
        test_sortBy()


if __name__ == '__main__':
    main()
    print('pass')




