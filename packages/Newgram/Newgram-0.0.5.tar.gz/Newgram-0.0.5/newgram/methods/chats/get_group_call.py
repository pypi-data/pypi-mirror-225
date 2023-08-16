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


from typing import Union

from newgram import raw



class GetGroupCall:
    async def get_group_call(
        self: "newgram.Client",
        chat_id: Union[int, str],
        limit: int = 1
    ) -> "newgram.raw.base.phone.GroupCall":
        """ Get group call
        """
        peer = await self.resolve_peer(chat_id)
        
        if isinstance(peer, raw.types.InputPeerChannel):
            call = (await self.invoke(
                raw.functions.channels.GetFullChannel(
                    channel=peer
                ))).full_chat.call
        else:
            if isinstance(peer, raw.types.InputPeerChat):
                call = (await self.invoke(
                    raw.functions.messages.GetFullChat(
                        chat_id=peer.chat_id
                    ))).full_chat.call

        if call is None:
            return call

        return await self.invoke(
            raw.functions.phone.GetGroupCall(
                call=call,
                limit=limit
            )
        )