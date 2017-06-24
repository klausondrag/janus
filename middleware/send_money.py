from typing import List

from middleware.interface import Contact as MWContact
from mock import User, Contact as BEContact, FigoConnector
import transformer as t


def search_contacts(user_id: str, name: str) -> List[BEContact]:
    user = User(user_id)
    matches = [c for c in user.get_contacts() if name.lower() in c.name.lower()]
    matches = [t.BEContact_to_MWContact(c) for c in matches]
    return matches


def send_money(contact: MWContact, money_amount: int, currency: str) -> bool:
    return FigoConnector.send_money(t.MWContact_to_BEContact(contact), money_amount, currency)
