class Contact:
    name = ''
    iban = ''
    bic = ''

    def __init__(self, name: str, iban: str, bic: str) -> None:
        super().__init__()
        self.name = name
        self.iban = iban
        self.bic = bic


class User:
    def __init__(self, id: str) -> None:
        self.id = id

    def get_contacts(self):
        if self.id == 1:
            return [Contact('Niklas', 'DE21 0000', ''),
                    Contact('Klaus', 'DE22 0000', '')]
        else:
            return [Contact('Niklas', 'DE21 0000', ''),
                    Contact('Thien', 'DE23 0000', '')]
