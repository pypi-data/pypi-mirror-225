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


class Error(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Error`.

    Details:
        - Layer: ``160``
        - ID: ``C4B9F9BB``

    Parameters:
        code (``int`` ``32-bit``):
            N/A

        text (``str``):
            N/A

    """

    __slots__: List[str] = ["code", "text"]

    ID = 0xc4b9f9bb
    QUALNAME = "types.Error"

    def __init__(self, *, code: int, text: str) -> None:
        self.code = code  # int
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Error":
        # No flags
        
        code = Int.read(b)
        
        text = String.read(b)
        
        return Error(code=code, text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.code))
        
        b.write(String(self.text))
        
        return b.getvalue()
