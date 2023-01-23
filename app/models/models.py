# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
import datetime
from enum import unique
from pyparsing import countedArray
from sqlalchemy import desc, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import expression
from app import db


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer,db.Identity(start=1, cycle=True), primary_key=True)#, server_default=TABLE_ID.next_value())
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())


# Define a User model
class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 

    # User Name + Fullname
    descrpt  = db.Column(db.String(128),  nullable=False)
    username = db.Column(db.String(128),  nullable=False, unique=True)
    fullname = db.Column(db.String(128),  nullable=False)
    image    = db.Column(db.String(128),  nullable=False)
    password = db.Column(db.String(128),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, descrpt, username, fullname, image, password):
        self.descrpt  = descrpt
        self.username = username
        self.fullname = fullname
        self.image    = image
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.userID) 

class Status(Base):
    __tablename__ = 'status'
    __table_args__ = {'extend_existing': True} 

    # User Name + Fullname
    username = db.Column(db.String(128),  nullable=False, unique=True)
    online   = db.Column(db.Boolean,  nullable=False, server_default=expression.false())
    last_seen= db.Column(db.DateTime,  default=db.func.current_timestamp())
    page     = db.Column(db.String(128),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, username, online, last_seen, page):
        self.username = username
        self.online   = online
        self.last_seen= last_seen
        self.page     = page

    def __repr__(self):
        return '<Status %r>' % (self.username)

class TruthDareHistory(Base):
    __tablename__ = 'truth_dare_history'
    __table_args__ = {'extend_existing': True} 

    # User Name + Fullname
    username = db.Column(db.String(128),  nullable=False)
    type     = db.Column(db.String(128),  nullable=False)
    cardID       = db.Column(db.Integer,  nullable=False)

    # New instance instantiation procedure
    def __init__(self, username, type, cardID):
        self.username = username
        self.type     = type
        self.cardID   = cardID

    def __repr__(self):
        return '<TruthDareHistory %r>' % (self.id)

class DnD_Campaign(Base):
    __tablename__ = 'dnd_campaign'
    __table_args__ = {'extend_existing': True} 

    name     = db.Column(db.String(128),  nullable=False)
    descrpt  = db.Column(db.String(1000),  nullable=False)
    theme    = db.Column(db.String(128),  nullable=False)
    location = db.Column(db.String(128),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, descrpt, theme, location):
        self.name     = name
        self.descrpt  = descrpt
        self.theme    = theme
        self.location = location

class DnD_Conversation(Base):
    __tablename__ = 'dnd_conversation'
    __table_args__ = {'extend_existing': True} 

    username = db.Column(db.String(128),  nullable=False)
    campaignID = db.Column(db.Integer,  nullable=False)
    message  = db.Column(db.String(12000),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, username, campaignID, message):
        self.username = username
        self.campaignID = campaignID
        self.message  = message

    def __repr__(self):
        return '<DnD_Conversation %r>' % (self.id)

class DnD_Context(Base):
    __tablename__ = 'dnd_context'
    __table_args__ = {'extend_existing': True} 

    campaignID = db.Column(db.Integer,  nullable=False)
    context  = db.Column(db.String(12000),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, campaignID, context):
        self.campaignID = campaignID
        self.context  = context

    def __repr__(self):
        return '<DnD_Context %r>' % (self.id)