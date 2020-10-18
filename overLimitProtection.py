import requests
import sqlite3
import json


def setOverLimitProtection(cardHolderID, accountID, limitAmount):
    return

def checkIfOverLimit(cardHolderID, accountID, cardID):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    #Insert user into the customers database
    result = c.execute("SELECT overLimitProtectionThreshold FROM merchants WHERE cardHolderID=\"" + cardHolderID +"\"")
    protectionThreshold = c.fetchall()[0]
    print(protectionThreshold)
    conn.close()
    return 

def hitLimit(accessToken,cardHolderID, accountID, cardID):

    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders/"+ str(cardHolderID) +"/accounts/"+ string(accountID) + "/cards/"+ string(cardID)

    payload = {"status": "frozen"}
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "Authorization": "Bearer " + accessToken
    }

    response = requests.request("PUT", url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(response)