from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

#from blog import db, login_manager
from blog import login_manager


@login_manager.user_loader 
def load_user(id):
    from blog import data
    return  data.get_user_by_id(int(id))    

""" class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    nome = db.Column(db.String(30),  nullable=False)
    cognome = db.Column(db.String(30),   nullable=False)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    image = db.Column(db.String(120))

    def __repr__(self):
        return f"User('{ self.id }', '{ self.username }', '{ self.email }')"

    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) """

class User(UserMixin):
    id : int
    created_at : datetime
    nome : str
    cognome : str
    username : str
    email : str
    password : str
    posts : list
    image : str
    
    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


""" class Post(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(240))
    body = db.Column(db.Text(), nullable=False)
    markdown = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(120))
    

    def __repr__(self):
        return f"Post('{ self.id }', '{ self.title }')" """

class Post(): 
    id : int
    user_id : int
    created_at : datetime
    title : str
    description : str
    body : str
    markdown : bool
    image : str
