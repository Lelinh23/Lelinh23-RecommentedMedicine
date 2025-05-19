from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import numpy as np
import pandas as pd
import ast
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from utils.model_loader import *
from text_processing.matching import *

bcrypt = Bcrypt()

# Kết nối với Firebase
try:
    cred = credentials.Certificate('data-recoment-drugs.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    print("Firebase initialization error:", e)
    
# Khởi tạo Firestore
db = firestore.client()

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
    def get_user_by_email(email):
        users = db.collection('users').where('email', '==', email).stream()
        for user in users:
            user_data = user.to_dict()
            user_data['id'] = user.id
            return user_data
        return None

class Consultation_Dease:
    def __init__(self, user_id, symptoms, suggested_medicine, date, notes=None):
        self.user_id = user_id
        self.symptoms = symptoms
        self.suggested_medicine = suggested_medicine
        self.date = date
        self.notes = notes

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "symptoms": self.symptoms,
            "suggested_medicine": self.suggested_medicine,
            "date": self.date,
            "notes": self.notes,
        }
        
def predict_conditions_symptom(selectedOptions):
    """Defining a function to recommend medicine"""
    inputs = np.array(selectedOptions)  # convert list to NumPy array
    inputs = inputs.reshape(1, -1)
    # Pass the inputs to your machine learning model and retrieve the predicted result
    recommend_Med = model_med.predict(inputs)
    # Return the predicted result to the user
    return recommend_Med[0]   

def serviceValidation(selected_symptoms):
    # Kiểm tra nếu model_N đã được tải thành công
    if model_N is None:
        raise ValueError("Model_N has not been loaded. Please check the model file.")

    # Chuyển đổi các triệu chứng thành đầu vào cho mô hình
    # Khởi tạo vector triệu chứng với giá trị mặc định là 0
    inputs = {key: 0 for key in symptom_mapping_d.keys()}
    
    # Chỉ cập nhật giá trị cho các triệu chứng nằm trong danh sách hợp lệ
    for s in selected_symptoms:
        if s in inputs:
            inputs[s] = 1

    # Chuyển đổi list thành NumPy array
    # inputs = np.array(inputs)
    # inputs = inputs.reshape(1, -1)
    
    # Tạo DataFrame từ vector triệu chứng
    df_test = pd.DataFrame(columns=list(inputs.keys()))
    df_test.loc[0] = np.array(list(inputs.values()))

    # Truyền inputs vào mô hình máy học để dự đoán
    predicted_result = model_N.predict(df_test)  # Lấy kết quả đầu tiên (dự đoán)
    # Chuyển từ mảng NumPy thành chuỗi đơn
    predicted_result = predicted_result[0] if isinstance(predicted_result, (list, np.ndarray)) else predicted_result
    print("Predicted result:", predicted_result)
    print("Type of predicted_result:", type(predicted_result))


    # Lấy mô tả bệnh từ helper
    dis_desc, dis_pre, dis_workout, dis_die = helper(predicted_result)
    print("Description of the predicted disease:", dis_desc)

    # Trả về kết quả dự đoán và mô tả  'Drug': re_med , "description": dis_desc, 'precautions': dis_pre, 'workout': dis_workout, 'diets': dis_die
    return {"predicted_result": predicted_result, "description": dis_desc, 'precautions': dis_pre, 'workout': dis_workout, 'diets': dis_die}

def helper(dis):
    
    desc = descrip[descrip['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precaution_df[precaution_df['Disease'] == dis][['Symptom_precaution_0','Symptom_precaution_1','Symptom_precaution_2','Symptom_precaution_3']]
    pre = pre.values.flatten()  # Chuyển thành mảng phẳng
    # Loại bỏ giá trị None hoặc NaN
    # Loại bỏ các giá trị NaN thực tế (numpy.nan) và giá trị None
    pre = [p for p in pre if p is not None and pd.notna(p)]
    
    diet_str = diets[diets['Disease'] == dis]['Diet']
    
    # Kiểm tra xem có dữ liệu không và chuyển chuỗi thành danh sách
    if diet_str.size > 0:
        diet_list = ast.literal_eval(diet_str.iloc[0])  # Chuyển chuỗi thành danh sách
    else:
        diet_list = []

    wrkout = workout[workout['disease'] == dis]['workout']
    wrkout = [wrkout for wrkout in wrkout.values]

    return desc, pre, wrkout, diet_list
