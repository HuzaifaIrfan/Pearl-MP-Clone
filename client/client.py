
from os import system


def clearscreen():
    system("cls")
    print("Pearl before Swine MultiPlayer Clone - Python Client")


import socketio

sio = socketio.Client()

username="aplayer"
myid="0"

players={}
gameplay=[]


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

# @sio.event
# def sendplayers(getplayers):
#     clearscreen()
#     print("Starting the game")
#     global players
#     players=getplayers


# @sio.event
# def startinggame(num):
#     clearscreen()
#     print("Starting game in",num,"seconds")



def drawscreen():
    global gameplay
    global players
    print(players["1"]["name"]," : ",players["1"]["score"],"                 ",players["2"]["name"]," : ",players["2"]["score"])
    for row in gameplay:
        for item in row:
            if item==1:
                print("O",end="")
            else:
                print("-",end="")
        print("")


def asknum(whatval):
	anum=None
	while(anum==None):
		try:
			anum=int(input(whatval))
		except:
			print("Number required")
			continue

		# if (anum <1 or anum >9):
		# 	print("Write a Number (from 1-9)")
		# 	anum=None


	return anum



def checkrow(rownum):
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
        


def askrow():
    rownum=0
    while(not checkrow(rownum)):
        rownum=asknum("Enter Row Number 1-3")
    asknumbers(rownum)


def checkitems(rownum,itemnum):
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


def removeitems(rownum,itemnum):
    global gameplay
    removed=0
    temprow=gameplay[rownum-1]
    length=len(temprow)
    for i in range(0,length):
        if removed < itemnum:
            if temprow[i]==1:
                temprow[i]=0
                removed= removed+1
    gameplay[rownum-1]=temprow
    #print(gameplay)
    input("")
    sio.emit('sendgameplay', gameplay)



def asknumbers(rownum):
    itemnum=0
    while(not checkitems(rownum,itemnum)):
          itemnum=asknum("Enter Number of pearls 1-3,4,5")
    removeitems(rownum,itemnum)





@sio.event
def sendgame(getgame):
    clearscreen()
    global players
    global gameplay
    players=getgame["players"]
    gameplay=getgame["gameplay"]
    # print(players)
    if players[myid]["turn"]==True:
        print("Your Turn")
    else:
        print("Opponent's Turn")
    drawscreen()
    if players[myid]["turn"]==True:
        askrow()
    


@sio.event
def playersfull():
    clearscreen()
    print("Two Players are already playing")


@sio.event
def disconnect():
    print('disconnected from server')










clearscreen()

sio.connect('http://localhost:5000/')



sio.emit('Connection', username)

sio.wait()

