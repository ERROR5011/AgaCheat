from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', f'{username} has joined the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', f'{username} has left the room.', room=room)

@socketio.on('message')
def on_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    emit('message', f'{username}: {message}', room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
