import requests
import json
import datetime
import sqlite3
import Syrup as syrup


def createTransaction (cardHolderID, accountID, amount, merchantName):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/"+ str(cardHolderID) + "/accounts/" + str(accountID) + "/transactions"
    payload = {
        "amount": int(amount),
        "merchant_name": merchantName
    }
    try:
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken,
            "content-type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
    except:
        _accessToken = syrup.refreshAuthorization()
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken,
            "content-type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return

def getCurrentMonthTransactions(cardHolderID, accountID):
    dateToday = str(datetime.date.today())
    currentMonth = int(dateToday[5:7])
    currentYear = int(dateToday[:4])
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + str(cardHolderID) + "/accounts/" + str(accountID) +"/transactions"

    try:
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("GET", url, headers=headers)
    except:
        _accessToken = syrup.refreshAuthorization()
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("GET", url, headers=headers)

    response = requests.request("GET", url, headers=headers)

    responseObj = response.json()

    transactions = {}
    # print(responseObj["transactions"][0])

    for transaction in responseObj["transactions"]:
        transactionMonth = int(transaction["timestamp"][5:7])
        transactionYear = int(transaction["timestamp"][:4])
        if transactionMonth == currentMonth and transactionYear == currentYear:
            transactionID = transaction["transaction_id"]
            transactionAmount = float(transaction["amount"])
            transactionMerchant = transaction["description"]
            transactions[transactionID] = (transactionAmount,transactionMerchant)
    return transactions


def createSpendingAccount(accessToken, cardHolderID):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + str(cardHolderID) + "/accounts"
    payload = {
        "account": {"processor_token": "99999"},
        "account_type": "spending_account"
    }
    try:
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken,
            "content-type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
    except:
        _accessToken = syrup.refreshAuthorization()
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken,
            "content-type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code != 201:
        raise Exception(response)
    
    return response.json()["account_id"]

def listAccounts(accessToken, cardHolderID):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + str(cardHolderID) + "/accounts"
    response = {}
    try:
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("GET", url, headers=headers)
    except:
        _accessToken = syrup.refreshAuthorization()
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("GET", url, headers=headers)

    responseObj = response.json()
    accounts=[]
    for account in responseObj["accounts"]:
        accounts.append(account["account_id"])
    return accounts

def fundAccount(destinationAccountID, sourceAccountID, amount):

    url = "https://sandbox.galileo-ft.com/instant/v1/transfers"

    payload = {
        "amount": amount,
        "destination_account_id": destinationAccountID,
        "source_account_id": sourceAccountID
    }

    try:
        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("POST", url, json=payload, headers=headers)
    except:
        _accessToken = syrup.refreshAuthorization()
        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code != 201:
        print(response.json())
        raise Exception(response)
    return

def retrieveAccount(cardHolderID, accountID=-1):
    url = ''
    if accountID != -1:
        url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + cardHolderID + "/accounts/" + accountID
    else:
        raise Exception("Account ID cannot be -1!")
    try:
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("GET", url, headers=headers)
    except:
        syrup.refreshAuthorization()
        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + syrup._accessToken
        }
        response = requests.request("GET", url, headers=headers)

    print(response.text)
    return
    
def getCardHolderID(email):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    return c.execute("SELECT cardHolderID FROM customers WHERE email=%s" % email)
