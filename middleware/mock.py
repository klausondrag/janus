class Contact:
    name = ''
    iban = ''
    bic = ''

    def __init__(self, name: str, iban: str, bic: str) -> None:
        super().__init__()
        self.name = name
        self.iban = iban
        self.bic = bic

    def __str__(self):
        return str(vars(self))


class User:
    def __init__(self, id: str) -> None:
        self.id = id

    def get_contacts(self):
        if self.id == 'U5ZRDUQGP':
            return [Contact('Niklas', 'DE21 0000', ''),
                    Contact('Valentin Zieglmeier', 'AT11 0000', ''),
                    Contact('Valentin Schluckmeier', 'DE22 0000', '')]
        else:
            return [Contact('Niklas', 'DE21 0000', ''),
                    Contact('Thien Nguyen', 'DE23 0000', ''),
                    Contact('Li Nguyen', 'DE24 9942', ''),
                    Contact('Burda', 'DE67900900424711951500', 'HYPERBURST')]


class FigoConnector:
    @staticmethod
    def send_money(contact: Contact, money_amount: int, currency: str) -> bool:
        return True

    @staticmethod
    def update(add_demo_data):
        pass
