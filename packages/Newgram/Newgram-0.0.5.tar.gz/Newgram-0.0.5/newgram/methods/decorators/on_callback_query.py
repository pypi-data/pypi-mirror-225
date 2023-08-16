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

from typing import Callable

import newgram
from newgram.filters import Filter


class OnCallbackQuery:
    def on_callback_query(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling callback queries.

        This does the same thing as :meth:`~newgram.Client.add_handler` using the
        :obj:`~newgram.handlers.CallbackQueryHandler`.

        Parameters:
            filters (:obj:`~newgram.filters`, *optional*):
                Pass one or more filters to allow only a subset of callback queries to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, newgram.Client):
                self.add_handler(newgram.handlers.CallbackQueryHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        newgram.handlers.CallbackQueryHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
