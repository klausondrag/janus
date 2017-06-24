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

import json
import functools
import logging
import traceback
import sys
from telegram.ext import Updater, MessageHandler, Filters
from wit import Wit

with open('config.json') as fp:
    config = json.load(fp)

logging.basicConfig(level=logging.INFO)
wit = Wit(access_token=config['wit_token'])


def handler(func):
    """
    Decorator for handlers that catches errors.
    """

    def wrapper(bot, update):
        try:
            return func(bot, update)
        except:
            exc_string = traceback.format_exc()
            if config.get('debug'):
                update.message.reply_text(exc_string)
            raise

    return wrapper


@handler
def reply(bot, update):
    logging.info('Received message from %s', update.message.from_user['username'])
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(config['telegram_token'])
    updater.dispatcher.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
