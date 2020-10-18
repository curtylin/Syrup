import sqlite3
import Syrup as syrup
import random

def getAllCategories():
    conn = sqlite3.connect('merchants.db')
    c = conn.cursor() 

    c.execute("SELECT category FROM merchants")
    categories = c.fetchall()
    possibleCategories = set()
    for category in categories:
        possibleCategories.add(category[0])
    return possibleCategories

def getIgnoredCategories(cardHolderID, accountID):
    topThreeCategories = set()
    for category in syrup.getTopThreeCategories(cardHolderID, accountID):
        topThreeCategories.add(category)
    return (getAllCategories() - topThreeCategories)

def suggestIgnoredMerchants(cardHolderID, accountID):
    numberOfMerchants = 4
    ignoredMerchants = getIgnoredMerchants(cardHolderID, accountID)
    suggested = []
    for i in range(numberOfMerchants):
        suggested.append(random.choice(ignoredMerchants))
    return suggested


    

def getIgnoredMerchants(cardHolderID, accountID):
    ignoredCategories = getIgnoredCategories(cardHolderID, accountID)

    conn = sqlite3.connect('merchants.db')
    c = conn.cursor() 
    merchants = []
    for ignoredCategory in ignoredCategories:
        c.execute("SELECT merchant_name FROM merchants WHERE category=\"" + ignoredCategory + "\"")
        merchants.append(c.fetchall()[0][0])
    conn.close()
    return merchants


