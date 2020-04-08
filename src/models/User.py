# used to create unique ids for each user
import uuid
# used when generated user file name
import random
# used to get path of current file (__file__) to generate user file
import pathlib
# used to generate JSON file
import json
# for listing files in readUsers function
from os import listdir

# directory to data files
DATA_DIR = pathlib.Path(__file__).parent.parent.parent.absolute().as_posix() + '/data/'

# On user selection screen, if 'Create' is clicked 
# a new instance of User will be initialized
class User:
    """Represents end user"""
    def __init__(self, f, l, e):

        # create a unique ID
        self._id = uuid.uuid4()

        # base file name
        self._base_file_name = f"{f}-{l}-{random.randrange(0, 10000)}"

        # create a unique file to hold user info
        self.user_file = self._base_file_name + '.json'

        # csv file holding all transactions
        self.transactions_file = self._base_file_name + '.csv'

        # assign first, last and email
        self.fname = f
        self.lname = l
        self.email = e

        # if user is active, they'll appear selectable in app
        self.active = True
    

    def __repr__(self):
        return str({
            'id': self.getIDasInt(),
            'user_file': self.user_file,
            'transactions_file': self.transactions_file,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'active': True})
    
    def __str__(self):
        return f"{self.fname} {self.lname} - {self.email}"

    def getIDasInt(self):
        return self._id.int

    # generates a unique user file
    def generate_user_file(self):
        with open(DATA_DIR + self.user_file, 'w') as outfile:
            json.dump(repr(self), outfile)
    
    # generates a unique CSV file that holds transaction detials
    def generate_transactions_file(self):
        pass


# returns a list of users
def readUsers():
    # holds list of users and their corresponding data
    users = []

    # append each .json file's data to users list
    for f in listdir(DATA_DIR):
        if f.endswith('.json'):
            with open(DATA_DIR + f, 'r') as data:
                userData = json.load(data)
                users.append(userData)
    
    return users

s = User('Cody', 'Maxie', 'maxiecody@gmail.com')
s.generate_user_file()
readUsers()