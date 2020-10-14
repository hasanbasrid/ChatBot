# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import bot
import flask
import flask_socketio
import random_name
from flask import request

MESSAGES_RECEIVED_CHANNEL = 'messages received'
BOT_NAME = "UNDECIDED-BOT"

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

users = 0
all_messages = []
user_names = {}


def emit_all_messages(channel):
    socketio.emit(channel, {
        'allMessages' : all_messages
    })

@socketio.on('connect')
def on_connect():
    global users
    users += 1
    socketio.emit('user count changed', {
        'users': users
    })
    user_names[request.sid] = random_name.create_random_name()
    print(user_names[request.sid] + ' connected!')
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    global users
    users -= 1
    socketio.emit('user count changed', {
        'users': users
    })
    print (user_names[request.sid] + ' disconnected!')
    user_names.pop(request.sid)
    

@socketio.on('new message input')
def on_new_address(data):
    print("Got an event for new message input with data:", data)
    all_messages.append([user_names[request.sid], data['message']])
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    bot_answer = bot.command(data['message'])
    if bot_answer:
        all_messages.append([BOT_NAME, bot_answer])
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


    