from sqlalchemy import Table, Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import mapper,relationship,backref
from .database import metadata, db_session 

class User(object):
    query = db_session.query_property()

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)
        
    def save(self,user):
        db_session.add(user)
        db_session.commit()
        db_session.remove()

    def update(self):
        db_session.commit()
        db_session.remove()
    
    def rollBack(self):
        db_session.rollback()
        
users = Table('User', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), unique=True),
    Column('email', String(120), unique=True),
    Column('password', String),
    Column('is_active',Boolean,default=False)
)

mapper(User, users)