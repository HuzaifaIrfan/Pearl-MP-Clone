

port=5000

print("Pearl Before Swine Multiplayer Clone Server")
import time


from flask import Flask, render_template, session, request,jsonify, send_from_directory, \
copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect


async_mode = None

app = Flask(__name__, static_url_path='')
import logging
logss = logging.getLogger('werkzeug')
logss.disabled = True

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)








ids=["1","2"]

players={"1":None,"2":None}

gameplay=[[1,1,1,1,1],[1,1,1,1],[1,1,1]]



def startgame():
    #emit("sendplayers",players,broadcast=True)
    # time.sleep(1)
    global gameplay
    global players
    emit("sendgame",{"players":players,"gameplay":gameplay},broadcast=True)

    print(players["1"]["name"]," : ",players["1"]["score"]," Turn : ",players["1"]["turn"])
    print(players["2"]["name"]," : ",players["2"]["score"]," Turn : ",players["2"]["turn"])
    for row in gameplay:
        for item in row:
            if item==1:
                print("O",end="")
            else:
                print("-",end="")
        print("")






@socketio.on('Connection')
def Connection(username):
    global players
    print(request.sid)
    if players["1"]==None:
        players["1"]={"name":username,"turn":True,"score":0}
        emit("waiting")
        emit("sendid","1")
        print("Waiting for 1 Player to Connect")
        print(players)
    else:
        if players["2"]==None:
            players["2"]={"name":username,"turn":False,"score":0}
            print(players)
            emit("sendid","2")
            print("Starting Game")
            startgame()
        else:
            print("No space Left")
            emit("playersfull")





@socketio.on('sendgameplay')
def sendgameplay(gotgameplay):
    global gameplay
    global players
    global ids
    gameplay=gotgameplay

    left=0
    for row in gameplay:
        for item in row:
            if item==1:
                left=left+1

    if left<2:
        for aid in ids:
            if players[aid]["turn"]==True:
                gameplay=[[1,1,1,1,1],[1,1,1,1],[1,1,1]]
                players[aid]["score"]=players[aid]["score"]+1


    
    players["1"]["turn"]=not players["1"]["turn"]
    players["2"]["turn"]=not players["2"]["turn"]

    emit("sendgame",{"players":players,"gameplay":gameplay},broadcast=True)

    print(players["1"]["name"]," : ",players["1"]["score"])
    print(players["2"]["name"]," : ",players["2"]["score"])
    for row in gameplay:
        for item in row:
            if item==1:
                print("O",end="")
            else:
                print("-",end="")
        print("")









@socketio.on('disconnect')
def disconnected():
    print("user disconnected")































if __name__ == '__main__':
    print("Server started on port "+f"{port}")
    print("Waiting for Players to Connect")
    socketio.run(app,host='0.0.0.0', port=port, debug=False)