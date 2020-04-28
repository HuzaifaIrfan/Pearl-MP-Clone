
from os import system


def clearscreen():
    system("cls")
    print("Pearl before Swine MultiPlayer Clone - Python Client")


import socketio

sio = socketio.Client()

username="aplayer"
myid="0"




@sio.event
def connect():
    print('connection established')

@sio.event
def sendid(gotid):
    global myid
    myid=gotid

@sio.event
def waiting():
    clearscreen()
    print("Waiting for second Player")

@sio.event
def sendplayers():
    clearscreen()
    print("Starting the game")

@sio.event
def disconnect():
    print('disconnected from server')










clearscreen()

sio.connect('http://localhost:5000/')



sio.emit('Connection', username)

sio.wait()

