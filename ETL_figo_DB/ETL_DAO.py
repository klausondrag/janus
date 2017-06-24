#!/usr/bin/env python

import json
from typing import List
import Contact

class Contact:
    name = ''
    iban = ''
    bic = ''

    def __init__(self, name: str, iban: str, bic: str) -> None:
        super().__init__()
        self.name = name
        self.iban = iban
        self.bic = bic

class ETL_DAO:
    id = ""

    def __init__(self, id: str) -> None:
        self.id = id

# Private methods
    def json_to_Contact(self, jdata) -> Contact:
        return Contact(jdata["name"], jdata["iban"], jdata["bic"])

# Interface

    def load_contact(self, iban: str, bic: str, id: str):
        pass

    def load_contacts(self) -> List[Contact]:
        with open("dummy_data.json", "r") as data_file:
            data = json.loads(data_file.read())
            users = data["users"]
            contacts_json = []
            for u in users:
                if u["id"] == self.id:
                    contacts_json = u["contacts"]

            contacts = []
            for c in contacts_json:
                contacts.append(self.json_to_Contact(c))

            return contacts

    def save_contact(self, iban: str, bic: str):
        pass

    def save_contacts(self, contacts: List[Contact]):
        pass

def main():
        print("a")
        a = ETL_DAO("1")
        a.load_contacts()

main()
