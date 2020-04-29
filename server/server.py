

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





users={}

games={}


# gameplay=[[1,1,1,1,1],[1,1,1,1],[1,1,1]]


@socketio.on('Connection')
def Connection(username):
    global users
    userobj={"username":username,"connected":True}
    users[request.sid]=userobj
    # print(users)
    # emit("sendgame",{"players":players,"gameplay":gameplay},broadcast=True)




@socketio.on('disconnect')
def disconnected():
    global users
    users[request.sid]["connected"]=False
    print(users[request.sid]["username"],"Disconnected")


if __name__ == '__main__':
    print("Server started on port "+f"{port}")
    print("Waiting for Players to Connect")
    socketio.run(app,host='0.0.0.0', port=port, debug=False)