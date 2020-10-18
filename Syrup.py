import SyrupUser as su
import overLimitProtection as olp
import requests
import sqlite3
import json
#import mysql.connector

_accessToken = ''        #Access token used throughout the API requests
_refreshToken = ''       #Refresh token used to refresh access to the API

#Documentation to creating a db from sqlite : https://docs.python.org/3/library/sqlite3.html
def setupDBs():
    # conn = sqlite3.connect('customers.db')
    # c = conn.cursor()
    # c.execute("DROP TABLE customers")

    # #Create table
    # c.execute('''CREATE TABLE customers 
    #             ( cardHolderID integer NOT NULL AUTO_INCREMENT PRIMARY KEY, email text NOT NULL, password text NOT NULL);''' )
    # #Save (commit) the changes
    # conn.commit()
    # #We can also close the connection if we are done with it.
    # #Just be sure any changes have been committed or they will be lost.
    # conn.close()


    conn = sqlite3.connect('merchants.db')
    c = conn.cursor()
    c.execute("DROP TABLE merchants")
    #Create table
    c.execute('''CREATE TABLE merchants (merchant_name, category)''')
    conn.commit()
    conn.close()

def setTokens(accessToken, refreshAuthorizationToken):
    global _accessToken, _refreshToken
    _accessToken = accessToken
    _refreshToken = refreshAuthorizationToken


def refreshAuthorization():
    url = "https://sandbox.galileo-ft.com/instant/v1/refresh"

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer " + _refreshToken
    }

    response = requests.request("POST", url , headers=headers)

    _accessToken = response.json()["access_token"]
    return response.json()["access_token"]

def getCardholderAgreements(productID):
    agreements = []
    businessID = 59115

    url = "https://sandbox.galileo-ft.com/instant/v1/businesses/"+ str(businessID) +"/products/"+str(productID)+"/agreements"

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer " + _accessToken
    }
    try:
        response = requests.request("GET", url, headers=headers)
        responseObj = response.json()
        for agreement in responseObj['agreements']:
            agreements.append(agreement["agreement_id"])
    except:
        refreshAuthorization()
        response = requests.request("GET", url, headers=headers)
        responseObj = response.json()
        for agreement in responseObj['agreements']:
            agreements.append(int(agreement["agreement_id"]))
    print(agreements)
    return agreements

def createUser (first_name, last_name, email, password, DOB, idString, id_type,incomeAmount, incomeFrequency, incomeOccupation, incomeSource, mobileNumber, shippingAddress1='', shippingAddress2='', shippingCity='', shippingState='', shippingZipcode='', addrln1='', addrln2='', city='', state='', zipcode='', productID=''):

    agreements = []
    agreements = getCardholderAgreements(productID)


    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders"
    
    payload = {
    "cardholder": {
        "address": {
            "city": city,
            "state": state,
            "street": addrln2,
            "zip_code": zipcode,
            "unit": addrln2
        },
        "agreements": agreements,
        "identification": {
            "date_of_birth": DOB,
            "id": idString,
            "id_type": id_type
        },
        "income": {
            "amount": incomeAmount,
            "frequency": incomeFrequency,
            "occupation": incomeOccupation,
            "source": incomeSource
        },
        "shipping_address": {
            "city": shippingCity,
            "state": shippingState,
            "street": shippingAddress1,
            "unit": shippingAddress2,
            "zip_code": shippingZipcode
        },
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "mobile": mobileNumber
    },
    "product_id": productID
}
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "Authorization": "Bearer " + _accessToken,
    }
    print("payload")
    print(payload)
    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code != 201:
        raise Exception(response,response.json())
    responseObj = response.json()

    cardHolderID = int(responseObj['cardholder_id'])

    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    #Insert user into the customers database
    c.execute("INSERT INTO customers VALUES (%s,%s, %s)", (cardHolderID,email, password))
    #Save (commit) the changes
    conn.commit()
    return

def calculateMonthlyTopThreeCategories(accessToken, cardHolderID, accountID):
    spending = {}
    conn = sqlite3.connect('merchants.db')
    c = conn.cursor()
   
    transactions = su.getCurrentMonthTransactions(accessToken, cardHolderID, accountID)
    for transaction in transactions:
        merchantName = transactions[transaction][1]
        result = c.execute("SELECT category FROM merchants WHERE merchant_name=\"" + merchantName +"\"")
        category = c.fetchall()[0][0]
        if category not in spending:
            spending[category] = abs(transactions[transaction][0])
        spending[category] += abs(transactions[transaction][0]) 
    
    #https://stackoverflow.com/questions/40496518/how-to-get-the-3-items-with-the-highest-value-from-dictionary
    topCategories = sorted(spending, key=spending.get, reverse=True)[:3]
    conn.close()
    return topCategories

#def deleteALLUsers():
