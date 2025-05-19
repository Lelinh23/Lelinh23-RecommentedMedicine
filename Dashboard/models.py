import Levenshtein
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from fuzzywuzzy import fuzz

bcrypt = Bcrypt()

# Kết nối với Firebase
try:
    cred = credentials.Certificate('data-recoment-drugs.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    print("Firebase initialization error:", e)
    
# Khởi tạo Firestore
db = firestore.client()

class Admin(UserMixin):
    def __init__(self, id, firstname, lastname, age, gender, email, address, password, pastcondition):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.email = email
        self.address = address
        self.password = password
        self.pastcondition = pastcondition

    @staticmethod
    def add_admin(id, firstname, lastname, age, gender, email, address, password, pastcondition):
        db.collection('admins').document(id).set({
            'firstname': firstname,
            'lastname': lastname,
            'age': age,
            'gender': gender,
            'email': email,
            'address': address,
            'password': bcrypt.generate_password_hash(password).decode('utf-8'),
            'pastcondition': pastcondition
        })

    @staticmethod
    def get_admin_by_email(email):
        admins = db.collection('admins').where('email', '==', email).stream()
        for admin in admins:
            print(admin.to_dict())  # In ra kết quả
            admin_data = admin.to_dict()
            admin_data['id'] = admin.id
            return admin_data
        return None

# Thêm, sửa, xóa Bác sĩ
class Doctor():
    def __init__(self, id, firstname, lastname, age, gender, email, address, disease,specialization, star):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.email = email
        self.address = address
        self.disease = disease
        self.specialization = specialization
        self.star = star
        
    @staticmethod
    def add_doctor(id, firstname, lastname, age, gender, email, address, disease, specialization, star):
        db.collection('doctors').document(id).set({
            'firstname': firstname,
            'lastname': lastname,
            'age': age,
            'gender': gender,
            'email': email,
            'address': address,
            'disease': disease,
            'specialization': specialization,
            'star': star
        })
        
    @staticmethod
    def get_all_doctors():
        docs = db.collection('doctors').stream()
        doctor_list = []
        for doc in docs:
            data = doc.to_dict()
            doctor_list.append(
                Doctor(
                    id=doc.id,
                    firstname=data.get('firstname'),
                    lastname=data.get('lastname'),
                    age=data.get('age'),
                    gender=data.get('gender'),
                    email=data.get('email'),
                    address=data.get('address'),
                    disease=data.get('disease'),
                    specialization=data.get('specialization'),
                    star=data.get('star')
                )
            )
        return doctor_list
    
# Thêm, sửa, xóa User
class User(UserMixin):
    def __init__(self, id, firstname, lastname, age, gender, email, address, password, pastcondition):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.email = email
        self.address = address
        self.password = password
        self.pastcondition = pastcondition
        
    @staticmethod
    def add_user(id, firstname, lastname, age, gender, email, address, password, pastcondition):
        db.collection('users').document(id).set({
            'firstname': firstname,
            'lastname': lastname,
            'age': age,
            'gender': gender,
            'email': email,
            'address': address,
            'password': bcrypt.generate_password_hash(password).decode('utf-8'),
            'pastcondition': pastcondition
        })
        
    @staticmethod
    def get_all_user():
        docs = db.collection('users').stream()
        users_list = []
        for doc in docs:
            data = doc.to_dict()
            users_list.append(
                User(
                    id=doc.id,
                    firstname=data.get('firstname'),
                    lastname=data.get('lastname'),
                    age=data.get('age'),
                    gender=data.get('gender'),
                    email=data.get('email'),
                    address=data.get('address'),
                    password=data.get('password', None),
                    pastcondition=data.get('pastcondition')
                )
            )
        return users_list