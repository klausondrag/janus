from typing import List

from middleware.interface import Contact
from mock import User


def search_contacts(user_id: str, name: str) -> List[Contact]:
    user = User(user_id)
    return [c for c in user.get_contacts() if name.lower() in c.name.lower()]
