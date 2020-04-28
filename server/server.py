


import eventlet
import socketio

port=5000

print("Pearl Before Swine Multiplayer Clone Server Running on PORT :",port)





sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})



@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)



























if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', port)), app)