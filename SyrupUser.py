import asyncio
import requests
import json


# class User:
#     def __init__(self, id):
#         # Spending dictionary where keys are categories and definition is the amount in that month.
#         self.spending = {}
#         # Total Spending is the current total for the current month.
#         self.totalSpending = 0

#         self.cardHolderID = id
#         self.accounts = []
        
#         self.address = ()

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

def getMonthlyTransactions(cardHolderID, accountID):

    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + cardHolderID + "/accounts/" + accountID +"/transactions"

    headers = {"accept": "*/*"}

    response = requests.request("GET", url, headers=headers)

    print(response.text)

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
    

