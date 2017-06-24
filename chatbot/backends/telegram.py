# Copyright (c) 2017  Janus Development Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import traceback
import typing
from . import User, Message
from telegram.ext import Updater, MessageHandler, Filters


class TelegramMessage(Message):

    def __init__(self, msg):
        user = User(msg.from_user['id'], msg.from_user['username'])
        Message.__init__(self, str(msg.message_id), msg.text, user)
        self._telegram_message = msg

    def reply(self, text):
        self._telegram_message.reply_text(text)


class TelegramBackend(object):

    def __init__(self, token, handler, debug=False):
        self.token = token
        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self._reply))
        self.handler = handler
        self.debug = debug

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def _reply(self, bot, update):
        try:
            self.handler.handle_message(TelegramMessage(update.message))
        except Exception as exc:
            traceback.print_exc()
            if self.debug:
                update.message.reply_text(traceback.print_exc())
            else:
                update.message.reply_text('Internal Error')
