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
import re
import string

from . import backends
from .backends.telegram import TelegramBackend
from .backends.slack import SlackBackend
from wit import Wit
from middleware.api import Contact, search_contacts, send_money, update_figo


class State(object):

    def __init__(self, name):
        self.name = name
        self.data = {}

    def next(self, value=NotImplemented):
        if value is NotImplemented:
            next = self.data.pop('next')
            print('entering state:', self.name)
            if isinstance(next, str):
                self.name = next
            elif isinstance(next, (list, tuple)):
                self.name = next[0]
                next = next[1:]
                if next:
                    self.data['next'] = next
            elif name is not None:
                raise ValueError('invalid next: {!r}'.format(next))
        else:
            self.data['next'] = value

    def call(self, obj, *args, **kwargs):
        handler = getattr(obj, 'state_' + self.name)
        handler(self, *args, **kwargs)


class Handler(backends.Handler):

    def __init__(self, wit):
        self.wit = wit
        self.states = {}  # Maps users to states

    def handle_message(self, message):
        # FIXME: Some proper logging
        print('Handling message from:', message.user)

        state = self.states.setdefault(message.user.id, State('idle'))
        print('@', state.name)
        if message.text.lower().strip() in ('restart', 'abort'):
            state.name = 'idle'
            state.data = {}
            message.reply("Alright, let's start over!")
            return

        elif message.text.lower().strip().startswith('trollmode'):
            value = message.text.lower().strip().split()[1:]
            if len(value) != 1 or value[0] not in ('on', 'off'):
                message.reply('Invalid value')
                return
            troll = value[0] == 'on'
            update_figo(troll)
            if troll:
                message.reply('Trollconfiguration activated.')
            else:
                message.reply('Back to normal.')
            return

        state.call(self, message)

    def print_receiver_details(self, message, contact):
        message.reply('--- {}'.format(contact.name))
        message.reply('IBAN: {}'.format(contact.iban))
        message.reply('BIC: {}'.format(contact.bic))

    def state_idle(self, state, message):
        response = self.wit.message(message.text)
        if not 'intent' in response['entities']:
            message.reply("Sorry, I didn't understand you.")
            return

        # Check if the intent is determined with some minimum confidence.
        if response['entities']['intent'][0]['confidence'] < 0.8:
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

        state.data['amount'] = amount
        state.data['currency'] = currency
        state.data['contact'] = None
        state.data['contact_name'] = contact

        contact_list = search_contacts(message.user.id, contact)
        if not contact_list:
            message.reply("Dude, you don't have a friend with the name {}!".format(contact))
            message.reply("Enter the damn IBAN manually, jeez ...")
            state.name = 'get_iban'
            state.data.update({
                'next': 'send_money'
            })
            return

        if len(contact_list) > 1:
            message.reply("Who will be the lucky one? Type the number")
            for i, contact in enumerate(contact_list, 1):
                message.reply('{}) {}'.format(i, contact.name))
            state.name = 'get_contact_from_index'
            state.data.update({
                'next': 'send_money',
                'contact_list': contact_list
            })
            return

        contact = contact_list[0]
        message.reply('Is this the lucky person to recieve your blessing?')
        self.print_receiver_details(message, contact)

        state.name = 'confirm'
        state.data['contact'] = contact
        state.next('send_money')

    def state_get_iban(self, state, message):
        text = re.sub('\s*', '', message.text.strip())
        if set(text).difference(set(string.ascii_letters + string.digits)):
            message.reply('IBAN must constist of digits and letters only')
            return
        state.next()
        state.data['contact'] = Contact(state.data['contact_name'], text, '')
        state.call(self, message)

    def state_get_contact_from_index(self, state, message):
        try:
            index = int(message.text.strip()) - 1
        except ValueError:
            message.reply('Not a number.')
            return
        if index < 0 or index >= len(state.data['contact_list']):
            message.reply('Not one of the available choices.')
            return
        state.data['contact'] = state.data['contact_list'][index]
        message.reply("Ok, we'll send {}{} to".format(state.data['amount'], state.data['currency']))
        self.print_receiver_details(message, state.data['contact'])
        message.reply('Is that right?')
        state.next()

    def state_confirm(self, state, message):
        reply = message.text.strip().lower()
        if reply in ('y', 'yes', 'true', 'valid', 'ok'):
            state.next()
            state.call(self, message)
        elif reply in ('n', 'no', 'false', 'invalid', 'wrong'):
            state.name = 'idle'
            message.reply("Ok, back to the beginning.")
        else:
            message.reply("I couldn't understand you.")

    def state_send_money(self, state, message):
        result = send_money(state.data['contact'],
            state.data['amount'], state.data['currency'])
        if result:
            message.reply("Bam! You sent {}{} to {}".format(
                state.data['amount'], state.data['currency'],
                state.data['contact'].name))
        else:
            message.reply("Hm, something went wrong :(")
        state.name = 'idle'
        state.data = {}


@click.command()
@click.option('--backend', type=click.Choice(['slack', 'telegram']), default='slack')
def main(backend):
    logging.basicConfig(level=logging.INFO)
    with open('config.json') as fp:
        config = json.load(fp)

    update_figo(False)

    wit = Wit(config['wit']['token'])
    handler = Handler(wit)

    if backend == 'telegram':
        backend = TelegramBackend(
            token = config['telegram']['token'],
            handler = handler,
            debug = config['debug'])
    elif backend == 'slack':
        backend = SlackBackend(
            botname = config['slack']['botname'],
            token = config['slack']['token'],
            handler = handler,
            mode = 'im',
            debug = config['debug'])
    else: assert False
    backend.start()


if __name__ == '__main__':
    main()
