from typing import Dict

from .user import User
from .util import to_json


class Data:
    def __init__(self, users: Dict[str, User]):
        self.users = users

    def to_json(self):
        return {
            "users": to_json(self.users)
        }
