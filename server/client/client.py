
from os import system
import time

def clearscreen():
    system("cls")
    print("Pearl before Swine MultiPlayer Clone - Python TUI Client")

def exitter(msg):
    print(msg)
    input("Return")





import socketio

sio = socketio.Client()

# username=input("Enter Your Name??\n")
username="player"


            



def menu():
    exit=False



    # time.sleep(1)



    while(not exit):
        clearscreen()
        print("C. Create Game")
        print("F. Fetch Game")
        print("X. Exit Game")
        ch=input("Enter Number to Start")
        if ch=="c"or ch=="C":
            exitter("Creating Game")
            sio.emit('creategame')
            exit=True
        elif ch=="f" or ch=="F":
            exitter("Fetching Games")
            sio.emit('fetchgames')
            exit=True
        elif ch=="x"or ch=="X":
            sio.disconnect()
            exit=True
            exitter("Bye Bye")
        else:
            exitter("Please Choose from Above")
            


def asknum(msg,high):
	anum=None
	while(anum==None):
		try:
			anum=int(input(msg))
		except:
			print(f"Number required (from 1-{high})")
			continue

		if (anum <1 or anum >high):
			print(f"Write a Number (from 1-{high})")
			anum=None


	return anum



def drawgame(gamecontent):
    clearscreen()
    for row in gamecontent.values():
        for item in row:
            if item ==1:
                print("O",end="")
            else:
                print("-",end="")
        print("")









@sio.event
def connect():
    print(sio.sid)
    print('Connection established')
    menu()



@sio.event
def gamecreated():
    clearscreen()
    print("Game created")
    print("Waiting for Player to Join")




@sio.event
def notfree(player1name):
    clearscreen()
    exitter(f"{player1name} Not Free")
    menu()


@sio.event
def loadinggame(loader):
    clearscreen()
    print("Starting Game with",loader["opponent"])
    drawgame(loader["game"]["gameplay"])



# @sio.event
# def startgame(game):
#     clearscreen()
#     exitter("Starting Game")



@sio.event
def showgames(freegames):
    clearscreen()
    print("Free Games")
    print(freegames)
    if len(freegames)>0:

        for i in range(0,len(freegames)):
            print(i+1,":",freegames[i]["creator"])
        
        gamenum=asknum("Enter Game ID",len(freegames))

        sio.emit('joingame', freegames[gamenum-1]["gameid"])



    else:
        menu()







@sio.event
def disconnect():
    print('Disconnected from server')




clearscreen()

sio.connect('http://localhost:5000/')

sio.emit('Connection', username)






sio.wait()

exitter("Exiting the Game")