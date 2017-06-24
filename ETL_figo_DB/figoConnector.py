import json
import webbrowser
from figo import FigoConnection, FigoSession
from contact import Contact
from pprint import pprint

#connection = FigoConnection("<client ID>", "<client secret>", "http://my-domain.org/redirect-url")


with open("config.json", "r") as data_file:
    data = json.loads(data_file.read)

session = FigoSession(data["token"])

#def start_login():
    # open the webbrowser to kick off the login process
    #webbrowser.open(connection.login_url(scope="accounts=ro transactions=ro", state="qweqwe"))
'''
def process_redirect(authentication_code, state):
    # handle the redirect url invocation, which gets passed an authentication code and the state (from the initial login_url call)

    # authenticate the call
    if state != "qweqwe":
        raise Exception("Bogus redirect, wrong state")

    # trade in authentication code for access token
    token_dict = connection.convert_authentication_code(authentication_code)

    # start session
    session = FigoSession(token_dict["access_token"])

    # access data
    for account in session.accounts:
        print(account.name)
'''
def get_accounts():
    accountlist = []
    for account in session.accounts:
        a = Contact(account.name, account.iban, account.bic)
        accountlist.append(a)
    return accountlist


def get_transactions(clientid: str):
    return list(session.get_account(clientid).transactions)
