# **********************************************************************************************************************
# Copyright (c) 2019-2022 David Briant. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
# **********************************************************************************************************************

from dm.testing import check, equals
from bones.core.errors import ErrSite
from bones.kernel.tests.fred import Fred


def test_site():
    f = Fred()
    repr(f.site1) >> check >> equals >> 'bones.kernel.tests.fred.Fred>>__init__'
    repr(f.site2) >> check >> equals >> 'bones.kernel.tests.fred.Fred>>__init__[#1]'


def test_from_ide():
    site = ErrSite()
    repr(site) >> check >> equals >> '__main__>>test_from_ide'



def main():
    test_site()


if __name__ == '__main__':
    main()
    test_from_ide()
    print('pass')
