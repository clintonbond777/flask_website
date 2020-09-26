from datetime import datetime
from flask_website import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    ### Links to Progam db model 
    create_program= db.relationship('Program', backref='creator', lazy=True)

    def __repr__(self):
        return f"User|'{self.id}','{self.username}','{self.email}','{self.image_file}','{self.password}','{self.create_program}'"

class Program(db.Model):
    __tablename__ = 'program'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    
    ### Relationship
    project = db.relationship("Project", back_populates = "program") # forward

    def __repr__(self):
        return f"Program|'{self.name}'),'{self.description}','{self.created_date}', '{self.created_by}'" 
        
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow) #auto
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False) 
    program_id = db.Column(db.Integer,db.ForeignKey('program.id'), nullable = False)
    
    program = db.relationship("Program", back_populates = "project")
    
    case = db.relationship("Case", back_populates = "project") # forward

    def __repr__(self):
        return f"Program|'{self.name}'),'{self.description}','{self.created_date}','{self.created_by}', '{self.program_id}','{self.program}'"

class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    project_id= db.Column(db.Integer, db.ForeignKey('project.id'), nullable = False)
    geometry_id = db.Column(db.Integer, db.ForeignKey('geometry.id'), nullable = False)
    
    project = db.relationship("Project", back_populates = "case")


    def __repr__(self):
        return f"Case|('{self.id}','{self.name}'),'{self.description}','{self.project_id}','{self.geometry_id}'"

class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return f"Geometry|'{self.name}'),'{self.description}','{self.created_date}'"

class Part(db.Model):
    __tablename__ = 'part'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    description = db.Column(db.Text,unique=False, nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    created_by = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    
Model_Part = db.Table('Model_Part', db.Model.metadata,
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('part_id', db.Integer, db.ForeignKey('part.id'), primary_key=True)
)   


class RideHeight(db.Model):
    __tablename__ = 'rideheight'  
    id = db.Column(db.Integer, primary_key=True)
    frh= db.Column(db.Float(), nullable=False)
    rrh= db.Column(db.Float(), nullable=False)
    yaw= db.Column(db.Float(), nullable=False)
    roll = db.Column(db.Float(), nullable=False)

    ridemap = db.relationship('RideMap', secondary= 'RideMap_Rideheight', lazy = 'subquery', backref = db.backref('rideheight', lazy=True))

class RideMap(db.Model):
    __tablename__ = 'ridemap'  
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Float(), nullable=False)
    description= db.Column(db.Float(), nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)

    #rideheight1 = db.relationship('RideHeight', secondary= 'RideMap_Rideheight', lazy = 'subquery', backref = db.backref('ridemap', lazy=True))


RideMap_Rideheight = db.Table('RideMap_Rideheight', db.Model.metadata,
    db.Column('rideheight_id', db.Integer, db.ForeignKey('rideheight.id'),primary_key=True),
    db.Column('ridemap_id', db.Integer, db.ForeignKey('ridemap.id'), primary_key=True)
)
