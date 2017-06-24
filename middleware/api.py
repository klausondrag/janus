from typing import List

from .interface import Contact
from .mock import User, Contact as BEContact, FigoConnector
from . import transformer as t
from ETL_figo_DB.dao import DAO
from ETL_figo_DB.etl import ETL


def search_contacts(user_id: str, name: str) -> List[BEContact]:
    user = User(user_id)
    matches = [c for c in user.get_contacts() if name.lower() in c.name.lower()]
    matches = [t.BEContact_to_MWContact(c) for c in matches]
    return matches


class PrepareTransaction(object):

    class Error(Exception):
        def __init__(self, type, message):
            self.type = type
            self.message = message

    SlackUserMapping = {
        'U5YAKQXT2': 'A1.1',  # Slack user 'niklas'
    }

    def __init__(self, sender: str, receiver: Contact, amount: float, currency: str):
        self.sender = self.SlackUserMapping[sender] # Q&D ¯\_(ツ)_/¯
        self.receiver = receiver
        self.amount = amount
        self.currency = currency

    def check(self, check_similar=True, check_excess=True):
        """
        Checks if sending the money makes sense?
        """

        dao = DAO(self.sender)
        spendings = [t for t in dao.load_transactions() if t.amount < 0][-10:]

        # Check balace
        #balance = dao.get_balance()
        #if balance < self.amount:
        #    raise self.Error('balance', "You're balance is {}{}, you can not send {}{}"
        #        .format(balance, self.currency, self.amount, self.currency))

        # Check if one of the last 3 transactions have the same recipient
        # and amount.
        if check_similar:
            transactions = spendings[-3:]
            for t in transactions:
                if t.amount == self.amount and t.contact.iban == self.contact.iban:
                    raise self.Error('similar', "You recently transfered {:.2f}{} to {}, are you"
                        "sure you want to do it again?"
                        .format(self.amount, self.currency, self.contact.name))

        # Check if our average spendings are increasing.
        if spendings and check_excess:
            total = abs(sum(t.amount for t in spendings))
            avg = total / len(spendings)
            new_avg = (total + self.amount) / (len(spendings) + 1)
            if new_avg > avg * 1.5:
                raise self.Error('excess', "You are going to spend significantly more "
                    "more than you did in the past. You're average from the last 20 "
                    "spendings is {:.2f}{}. Are you sure you want to continue?"
                    .format(avg, self.currency))

    def send(self):
        return True


def update_figo(add_demo_data: bool) -> None:
    print("!!! NOTE !!! Skipping ETL.update() for now")
    #ETL.update(add_demo_data)
