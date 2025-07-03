# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

import datetime

from coppertop.pipe import *
from coppertop.dm.core import keys_, first, kvs, drop
from coppertop.dm.examples.cluedo.core import *
from coppertop.dm.examples.cluedo.core import one
from coppertop.dm.examples.cluedo.algos import createHelper, figureKnown, processResponses, processSuggestions1, \
    processSuggestions2
from coppertop.dm.examples.cluedo.reports import PP, rep2



def game1():
    deal, events = game1_data()
    Me, hand = deal >> kvs >> first
    otherHandSizesById = deal >> drop >> Me
    events = [
        [Or, Bi],
        [Or, Mu],
        [Mu, Re],
        [Pl, Ca],
    ] + events

    createHelper(Me, hand, otherHandSizesById)  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP

def game1_data():
    return (
        {Sc: [Ha, Co, Sc], Pe: 3, Pl: 3, Gr: 3, Mu: 3, Or: 3},
        [
            [Gr, Pe, Ro, Bi], Mu, Or - one,
            [Mu, Mu, Ro, Li], Or - one,
            [Or, Gr, Ca, Ba], Sc, Pe - one,
            [Sc, Or, Da, Ki], Pe, [Pl, Da],
            [Pe, Mu, Re, Co], Pl, Gr, Mu - one,
            [Pl, Sc, Wr, Ba], Gr, Mu, Or, [Sc, Sc],
            [Gr, Pl, Le, Di], Mu - one,
            [Mu, Pe, Ro, Li], Or, Sc, Pe - one,
            [Or, Pl, Le, Di], Sc, Pe - one,
            [Sc, Pe, Wr, Ba], [Pe, Pe],
            [Pe, Or, Da, Ki], Pl - one,
            [Pl, Pl, Re, Ki], Gr, Mu - one,
            [Gr, Sc, Wr, Ha], Mu, Or, [Sc, Sc],
            [Mu, Gr, Le, St], Or, Sc, Pe - one,
            [Or, Mu, Ca, St], Sc, Pe, Pl - one,
            [Sc, Or, Sc, St], Pe, Pl, [Gr, St],

            [Pe, Or, Ro, Di], Pl - one,
            [Pl, Pl, Wr, St], Gr - one,
            [Gr, Pl, Wr, Ha], Mu, Or, [Sc, Ha],
            [Mu, Pl, Re, Li], Or, Sc, Pe, Pl, Gr,
        ]
    )



def game2():
    deal, events = game2_data()
    Me, hand = deal >> kvs >> first
    otherHandSizesById = deal >> drop >> Me
    events = [
        [Sc, Pl],
        [Pe, Ha],
        [Sc, Sc],
        [Or, Mu],
    ] + events

    createHelper(Me, hand, otherHandSizesById)  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP

def game2_data():
    return (
        {Pl: [Gr, Ro, Lo], Gr: 3, Mu: 3, Or: 3, Sc: 3, Pe: 3},
        [
            [Pl, Mu, Da, Di], Gr, [Mu, Di],
            [Gr, Gr, Da, Li], Mu, Or, Sc, Pe, [Pl, Gr],
            [Mu, Pl, Da, Lo], Or, Sc - one,
            [Or, Sc, Da, Ha], Sc - one,
            [Sc, Or, Da, Ha], Pe - one,
            [Pe, Or, Ca, Ba], Pl, Gr - one,

            [Pl, Or, Ca, Lo], [Gr, Or],
            [Gr, Pe, Ca, Bi], Mu, Or, Sc, Pe - one,
            [Mu, Sc, Da, Ha], Or, Sc - one,
            [Or, Pl, Da, Ha], Sc - one,
            [Sc, Or, Da, Di], Pe, Pl, Gr - one,
            [Pe, Mu, Da, Bi], Pl, Gr, Mu, Or - one,

            [Pl, Gr, Ro, Li], [Gr, Li],  # We won?
        ]
    )



def game3():
    deal, events = game3_data()
    Me, hand = deal >> kvs >> first
    otherHandSizesById = deal >> drop >> Me
    events = [
        [Or, Ro],
    ] + events

    createHelper(Me, hand, otherHandSizesById)  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP

