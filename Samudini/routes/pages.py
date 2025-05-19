from flask_bcrypt import Bcrypt
from flask import Blueprint, Flask, render_template, request, jsonify
import math
from model.models import *
from model.symptom import *
from model.recomment_df import *

admin = Blueprint('admin', __name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)

response2=dict()
response3=dict()
response=dict()
response2 = []

@admin.route('/faq')
def faq():
    symptoms = get_symptoms()
    
    # Lấy dữ liệu từ Firebase
    doc_ref = db.collection('term_servic_pages').document('samudi_terms')
    doc = doc_ref.get()
    if not doc.exists:
        return "No data found. Please initialize the data."
    
    d = doc.to_dict()
    return render_template('faq.html', data=d, symptoms=symptoms)

response2 = []
# Nhận dữ liệu từ yêu cầu AJAX, xử lý dữ liệu triệu chứng để dự đoán bệnh, và trả về thông tin dự đoán cùng các biện pháp phòng ngừa.
@admin.route('/send_data', methods=['POST'])
def send_data():
    # Retrieve the data from the AJAX request
    global symptoms 
    symptoms = request.get_json()
    print("symptoms",symptoms)

    symsmapping = create_symptom_mapping(symptoms, symptom_mapping)
    
    # Dự đoán bệnh: model_dis.predict_proba() trả về xác suất của từng bệnh
    probabilities = model_dis.predict_proba([symsmapping])
    disease_probabilities = dict(zip(model_dis.classes_, probabilities[0]))

    top_n = 5
    sorted_probabilities = sorted(disease_probabilities.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # Prepare the response data
    response2.clear()
    for disease, probability in sorted_probabilities:
        if probability > 0:
            predicted_disease_precautions = precaution_df[precaution_df['Disease'] == disease]
            prec = []
            if not predicted_disease_precautions.empty:
                for column in ['Symptom_precaution_0', 'Symptom_precaution_1', 'Symptom_precaution_2', 'Symptom_precaution_3']:
                    precaution_value = predicted_disease_precautions[column].values[0]
                    # Convert 'NaN' values to 'None'
                    precaution_value = None if isinstance(precaution_value, float) and math.isnan(precaution_value) else precaution_value
                    prec.append(precaution_value)

            result = doctype.loc[doctype['Disease'] == disease, 'Doctor']
            print("---in send_data()---",result.values[0])
            doc_type=result.values[0]

            disease_details = {
                'disease': disease,
                'probability': int(probability * 100),
                'precautions': prec,
                'doc_type':doc_type
            }
            
            response2.append(disease_details)

    print(response2)
    
    # Convert response2 to JSON and send it to the client
    return jsonify(response2)

# Cập nhật thông tin cá nhân của người dùng: tên, tuổi, cân nặng, chiều cao, giới tính, thói quen uống rượu, và tình trạng mang thai.
@admin.route('/update', methods=['POST'])
def update():
    
    print('*******************************')
    # name = request.form['name']
    name = request.form.get('name')

    # age = request.form['age']
    age = request.form.get('age')
    weight=request.form.get('weight')
    height=request.form.get('height')
    gender = request.form.get('gender')


    alcohol = request.form.get('alcohol', ['X','N'])
    # cigar = request.form.get('cigar', 'no')
    # preg = request.form.get('pregyesno', 'no')
    trisemister = request.form.get('trisemister', ['A','B','C','D','N','X'])
    
    predtxt=[name,age,weight,height,gender,alcohol,trisemister]
    print(predtxt)
    # syms = request.form.get('syms')

    # Process the data and generate the updated content
    response.update({'name': name, 'age': age,'weight':weight,'height':height,'gender':gender,'alcohol':alcohol,'trisemister':trisemister})

    print("______")
    print(response)

    return jsonify(response)

#  Trả về danh sách các bệnh và thông tin liên quan đã được dự đoán bởi send_data
@admin.route('/medic', methods=['POST','GET'])
def medic():

    print("medic func")
    print(response2)

    return jsonify(response2)

response3=dict()
# Dựa trên dữ liệu đầu vào như bệnh, tuổi, tình trạng mang thai, và thói quen uống rượu, cung cấp hướng dẫn về thuốc và mức độ cần thiết phải đến bệnh viện.
@admin.route('/displaymedic', methods=['POST','GET'])
def displaymedic():
    response3.clear()
    global symptoms

    syms = [input_string.replace('_', ' ') for input_string in symptoms]
    disease = request.form.get('disease')
    probability = int(request.form.get('probability', 0))

    if not disease:
        return jsonify({"error": "Disease not provided"}), 400

    age = int(response.get('age', 0))
    pregnancy_condition = response.get('trisemister', None)
    alcohol = response.get('alcohol', None)
    gender = response.get('gender', None)

    doc_type = get_doctor_type(disease)

    if age > 50:
        response3.update({"gotohospital": "urgent"})
    elif probability < 50:
        medications = get_medication_info(syms)
        response3.update({"gotohospital": "for conformation", "medications": medications})
    else:
        medications = recmedicine(disease, age, gender, pregnancy_condition, alcohol)
        if medications:
            response3.update({"medications": medications})
        else:
            general_medications = get_medication_info([disease])
            response3.update({"medications": general_medications})

    response3.update({"disease": disease, "probability": probability, "doc_type": doc_type})
    return jsonify(response3)
from flask import Blueprint, Flask, render_template, request, jsonify
import math
from model.models import *
from model.symptom import *
from model.recomment_df import *

admin = Blueprint('admin', __name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)

response2=dict()
response3=dict()
response=dict()
response2 = []

@admin.route('/faq')
def faq():
    symptoms = get_symptoms()
    
    # Lấy dữ liệu từ Firebase
    doc_ref = db.collection('term_servic_pages').document('samudi_terms')
    doc = doc_ref.get()
    if not doc.exists:
        return "No data found. Please initialize the data."
    
    d = doc.to_dict()
    return render_template('faq.html', data=d, symptoms=symptoms)

response2 = []
# Nhận dữ liệu từ yêu cầu AJAX, xử lý dữ liệu triệu chứng để dự đoán bệnh, và trả về thông tin dự đoán cùng các biện pháp phòng ngừa.
@admin.route('/send_data', methods=['POST'])
def send_data():
    # Retrieve the data from the AJAX request
    global symptoms 
    symptoms = request.get_json()
    print("symptoms",symptoms)

    symsmapping = create_symptom_mapping(symptoms, symptom_mapping)
    
    # Dự đoán bệnh: model_dis.predict_proba() trả về xác suất của từng bệnh
    probabilities = model_dis.predict_proba([symsmapping])
    disease_probabilities = dict(zip(model_dis.classes_, probabilities[0]))

    top_n = 5
    sorted_probabilities = sorted(disease_probabilities.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    # Prepare the response data
    response2.clear()
    for disease, probability in sorted_probabilities:
        if probability > 0:
            predicted_disease_precautions = precaution_df[precaution_df['Disease'] == disease]
            prec = []
            if not predicted_disease_precautions.empty:
                for column in ['Symptom_precaution_0', 'Symptom_precaution_1', 'Symptom_precaution_2', 'Symptom_precaution_3']:
                    precaution_value = predicted_disease_precautions[column].values[0]
                    # Convert 'NaN' values to 'None'
                    precaution_value = None if isinstance(precaution_value, float) and math.isnan(precaution_value) else precaution_value
                    prec.append(precaution_value)

            result = doctype.loc[doctype['Disease'] == disease, 'Doctor']
            print("---in send_data()---",result.values[0])
            doc_type=result.values[0]

            disease_details = {
                'disease': disease,
                'probability': int(probability * 100),
                'precautions': prec,
                'doc_type':doc_type
            }
            
            response2.append(disease_details)

    print(response2)
    
    # Convert response2 to JSON and send it to the client
    return jsonify(response2)

# Cập nhật thông tin cá nhân của người dùng: tên, tuổi, cân nặng, chiều cao, giới tính, thói quen uống rượu, và tình trạng mang thai.
@admin.route('/update', methods=['POST'])
def update():
    
    print('*******************************')
    # name = request.form['name']
    name = request.form.get('name')

    # age = request.form['age']
    age = request.form.get('age')
    weight=request.form.get('weight')
    height=request.form.get('height')
    gender = request.form.get('gender')


    alcohol = request.form.get('alcohol', ['X','N'])
    # cigar = request.form.get('cigar', 'no')
    # preg = request.form.get('pregyesno', 'no')
    trisemister = request.form.get('trisemister', ['A','B','C','D','N','X'])
    
    predtxt=[name,age,weight,height,gender,alcohol,trisemister]
    print(predtxt)
    # syms = request.form.get('syms')

    # Process the data and generate the updated content
    response.update({'name': name, 'age': age,'weight':weight,'height':height,'gender':gender,'alcohol':alcohol,'trisemister':trisemister})

    print("______")
    print(response)

    return jsonify(response)

#  Trả về danh sách các bệnh và thông tin liên quan đã được dự đoán bởi send_data
@admin.route('/medic', methods=['POST','GET'])
def medic():

    print("medic func")
    print(response2)

    return jsonify(response2)

response3=dict()
# Dựa trên dữ liệu đầu vào như bệnh, tuổi, tình trạng mang thai, và thói quen uống rượu, cung cấp hướng dẫn về thuốc và mức độ cần thiết phải đến bệnh viện.
@admin.route('/displaymedic', methods=['POST','GET'])
def displaymedic():
    response3.clear()
    global symptoms
    
    syms = [input_string.replace('_', ' ') for input_string in symptoms]
    print(syms)
    
    disease = request.form['disease']
    print(disease)
    probability=int(request.form['probability'])
    age = int(response['age'])
    pregnancy_condition = response['trisemister']
    alcohol=response['alcohol']
    gender=response['gender']

    
    result = doctype.loc[doctype['Disease'] == disease, 'Doctor']
    print(result.values[0])
    doc_type=result.values[0]
    
    # Đưa ra khuyến nghị: Nếu tuổi trên 50, khuyến cáo nhập viện khẩn cấp. 
    # Nếu xác suất bệnh thấp, cung cấp danh sách thuốc để kiểm tra.
    if age > 50:
        response3.update({"gotohospital": "urgent"})
    else:
        # Lấy thuốc phù hợp
        if(int(request.form['probability'])<50): 
            #  -> khuyến nghị đi kiểm tra thêm để xác nhận
            print(response2)
            # Cung cấp danh sách các loại thuốc hoặc thông tin liên quan đến triệu chứng đã cung cấp bằng cách gọi hàm get_medication_info
            medications = get_medication_info(syms)
            response3.update({"gotohospital": "for conformation","medications": medications})
            
        else:   
            # Xác suất bệnh >= 50%
            medications = recmedicine(disease, age, gender, pregnancy_condition, alcohol)
            if(len(medications)!=0):
                # Nếu có thuốc phù hợp, Tìm thuốc phù hợp (dựa trên thông tin cá nhân)
                response3.update({"medications": medications})
            else:
                # Nếu không có thuốc phù hợp, cung cấp thông tin thuốc chung cho bệnh.
                # Gọi hàm get_medication_info([disease]) để lấy danh sách thuốc dựa trên tên bệnh (không quan tâm yếu tố cá nhân).
                medications1 = get_medication_info([disease])
                response3.update(medications1)

    response3.update({"disease": disease,"probability":probability,"doc_type":doc_type})
    print(response3)
    return jsonify(response3)

