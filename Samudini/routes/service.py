from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import Blueprint, Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from forms import *
from firebase_admin import credentials, firestore, initialize_app
from model.models import *
from model.recomment_df import *
from model.symptom import *

service = Blueprint('service', __name__)

@service.route('/service', methods=['GET', 'POST'])
@login_required
def service_route():
    global predicted_result

    # Lấy thông tin người dùng từ Firestore dựa vào email trong current_user
    user_doc = db.collection('users').document(current_user.id).get()
    if not user_doc.exists:
        flash('User not found!', 'error')
        return redirect(url_for('signin'))

    user = user_doc.to_dict()

    form = serviceForm()  # Đảm bảo serviceForm được định nghĩa trước đó
    if form.validate_on_submit():
        # Lấy danh sách triệu chứng từ form
        selectedSymptoms = [form.symptom1.data, form.symptom2.data, form.symptom3.data, form.symptom4.data]

        # Gọi hàm serviceValidation (đảm bảo nó được định nghĩa)
        result = serviceValidation(selectedSymptoms)  # Lưu trữ toàn bộ kết quả trả về
        predicted_result = result.get("predicted_result", "")  # Tách riêng predicted_result
        description = result.get("description", "")  # Tách riêng description
        precautions = result.get("precautions", "")
        workout = result.get("workout", "")
        diets = result.get("diets", "")
        
        # Lưu lịch sử tư vấn vào Firebase
        consultation_data = {
            "user_id": current_user.id,  # ID của người dùng hiện tại
            "symptoms": selectedSymptoms,
            "predicted_result": predicted_result,
            "description": description,
            "precautions": precautions,
            "workout": workout,
            "diets": diets,
            "timestamp": datetime.now().isoformat(),  # Lưu thời gian hiện tại
        }
        
        # Thêm vào collection 'consultation_history'
        db.collection('consultation_dease').add(consultation_data)

        return render_template(
            'service.html', 
            form=form, 
            predicted_result=predicted_result, 
            description=description,
            precautions = precautions,
            workout= workout, 
            diets = diets,
            id=user.get('id'), 
            name=user.get('firstname', '').upper(), 
            age=user.get('age', ''), 
            gender=user.get('gender', '')
        )

    # Render form nếu không có POST
    return render_template(
        'service.html', 
        form=form, 
        predicted_result=None, 
        description=None,
        precautions = None,
        workout = None, 
        diets = None,
        id=user.get('id'), 
        name=user.get('firstname', '').upper(), 
        age=user.get('age', ''), 
        gender=user.get('gender', '')
    )

@service.route('/med_service', methods=['GET', 'POST'])
@login_required
def med_service():
    form = medForm()

    # Lấy thông tin người dùng từ Firestore dựa vào ID của current_user
    user_doc = db.collection('users').document(current_user.id).get()

    if not user_doc.exists:
        return "User not found", 404

    # Chuyển dữ liệu người dùng sang dạng từ điển
    user_data = user_doc.to_dict()

    if form.validate_on_submit():
        selectedOptions = [form.disease.data, form.age.data, form.gender.data, form.severity.data]

        # Gọi hàm để lấy thuốc được đề xuất
        recommend_Med = predict_conditions_symptom(selectedOptions)

        # Trả kết quả ra giao diện
        return render_template(
            "med_service.html",
            form=form,
            predicted_result=recommend_Med.upper(),
            id=current_user.id,  # Sử dụng ID từ current_user
            name=user_data.get('firstname', '').upper(),
            age=user_data.get('age', ''),
            gender=user_data.get('gender', ''),
        )

    # Hiển thị giao diện ban đầu
    return render_template(
        "med_service.html",
        form=form,
        id=current_user.id,
        name=user_data.get('firstname', '').upper(),
        age=user_data.get('age', ''),
        gender=user_data.get('gender', ''),
    )
    
@service.route('/doc_service')
@login_required
def doc_service():
    # Lấy thông tin người dùng từ Firestore dựa vào ID của current_user
    user_doc = db.collection('users').document(current_user.id).get()

    # Kiểm tra xem tài liệu có tồn tại không
    if not user_doc.exists:
        return "User not found", 404

    # Chuyển tài liệu sang dạng từ điển
    user_data = user_doc.to_dict()

    # Lấy dữ liệu người dùng từ từ điển, với giá trị mặc định nếu trường không tồn tại
    user_id = current_user.id
    firstname = user_data.get('firstname', '').upper()
    age = user_data.get('age', 'N/A')
    gender = user_data.get('gender', 'N/A')

    # Render template với dữ liệu người dùng
    return render_template(
        "doc_service.html",
        id=user_id,
        name=firstname,
        age=age,
        gender=gender
    )
    
@service.route('/re_drugs_review', methods=['GET', 'POST'])
@login_required
def re_drugs_review():
    # Lấy thông tin người dùng từ Firestore
    user_doc = db.collection('users').document(current_user.id).get()

    # Kiểm tra xem tài liệu có tồn tại không
    if not user_doc.exists:
        return "User not found", 404

    # Chuyển tài liệu sang dạng từ điển
    user_data = user_doc.to_dict()

    # Lấy dữ liệu người dùng từ từ điển
    user_id = current_user.id
    firstname = user_data.get('firstname', '').upper()
    age = user_data.get('age', 'N/A')
    gender = user_data.get('gender', 'N/A')

    # Tạo form nhập liệu
    form_drugs_reviews = Reviews()

    result = None  # Biến lưu kết quả dự đoán, mặc định là None

    if form_drugs_reviews.validate_on_submit():
        # Lấy danh sách triệu chứng từ form
        selectedSymptoms = [form_drugs_reviews.review.data]

        # Gọi hàm predict_text
        prediction_df = predict_text(selectedSymptoms)

        # Lấy điều kiện dự đoán từ kết quả
        predicted_condition = prediction_df['prediction'].iloc[0]

        # Lấy danh sách thuốc tương ứng từ Firestore
        top_drugs = get_top_drug(predicted_condition)

        # Chuẩn bị kết quả để hiển thị trong template
        result = [{
            'condition': predicted_condition,
            'text': form_drugs_reviews.review.data,
            'top_drugs': top_drugs
        }]
        
    # Trả kết quả dự đoán về template
    return render_template(
        'reviews/re_with_reviews.html',  # Template sẽ hiển thị kết quả
        form=form_drugs_reviews,
        result=result,  # Truyền kết quả ra template
        id=user_id,
        name=firstname,
        age=age,
        gender=gender
    )