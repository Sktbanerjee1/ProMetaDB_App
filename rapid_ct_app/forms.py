from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rapid_ct_app.models import User, Project
from rapid_ct_app.helpers import ProjectChoicesIter

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ProjectCreateForm(FlaskForm):
    # project name
    project = StringField('Project Name', validators=[
        DataRequired(),
        Length(min=3, max=10)
    ])
    
    # sample labels
    label = SelectField(
        'Samples label',
        choices=[
            ('Bleed-ICH', 'ICH patient with visible bleed'),
            ('Control', 'Normal patient without ICH'),
            ('Lesion', 'Patient with visible lesion '),
            ('Calcification', 'Patient with visible calcification'),
            ('No-ICH-abnormal', 'No visible condition but abnormal'),
            ('Unknown', 'No available label '),    
        ]
    )
    #submit
    submit = SubmitField('Create Project')

    def validate_project(self, project):
        project = Project.query.filter_by(project=project.data).first()
        if project:
            raise ValidationError('Existing project found with same name!')



class FileUploadForm(FlaskForm):
    # parent project
    parent_project = SelectField(
        'Parent project',
        choices= ProjectChoicesIter()
    )
    #submit
    submit =  SubmitField('Upload Files')