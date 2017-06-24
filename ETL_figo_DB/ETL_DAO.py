#!/usr/bin/env python

def main():
    print("a")
    a = ETL_DAO
    a.id = 1
    a.load_contacts()

class ETL_DAO:
    id = 0

    def load_contact(iban: str, bic: str, id: int):
        pass

    def load_contacts():
        with open("dummmy_data.json", "r") as data_file:
            data = json.loads(data_file.read())
            users = data["users"]
            for u in users:
                print(u)

    def save_contact(iban: str, bic: str):
        pass

    def save_contacts(contactlist):
        pass
