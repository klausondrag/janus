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

from typing import List
import abc

from middleware.api import search_contacts


class Node(object, metaclass=abc.ABCMeta):
  """
  A node in the state machine.
  """

  def init(self, wit, bot, update):
    pass

  @abc.abstractmethod
  def work(self, wit, bot, update) -> 'Node':
    pass


class Idle(Node):

  def work(self, wit, bot, update):
    data = wit.message(update.message.text)
    if not data['entities'] or data['intent'] not in ('send_money',):
      update.message.reply_text("Sorry, I don't know what you want to do.")
      return

    contact = data['entities']['contact']['value']
    amount = data['entities']['amount_of_money']['value']
    currency = data['entities']['amount_of_money']['unit']
    if currency != 'EUR':
      update.message.reply_text("Sorry, currently we only support EURO transactions.")
      return

    return FindContact(contact, SendMoney(None, amount, currency))


class FindContact(Node):

  def __init__(self, update, contact_name, successor):
    self.contact_name = contact_name
    self.contacts = search_contacts(str(update.message.username['id']), contact_name)
    self.successor = successor

  def init(self, wit, bot, update):
    if not self.contacts:
      update.message.reply_text("We could not find a contact matching '{}'".format(self.contact_name))


  def work(self, wit, bot, update):
    pass


class SendMoney(Node):

  def work(self, wit, bot, update):

    pass
