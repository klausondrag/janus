from contact import Contact

class Transaction:
    id = ""
    contact = Contact("", "", "")
    type = ""
    purpose = ""
    booking_text = ""

    def __init__(self, id: str, contact: Contact, type: str, purpose: str, booking_text: str) -> None:
        self.id = id
        self.contact = contact
        self.type = type
        self.purpose = purpose
        self.booking_text = booking_text