import json


class Contact:
    def __init__(self, name: str, iban: str, bic: str) -> None:
        self.name = name
        self.iban = iban
        self.bic = bic


def ContactEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Contact):
            return "{ \"name\" : " + self.name + ", \"iban\" : " + self.iban + ", \"bic\" : " + self.bic + "}"
