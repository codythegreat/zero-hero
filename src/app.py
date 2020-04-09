import PySimpleGUI as sg

# model imports
import models.User as User
import models.Transaction as Transaction

# dash view import
import dash

# Layout allows selection of existing user or new user
layout = []

# get list of users and append to start of layout for selection
users = User.readUsers()
for user in users:
    layout.append([sg.Text(f"{user.get('fname', '')} {user.get('lname', '')} - {user.get('email', '')}")])
    layout.append([sg.Button('Select', key=user.get('id'))])

# add user creation form to layout
layout += [
    [sg.Text('Create a new user:')],
    [sg.Text('First Name')],
    [sg.InputText(key='fname')],
    [sg.Text('Last Name')],
    [sg.InputText(key='lname')],
    [sg.Text('Email')],
    [sg.InputText(key='email')],
    [sg.Button('Create')]
]

window = sg.Window('Zero Hero', layout)

while True:
    event, values = window.read()
    # handle existing user selection
    if (event == 'Select'):
        pass
    # handle new user creation
    elif (event == 'Create'):
        # add a new user
        user = User.User(values.get('fname'), values.get('lname'), values.get('email'))
        user.generate_user_file()
        user.generate_transactions_file()
        window.close()
        dash.dash(user.asDict())
    # on 'None' exit
    elif event is None:
        break

    # else, get the selected user and continue
    else:
        for user in users:
            if user.get('id') == event:
                window.close()
                print(f"{user.get('fname')} {user.get('lname')}")
                dash.dash(user)
        #TODO: go to transactions screen


    # log event and values to console for debugging
    print(event, ' -- ', values)

window.close()