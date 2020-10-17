import asyncio
import requests


class User:
    def __init__(self, id):
        # Spending dictionary where keys are categories and definition is the amount in that month.
        self.spending = {}
        # Total Spending is the current total for the current month.
        self.totalSpending = 0

        self.cardHolderID = id
        self.accounts = []
        
        self.address = ()

    def createTransaction (self, transaction):
        category = transaction["category"]
        amount = float(transaction["amount"])
        self.spending[category] += amount
        self.totalSpending += amount
        return

    def clearTransactions (self):
        self.spending = {}
        self.totalSpending = 0
    

    def createSpendingAccount(self):
        url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + str(self.cardHolderID) + "/accounts"

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
        
        self.accounts.append(int(response.json()['account_id']))
        return
    

    def ListAccounts(self):
        url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + self.cardHolderID + "/accounts"

        headers = {"accept": "*/*"}

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        return


    def retrieveAccount(self, accountID=-1, accountIndex=0):
        url = ''
        if accountID != -1:
            url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + self.cardHolderID + "/accounts/" + accountID
        else:
            url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/" + self.cardHolderID + "/accounts/" + self.accounts[accountIndex]

        headers = {"accept": "*/*"}

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        return
    
    async def setAddress(self, addrln1, addrln2, city, state, zipcode):
        self.address = (addrln1, addrln2, city, state, zipcode)
        return
    
    def getAddress(self):
        return self.address

def computeTransactionCategory(transaction):
    transactionDescription = transaction["description"]
    switch(transactionDescription)
    return
    

