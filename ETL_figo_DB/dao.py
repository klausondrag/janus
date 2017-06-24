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
        with open("dummy_data.json", "r") as data_file:
            data = json.loads(data_file.read())
            contacts_json = data["users"][self.id]["contacts"]

            contacts = []
            for c in contacts_json:
                contacts.append(self.json_to_Contact(c))

            return contacts

    def save_contact(self, contact: Contact) -> None:
        contacts = self.load_contacts()
        for c in contacts:
            if (c.iban == contact.iban and c.bic == contact.bic):
                c.name = contact.name

        data = None
        file = "dummy_data.json"
        with open(file, "r") as data_file:
            data = json.loads(data_file.read())
            contacts = map(lambda x: x.__dict__, contacts)
            data["users"][self.id]["contacts"] = contacts

        print(contacts[0])

        with open("test.json", "w") as out_file:
            json.dump(data, out_file)

    def save_contacts(self, contacts: List[Contact]) -> None:
        for c in contacts:
            self.save_contact(c)

    def delete_contact(self, contact: Contact) -> bool:
        pass

    def load_transactions(self) -> List[Transaction]:
        pass

    def save_transactions(self, transactions: List[Transaction]):
        pass

    ### Private methods ###

    def json_to_Contact(self, jdata) -> Contact:
        return Contact(jdata["name"], jdata["iban"], jdata["bic"])

    def write_contacts(self, contacts: List[Contact]) -> None:
        pass


if __name__ == '__main__':
    d = DAO('1')
    d._save_data()
