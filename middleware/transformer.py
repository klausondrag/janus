from .interface import Contact as MWContact
from .mock import Contact as BEContact


def MWContact_to_BEContact(contact: MWContact) -> BEContact:
    return BEContact(**vars(contact))


def BEContact_to_MWContact(contact: BEContact) -> MWContact:
    return MWContact(**vars(contact))


if __name__ == '__main__':
    print(MWContact_to_BEContact(MWContact('Klaus', 'DE22', '')))
    print(BEContact_to_MWContact(BEContact('Niklas', 'DE21', '')))
