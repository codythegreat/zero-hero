import PySimpleGUI as sg

# Layout allows selection of existing user or new user
layout = [
    #TODO: existing user

    # or create a new user
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
        pass
    print(event, ' -- ', values)