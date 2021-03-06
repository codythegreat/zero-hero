import uuid
import random
import csv
from datetime import datetime
import pathlib

# path to data directory
DATA_DIR = pathlib.Path(__file__).parent.parent.parent.absolute().as_posix() + '/data/'

class Transaction:
    """ represents a (single) transaction """
    def __init__(self, t, d, amt, date):

        # create a unique ID
        self._id = uuid.uuid4()

        # assign title, desc and amt
        self.title = t
        self.description = d
        self.amount = amt

        # create date from string
        if date is None:
            self.date = datetime.now()
        else:
            self.date = date

    # return a representation of the instance as dictionary 
    def asDict(self):
        return {
            'id': self._id.int,
            'title': self.title,
            'description': self.description,
            'amount': self.amount,
            'date': self.date.strftime("%m/%d/%Y")
        }

    def __repr__(self):
        return str(self.asDict())
    
    def __str__(self):
        return f"{self.title} : {self.amount}"
    
    def setAmount(self, a):
        self.amount = a
    
    def setTitle(self, t):
        self.title = t

    def setDesc(self, d):
        self.description = d
    
    def setDate(self, d):
        self.date = datetime.strptime(d, '%m/%d/%y %H:%M:%S')

def writeTransactionToFile(filename, transaction):
    # if file doesn't already exist, it'll need a header
    fileExists = pathlib.Path(DATA_DIR+filename).is_file()

    # open csv and write our Transaction to the file (in dict format)
    with open(DATA_DIR + filename, 'a', newline='') as csvfile:
        csvWriter = csv.DictWriter(csvfile, fieldnames=transaction.asDict().keys())
        if not fileExists:
            csvWriter.writeheader()
        csvWriter.writerow(transaction.asDict())

# delete a specific transaction from a given file
def deleteTransactionFromFile(filename, transactionID):
    with open(DATA_DIR + filename, "r") as f:
        data = list(csv.reader(f))

    with open(DATA_DIR + filename, "w") as f:
        writer = csv.writer(f)
        for row in data:
            if row[0] != transactionID:
                writer.writerow(row)

def retrieveTransactionFromFile(filename, transactionID):
    with open(DATA_DIR + filename, 'r') as f:
        data = list(csv.reader(f))
        for row in data:
            if row[0] == transactionID:
                return {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'amount': row[3],
                    'date': row[4],
                }


# takes a list of transactions and returns sum of 4th col (amt)
def sumListOfTransactions(transactions):
    sum = 0
    # add each amount in column 3 for each row
    for t in transactions:
        sum += float(t[3])
    return sum
