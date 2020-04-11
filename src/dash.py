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
    return [
        [
            sg.Button('Delete'),
            sg.Button('Edit') 
        ]
    ]

# create a pysimplegui table from transactions list
def createTransactionsTable(transactions):
    try:
        # add a header for the rows of transactions
        layout = [[sg.Text('Select', size=(20,1))] + [sg.Text(h, size=(20,1)) for h in transactions[0][1:]]] 

        # add each row to the layout with checkbox to select
        for t in transactions[1:]:
            layout += [
                [sg.Checkbox('', size=(17,1), key=t[0])] +
                [sg.Text(c, size=(20,1)) for c in t[1:]]
            ]

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
        [sg.Button('Add'), sg.Button('Update', visible=False)]
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

    # Get the sum of all transactions to 2 decimal places
    sum = format(Transaction.sumListOfTransactions(transactions[1:]), '.2f')
    # Get count of transactions
    count = len(transactions[1:])
    # Add transaction statistics to layout
    layout += [
        [sg.Text(f"You have ${sum} to allocate. You've created {count} transactions.")]
    ]

    # add a header for the rows of transactions
    layout += createTransactionsTable(transactions)

    # add transaction form to layout
    layout += createTransactionForm()

    return layout

def handleEventAndValues(event, values, window, user):

    userFile = user.get('transactions_file')

    # on Add, create new transaction from form, save to CSV file, refresh window
    if (event == 'Add'):
        # create a new transaction
        t = Transaction.Transaction(values.get('title'), values.get('description'), values.get('amount'), values.get('date'))
        # write transaction to file
        Transaction.writeTransactionToFile(userFile, t)

    # on Delete, transaction will be removed from user's csv file
    if (event == 'Delete'):
        for k, v in values.items():
            if v == True:
                Transaction.deleteTransactionFromFile(userFile, k)

    # on Edit, fill form inputs with transaction details
    if (event == 'Edit'):
        for k, v in values.items():
            if v == True:
                # Get the transaction's values
                t = Transaction.retrieveTransactionFromFile(userFile, k)
                # update from inputs with transaction's values
                window['title'].update(t.get('title'))
                window['description'].update(t.get('description'))
                window['amount'].update(t.get('amount'))
                window['date'].update(t.get('date'))

                # make update button visible and add invisible
                window['Update'].update(visible=True)
                window['Add'].update(visible=False)

                # reread event and values for Update event
                event, values = window.read()

                # return when finished so transactions are reset
                return handleEventAndValues(event, values, window, user)
    
    if (event == 'Update'):
        for k, v in values.items():
            if v == True:
                Transaction.deleteTransactionFromFile(userFile, k)
                t = Transaction.Transaction(values.get('title'), values.get('description'), values.get('amount'), values.get('date'))
                # write transaction to file
                Transaction.writeTransactionToFile(userFile, t)
                return

    # on Save, user selects folder for csv to be saved to
    if (event == 'Save'):
        pass

    # on exit, exit loop where window will close
    if event is None:
        return 1



def dash(user):
    # loop until event, and handle event
    while True:
        # initialize the window
        window = sg.Window(f"Zero Hero: {user.get('fname')} {user.get('lname')}", createLayout(user))

        # on button click, read event and values
        event, values = window.read()

        # execute appropriate code based on event and values
        # if return value is 1 (exit button) break
        if handleEventAndValues(event, values, window, user):
            break
        
        # for debugging, print the current event and values
        print(event, ' -- ', values)

        window.close()

    # close the window and exit program
    window.close()