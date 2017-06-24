from contact import Contact

class Transaction:
    def __init__(self, id: str, contact: Contact, type: str, 
                 purpose: str, booking_text: str, amount: float) -> None:
        self.id = id
        self.contact = contact
        self.type = type
        self.purpose = purpose
        self.booking_text = booking_text
        self.amount = amount
