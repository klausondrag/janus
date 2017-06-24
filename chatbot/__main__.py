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

import click
import logging
import json
import os

from . import state
from . import backends
from .backends.telegram import TelegramBackend
from .backends.slack import SlackBackend
from wit import Wit


class Handler(backends.Handler):

    def __init__(self, wit):
        self.wit = wit

    def handle_message(self, message):
        print('Handling message from:', message.user)
        response = self.wit.message(message.text)
        message.reply('```\n' + json.dumps(response, indent=2) + '\n```')


@click.command()
@click.option('--backend', type=click.Choice(['slack', 'telegram']), default='slack')
def main(backend):
    logging.basicConfig(level=logging.INFO)
    with open('config.json') as fp:
        config = json.load(fp)

    wit = Wit(config['wit']['token'])
    handler = Handler(wit)

    if backend == 'telegram':
        backend = TelegramBackend(
            config['telegram']['token'],
            handler,
            config['debug'])
    elif backend == 'slack':
        backend = SlackBackend(
            config['slack']['botname'],
            config['slack']['token'],
            handler,
            config['debug'])
    else: assert False
    backend.start()


if __name__ == '__main__':
    main()
