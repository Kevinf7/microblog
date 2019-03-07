from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin, AnonymousUserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    email = db.Column(db.String(120), index=True, unique=True)
    #store hash of the password instead of actual password in db
    password_hash = db.Column(db.String(128))
    #this is not an actual database field
    #added to the one side, and is used to easily access the many side
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    #override constructor so we can assign default role to user
    def __init__(self,**kwargs):
        #also call parent constructor
        super(User, self).__init__(**kwargs)
        self.role = Role.query.filter_by(default=True).first()

    #generate hash of given password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #return hash of given password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=monsterid&s={}'.format(digest, size)

    def is_admin(self):
        return self.role.name == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)

#This allows application to freely call these methods even if you're not logged in
class AnonymousUser(AnonymousUserMixin):
    def set_password(self, password):
        return False
    def check_password(self, password):
        return False
    def avatar(self, size):
        return False
    def is_admin(self):
        return False
#This tells flask login which class to use if user is not logged in
login.anonymous_user = AnonymousUser

class Role(db.Model):
    __tablename__='role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #only one role is set to true this is to be used as the default role
    #we also set index to true as the application will search for this field
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User',backref='role',lazy='dynamic')

class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    #Use utcnow to store time in database so it is universal
    #we pass in the function 'utcnow' NOT the results of the function 'utcnow()'
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

#Used by flask-login
#This callback is used to reload the user object from the user ID stored in the session
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
