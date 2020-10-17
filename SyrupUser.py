
class User:
    def __init__(self, id):
        # Spending dictionary where keys are categories and definition is the amount in that month.
        self.spending = {}
        # Total Spending is the current total for the current month.
        self.totalSpending = 0

        self.id = id

    def createTransaction (self, transaction):
        category = transaction["category"]
        amount = float(transaction["amount"])
        self.spending[category] += amount
        self.totalSpending += amount
        return

    def clearTransactions (self):
        self.spending = {}
        self.totalSpending = 0

def computeTransactionCategory(transaction):
    transactionDescription = transaction["description"]
    switch(transactionDescription)
    return
    

