import SyrupUser as su
import requests
import sqlite3
import json

#Documentation to creating a db from sqlite : https://docs.python.org/3/library/sqlite3.html
def setupDBs():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()

    #Create table
    c.execute('''CREATE TABLE customers
                (cardHolderID, email, password)''')
    #Save (commit) the changes
    conn.commit()
    #We can also close the connection if we are done with it.
    #Just be sure any changes have been committed or they will be lost.
    conn.close()


    conn = sqlite3.connect('merchants.db')
    c = conn.cursor()
    #Create table
    c.execute('''CREATE TABLE merchants (merchant_name, category)''')
    conn.commit()
    conn.close()


def createUser (first_name, last_name, email, password, agreements, DOB, idString, id_type,incomeAmount, incomeFrequency, incomeOccupation, incomeSource, mobileNumber, shippingAddress1='', shippingAddress2='', shippingCity='', shippingState='', shippingZipcode='', addrln1='', addrln2='', city='', state='', zipcode='', productID=''):

    url = "https://sandbox.galileo-ft.com/instant/v1/cardholders"
    
    payload = {"cardholder": {
        "address": {
            "state": state,
            "city": city,
            "street": addrln1,
            "unit": addrln2,
            "zip_code": zipcode
        },
        "identification": {
            "date_of_birth": DOB,
            "id": idString,
            "id_type": id_type
        },
        "income": {
            "frequency": incomeFrequency,
            "amount": incomeAmount,
            "occupation": incomeOccupation,
            "source": incomeSource
        },
        "shipping_address": {
            "city": shippingCity,
            "state": shippingState,
            "street": shippingAddress1,
            "zip_code": shippingZipcode,
            "unit": shippingAddress2
        },
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "mobile": mobileNumber
    }}
    headers = {
        "accept": "*/*",
        "content-type": "application/json"
    }

    response = requests.request("POST", url, headers=headers)

    if response.status_code != 201:
        raise Exception(response)
    responseObj = response.json()

    cardHolderID = int(responseObj['cardholder_id'])

    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    #Insert user into the customers database
    c.execute("INSERT INTO customers VALUES (%s,%s, %s, %s)" % (cardHolderID, email, password))
    #Save (commit) the changes
    conn.commit()
    return
