from datetime import datetime
from flask_website import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    ### Links to Progam db model 
    program = db.relationship('Program', backref='creator', lazy=True)

    def __repr__(self):
        return f"User ('{self.id}','{self.username}'),'{self.email}','{self.image_file}','{self.password}'"

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Program ('{self.name}'),'{self.description}','{self.created_date}', '{self.created_by}'"

class Project(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    program = realtionship("Program")

class Geometry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f"Geometry ('{self.name}'),'{self.description}','{self.created_date}'"

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    geometry =
    
class Case(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    geometry = relationship("Geometry")
    
class RideHeight(db.Model):
     id = db.Column(db.Integer, primary_key=True)
    FRH = db.Column(db.Float(), nullable=False)
    RRH = db.Column(db.Float(), nullable=False)
    YAW = db.Column(db.Float(), nullable=False)

