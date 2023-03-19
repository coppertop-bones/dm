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

from bones.core.errors import ErrSite

class Fred(object):
    def __init__(self):
        self.site1 = ErrSite(self.__class__)
        self.site2 = ErrSite(self.__class__, "#1")

def fred():
    return ErrSite("#1")
