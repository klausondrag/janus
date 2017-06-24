#!/usr/bin/env python

from typing import List
from . import figoConnector
from .contact import Contact
from .transaction import Transaction

class ETL:
    def update(add_demo_data: bool) -> None:
        transactions = get_formatted_transactions()
        # 3. Transform data
        #    a. Extract contacts and transform to Contact
        #    b. Transform transactions
        # 4. Save contacts, transactions and meta (last access)
        pass


        ### Private methods ###
    def get_formatted_transactions(): #-> Dict[str, List[Transaction]]:
            # 1. get_accounts

            # 2. get_transactions
        accounts = figoConnector.get_account()
        acc_dict = {}
        for acc in accounts:
            acc_dict.update({acc.account_id: figoConnector.get_transactions(acc)})

        return acc_dict
