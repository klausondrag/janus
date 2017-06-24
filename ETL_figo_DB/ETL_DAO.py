#!/usr/bin/env python

import json
from typing import List
from contact import Contact

class ETL_DAO:
    id = ""

    def __init__(self, id: str) -> None:
        self.id = id

# Private methods
    def json_to_Contact(self, jdata) -> Contact:
        return Contact(jdata["name"], jdata["iban"], jdata["bic"])

# Interface

    def load_contact(self, iban: str, bic: str, id: str):
        contacts = self.load_contacts()
        for c in contacts:
            if c.iban == iban and c.bic == bic:
                return c

        return Contact("", "", "")


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


    def save_contact(self, contact: Contact):
        self.load_contacts()


    def save_contacts(self, contacts: List[Contact]):
        for c in contacts:
            self.save_contact(c)
