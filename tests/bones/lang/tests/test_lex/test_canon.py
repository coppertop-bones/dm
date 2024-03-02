# **********************************************************************************************************************
# Copyright (c) 2019-2022 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

from glob import glob
import os
from bones.lang import lex
from dm.pp import PP


def test_canon():
    # home = os.path.expanduser('~/arwen/bones/canon')
    home = os.path.abspath(os.path.join(lex.__file__, '../../../../canon'))
    pfns = glob('**/*.b', root_dir=home, recursive=True)
    assert pfns, f"didn't find bones files in tour path {home}"
    for pfn in pfns:
        os.path.join('bones/canon', pfn) >> PP
        with open(os.path.join(home, pfn)) as f:
            tokens, lines = lex.lexBonesSrc(0, f.read())


def main():
    test_canon()


if __name__ == '__main__':
    main()
    print('pass')
