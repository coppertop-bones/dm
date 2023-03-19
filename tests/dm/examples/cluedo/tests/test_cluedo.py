# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#                               Contact the copyright holder for licensing terms.
#
# **********************************************************************************************************************


from coppertop.pipe import *
from dm.examples.cluedo.cards import *
from dm.examples.cluedo.core import one
from dm.examples.cluedo.algos import createBag, figureKnown, processResponses, processSuggestions
from dm.examples.cluedo.reports import rep1
from dm.examples.cluedo.core import cluedo_bag
import dm.pp
from groot import PP


@coppertop
def PP(bag:cluedo_bag) -> cluedo_bag:
    bag.pad >> rep1(_, bag.handId) >> PP
    return bag


def test():
    Me = Pl
    events = [

        [Me, Gr, Re, Ba], [Gr, Ba],
        [Gr, Mu, Re, Ki], Or - one,
        [Or, Or, Ro, Lo], Pe - one,
        [Pe, Gr, Da, Co], [Me, Da],

        [Me, Or, Wr, Co], Gr, Or, [Pe, Or],
        [Gr, Sc, Ca, Ki], Or, Pe, [Me, Ca],
        [Or, Pe, Ro, Ba], Pe, Me, Gr - one,
        [Pe, Mu, Re, Co], Me, Gr, Or - one,

        #     [Me, Sc, Wr, Bi], [Gr, Bi],         # Sc, Wr, Co
        #     [Gr, Sc, Le, Ba], Or, Pe, [Me, Le],

        #     [Or, Pe, Re, Co], Pe, Me, Gr,   # won

    ]

    like = {0 :100, 1 :10, 2 :5, 3 :0}
    bag = createBag(Me, [Ki, Di, Le, Da, Ca], {Gr: 5, Or: 4, Pe: 4}) \
          >> figureKnown >> events >> processResponses >> events >> processSuggestions(_, _, like) >> events
    bag >> PP



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')
