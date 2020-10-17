import SyrupUser as su
import requests


## Spending dictionary where users are stored.
users = []

def createUser (first_name, last_name, email, agreements, DOB, idString, id_type,incomeAmount, incomeFrequency, incomeOccupation, incomeSource, mobileNumber, shippingAddress1, shippingAddress2='', shippingCity, shippingState, shippingZipcode, addrln1, addrln2='', city, state, zipcode, productID):

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

    user = su.User(cardHolderID)
    users[cardHolderID] = user
    return

# At the start of each month, all of the transactions for each user is reset and cleared. 
def NewMonth():
    for user in users:
        user.clearTransactions()
