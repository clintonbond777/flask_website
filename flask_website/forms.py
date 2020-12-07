from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_website.models import User, Program
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username taken already. Please use a unique username')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken already. Please use a unique email')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username: #if changed from current db 
            user = User.query.filter_by(username = username.data).first() # check if it already exists in db
            if user:
                raise ValidationError('Username taken already. Please use a unique username')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email taken already. Please use a unique email')

class CreateProgramForm(FlaskForm):
    name =  StringField('Program Name',
                           validators=[DataRequired(), 
                           Length(min=2, max=20)])

    description = StringField('Description',
                           validators=[DataRequired()])
    submit = SubmitField('Create Program')

    def validate_program_name(self, program):
        program_validate = Program.query.filter_by(program = name.data).first() # check if it already exists in db
        if program_validate:
            raise ValidationError('Program taken already. Please use a unique program')
   
class CreateProjectForm(FlaskForm):
    def get_current_programs():
        return [(str(u.id),u.name) for u in Program.query.all()]
    # select program to be associated with
    program_select = SelectField(choices = get_current_programs())
    # create name of project
    name =  StringField('Project',
                           validators=[DataRequired(), 
                           Length(min=2, max=20)])
    # put a description of the project

    description = StringField('Description',
                           validators=[DataRequired()])


    #submit all that information to server with nice button 
    submit = SubmitField('Create Project')

class CreateCaseForm(FlaskForm):
    # figure out which project the user came from and assume that is where they want to create a case

    # else figure out what project it needs to be placed in a double level list.

    def get_current_program():
        return [(str(u.id),u.name) for u in Program.query.all()]
    # select program to be associated with
    program_select = SelectField(choices = get_current_programs())
    # create name of project
    name =  StringField('Project',
                           validators=[DataRequired(), 
                           Length(min=2, max=20)])
    # put a description of the project

    description = StringField('Description',
                           validators=[DataRequired()])


    #submit all that information to server with nice button 
    submit = SubmitField('Create Project')