from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, Length
from flask_login import UserMixin
from app.models import User
from flask_ckeditor import CKEditorField

#usermixin provides some handy functions for user class
class LoginForm(FlaskForm, UserMixin):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    #wtforms takes validate_<field_name> as custom validators
    #so the below validator gets invoked on username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already taken.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0,max=140)])
    submit = SubmitField('Submit')

    #overloaded constructor which saves an instance variable of the original username
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        #if data entered on form is different to the original name then...
        if username.data != self.original_username:
            #we want to check if the new name entered is already in the db
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('That username is already taken. Please enter another username')

class PostForm(FlaskForm):
    #post = TextAreaField('Say something', validators=[InputRequired(), Length(min=1, max=200)])
    post = CKEditorField('Say something')
    submit = SubmitField('Submit')
