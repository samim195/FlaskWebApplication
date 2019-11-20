from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PedForm(FlaskForm):
    terminal = IntegerField('Terminal', validators=[DataRequired()])
    serial = StringField('Serial', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    delivered_to_customer = StringField('Delivered To Customer', validators=[DataRequired()])
    date_delivered = StringField('Date Delivered', validators=[DataRequired()])
    returned_to_logistics = StringField('Returned To Logistics', validators=[DataRequired()])
    date_returned = StringField('Date Returned', validators=[DataRequired()])
    submit = SubmitField('ped')

# class PedSearchForm(FlaskForm):
#     choices = [('serial')]
#     select = SelectField('Search for Device:', choices=choices)
#     search = StringField('')