def game3_data():
    return (
        {Pl: [St, Li, Di, Wr, Sc], Gr: 5, Or: 4, Pe: 4},
        [
            [Gr, Mu, Da, Bi], Or - one,
            [Or, Gr, Re, Ba], Pe - one,
            [Pe, Gr, Wr, Ki], [Pl, Wr],
            [Pl, Gr, Da, Ba], [Gr, Gr],

            [Gr, Pe, Le, Bi], Or, Pe - one,
            # Or misses a go
            [Pe, Sc, Da, Li], [Pl, Sc],
            [Pl, Pe, Le, Bi], Gr, Or, [Pe, Pe],

            [Gr, Gr, Ro, Li], Or - one,
            [Or, Pl, Wr, Di], Pe, [Pl, Wr],
            [Pe, Pl, Le, Bi], Pl, Gr, Or,
        ]
    )



def game4():
    deal, events = game4_data()
    Me, hand = deal >> kvs >> first
    otherHandSizesById = deal >> drop >> Me
    events = [
        [Or, Ro],
    ] + events

    createHelper(Me, hand, otherHandSizesById)  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP

    #                                   Me          Green       Orchid      Peacock
    # Green            -                   X           -           -           -
    # Mustard          -                   X           -           -           -
    # Orchid           X                   -           -           -           -
    # Peacock          -                   X           -           -           -
    # Plum             -         L1        -           -           -           X L1
    # Scarlet          -                   -           -           X           -
    # ----
    # Candlestick        4                 -           ?           ?           ?
    # Dagger             2    S2 L1     2  -        1  -           -        2  ? L1
    # Lead Pipe          3    S1 L4        -        1  ?        1  -           ? L4
    # Revolver           4    S1 L2        -        1  ?           ? L2        ?
    # Rope               3    S1           -           ?        1  ?           -
    # Wrench           -                   X           -           -           -
    # ----
    # Kitchen            4    S1           -           ?           ?        1  ?
    # Ballroom           3    S2 L2        -        1  ?           -        1  ? L2
    # Conservatory       4                 -           ?           ?           ?
    # Billiard Room      4    S1 L2        -           ?        1  ?           ? L2
    # Library            3    S1           -           ?        1  ?           -
    # Study              3    S2 L2        -        1  ?        1  ? L2        -
    # Hall               4                 -           ?           ?           ?
    # Lounge           -                   X           -           -           -
    # Dining Room        2    S1 L1     2  -        1  -           -        1  ? L1

def game4_data():
    return (
        {Pl: [Lo, Wr, Pe, Mu, Gr], Gr: 5, Or: 4, Pe: 4},
        [
            [Gr, Pl, Da, Di], Or, Pe - one,
            [Or, Mu, Le, Bi], Pe - one,
            [Pe, Mu, Wr, Ba], [Pl, Mu],
            [Pl, Sc, Da, Di], Gr, [Or, Sc],

            [Gr, Pe, Le, Ba], Or, Pe - one,
            [Or, Gr, Ro, Li], Pe, [Pl, Gr],
            [Pe, Gr, Da, Ki], [Pl, Gr],
            [Pl, Pl, Da, Di], Gr, Or, [Pe, Pl],

            [Gr, Or, Re, St], Or - one,
            [Or, Mu, Wr, St], Pe, [Pl, Mu],
            [Pe, Or, Da, Di], Pl, Gr, Or,
        ]
    )


def game5():
    deal, events = game5_data()
    Me, hand = deal >> kvs >> first
    otherHandSizesById = deal >> drop >> Me
    events = [
        [Or, Ro],
    ] + events

    like = {0:100, 1:10, 2:5, 3:0}
    helper = createHelper(Me, hand, otherHandSizesById)  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> processSuggestions1(_, _, like) >> events
    helper >> PP

def game5_data():
    return (
        {Pl: [Ki, Di, Le, Da, Ca], Gr: 5, Or: 4, Pe: 4},
        [
            [Pl, Gr, Re, Ba], [Gr, Ba],
            [Gr, Mu, Re, Ki], Or - one,
            [Or, Or, Ro, Lo], Pe - one,
            [Pe, Gr, Da, Co], [Pl, Da],

            [Pl, Or, Wr, Co], Gr, Or, [Pe, Or],
            [Gr, Sc, Ca, Ki], Or, Pe, [Pl, Ca],
            [Or, Pe, Ro, Ba], Pe, Pl, Gr - one,
            [Pe, Mu, Re, Co], Pl, Gr, Or - one,

            [Pl, Sc, Wr, Bi], [Gr, Bi],  # Sc, Wr, Co
            [Gr, Sc, Le, Ba], Or, Pe, [Pl, Le],
            [Or, Pe, Re, Co], Pe, Pl, Gr,  # Or won
        ]
    )


