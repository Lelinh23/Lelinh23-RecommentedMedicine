from datetime import datetime
import math
from flask_bcrypt import Bcrypt
from flask import Blueprint, Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, RegisterForm, medForm
from firebase_admin import credentials, firestore, initialize_app
from model.models import *
from model.symptom import *
from forms import *

auth = Blueprint('auth', __name__)
admin = Flask(__name__)
bcrypt = Bcrypt(admin)

global response

response=dict()
response2=dict()

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user_data = User.get_user_by_email(form.email.data)
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user_obj = User(**user_data)
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('service.service_route'))
        flash('Invalid email or password.', 'error')
    return render_template('signin.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.add_user(
            id=request.form.get('email'),
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            age=form.age.data,
            gender=form.gender.data,
            email=form.email.data,
            address=form.address.data,
            password=form.password.data,
            pastcondition=form.pastcondition.data
        )
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.signin'))
    return render_template('register.html', form=form)

