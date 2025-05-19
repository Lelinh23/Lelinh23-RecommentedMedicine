from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from model.models import *
from utils.model_loader import *

class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "First Name"})
    lastname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Last Name"})
    age = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Age"})
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    email = StringField(validators=[InputRequired(), Length(min=10, max=40)], render_kw={"placeholder": "Email"})
    address = StringField(validators=[InputRequired(), Length(min=4, max=2000)], render_kw={"placeholder": "City"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    pastcondition = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Past Conditions"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_user_email = User.get_user_by_email(email.data)
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

# Creating Symptoms dropdown Menu for selecting Symptoms
class serviceForm(FlaskForm):
    choices = [('', 'Select a Symptom')] + choices_symptom
    symptom1 = SelectField('1st Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom2 = SelectField('2nd Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom3 = SelectField('3rd Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom4 = SelectField('4th Symptom', choices=choices, default= None,validators=[DataRequired()])

class Reviews(FlaskForm):
    review = TextAreaField('Symptom', validators=[InputRequired(), Length(min=40, max=20000)], render_kw={"placeholder": "Enter symptom..."})
    submit = SubmitField('Recommend Drugs')
