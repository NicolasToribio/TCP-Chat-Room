import socket
import threading
import PySimpleGUI as sg
import queue

message_queue = queue.Queue()

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                message_queue.put(message)
        except:
            print("An error occured!")
            client.close()
            break

def write(message):
    message = f'{nickname}: {message}'
    client.send(message.encode('ascii'))

# Startup window
layout = [[sg.Text('Enter host IP:'), sg.InputText(key='-IP-')],
          [sg.Text('Enter nickname:'), sg.InputText(key='-NICK-')],
          [sg.Button('Connect'), sg.Button('Exit')]]

window = sg.Window('Startup', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        exit(0)
    elif event == 'Connect':
        host = values['-IP-']
        nickname = values['-NICK-']
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, 55555))
        break

window.close()

# Main chat window
layout = [[sg.Output(size=(50,20), key='-OUTPUT-')],
          [sg.InputText(key='-IN-', size=(44,1)), sg.Button('Send', bind_return_key=True)]]

window = sg.Window('Chat Window', layout, return_keyboard_events=True)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

while True:
    event, values = window.read(timeout=100)  # Check for events every 100 ms
    if event == sg.WINDOW_CLOSED:
        client.close()
        exit(0)
    elif event == 'Send':
        write(values['-IN-'])
        window['-IN-'].update('')
    while not message_queue.empty():
        message = message_queue.get()
        window['-OUTPUT-'].update(message+'\n', append=True)
