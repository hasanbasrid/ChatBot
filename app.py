# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import bot
import flask
import flask_socketio
import flask_sqlalchemy
import models
from flask import request
from message_type import get_message_type

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
user_emails = {}

def emit_all_messages(channel):
    messages = db.session.query(models.Chat).all()
    all_messages = []
    for msg in messages:
        user = models.Users.query.get(msg.sender)
        all_messages.append([msg.msg_type, user.profile_pic, user.name, msg.message])
    socketio.emit(channel, {
        'allMessages' : all_messages
    })

@socketio.on('connect')
def on_connect():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    print('Someone connected!')
    

@socketio.on('new google user')
def authorize(data):
    global users
    users += 1
    user_emails[request.sid] = data['email']
    print(user_emails)
    user = models.Users.query.get(user_emails[request.sid])
    if not user:
        db.session.add(models.Users(data['email'], data['name'], data['imageURL']));
        db.session.commit();
    else:
        user.name = data['name']
        user.profile_pic = data['imageURL']
        db.session.commit();

    socketio.emit('user count changed', {
        'users': users
    })
    
@socketio.on('disconnect')
def on_disconnect():
    global users
    users -= 1
    socketio.emit('user count changed', {
        'users': users
    })
    user_emails.pop(request.sid)

@socketio.on('new message input')
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    message_type = get_message_type(data['message'])
    user = models.Users.query.get(user_emails[request.sid])
    db.session.add(models.Chat(user.email, data['message'], message_type));
    db.session.commit();
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    bot_answer = bot.command(data['message'])
    if bot_answer:
        db.session.add(models.Chat(BOT_NAME, bot_answer, message_type));
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


    