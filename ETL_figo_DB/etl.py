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
    def get_formatted_transactions() -> List[Transaction]:
        # 1. get_accounts
        # 2. get_transactions
        pass
