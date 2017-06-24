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
from middleware.api import search_contacts


class State(object):

    def __init__(self, name, data=None):
        self.name = name
        self.data = data


class Handler(backends.Handler):

    def __init__(self, wit):
        self.wit = wit
        self.states = {}  # Maps users to states

    def handle_message(self, message):
        # FIXME: Some proper logging
        print('Handling message from:', message.user)

        state = self.states.setdefault(message.user.id, State('idle', None))
        if message.text.lower().strip() in ('restart', 'abort'):
            state.name = 'idle'
            message.reply("Alright, let's start over!")
            return

        handler = getattr(self, 'state_' + state.name)
        handler(state, message)

    def state_idle(self, state, message):
        response = self.wit.message(message.text)
        if not 'intent' in response['entities']:
            message.reply("Sorry, I didn't understand you.")
            return

        intent = response['entities']['intent'][0]['value']
        if intent != 'send_money':
            # FIXME: Currently we only handle the send_money intent.
            message.reply("This intent is currently not supported ({})".format(intent))
            return

        contact = response['entities']['contact'][0]['value']
        amount = response['entities']['amount_of_money'][0]['value']
        currency = response['entities']['amount_of_money'][0]['unit']
        if currency != 'EUR':
            message.reply("Sorry, currently we only handle EUR transactions.")
            return

        send_data = {'contact': None, 'amount': amount, 'currency': currency}
        print('Contact:', contact)
        print('Send Data:', send_data)

        contact_list = search_contacts(message.user.id, contact)
        if not contact_list:
            message.reply("Dude, you don't have a friend with the name {}!".format(contact))
            message.reply("Enter the damn IBAN manually, jeez ...")
            state.name = 'get_iban'
            state.data = {'follow_up': 'send_money', 'data': send_data}
            return

        if len(contact_list) > 1:
            message.reply("Aha, Mr. rich bitch has many friends it seems.")
            message.reply("Who will be the lucky one? Type the number")
            for i, contact in enumerate(contact_list, 1):
                message.reply('{}) {}'.format(i, contact.name))
            state.name = 'get_contact_from_index'
            state.data = {'follow_up': 'send_money', 'data': send_data}
            return

        contact = contact_list[0]
        message.reply('Is this the lucky person to recieve your blessing?')
        message.reply('--- {}'.format(contact.name))
        message.reply('IBAN: {}'.format(contact.iban))
        message.reply('BIC: {}'.format(contact.bic))

        send_data['contact'] = contact
        state.name = 'confirm'
        state.data = {'follow_up': 'send_money', 'data': send_data}

    def state_get_iban(self, state, message):
        message.reply('TODO: parse IBAN data')

    def state_get_contact_from_index(self, state, message):
        message.reply('TODO: get contact from contact list')

    def state_send_money(self, state, message):
        message.reply('TODO: send money to', state.data)


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
