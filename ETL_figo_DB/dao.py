#!/usr/bin/env python

import json
from typing import List
from contact import Contact
from transaction import Transaction

class DAO:
    id = ""

    def __init__(self, id: str) -> None:
        self.id = id


    ### Interface methods ###

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
        
        with open("dummy_data.json", "w") as data_file:
            data = json.loads(data_file.read())
            print(data["users"]["1"])


    def save_contacts(self, contacts: List[Contact]) -> None:
        for c in contacts:
            self.save_contact(c)


    def delete_contact(self, contact: Contact) -> bool:
        pass


    def load_transactions(self) -> List[Transaction]:
        pass


    ### Private methods ###

    def json_to_Contact(self, jdata) -> Contact:
        return Contact(jdata["name"], jdata["iban"], jdata["bic"])


    def write_contacts(self, contacts: List[Contact]) -> None:
        pass
