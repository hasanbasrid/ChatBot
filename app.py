# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import bot
import flask
import flask_socketio
import flask_sqlalchemy
import random_name
import models
from flask import request

MESSAGES_RECEIVED_CHANNEL = 'messages received'
BOT_NAME = "1337-BOT"

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

users = 0
usernames = {}

def emit_all_messages(channel):
    all_messages = [[msg.sender, msg.message] for msg in db.session.query(models.Chat).all()]
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
    usernames[request.sid] = random_name.create_random_name()
    print(usernames[request.sid] + ' connected!')
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    global users
    users -= 1
    socketio.emit('user count changed', {
        'users': users
    })
    print (usernames[request.sid] + ' disconnected!')
    usernames.pop(request.sid)
    

@socketio.on('new message input')
def on_new_address(data):
    print("Got an event for new message input with data:", data)
    db.session.add(models.Chat(usernames[request.sid], data['message']));
    db.session.commit();
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    bot_answer = bot.command(data['message'])
    if bot_answer:
        db.session.add(models.Chat(BOT_NAME, bot_answer));
        db.session.commit();
        emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@app.route('/')
def index():
    models.db.create_all()
    db.session.commit()
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )


    