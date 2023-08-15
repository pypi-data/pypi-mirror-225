#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class GetStoryViewsList(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``160``
        - ID: ``4B3B5E97``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        offset_date (``int`` ``32-bit``):
            N/A

        offset_id (``int`` ``64-bit``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`stories.StoryViewsList <pyrogram.raw.base.stories.StoryViewsList>`
    """

    __slots__: List[str] = ["id", "offset_date", "offset_id", "limit"]

    ID = 0x4b3b5e97
    QUALNAME = "functions.stories.GetStoryViewsList"

    def __init__(self, *, id: int, offset_date: int, offset_id: int, limit: int) -> None:
        self.id = id  # int
        self.offset_date = offset_date  # int
        self.offset_id = offset_id  # long
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStoryViewsList":
        # No flags
        
        id = Int.read(b)
        
        offset_date = Int.read(b)
        
        offset_id = Long.read(b)
        
        limit = Int.read(b)
        
        return GetStoryViewsList(id=id, offset_date=offset_date, offset_id=offset_id, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Int(self.offset_date))
        
        b.write(Long(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
