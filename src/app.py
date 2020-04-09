import PySimpleGUI as sg

# model imports
import models.User as User
import models.Transaction as Transaction

# dash view import
import dash

# create PySimpleGUI layout for user selection
def createUserSelect(users):
    layout = []
    for user in users:
        layout.append([sg.Text(f"{user.get('fname', '')} {user.get('lname', '')} - {user.get('email', '')}")])
        layout.append([sg.Button('Select', key=user.get('id'))])
    return layout

# create PySimpleGUI layout for user creation form
def createNewUserForm():
    return [
        [sg.Text('Create a new user:')],
        [sg.Text('First Name')],
        [sg.InputText(key='fname')],
        [sg.Text('Last Name')],
        [sg.InputText(key='lname')],
        [sg.Text('Email')],
        [sg.InputText(key='email')],
        [sg.Button('Create')]
    ]

# combines user select and new user form layouts
def createLayout(users):
    return createUserSelect(users) + createNewUserForm()

while __name__ == "__main__":
    # get users for user selection
    users = User.readUsers()

    # initialize the window
    window = sg.Window('Zero Hero', createLayout(users))

    # on button click, read event and values
    event, values = window.read()

    # handle new user creation
    if (event == 'Create'):

        # make sure that all form inputs are filled
        unfilled = False
        for v in values.values():
            if v == '':
                unfilled = True

        # add a new user and go to dash if filled
        if not unfilled:
            user = User.User(values.get('fname'), values.get('lname'), values.get('email'))
            user.generate_user_file()
            user.generate_transactions_file()
            window.close()
            dash.dash(user.asDict())

        # close and reload window
        else:
            window.close()

    # on 'None' exit
    elif event is None:
        break

    # else, get the selected user and continue
    else:
        for user in users:
            if user.get('id') == event:
                window.close()
                dash.dash(user)

    # log event and values to console for debugging
    print(event, ' -- ', values)

window.close()