

port=5000

print("Pearl Before Swine Multiplayer Clone Server")



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










players={"1":None,"2":None}

gameplay=[[1,1,1,1,1],[1,1,1,1],[1,1,1]]



def startgame():
    emit("sendplayers",players,broadcast=True)
    emit("sendgame",gameplay,broadcast=True)





@socketio.on('Connection')
def Connection(username):
    global players

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



@socketio.on('disconnect')
def disconnected():
    print("user disconnected")































if __name__ == '__main__':
    print("Server started on port "+f"{port}")
    print("Waiting for 2 Players to Connect")
    socketio.run(app,host='0.0.0.0', port=port, debug=False)