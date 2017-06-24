from .util import to_json


class Contact:
    def __init__(self, name, iban, bic):
        self.name = name
        self.iban = iban
        self.bic = bic

    def to_json(self):
        return {
            'name': to_json(self.name),
            'iban': to_json(self.iban),
            'bic': to_json(self.bic)
        }
