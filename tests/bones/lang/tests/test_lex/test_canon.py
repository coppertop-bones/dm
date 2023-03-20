# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2022 David Briant. All rights reserved.
#
# This file is part of coppertop-bones.
#
# coppertop-bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General 
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# coppertop-bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License 
# for more details.
#
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

from glob import glob
import os
from bones.lang import lex
from dm.pp import PP


def test_canon():
    home = os.path.expanduser('~/arwen/bones/canon')
    pfns = glob('**/*.b', root_dir=home, recursive=True)
    assert pfns, "didn't find bones files in tour path"
    for pfn in pfns:
        os.path.join('bones/canon', pfn) >> PP
        with open(os.path.join(home, pfn)) as f:
            tokens, lines = lex.lexBonesSrc(0, f.read())


def main():
    test_canon()


if __name__ == '__main__':
    main()
    print('pass')
