import json
import webbrowser
from figo import FigoConnection, FigoSession
from pprint import pprint

#connection = FigoConnection("<client ID>", "<client secret>", "http://my-domain.org/redirect-url")
with open("config.json", "r") as data_file:
    data = json.loads(data_file.read())
session = FigoSession(data["figo"]["token"])


def get_accounts():
    accountlist = []
    for account in session.accounts:
        accountlist.append(account)

    return accountlist


def get_transactions(account):
    transact_list = []
    for trans in session.get_account(account.account_id).transactions:
        transact_list.append(trans)
    return transact_list
    #return list(session.get_account(account.account_id).transactions)

#testing
#l = get_accounts()
#g = get_transactions(l[0])
#print(g[0].type)
