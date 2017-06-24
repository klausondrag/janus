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


def send_money(contact: Contact, money_amount: int, currency: str) -> bool:
    return FigoConnector.send_money(t.MWContact_to_BEContact(contact), money_amount, currency)


def update_figo(add_demo_data: bool) -> None:
    FigoConnector.update(add_demo_data)


def poll_errors(user_id: str, throw_error: bool) -> List[Transaction]:
    etl.update(throw_error)
    dao = DAO(user_id)
    transactions = dao.load_transactions()
    for t in transactions:
        if t.contact.iban == "GE29NB0000000101904900":
            return [t]
    
    return []

if __name__ == '__main__':
    poll("A1.1", False)
