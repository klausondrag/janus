#!/usr/bin/env python

import json
from typing import List, Dict, Collection, Mapping

from .contact import Contact
from .data import Data
from .transaction import Transaction
from .user import User
from .util import to_json


class DAO:
    def __init__(self, user_id: str) -> None:
        self._file_name = 'dummy_data.json'
        self.user_id = user_id
        self._data = self._load_data()

    def _load_data(self) -> Data:
        with open(self._file_name, 'r') as data_file:
            json_text = json.loads(data_file.read())
            users = {}
            for k, v in json_text['users'].items():
                contacts = [Contact(**c) for c in v['contacts']]
                transactions = [Transaction(**t) for t in v['transactions']]
                users[k] = User(contacts, transactions)
            return Data(users)

    def _save_data(self) -> None:
        with open(self._file_name, 'w') as data_file:
            json.dump(to_json(self._data), data_file, indent=2)

    def load_contacts(self) -> List[Contact]:
        return self._data.users[self.user_id].contacts

    def save_contact(self, contact: Contact) -> None:
        for c in self._data.users[self.user_id].contacts:
            if c.iban == contact.iban and c.bic == contact.bic:
                c.name = contact.name
        self._save_data()

    def save_contacts(self, contacts: List[Contact]) -> None:
        for c in contacts:
            self.save_contact(c)

    def overwrite_contacts(self, contacts: List[Contact]) -> None:
        self._data.users[self.user_id].contacts = contacts
        self._save_data()

    def load_transactions(self) -> List[Transaction]:
        return self._data.users[self.user_id].transactions

    def save_transactions(self, transactions: List[Transaction]):
        self._data.users[self.user_id].transactions = transactions
        self._save_data()


if __name__ == '__main__':
    d = DAO('1')
    d._save_data()
    print(d.load_contacts())
