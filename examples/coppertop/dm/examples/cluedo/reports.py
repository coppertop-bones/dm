# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

from coppertop.pipe import *
from coppertop._scopes import _CoWProxy
from coppertop.dm.core.aggman import keys, collect, count, first, values, join, joinAll, without, interleave, values_
from coppertop.dm.flux import append
from coppertop.dm.core.conv import to
from coppertop.dm.core.text import pad as pad_
from coppertop.dm.core.types import txt, N, pylist, pydict, dseq, dstruct

from coppertop.dm.examples.cluedo.utils import hjoin, PP
from coppertop.dm.examples.cluedo.core import Card, people, weapons, rooms, TBI, cluedo_pad, YES, NO, MAYBE, display_table, \
    cluedo_bag


# coercers - # OPEN: can these b§e sensibly defaulted in metatypes or templated?
(Card^txt).setCoercer(makeFn)
(N**Card)[dseq].setCoercer(dseq)


@coppertop
def ppCell(cell, stat, cfg):
    txtSuggest = ('' if stat.tbi != MAYBE else (str(cell.suggestions >> count) if cell.suggestions else "")) >> pad_(_, dict(center=2))
    txtState = cell.state #(YES if cell.state == YES else ' ') if stat.tbi == YES else cell.state
    txtLike = f'{int(derefIfCow(cell.posterior) * 100)}%' if cell.posterior else ''
    return f'{txtSuggest} {txtState} {txtLike}' >> pad_(_, dict(center=cfg.cellWidth))

def derefIfCow(maybeCow):
    return maybeCow._target if isinstance(maybeCow, _CoWProxy) else maybeCow

@coppertop
def ppCardSummary(card, player, pad, stats, cfg, cHands):
    t1 = ('' if stats[card].tbi == MAYBE else stats[card].tbi) >> pad_(_, dict(left=cfg.hasWidth))
    t2 = ('' if stats[card].tbi in (YES, NO) else str(cHands - stats[card].noCount)) >> pad_(_, dict(left=cfg.noCountWidth))
    t3 = (f'BTStruct{stats[card].sumMaybeSuggests}' if stats[card].sumMaybeSuggests else '') >> pad_(_, dict(left=cfg.suggestCountWidth))
    t4 = (f'{int(stats[card].mulPriors * 100)}%' if stats[card].mulPriors else '') >> pad_(_, dict(left=cfg.likeWidth))
    return t1 + t2 + t3 + t4


@coppertop
def rep1(pad:cluedo_pad, handId:Card) -> display_table:
    cfg = dstruct(nameWidth=17, cellWidth=12, hasWidth=2, noCountWidth=5, suggestCountWidth=3, likeWidth=7)

    handIds = (pad >> values_ >> first >> keys >> to >> pylist | (N ** Card)[dseq]) >> without >> TBI

    titlesPadding = ' ' * (cfg.nameWidth + cfg.hasWidth + cfg.noCountWidth + cfg.suggestCountWidth + cfg.likeWidth)
    tTitle = [titlesPadding + (
        handIds
            >> collect >> ((lambda hId: ('Me' if hId == handId else repr(hId)) >> pad_(_, dict(left=cfg.cellWidth))) | Card^txt)
            >> joinAll
    )] | display_table

    tNames = (people, weapons, rooms)  \
        >> collect >> (lambda cards: cards >> collect >> str) \
        >> interleave >> ['----']  \
        >> collect >> (lambda c: c >> pad_(_, dict(left=cfg.nameWidth))) | display_table

    # show TBI, countHands - noCount, sum priors, sum suggests
    stats = genStats(pad, handId)

    cHands = handIds >> count   # i.e. the number of players in the game, the number of hands less the TBI hand
    tSummary = (people, weapons, rooms)  \
        >> collect >> (lambda g: g
            >> collect >> (lambda c: c
                >> ppCardSummary(_, handId, pad, stats, cfg, cHands)
            )
        )  \
        >> interleave >> ['']  \
        >> collect >> (lambda c: c >> pad_(_, dict(left=cfg.nameWidth)))  \
        | display_table

    tHands = (people, weapons, rooms)  \
        >> collect >> (lambda g: g
            >> collect >> (lambda c: handIds  \
                >> collect >> ((lambda hId:  \
                    pad[c][hId] >> ppCell(_, stats[c], cfg)
                ) | Card^txt)
                >> joinAll
            )
        )  \
        >> interleave >> ['']  \
        >> collect >> (lambda c: c >> pad_(_, dict(left=cfg.nameWidth)))  \
        | display_table


    a = (tTitle >> join >> (tNames >> hjoin >> tSummary >> hjoin >> tHands)) | display_table
    return a


@coppertop
def PP(bag:cluedo_bag) -> cluedo_bag:
    bag.pad >> rep1(_, bag.handId) >> PP
    return bag

@coppertop
def ppFnOfCard(fn) -> display_table:
    return ppFnOfCard(fn, '')


@coppertop
def ppFnOfCard(fn, sep) -> display_table:
    return dseq(display_table,
        people >> collect >> fn >> append >> sep
        >> join >> (weapons >> collect >> fn >> append >> sep)
        >> join >> (rooms >> collect >> fn)
    )


@coppertop
def genStats(pad:pydict, handId) -> dstruct:
    stats = dstruct()
    handIds = pad >> values_ >> first >> keys
    for c in pad >> keys:
        noCount = 0
        sumMaybeSuggests = 0
        mulPriors = 0
        for hId in handIds:
            if hId == TBI or hId == handId:
                continue
            else:
                e = pad[c][hId]
                noCount += e.state == NO
                sumMaybeSuggests += e.suggestions >> count if e.state == MAYBE else 0
                mulPriors += e.posterior if e.state == MAYBE else 0
        stats[c] = dstruct(
            tbi=pad[c][TBI].state,
            noCount=noCount,
            sumMaybeSuggests=sumMaybeSuggests,
            mulPriors=mulPriors
        )
    return stats

