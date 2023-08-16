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

from uuid import uuid4

import newgram
from newgram import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~newgram.types.InlineQueryResultCachedAudio`
    - :obj:`~newgram.types.InlineQueryResultCachedDocument`
    - :obj:`~newgram.types.InlineQueryResultCachedAnimation`
    - :obj:`~newgram.types.InlineQueryResultCachedPhoto`
    - :obj:`~newgram.types.InlineQueryResultCachedSticker`
    - :obj:`~newgram.types.InlineQueryResultCachedVideo`
    - :obj:`~newgram.types.InlineQueryResultCachedVoice`
    - :obj:`~newgram.types.InlineQueryResultArticle`
    - :obj:`~newgram.types.InlineQueryResultAudio`
    - :obj:`~newgram.types.InlineQueryResultContact`
    - :obj:`~newgram.types.InlineQueryResultDocument`
    - :obj:`~newgram.types.InlineQueryResultAnimation`
    - :obj:`~newgram.types.InlineQueryResultLocation`
    - :obj:`~newgram.types.InlineQueryResultPhoto`
    - :obj:`~newgram.types.InlineQueryResultVenue`
    - :obj:`~newgram.types.InlineQueryResultVideo`
    - :obj:`~newgram.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "newgram.Client"):
        pass
