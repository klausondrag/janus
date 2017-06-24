from contact import Contact
from dao import DAO

def main():
    d = DAO("1")
    d.save_contact(Contact("BLA", "AL47212110090000000235698741", "OKOYFIHH"))

main()
