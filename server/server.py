

port=5000

print("Pearl Before Swine Multiplayer Clone Server")
import time
import random


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





users={}

games={}


# gameplay=[[1,1,1,1,1],[1,1,1,1],[1,1,1]]





@socketio.on('Connection')
def Connection(username):
    global users
    userobj={"userid":request.sid,"username":username,"connected":True,"opponent":None,"gameid":None}
    users[request.sid]=userobj
    print(users)
    # emit("sendgame",{"players":players,"gameplay":gameplay},broadcast=True)



@socketio.on('creategame')
def creategame():
    global users
    global games
    gameid=str(random.getrandbits(128))

    users[request.sid]["gameid"]=gameid

    gameobj={"gameid":gameid,"creator":users[request.sid]["username"],"player1":request.sid,"p1again":None,"player2":None,"p2again":None,"game":None}
    games[gameid]=gameobj
    # print(users)
    emit("gamecreated")




@socketio.on('fetchgames')
def fetchgames():
    global games
    freegames=[]
    for game in games.values():
        if game["player2"]==None:
            freegames.append(game)

    emit("showgames",freegames)




@socketio.on('joingame')
def joingame(gotgameid):
    global games
    global users

    if games[gotgameid]["player2"]==None:
        games[gotgameid]["player2"]=request.sid
        users[request.sid]["gameid"]=gotgameid
        users[request.sid]["opponent"]=games[gotgameid]["player1"]
        users[games[gotgameid]["player1"]]["opponent"]=games[gotgameid]["player2"]


        games[gotgameid]["game"]={"gameid":gotgameid,"player1":{"username":users[games[gotgameid]["player1"]]["username"],"score":0,"turn":False},"player2":{"username":users[games[gotgameid]["player2"]]["username"],"score":0,"turn":True},"gameplay":[[1,1,1,1,1],[1,1,1,1],[1,1,1]]}


        emit("loadinggame",{"game":games[gotgameid]["game"],"opponent":games[gotgameid]["game"]["player2"]["username"],"turn":games[gotgameid]["game"]["player1"]["turn"]}  ,room=games[gotgameid]["player1"])
        emit("loadinggame",{"game":games[gotgameid]["game"],"opponent":games[gotgameid]["game"]["player1"]["username"],"turn":games[gotgameid]["game"]["player2"]["turn"]}  ,room=games[gotgameid]["player2"])




    

    else:
        emit("notfree",games[gotgameid]["creator"])








@socketio.on('disconnect')
def disconnected():
    global users
    global games
    users[request.sid]["connected"]=False
    print(users[request.sid]["username"],"Disconnected")

    opponentid=users[request.sid]["opponent"]
    gameid=users[request.sid]["gameid"]

    if not(gameid == None):
        games[gameid]["player2"]="noone"
    if not(opponentid == None):
        users[opponentid]["gameid"]=None
        users[opponentid]["opponent"]=None
        emit("opponentleft",users[request.sid]["username"],room=opponentid)


if __name__ == '__main__':
    print("Server started on port "+f"{port}")
    print("Waiting for Players to Connect")
    socketio.run(app,host='0.0.0.0', port=port, debug=False)