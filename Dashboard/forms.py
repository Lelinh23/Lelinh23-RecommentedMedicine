from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, EqualTo, NumberRange
from models import *

class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "First Name"})
    lastname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Last Name"})
    age = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Age"})
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    email = StringField(validators=[InputRequired(), Length(min=10, max=40)], render_kw={"placeholder": "Email"})
    address = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "City"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    confirmpassword = PasswordField(
        validators=[
            InputRequired(), 
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Confirm Password"}
    )
    pastcondition = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Past Conditions"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_user_email = Admin.get_admin_by_email(email.data)
        if existing_user_email:
            raise ValidationError('That email already exists.')

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Email"})
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

class medForm(FlaskForm):
    gender = SelectField('Gender :', render_kw={"style": "width: 170px;"}, choices=[('', 'Select your gender'), (1, 'Male'), (0, 'Female')], default=None, validators=[DataRequired()])
    age = StringField(validators=[InputRequired()], render_kw={"style": "width: 60px;", "placeholder": "Age"})
    severity = SelectField('Severity :', render_kw={"style": "width: 220px;"}, choices=[('', 'Select the level of severity'), (0, 'Few days'), (1, 'A week'), (2, 'Few weeks or more')], default=None, validators=[DataRequired()])
    disease = SelectField('Disease :', render_kw={"style": "width: 150px;"}, choices=[('', 'Select the disease'), (0, 'Diarrhea'), (1, 'Gastritis'), (2, 'Arthritis'), (3, 'Migraine')], default=None, validators=[DataRequired()])

class AddDoctor(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "First Name"})
    lastname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Last Name"})
    age = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Age"})
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    email = StringField(validators=[InputRequired(), Length(min=10, max=40)], render_kw={"placeholder": "Email"})
    address = StringField(validators=[InputRequired(), Length(min=4, max=5000)], render_kw={"placeholder": "City"})
    disease = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Disease"})
    specialization = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Specialization"})
    star = IntegerField(validators=[InputRequired(), NumberRange(min=1, max=5)], render_kw={"placeholder": "Star"})
    submit = SubmitField('Add Doctor')
    
