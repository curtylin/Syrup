import Syrup as syrup
import SyrupUser as su
import MerchantsSeeding as ms
import requests
import json

## Testing script for all of the API and transactions. 

# Api URL: https://sandbox.galileo-ft.com/instant/v1/
GalileoAPIUsername = ''
GalileoAPIPassword = ''
accessToken = ''        #Access token used throughout the API requests
refreshToken = ''       #Refresh token used to refresh access to the API


def setupTest():
    response = requests.post('https://sandbox.galileo-ft.com/instant/v1/login?username=' + GalileoAPIUsername + '&password=' + GalileoAPIPassword)
    if response.status_code != 200:
        raise Exception(response)
    responseObj = response.json()
    accessToken = responseObj['access_token']
    refreshToken = responseObj['refresh_token']
    ms.seedMerchants()
    return


setupTest()

syrup.createUser("Curtis", "Lin", "clx@gmail.com", "123Password$%^", [1,2,3], "2000-03-04", 000000000, "ssn", "u150k", "weekly", "science_engineering", "employment", 0000000000, "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234")
syrup.createUser("Bill", "Nye", "billnye@gmail.com", "123Password$%^", [1,2,3], "2000-03-04", 000000000, "ssn", "u150k", "weekly", "science_engineering", "employment", 0000000000, "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234")
syrup.createUser("Jonathan", "Fairbanks", "jfk@gmail.com", "123Password$%^", [1,2,3], "2000-03-04", 000000000, "ssn", "u150k", "weekly", "science_engineering", "employment", 0000000000, "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234")
syrup.createUser("Jeff", "Gay", "jgy@gmail.com", "123Password$%^", [1,2,3], "2000-03-04", 000000000, "ssn", "u150k", "weekly", "science_engineering", "employment", 0000000000, "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234E 100S", "", "Salt Lake City", "UT", "84102", "1234")

curtisCardHolderID = syrup.getCardHolderID("clx@gmail.com")
curtisAccountID = su.createSpendingAccount(curtisCardHolderID)
su.createTransaction(curtisCardHolderID, curtisAccountID, 20, "Chipotle")
su.createTransaction(curtisCardHolderID, curtisAccountID, 30, "Smiths")
su.createTransaction(curtisCardHolderID, curtisAccountID, 222, "Delta")
su.createTransaction(curtisCardHolderID, curtisAccountID, 1200.58, "Apple_Inc")
su.createTransaction(curtisCardHolderID, curtisAccountID, 20, "Chipotle")

print(su.calculateMonthlyTopThreeCategories())




