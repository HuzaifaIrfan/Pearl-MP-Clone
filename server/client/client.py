
from os import system
import time

def clearscreen():
    system("clear")
    print("Pearl before Swine MultiPlayer Clone - Python TUI Client")

def exitter(msg):
    print(msg)
    input("Return")





import socketio

sio = socketio.Client()

username=input("Enter Your Name??\n")
# username="player"


            



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


def asknum(msg):
	anum=None
	while(anum==None):
		try:
			anum=int(input(msg))
		except:
			print("Number required")
			continue

	return anum



def asknumrange(msg,high):
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




def drawgamecontent(gamecontent):

    for row in gamecontent:
        for item in row:
            if item ==1:
                print("O",end="")
            else:
                print("-",end="")
        print("")
















def checkrow(gameplay,rownum):
    if rownum<1 or rownum>3:
        return False
    nitems=0
    rowitems=gameplay[rownum-1]
    for item in rowitems:
        if item==1:
            nitems=nitems+1
    if nitems==0:
        print("No items in this row please select another")
        return False
    return True
        

def checkitems(gameplay,rownum,itemnum):
    if itemnum==0:
        return False
    nitems=0
    rowitems=gameplay[rownum-1]
    for item in rowitems:
        if item==1:
            nitems=nitems+1
    if itemnum<=nitems:
        return True
    else:
        print("Too Many")
        return False





def asknumbers(gameplay,rownum):
    itemnum=0
    while(not checkitems(gameplay,rownum,itemnum)):
          itemnum=asknum("Enter Number of pearls 1-3,4,5\n")

    # removeitems(gameplay,rownum,itemnum)
    sio.emit('removepearls', {"row":rownum,"pearls":itemnum})





def askrow(gameplay):
    rownum=0
    while(not checkrow(gameplay,rownum)):
        rownum=asknum("Enter Row Number 1-3\n")
    asknumbers(gameplay,rownum)







# def removeitems(rownum,itemnum):
#     global gameplay
#     removed=0
#     temprow=gameplay[rownum-1]
#     length=len(temprow)
#     for i in range(0,length):
#         if removed < itemnum:
#             if temprow[i]==1:
#                 temprow[i]=0
#                 removed= removed+1
#     gameplay[rownum-1]=temprow
#     #print(gameplay)
#     input("")
#     sio.emit('sendgameplay', gameplay)

















def drawgame(gameobj):
    gameplay=gameobj["game"]["gameplay"]

    player1=gameobj["game"]["player1"]
    player2=gameobj["game"]["player2"]

    print(player1["username"],":",player1["score"])
    print(player2["username"],":",player2["score"])


    drawgamecontent(gameplay)
    global username
    if gameobj["turn"]==True:
        print(f"Your Turn {username}")
        askrow(gameplay)
    else:
        print(f"{gameobj['opponent']}'s Turn")








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
def opponentleft(opponentname):
    clearscreen()
    exitter(f"{opponentname} left the game.")
    menu()

@sio.event
def loadinggame(loader):
    clearscreen()
    print("Starting Game with",loader["opponent"])
    drawgame(loader)


@sio.event
def nextturn(gameobj):
    clearscreen()
    drawgame(gameobj)


@sio.event
def tomainmenu():
    clearscreen()
    menu()


def playagain():
    print("Do you want to play Again? Y/n ")
    ans=input("")
    if ans=="n"or ans=="N":
        sio.emit('noplayagain')
    else:
        sio.emit('playagain')
        print("Waiting for other Player to Respond!!")


@sio.event
def winner():
    clearscreen()
    print("You Win")

    playagain()




@sio.event
def looser():
    clearscreen()
    print("You Lose")

    playagain()


# @sio.event
# def startgame(game):
#     clearscreen()
#     exitter("Starting Game")



@sio.event
def showgames(freegames):
    clearscreen()
    print("Free Games")
    # print(freegames)
    if len(freegames)>0:

        for i in range(0,len(freegames)):
            print(i+1,":",freegames[i]["creator"])
        
        gamenum=asknumrange("Enter Game ID",len(freegames))

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