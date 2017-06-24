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

import abc
import typing


class User(object):
    """
    Represents a user.
    """

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return str(self.name)


class Message(object, metaclass=abc.ABCMeta):
    """
    Represents a message that is sent by a user to the chatbot.
    """

    def __init__(self, id: str, text: str, user: User):
        self.id = id
        self.text = text
        self.user = user

    @abc.abstractmethod
    def reply(self, text):
        pass


class Handler(object):

    @abc.abstractmethod
    def handle_message(self, message):
        pass

