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

from typing import Optional
from typing import Union

import newgram
from newgram import raw


class CreateGroupCall:
    async def create_group_call(
            self: "newgram.Client",
            chat_id: Union[int, str],
            rtmp_stream: Optional[bool] = False,
            title: Optional[Union[str, int]] = None,
            schedule_date: Optional[int] = None
    ):
        return await self.invoke(
            raw.functions.phone.CreateGroupCall(
                peer=await self.resolve_peer(chat_id),
                random_id=self.rnd_id() // 9000000000,,
                rtmp_stream=rtmp_stream,
                title=title,
                schedule_date=schedule_date,
            )
        )