import requests
import json
import datetime
import sqlite3

def createTransaction (cardHolderID, accountID, amount, merchantName):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/"+ cardHolderID + "/accounts/" + accountID + "/transactions"
    payload = {
        "amount": amount,
        "merchant_name": merchantName
    }
    headers = {
        "accept": "*/*",
        "content-type": "application/json"
    }
    
    response = requests.request("POST", url, json=payload, headers=headers)
    
    print(response.text)
    return

def getCurrentMonthTransactions(cardHolderID, accountID):
    currentMonth = datetime.date.month
    currentYear = datetime.date.year

    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + cardHolderID + "/accounts/" + accountID +"/transactions"

    headers = {"accept": "*/*"}

    response = requests.request("GET", url, headers=headers)

    responseObj = response.json()

    transactions = {}

    for transaction in responseObj["transactions"]:
        transactionMonth = transaction["timestamp"][5:7]
        transactionYear = transaction["timestamp"][:5]
        if transactionMonth == currentMonth and transactionYear == currentYear:
            transactionID = transaction["transaction_id"]
            transactionAmount = transaction["amount"]
            transactionMerchant = transaction["description"]
            transactions[transactionID] = (transactionAmount,transactionMerchant)
    return transactions


def createSpendingAccount(cardHolderID):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + str(cardHolderID) + "/accounts"
    payload = {
        "account": {"processor_token": "99999"},
        "account_type": "spending_account"
    }
    headers = {
        "accept": "*/*",
        "content-type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code != 201:
        raise Exception(response)
    
    return response.json()["account_id"]

def listAccounts(cardHolderID):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + cardHolderID + "/accounts"
    headers = {"accept": "*/*"}
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return 


def retrieveAccount(cardHolderID, accountID=-1):
    url = ''
    if accountID != -1:
        url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + cardHolderID + "/accounts/" + accountID
    else:
        raise Exception("Account ID cannot be -1!")
    headers = {"accept": "*/*"}
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return
    
def getCardHolderID(email):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    return c.execute("SELECT cardHolderID FROM customers WHERE email=%s" % email)
