import Syrup as syrup
import SyrupUser as su
import MerchantsSeeding as ms
import BonusCashBack as bcb
import requests
import json

## Testing script for all of the API and transactions. 

# Api URL: https://sandbox.galileo-ft.com/instant/v1/
GalileoAPIUsername = 'CgZ1b6oVWOGP'
GalileoAPIPassword = '2nN3YeCt52DGe9wf0Xa2'
accessToken = ''        #Access token used throughout the API requests
refreshToken = ''       #Refresh token used to refresh access to the API


def setupTest():
    # response = requests.post('https://sandbox.galileo-ft.com/instant/v1/login?username=' + GalileoAPIUsername + '&password=' + GalileoAPIPassword)
    response = requests.post(f'https://sandbox.galileo-ft.com/instant/v1/login?username={GalileoAPIUsername}&password={GalileoAPIPassword}')
    # if response.status_code != 201 or response.status_code != 200:
    #     raise Exception(response)
    responseObj = response.json()
    accessToken = responseObj['access_token']
    refreshToken = responseObj['refresh_token']
    syrup.setTokens(accessToken=accessToken, refreshAuthorizationToken=refreshToken)
    syrup.setupDBs()
    ms.seedMerchants()
    return

def createUsers():
    syrup.createUser(first_name="Curtis", last_name="Lin", email="clxddf@gmail.com", password="123Password$%^", DOB="2000-01-01", idString="110229485", id_type="ssn", incomeAmount="u150k", incomeFrequency="weekly", incomeOccupation="science_engineering", incomeSource="employment", mobileNumber="1237890456", shippingAddress1="1234E 100S", shippingAddress2="Apt. 1", shippingCity="Salt Lake City", shippingState="UT", shippingZipcode="84102", addrln1="1234E 100S", addrln2="Apt. 1", city="Salt Lake City", state="UT", zipcode="84102", productID=19467)
    syrup.createUser(first_name="Bill", last_name="Nye", email="jssfk@gmail.com", password="123Password$%^", DOB="2000-03-04", idString="112289015", id_type="ssn", incomeAmount="u150k", incomeFrequency="weekly", incomeOccupation="science_engineering", incomeSource="employment", mobileNumber="9087654321", shippingAddress1="1234E 100S", shippingAddress2="Apt. 1", shippingCity="Salt Lake City", shippingState="UT", shippingZipcode="84102", addrln1="1234E 100S", addrln2="Apt. 1", city="Salt Lake City", state="UT", zipcode="84102", productID=19467)
    syrup.createUser(first_name="Jonathan", last_name="Fairbanks", email="jddgy@gmail.com", password="123Password$%^", DOB="2000-03-04", idString="112901845", id_type="ssn", incomeAmount="u150k", incomeFrequency="weekly", incomeOccupation="science_engineering", incomeSource="employment", mobileNumber="1204378956", shippingAddress1="1234E 100S", shippingAddress2="Apt. 1", shippingCity="Salt Lake City", shippingState="UT", shippingZipcode="84102", addrln1="1234E 100S", addrln2="Apt. 1", city="Salt Lake City", state="UT", zipcode="84102", productID=19467)
    syrup.createUser(first_name="Jeff", last_name="Gay", email="billnye@gmail.com", password="123Password$%^", DOB="2000-03-04", idString="122148105", id_type="ssn", incomeAmount="u150k", incomeFrequency="weekly", incomeOccupation="science_engineering", incomeSource="employment", mobileNumber="1230478956", shippingAddress1="1234E 100S", shippingAddress2="Apt. 1", shippingCity="Salt Lake City", shippingState="UT", shippingZipcode="84102", addrln1="1234E 100S", addrln2="Apt. 1", city="Salt Lake City", state="UT", zipcode="84102", productID=19467)

def fundAndCreateTransactions():
    su.fundAccount(test_AccountID, dashboardAccountID, 30)
    su.createTransaction(cardHolderID=test_CardHolderID, accountID=test_AccountID, amount=2, merchantName="Chipotle")
    su.createTransaction(cardHolderID=test_CardHolderID, accountID=test_AccountID, amount=3.2, merchantName="Smiths")
    su.createTransaction(cardHolderID=test_CardHolderID, accountID=test_AccountID, amount=4.43, merchantName="Delta")
    su.createTransaction(cardHolderID=test_CardHolderID, accountID=test_AccountID, amount=2.58, merchantName="Apple_Inc")
    su.createTransaction(cardHolderID=test_CardHolderID, accountID=test_AccountID, amount=4, merchantName="Chipotle")



setupTest()
# createUsers()
# fundAndCreateTransactions()


test_CardHolderID = 5063
dashboardAccountID = 10467
test_AccountID = su.listAccounts(accessToken, test_CardHolderID)[0]


# calculatedMonthlyCategories = syrup.calculateMonthlyCategories(test_CardHolderID, test_AccountID)
# topThreeCategories = syrup.getTopThreeCategories(calculatedMonthlyCategories)

print(bcb.getIgnoredMerchants(test_CardHolderID, test_AccountID))