def game6():
    deal, events = game6_data()
    Me, hand = deal >> kvs >> first
    otherHandSizesById = deal >> drop >> Me
    events = [
        [Or, Wr],
        [Mu, Ha],
        [Or, Sc],
    ] + events

    like = {0:100, 1:10, 2:5, 3:0}
    helper = createHelper(Me, hand, otherHandSizesById)  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> processSuggestions1(_, _, like) >> events
    helper >> rep2 >> PP

def game6_data():
    return (
        {Pl: [Ba, Pl, Pe, Mu], Gr: 4, Mu: 4, Or: 3, Pe: 3},
        [
            [Pe, Sc, Ro, Ki], Pl, Gr - one,
            [Pl, Mu, Re, St], Gr, [Mu, Re],
            [Gr, Gr, Ca, Ba], Mu, Or, Pe, [Pl, Ba],
            [Mu, Pe, Wr, Li], Or - one,
            [Or, Or, Da, Di], Pl, Gr - one,

            [Pe, Pe, Le, Bi], [Pl, Pe],
            [Pl, Gr, Ca, Li], Gr, Mu, Or, [Pe, Li],
            [Gr, Sc, Ca, Bi], Mu, Or - one,
            [Mu, Sc, Ca, Bi], Or - one,
            [Or, Gr, Ca, Ha], Pl, Gr, Mu - one,

            [Pe, Gr, Ca, Li], Pl, Gr, Or,
            [Pl, Pe, Ca, St], Gr, Mu, Or, [Pe, St],
            [Gr, Gr, Ro, Bi], Mu, Or, Pe, Pl,  # Gr won
        ]
    )


def game7():
    deal, events = game7_data()
    Me, hand = deal >> kvs >> first
    otherHandSizesById = deal >> drop >> Me
    events = [
        [Pe, Ha],
        [Pe, Or],
        [Mu, Wr],
    ] + events

    like = {0:100, 1:10, 2:5, 3:0}
    helper = createHelper(Me, hand, otherHandSizesById)  \
        >> figureKnown >> events \
        >> processResponses >> events \
        >> processSuggestions2(_, _, like) >> events
    helper >> rep2 >> PP

def game7_data():
    return (
        {Pl: [St, Di, Co, Ca], Gr: 4, Mu: 4, Or: 3, Pe: 3},
        [
            [Pl, Gr, Da, Ha], [Gr, Gr],
            [Gr, Mu, Wr, Ha], Mu - one,
            [Mu, Sc, Ro, Lo], Or, Pe, Pl, Gr - one,
            [Or, Pl, Re, Li], Pe - one,
            [Pe, Gr, Ca, St], [Pl, Ca],

            [Pl, Sc, Ro, Li], [Gr, Ro],
            [Gr, Or, Da, St], Mu, Or, Pe - one,
            [Mu, Sc, Ca, Ha], Or, Pe - one,
            [Or, Gr, Wr, Li], Pe, Pl, Gr - one,

            [Pe, Pe, Re, Ki], Pl, Gr - one,
            [Pl, Sc, Wr, Bi], [Gr, Sc],
            [Gr, Mu, Le, Li], Mu - one,
            [Mu, Sc, Da, Bi], Or, Pe, Pl, Gr - one,
            [Or, Mu, Da, Bi], Pe, Pl, Gr, Mu,  # Or won
        ]
    )


# if someone suggests a card that I know they have it increases the likelihood of them not having the other two cards


def main():
    game6()
    t1 = datetime.datetime.now()
    # game7()
    t2 = datetime.datetime.now()
    f'\n{(t2 - t1).microseconds / 1000}ms' >> PP

    # import coppertop._singletons
    # f'{int(coppertop._singletons._numNotCopied / (coppertop._singletons._numNotCopied + coppertop._singletons._numCopies)*100)}%' >> PP

    # totalCombs =
    #     num(people) - num(my people) - num(TBI people)
    #     * num(weapons) - num(my weapons) - num(TBI weapons)
    #     * num(rooms) - num(my rooms) - num(TBI rooms)
    #     * perms (remaining cards, num other players)

if __name__ == '__main__':
    main()
