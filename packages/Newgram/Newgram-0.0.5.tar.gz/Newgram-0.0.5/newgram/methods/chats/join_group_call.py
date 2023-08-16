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

from typing import Union, Optional
from datetime import datetime

from newgram import raw



class JoinGroupCall:
    async def join_group_call(
        self: "newgram.Client",
        chat_id: Union[int, str],
        muted: Optional[bool] = None,
        video_stopped: Optional[bool] = None,
        invite_hash: Optional[str] = None,
    ) -> "newgram.raw.base.Updates":
        """ Join group call
        """
        group_call = await self.get_group_call(chat_id)

        if group_call is None:
            return None

        call = group_call.call

        return await self.invoke(
            raw.functions.phone.JoinGroupCall(
                call=raw.types.InputGroupCall(
                    id=call.id,
                    access_hash=call.access_hash
                ),
                join_as=raw.types.InputUserSelf(),
                params=await self.invoke(
                    raw.functions.phone.GetCallConfig()
                ),
                muted=muted,
                video_stopped=video_stopped,
                invite_hash=invite_hash
            )
        )