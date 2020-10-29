# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import bot
import flask
import flask_socketio
import flask_sqlalchemy

from flask import request
from message_type import get_message_type

MESSAGES_RECEIVED_CHANNEL = 'messages received'
BOT_NAME = "1337-BOT"
BOT_PICTURE = "https://static-cdn.jtvnw.net/emoticons/v1/28/3.0"

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app
import models

user_emails = {}

def emit_all_messages(channel):
    messages = get_messages()
    all_messages = []
    for msg in messages:
        if(msg.sender == BOT_NAME):
            all_messages.append([msg.msg_type, BOT_PICTURE, BOT_NAME, msg.message])
        else:
            user = get_user(msg.sender)
            all_messages.append([msg.msg_type, user.profile_pic, user.name, msg.message])
    socketio.emit(channel, {
        'allMessages' : all_messages
    })

@socketio.on('connect')
def on_connect():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    socketio.emit('user count changed', {
        'users': len(user_emails.keys())
    })
    

@socketio.on('new google user')
def authorize(data):
    
    user_emails[request.sid] = data['email']
    update_user(data)
    socketio.emit('user count changed', {
        'users': len(user_emails.keys())
    })
    
@socketio.on('disconnect')
def on_disconnect():
    user_emails.pop(request.sid, None)
    socketio.emit('user count changed', {
        'users': len(user_emails.keys())
    })
    

@socketio.on('new message input')
def on_new_message(data):
    add_message_to_db(data)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")

def get_messages():
    return db.session.query(models.Chat).all()

def update_user(data):
    user = get_user(data['email'])
    if not user:
        db.session.add(models.Users(data['email'], data['name'], data['imageURL']));
        db.session.commit();
    else:
        user.name = data['name']
        user.profile_pic = data['imageURL']
        db.session.commit();

def add_message_to_db(data):
    message_type = get_message_type(data['message'])
    user = models.Users.query.get(user_emails[request.sid])
    db.session.add(models.Chat(user.email, data['message'], message_type));
    db.session.commit();
    
    bot_answer = bot.command(data['message'])
    if bot_answer:
        db.session.add(models.Chat(BOT_NAME, bot_answer, 'text'));
        db.session.commit();
        
def get_user(email):
    return models.Users.query.get(email)
    
if __name__ == '__main__': 
    models.db.create_all()
    db.session.commit()
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )