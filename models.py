# models.py
import flask_sqlalchemy
from app import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(60))
    message = db.Column(db.String())
    
    def __init__(self, usr, msg):
        self.sender = usr
        self.message = msg
        
    def __repr__(self):
        return '<Message: %s>' % self.message