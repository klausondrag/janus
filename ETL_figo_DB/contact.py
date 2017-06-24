class Contact:
    name = ''
    iban = ''
    bic = ''

    def __init__(self, name: str, iban: str, bic: str) -> None:
        super().__init__()
        self.name = name
        self.iban = iban
        self.bic = bic