from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
                           validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description',
                           validators=[DataRequired()])
    submit = SubmitField('Create Program')

    def validate_program_name(self,program):
        program = Program.query.filter_by(program = program.data).first() # check if it already exists in db
        if program:
            raise ValidationError('Program taken already. Please use a unique program')