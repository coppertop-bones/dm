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
