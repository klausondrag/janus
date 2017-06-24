#!/usr/bin/env python

from typing import List, Dict
from . import figoConnector
from .contact import Contact
from .transaction import Transaction
from .dao import DAO

class ETL:
    def update(add_demo_data: bool) -> None:
        transactions_kvps = ETL.get_formatted_transactions()
        # 3. Transform data
        for key in transactions_kvps.keys():
            # a. Extract contacts and transform to Contact
            contacts = []
            for transaction in transactions_kvps[key]:
                c = transaction.contact
                saved = False
                for contact in contacts:
                    if contact.iban == c.iban and contact.bic == c.bic:
                        saved = True

                if not saved:
                    contacts.append(transaction.contact)

            dao = DAO(key)
            dao.save_contacts(contacts)

            # b. Transform transactions
            transactions = transactions_kvps[key]
            if add_demo_data:
                c = Contact("Heinz Betrueger", "GE29NB0000000101904900", "HANDFIHH")
                t = Transaction("230", c, "Remittance", "Illegale Ueberweisung", "Ueberweisung", "-100000.10")
                transactions.append(t)

            dao.save_transactions(transactions)

        # 4. Save contacts, transactions and meta (last access)
        pass


        ### Private methods ###
    def get_formatted_transactions(): #-> Dict[str, List[Transaction]]:
            # 1. get_accounts

            # 2. get_transactions
        accounts = figoConnector.get_accounts()
        acc_dict = {}
        for acc in accounts:
            acc_dict.update({acc.account_id: figoConnector.get_transactions(acc)})

        return acc_dict

if __name__ == '__main__':
    ETL.update(False)
