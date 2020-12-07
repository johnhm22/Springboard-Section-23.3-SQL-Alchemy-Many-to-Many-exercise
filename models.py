"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)

    last_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)

    image_url = db.Column(db.String(500),
                    nullable=True,
                    unique=False)
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    nullable = False,
                    autoincrement=True)
    
    title = db.Column(db.String(50),
                    nullable = False,
                    unique = True)
                
    content = db.Column(db.String(1000),
                    nullable=False,
                    unique = True)
    
    created_at = db.Column(db.DateTime,
                    nullable = False,
                    default = datetime.utcnow
                    )

    assignments = db.relationship('PostTag', backref = 'posts')


class Tag(db.Model):
    __tablename__ = 'tags'

       id = db.Column(db.Integer,
                    primary_key=True,
                    nullable = False,
                    autoincrement=True)
    
        name = db.Column(db.String(100),
                    nullable = False,
                    unique = True) 

        assignments = db.relationship('PostTag', backref = 'tags')


class PostTag(db.Model):

   __tablename__ = 'post_tags'

   post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
   tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)



    user_id = db.Column(
                    db.Integer,
                    db.ForeignKey('users.id'))


    user = db.relationship('User', backref='posts')
