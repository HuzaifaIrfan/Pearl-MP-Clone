

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



player1=None
player2=None


















@socketio.on('Connection')
def Connection(username):
    print(username,"connected")





































if __name__ == '__main__':
    print("Server started on port "+f"{port}")
    print("Waiting for 2 Players to Connect")
    socketio.run(app,host='0.0.0.0', port=port, debug=False)