from . import db
from werkzeug.security import generate_password_hash, check_password_hash
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
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    jokes = db.relationship('Joke', backref='user', lazy='dynamic')
    commentsjokes = db.relationship('Commentjoke', backref = 'user', lazy = 'dynamic')
    debate = db.relationship('Debate', backref = 'user', lazy = 'dynamic')
    commentsdebates = db.relationship('Commentdebate', backref = 'user', lazy = 'dynamic')
    pickups = db.relationship('Pickup', backref = 'user', lazy = 'dynamic')
    commentspickups = db.relationship('Commentlines', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'

class Joke(db.Model):
    __tablename__ = 'jokes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Commentjoke', backref='title', lazy='dynamic')

    def save_joke(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_jokes(cls):
        jokes = Joke.query.all()
        return jokes

class Commentjoke(db.Model):
    __tablename__ = 'jokecomments'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id'))
    description = db.Column(db.String(255))

    def save_comment(self):
        """
        Function that saves the jokes' comments
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Commentjoke.query.filter_by(joke_id=id).all()
        return comment

    def __repr__(self):
        return f'Comment: {self.content}'
class Pickup(db.Model):
    __tablename__ = 'lines'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Commentlines', backref='title', lazy='dynamic')

    def save_pickup(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pickups(cls):
        lines = Pickup.query.all()
        return lines

class Commentlines(db.Model):
    __tablename__ = 'linescomments'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pickup_id = db.Column(db.Integer, db.ForeignKey('lines.id'))
    description = db.Column(db.String(255))

    def save_commentl(self):
        """
        Function that saves the pickup lines' comments
        """
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_commentsl(self, id):
        comment = Commentlines.query.filter_by(pickup_id=id).all()
        return comment

    def __repr__(self):
        return f'Comment: {self.content}'

class Debate(db.Model):
    __tablename__ = 'debates'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Commentdebate', backref='title', lazy='dynamic')

    def save_debate(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_debates(cls):
        debs = Debate.query.all()
        return debs

class Commentdebate(db.Model):
    __tablename__ = 'debatecomments'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    debate_id = db.Column(db.Integer, db.ForeignKey('debates.id'))
    description = db.Column(db.String(255))

    def save_commentd(self):
        """
        Function that saves the debates' comments
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_commentsd(self, id):
        comment = Commentdebate.query.filter_by(debate_id=id).all()
        return comment

    def __repr__(self):
        return f'Comment: {self.content}'