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

from coppertop.pipe import *
from coppertop._scopes import _CoWProxy
from dm.core.aggman import keys, collect, count, first, values, join, joinAll, without, interleave
from dm.flux import append
from dm.core.conv import to
from dm.core.text import pad as pad_
from dm.core.types import txt, N, pylist, pydict, dseq, dstruct

from .core import cluedo_pad, YES, NO, MAYBE
from .utils import display_table, hjoin
from .cards import Card, people, weapons, rooms, TBI


# coercers - # OPEN: can these be sensibly defaulted in metatypes or templated?
(Card^txt).setCoercer(makeFn)
(N**Card)[dseq].setCoercer(dseq)


@coppertop
def ppCell(cell, stat, cfg):
    txtSuggest = ('' if stat.tbi != MAYBE else (str(cell.suggestions >> count) if cell.suggestions else "")) >> pad_(_, dict(center=2))
    txtState = cell.state #(YES if cell.state == YES else ' ') if stat.tbi == YES else cell.state
    txtLike = f'{int(derefIfCow(cell.posterior) * 100)}%' if cell.posterior else ''
    return f'{txtSuggest} {txtState} {txtLike}' >> pad_(_, dict(center=cfg.cellWidth))

def derefIfCow(maybeCow):
    return maybeCow._traget if isinstance(maybeCow, _CoWProxy) else maybeCow

@coppertop
def ppCardSummary(card, player, pad, stats, cfg, cHands):
    t1 = ('' if stats[card].tbi == MAYBE else stats[card].tbi) >> pad_(_, dict(left=cfg.hasWidth))
    t2 = ('' if stats[card].tbi in (YES, NO) else str(cHands - stats[card].noCount)) >> pad_(_, dict(left=cfg.noCountWidth))
    t3 = (f'S{stats[card].sumMaybeSuggests}' if stats[card].sumMaybeSuggests else '') >> pad_(_, dict(left=cfg.suggestCountWidth))
    t4 = (f'{int(stats[card].mulPriors * 100)}%' if stats[card].mulPriors else '') >> pad_(_, dict(left=cfg.likeWidth))
    return t1 + t2 + t3 + t4


@coppertop
def rep1(pad:cluedo_pad, handId:Card) -> display_table:
    cfg = dstruct(nameWidth=17, cellWidth=12, hasWidth=2, noCountWidth=5, suggestCountWidth=3, likeWidth=7)

    handIds = (pad >> values >> first >> keys >> to >> pylist | (N ** Card)[dseq]) >> without >> TBI

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
    handIds = pad >> values >> first >> keys
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

