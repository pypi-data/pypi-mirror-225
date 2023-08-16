#  Newgram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2023-present Noel <https://github.com/jokokendi>
#
#  This file is part of Newgram.
#
#  Newgram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Newgram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Newgram.  If not, see <http://www.gnu.org/licenses/>.

from typing import List

import newgram
from newgram import raw
from newgram import types


class GetDefaultEmojiStatuses:
    async def get_default_emoji_statuses(
        self: "newgram.Client",
    ) -> List["types.EmojiStatus"]:
        """Get the default emoji statuses.

        .. include:: /_includes/usable-by/users-bots.rst

        Returns:
            List of :obj:`~newgram.types.EmojiStatus`: On success, a list of emoji statuses is returned.

        Example:
            .. code-block:: python

                default_emoji_statuses = await app.get_default_emoji_statuses()
                print(default_emoji_statuses)
        """
        r = await self.invoke(
            raw.functions.account.GetDefaultEmojiStatuses(hash=0)
        )

        return types.List([types.EmojiStatus._parse(self, i) for i in r.statuses])
