#!/usr/bin/env python

from typing import List, Dict
#from . import figoConnector
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
    def get_formatted_transactions() -> Dict[str, List[Transaction]]:
        # 1. get_accounts
        # 2. get_transactions
        # TEMP TEMP TEMP STUB CODE STUB CODE
        c1 = Contact("A", "BLA", "BIC")
        c2 = Contact("B", "BLU", "BIC")
        t1 = Transaction("1", c1, "t", "p", "bt", "-100.10")
        t2 = Transaction("2", c2, "jdfk", "jdifjfd", "mdfjkd", "500")
        t3 = Transaction("2", c2, "jkkkkk", "a", "a", "10000")
        return {"A1.1":[t1, t2], "A1.2":[t2, t3]}

if __name__ == '__main__':
    ETL.update(False)