# models.py
import flask_sqlalchemy
from app import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String())
    message = db.Column(db.String())
    msg_type = db.Column(db.String(10))
    
    def __init__(self, usr, msg, msg_type):
        self.sender = usr
        self.message = msg
        self.msg_type = msg_type
        
    def __repr__(self):
        return '<Message: %s>' % self.message
        

class Users(db.Model):
    email = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    profile_pic = db.Column(db.String())
    
    def __init__(self, email, name, profile_pic):
        self.email = email
        self.name = name
        self.profile_pic = profile_pic
    
    def __repr__(self):
        return '<User: profilepic: {} name : {} email: {}>'.format(self.profile_pic, self.email, self.name)