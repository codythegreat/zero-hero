import PySimpleGUI as sg
import pathlib
import csv
import models.User as User
import models.Transaction as Transaction

# path to data folder
DATA_DIR = pathlib.Path(__file__).parent.parent.absolute().as_posix() + '/data/'

# return list of transactions from given csv file
def CSVToListOfTransactions(filename):
    try:
        t = []
        with open(DATA_DIR + filename, newline='') as csvFile:
            csvReader = csv.reader(csvFile)
            for row in csvReader:
                t.append(row)
        return t
    except:
        return []

def createTransactionButtonRow():
    return [[sg.Button('Delete'), sg.Button('Edit')]]

# create a pysimplegui table from transactions list
def createTransactionsTable(transactions):
    try:
        # add a header for the rows of transactions
        layout = [[sg.Text('Select', size=(20,1))] + [sg.Text(h, size=(20,1)) for h in transactions[0][1:]]] 

        # add each row to the layout with checkbox to select
        for t in transactions[1:]:
            layout += [[sg.Checkbox('', size=(17,1), key=t[0])]+[ sg.Text(c, size=(20,1)) for c in t[1:]]]

        # add bottom row of table controls
        layout += createTransactionButtonRow()
        return layout
    except:
        return []

# create a pysimplegui form to create new transaction
def createTransactionForm():
    return [
        [sg.Text('Add Transaction')],
        [sg.Text('Amount')],
        [sg.InputText(key='amount')],
        [sg.Text('Title')],
        [sg.InputText(key='title')],
        [sg.Text('Description')],
        [sg.InputText(key='description')],
        [sg.Text('Date')],
        [sg.InputText(key='date')],
        [sg.Button('Add')]
    ]

# creates layout with greeting, transactions, and form
def createLayout(user):
    # Say hello to the user 
    username = f"{user.get('fname')} {user.get('lname')}"
    layout = [
        [sg.Text(f"Hello {username}")]
    ]

    # if transactions exist, add them to an iterable list
    transactions = CSVToListOfTransactions(user.get('transactions_file'))

    # add transaction statistics to layout
    sum = Transaction.sumListOfTransactions(transactions[1:])
    layout += [
        [sg.Text(f"You have ${sum} to allocate. You've created {len(transactions[1:])} transactions.")]
    ]

    # add a header for the rows of transactions
    layout += createTransactionsTable(transactions)

    # add transaction form to layout
    layout += createTransactionForm()

    return layout

def dash(user):
    # loop until event, and handle event
    while True:
        # initialize the window
        window = sg.Window(f"Zero Hero: {user.get('fname')} {user.get('lname')}", createLayout(user))

        # on button click, read event and values
        event, values = window.read()

        # on Add, create new transaction from form, save to CSV file, refresh window
        if (event == 'Add'):
            # create a new transaction
            t = Transaction.Transaction(values.get('title'), values.get('description'), values.get('amount'), values.get('date'))
            # write transaction to file
            Transaction.writeTransactionToFile(user.get('transactions_file'), t)
            # close the window (create a new window on next loop)
            window.close()

        # on Delete, transaction will be removed from user's csv file
        if (event == 'Delete'):
            for k, v in values.items():
                if v == True:
                    Transaction.deleteTransactionFromFile(user.get('transactions_file',), k)
            window.close()
        
        # on Export, user selects folder for csv to be saved to
        if (event == 'Export'):
            pass

        # on exit, exit loop where window will close
        if event is None:
            break
        
        # for debugging, print the current event and values
        print(event, ' -- ', values)

    # close the window and exit program
    window.close()