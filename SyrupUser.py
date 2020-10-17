import requests
import json
import datetime

def createTransaction (self, transaction):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/9999/accounts/9887/transactions"
    payload = {
        "amount": 10,
        "merchant_name": "Chipotle"
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


def createSpendingAccount(userID):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + str(userID) + "/accounts"
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
    
    return

def listAccounts(userID):
    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + userID + "/accounts"
    headers = {"accept": "*/*"}
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return


def retrieveAccount(userID, accountID=-1):
    url = ''
    if accountID != -1:
        url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + userID + "/accounts/" + accountID
    else:
        raise Exception("Account ID cannot be -1!")
    headers = {"accept": "*/*"}
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return
    

