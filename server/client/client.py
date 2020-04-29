
from os import system


def clearscreen():
    system("cls")
    print("Pearl before Swine MultiPlayer Clone - Python TUI Client")


import socketio

sio = socketio.Client()

username=input("Enter Your Name??\n")





@sio.event
def connect():
    print('connection established')



# @sio.event
# def sendid(gotid):










@sio.event
def disconnect():
    print('Disconnected from server')







clearscreen()

sio.connect('http://localhost:5000/')



sio.emit('Connection', username)

sio.wait()

