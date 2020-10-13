# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_socketio
import random_name
from flask import request

MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)


socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

all_messages = []
user_names = {}

def emit_all_messages(channel):
    socketio.emit(channel, {
        'allMessages' : all_messages
    })

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    user_names[request.sid] = random_name.create_random_name()
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new message input')
def on_new_address(data):
    print("Got an event for new message input with data:", data)
    all_messages.append([user_names[request.sid], data['message']])
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )


    