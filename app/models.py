from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    upvotes = db.relationship('Upvote', backref = 'user', lazy = 'dynamic')
    downvotes = db.relationship('Downvote', backref = 'user', lazy = 'dynamic')
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)     
    def __repr__(self):
        return f'User {self.username}'  

class Pitch(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    category = db.Column(db.String(255))
    content = db.Column(db.String(255))
    comments = db.relationship('Comment', backref = 'pitch', lazy = 'dynamic')
    upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
    downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')
    def __repr__(self):
        return f'The pitch category {self.category}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    description = db.Column(db.String(255))
    def __repr__(self):
        return f'Comment: {self.description}'        


class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    number_upvote = db.Column(db.Integer,default=1)
    def __repr__(self):
        return f'Upvote number: {self.number_upvote}'  


class Downvote(db.Model):
    __tablename__ = 'downvotes'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    number_downvote = db.Column(db.Integer,default=1)
    def __repr__(self):
        return f'Downvote number: {self.number_downvote}'            